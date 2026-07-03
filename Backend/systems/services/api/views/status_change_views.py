"""
StatusChangeForm ViewSet — يستخدم FormRegistry كمصدر وحيد

لا يوجد أي تعريف حقول أو مرفقات هنا — كل شيء في:
    services.registries.FormRegistry
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db import transaction
from datetime import date

from systems.services.models import StatusChangeForm
from infra.storage.models import Document
from systems.services.application.services.attachment_service import AttachmentService
from systems.services.application.registries.form_registry import FormRegistry
from systems.personnel.models import PersonnelMaster
from core.services import AuditService, NotificationService, ServiceEventService

# ── Clean Architecture Imports ──
from systems.services.infrastructure.repositories.django_status_change_repo import DjangoStatusChangeFormRepository
from systems.services.infrastructure.adapters import DjangoPersonnelUpdater, DjangoEventPublisher, DjangoAttachmentCommitter
from systems.services.application.use_cases.status_change_use_cases import (
    SubmitStatusFormUseCase, SubmitFormCommand,
    ApproveStatusFormUseCase, ApproveFormCommand,
    RejectStatusFormUseCase, RejectFormCommand
)
from systems.services.domain.value_objects.status_change import ApprovalLevel


class StatusChangeFormViewSet(viewsets.ModelViewSet):
    """
    إدارة استمارات إثبات الحالة — 11 نوع رسمي.
    كل التعريفات في FormRegistry — هنا فقط المنطق.
    """
    permission_classes = [IsAuthenticated]

    @property
    def repo(self):
        return DjangoStatusChangeFormRepository()

    @property
    def event_publisher(self):
        return DjangoEventPublisher()

    @property
    def personnel_updater(self):
        return DjangoPersonnelUpdater()

    @property
    def attachment_committer(self):
        return DjangoAttachmentCommitter()

    # ─── QuerySet مع فلاتر ───
    def get_queryset(self):
        qs = StatusChangeForm.objects.select_related(
            'personnel', 'personnel__current_rank',
            'from_status', 'to_status', 'submitted_by',
        ).order_by('-created_at')

        params = self.request.query_params
        if params.get('type'):
            qs = qs.filter(form_type=params['type'])
        if params.get('status'):
            qs = qs.filter(status=params['status'])
        if params.get('personnel'):
            qs = qs.filter(personnel__military_number=params['personnel'])
        if params.get('governorate'):
            qs = qs.filter(governorate_id=params['governorate'])
        return qs

    # ─── Serializer موحد ───
    def _serialize(self, form):
        p = form.personnel
        return {
            'id': form.pk,
            'form_type': form.form_type,
            'form_type_display': form.get_form_type_display(),
            'status': form.status,
            'status_display': form.get_status_display(),
            'personnel': {
                'military_number': p.military_number,
                'full_name': p.full_name,
                'rank': p.current_rank.name if p.current_rank else '',
            } if p else None,
            'from_status': form.from_status.name if form.from_status else None,
            'to_status': form.to_status.name if form.to_status else None,
            'effective_date': form.effective_date,
            'form_data': form.form_data,
            'notes': form.notes,
            'required_attachments': form.required_attachments,
            'attachments': list(form.attachments.values('id', 'document_type', 'file', 'status')),
            'attachments_complete': form.attachments_complete,
            'submitted_by': getattr(form.submitted_by, 'username', None),
            'submitted_at': form.submitted_at,
            'services_approved_by': getattr(form.services_approved_by, 'username', None),
            'services_approved_at': form.services_approved_at,
            'hr_approved_by': getattr(form.hr_approved_by, 'username', None),
            'hr_approved_at': form.hr_approved_at,
            'director_approved_by': getattr(form.director_approved_by, 'username', None),
            'director_approved_at': form.director_approved_at,
            'rejection_reason': form.rejection_reason,
            'created_at': form.created_at,
            'updated_at': form.updated_at,
        }

    # ─── LIST ───
    def list(self, request):
        qs = self.get_queryset()
        page = self.paginate_queryset(qs)
        data = [self._serialize(f) for f in (page or qs)]
        if page is not None:
            return self.get_paginated_response(data)
        return Response({'success': True, 'count': len(data), 'results': data})

    # ─── RETRIEVE ───
    def retrieve(self, request, pk=None):
        return Response({'success': True, 'data': self._serialize(self.get_object())})

    # ─── CREATE (مسودة) ───
    def create(self, request):
        """
        Body: {
            "personnel": "7348799", "form_type": "martyr",
            "form_data": {...}, "to_status_id": 20,
            "effective_date": "2026-05-14", "document_ids": [5,6], "notes": ""
        }
        """
        d = request.data
        mil, form_type = d.get('personnel'), d.get('form_type')

        if not mil or not form_type:
            return Response({'success': False, 'error': 'الرقم العسكري ونوع الاستمارة مطلوبان'},
                            status=status.HTTP_400_BAD_REQUEST)

        # ── التحقق من النوع عبر Registry ──
        if not FormRegistry.exists(form_type):
            return Response({'success': False, 'error': f'نوع غير صالح: {form_type}'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            personnel = PersonnelMaster.objects.get(military_number=mil)
        except PersonnelMaster.DoesNotExist:
            return Response({'success': False, 'error': 'الفرد غير موجود'},
                            status=status.HTTP_404_NOT_FOUND)

        # ── التحقق من form_data عبر Registry ──
        form_data = d.get('form_data', {})
        is_valid, errors = FormRegistry.validate(form_type, form_data)
        if not is_valid:
            return Response({
                'success': False, 'error': 'حقول ناقصة في بيانات الاستمارة',
                'validation_errors': errors,
                'required_fields': FormRegistry.schema(form_type)['fields'],
            }, status=status.HTTP_400_BAD_REQUEST)

        # ── الحالة المستهدفة ──
        from core.models import ServiceStatus
        to_status_obj = None
        to_id = d.get('to_status_id')
        if to_id:
            to_status_obj = ServiceStatus.objects.filter(pk=to_id).first()

        # ── الإنشاء ──
        defn = FormRegistry.get(form_type)
        att_labels = FormRegistry.attachment_labels(form_type)

        with transaction.atomic():
            form = StatusChangeForm.objects.create(
                personnel=personnel,
                governorate=getattr(personnel, 'governorate', None),
                form_type=form_type,
                form_data=form_data,
                from_status=personnel.current_status,
                to_status=to_status_obj,
                effective_date=d.get('effective_date'),
                status='draft',
                submitted_by=request.user,
                required_attachments=att_labels,
                notes=d.get('notes', ''),
            )

            doc_ids = d.get('document_ids', [])
            if doc_ids:
                docs = Document.objects.filter(id__in=doc_ids)
                form.attachments.set(docs)
                form.attachments_complete = len(docs) >= defn.min_documents
                form.save(update_fields=['attachments_complete'])

        # ── بعد نجاح المعاملة — تسجيل التدقيق (يُنفَّذ فقط بعد commit) ──
        transaction.on_commit(lambda: AuditService.log_form_created(request.user, form, mil))

        return Response({
            'success': True,
            'message': f'تم إنشاء مسودة {defn.label}',
            'data': self._serialize(form),
        }, status=status.HTTP_201_CREATED)

    # ═══════ دورة الاعتماد (Workflow) — Mixin pattern ═══════

    def _execute_approve(self, request, level, msg):
        try:
            uc = ApproveStatusFormUseCase(
                self.repo,
                self.personnel_updater,
                self.attachment_committer,
                self.event_publisher
            )
            cmd = ApproveFormCommand(
                form_id=self.get_object().id,
                level=level,
                approved_by=request.user.id,
                approved_at=timezone.now()
            )
            uc.execute(cmd)
            return Response({'success': True, 'message': msg})
        except ValueError as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        try:
            uc = SubmitStatusFormUseCase(self.repo)
            cmd = SubmitFormCommand(
                form_id=self.get_object().id,
                submitted_by=request.user.id,
                submitted_at=timezone.now()
            )
            uc.execute(cmd)
            return Response({'success': True, 'message': 'بانتظار اعتماد قسم الخدمات'})
        except ValueError as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='approve-services')
    def approve_services(self, request, pk=None):
        return self._execute_approve(request, ApprovalLevel.SERVICES, 'تم اعتماد الخدمات — بانتظار الموارد البشرية')

    @action(detail=True, methods=['post'], url_path='approve-hr')
    def approve_hr(self, request, pk=None):
        return self._execute_approve(request, ApprovalLevel.HR, 'تم اعتماد الموارد البشرية — بانتظار المدير العام')

    @action(detail=True, methods=['post'], url_path='approve-director')
    def approve_director(self, request, pk=None):
        form_obj = self.get_object()
        old_status_name = form_obj.personnel.current_status.name if form_obj.personnel and form_obj.personnel.current_status else ''
        to_status_name = form_obj.to_status.name if form_obj.to_status else ''
        msg = f'تم الاعتماد — الحالة: {old_status_name} → {to_status_name}'
        return self._execute_approve(request, ApprovalLevel.DIRECTOR, msg)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        try:
            uc = RejectStatusFormUseCase(self.repo, self.event_publisher)
            cmd = RejectFormCommand(
                form_id=self.get_object().id,
                reason=request.data.get('reason', 'تم الرفض'),
                rejected_by=request.user.id
            )
            uc.execute(cmd)
            return Response({'success': True, 'message': 'تم رفض الاستمارة'})
        except ValueError as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # ═══════ Schema + Export ═══════

    @action(detail=False, methods=['get'], url_path='schema')
    def form_schema(self, request):
        """GET /forms/schema/?type=martyr أو بدون type للكل"""
        ft = request.query_params.get('type')
        if ft:
            if not FormRegistry.exists(ft):
                return Response({'success': False, 'error': f'نوع غير صالح: {ft}'},
                                status=status.HTTP_400_BAD_REQUEST)
            return Response({'success': True, 'data': FormRegistry.schema(ft)})
        return Response({'success': True, 'data': FormRegistry.all_schemas()})

    @action(detail=False, methods=['get'])
    def export(self, request):
        qs = self.get_queryset()
        rows = []
        for i, f in enumerate(qs, 1):
            p = f.personnel
            rows.append({
                'seq': i,
                'rank': p.current_rank.name if p and p.current_rank else '',
                'military_number': p.military_number if p else '',
                'full_name': p.full_name if p else '',
                'form_type': f.get_form_type_display(),
                'status': f.get_status_display(),
                'effective_date': str(f.effective_date) if f.effective_date else '',
                'from_status': f.from_status.name if f.from_status else '',
                'to_status': f.to_status.name if f.to_status else '',
                'notes': f.notes,
            })
        return Response({
            'success': True, 'count': len(rows),
            'columns': [
                {'key': 'seq', 'label': 'م'}, {'key': 'rank', 'label': 'الرتبة'},
                {'key': 'military_number', 'label': 'الرقم العسكري'},
                {'key': 'full_name', 'label': 'الاسم'},
                {'key': 'form_type', 'label': 'نوع الاستمارة'},
                {'key': 'from_status', 'label': 'الحالة السابقة'},
                {'key': 'to_status', 'label': 'الحالة الجديدة'},
                {'key': 'status', 'label': 'حالة الطلب'},
                {'key': 'effective_date', 'label': 'تاريخ النفاذ'},
                {'key': 'notes', 'label': 'ملاحظات'},
            ],
            'data': rows,
        })
