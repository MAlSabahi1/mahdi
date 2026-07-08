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
from systems.services.infrastructure.adapters import DjangoEventPublisher, DjangoAttachmentCommitter
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
    def execution_engine(self):
        from systems.services.infrastructure.adapters import DjangoExecutionActionEngine
        return DjangoExecutionActionEngine()

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
        approval_type = params.get('approval_type')
        if approval_type:
            from systems.services.models import ServiceCatalog
            catalog_items = ServiceCatalog.objects.filter(approval_type=approval_type)
            codes = list(catalog_items.values_list('code', flat=True))
            form_types = list(catalog_items.exclude(form_type__isnull=True).values_list('form_type', flat=True))
            valid_types = list(set(codes + form_types))
            qs = qs.filter(form_type__in=valid_types)

        if params.get('type'):
            qs = qs.filter(form_type=params['type'])
        if params.get('status'):
            qs = qs.filter(status=params['status'])
        if params.get('personnel'):
            qs = qs.filter(personnel__military_number=params['personnel'])
        if params.get('security_admin'):
            qs = qs.filter(security_admin_id=params['security_admin'])
        return qs

    # ─── Serializer موحد ───
    def _serialize(self, form):
        p = form.personnel
        
        # Dynamic resolution of form_type_display
        form_type_display = form.form_type
        service_type = 'correction'
        from systems.services.models import ServiceCatalog
        catalog = ServiceCatalog.objects.prefetch_related('workflow_steps__stage').filter(code=form.form_type).first()
        all_steps = []
        current_step_index = -1
        if catalog:
            form_type_display = catalog.name_ar
            service_type = catalog.service_type
            ordered_steps = catalog.workflow_steps.order_by('order')
            all_steps = [getattr(getattr(s, 'stage', None), 'name_ar', '') for s in ordered_steps]
            if getattr(form, 'current_step', None):
                for idx, s in enumerate(ordered_steps):
                    if s.id == form.current_step.id:
                        current_step_index = idx
                        break
        else:
            # Fallback for legacy types
            form_type_display = dict(form.FORM_TYPE_CHOICES).get(form.form_type, form.form_type)
            
        return {
            'id': form.pk,
            'form_type': form.form_type,
            'form_type_display': form_type_display,
            'service_type': service_type,
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
            'is_printed': form.is_printed,
            'ministry_approval_doc_id': form.ministry_approval_doc_id,
            'current_step_name': form.current_step.stage.name_ar if getattr(form, 'current_step', None) and getattr(form.current_step, 'stage', None) else None,
            'all_steps': all_steps,
            'current_step_index': current_step_index,
            'workflow_log': form.workflow_log,
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

        # ── التحقق من النوع عبر Registry أو Catalog ──
        from systems.services.models import ServiceCatalog
        is_dynamic = False
        
        if not FormRegistry.exists(form_type):
            if not (ServiceCatalog.objects.filter(code=form_type).exists() or ServiceCatalog.objects.filter(form_type=form_type).exists()):
                return Response({'success': False, 'error': f'نوع غير صالح: {form_type}'},
                                status=status.HTTP_400_BAD_REQUEST)
            is_dynamic = True

        try:
            personnel = PersonnelMaster.objects.get(military_number=mil)
        except PersonnelMaster.DoesNotExist:
            return Response({'success': False, 'error': 'الفرد غير موجود'},
                            status=status.HTTP_404_NOT_FOUND)

        # ── التحقق من form_data عبر Registry ──
        form_data = d.get('form_data', {})
        if not is_dynamic:
            is_valid, errors = FormRegistry.validate(form_type, form_data)
            if not is_valid:
                return Response({
                    'success': False, 'error': 'حقول ناقصة في بيانات الاستمارة',
                    'validation_errors': errors,
                    'required_fields': FormRegistry.required_field_keys(form_type),
                }, status=status.HTTP_400_BAD_REQUEST)

        # ── الحالة المستهدفة ──
        from core.models import ServiceStatus
        to_status_obj = None
        to_id = d.get('to_status_id')
        if to_id:
            to_status_obj = ServiceStatus.objects.filter(pk=to_id).first()
        elif not is_dynamic:
            defn = FormRegistry.get(form_type)
            if defn and defn.target_status:
                target_name = defn.target_status
                to_status_obj = ServiceStatus.objects.filter(name__icontains=target_name).first()
                if not to_status_obj:
                    for word in target_name.split():
                        to_status_obj = ServiceStatus.objects.filter(name__icontains=word).first()
                        if to_status_obj:
                            break

        # ── الإنشاء ──
        if is_dynamic:
            att_labels = []
            min_docs = 0
            label_msg = f'طلب خدمة {form_type}'
        else:
            defn = FormRegistry.get(form_type)
            att_labels = FormRegistry.attachment_labels(form_type)
            min_docs = defn.min_documents
            label_msg = defn.label

        with transaction.atomic():
            form = StatusChangeForm.objects.create(
                personnel=personnel,
                security_admin=getattr(personnel, 'security_admin', None),
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
                form.attachments_complete = len(docs) >= min_docs
                form.save(update_fields=['attachments_complete'])

        # ── بعد نجاح المعاملة — تسجيل التدقيق (يُنفَّذ فقط بعد commit) ──
        transaction.on_commit(lambda: AuditService.log_create(user=request.user, obj=form, module='SERVICES'))

        return Response({
            'success': True,
            'message': f'تم إنشاء مسودة {label_msg}',
            'data': self._serialize(form),
        }, status=status.HTTP_201_CREATED)

    # ═══════ دورة الاعتماد (Workflow) — Mixin pattern ═══════

    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        try:
            form = self.get_object()
            from systems.services.models import ServiceCatalog
            catalog = ServiceCatalog.objects.filter(code=form.form_type).first() or ServiceCatalog.objects.filter(form_type=form.form_type).first()
            if not catalog:
                return Response({'success': False, 'error': 'لم يتم العثور على الخدمة'}, status=400)
            
            uc = SubmitStatusFormUseCase(self.repo)
            cmd = SubmitFormCommand(
                form_id=form.id,
                submitted_by=request.user.id,
                submitted_at=timezone.now(),
                first_step_id=None
            )
            uc.execute(cmd)
            return Response({'success': True, 'message': 'تم التقديم بنجاح. بانتظار الاعتماد.'})
        except ValueError as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def mark_printed(self, request, pk=None):
        try:
            form = self.get_object()
            if form.status != 'in_progress':
                return Response({'success': False, 'error': 'الطلب ليس قيد الإجراء'}, status=400)
            
            form.is_printed = True
            form.save(update_fields=['is_printed'])
            return Response({'success': True, 'message': 'تم تسجيل الطباعة بنجاح'})
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=400)

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        try:
            form = self.get_object()
            if getattr(form, 'status', None) != 'in_progress':
                return Response({'success': False, 'error': 'الطلب ليس في مرحلة قيد الإجراء'}, status=400)
            
            from systems.services.models import ServiceCatalog
            catalog = ServiceCatalog.objects.filter(code=form.form_type).first() or ServiceCatalog.objects.filter(form_type=form.form_type).first()
            
            # Validation for external requests
            if catalog and getattr(catalog, 'approval_type', '') == 'external':
                if not form.is_printed:
                    return Response({'success': False, 'error': 'يجب طباعة الاستمارة وإرسالها للوزارة أولاً قبل الاعتماد.'}, status=400)
                
                ministry_doc_id = request.data.get('ministry_document_id')
                if not ministry_doc_id:
                    return Response({'success': False, 'error': 'يجب إرفاق مستند موافقة الوزارة.'}, status=400)
                
                from infra.storage.models import Document
                doc = Document.objects.filter(id=ministry_doc_id).first()
                if not doc:
                    return Response({'success': False, 'error': 'المستند المرفق غير صالح.'}, status=400)
                
                # Attach the document
                form.ministry_approval_doc = doc
                form.attachments.add(doc)
                form.save(update_fields=['ministry_approval_doc'])
            
            # Determine next workflow step dynamically
            next_step_id = None
            if catalog:
                ordered_steps = list(catalog.workflow_steps.order_by('order'))
                if form.current_step:
                    current_idx = next((i for i, s in enumerate(ordered_steps) if s.id == form.current_step_id), -1)
                    if current_idx >= 0 and current_idx < len(ordered_steps) - 1:
                        next_step_id = ordered_steps[current_idx + 1].id
                    # else: last step → next_step_id stays None → triggers final approval
                elif ordered_steps:
                    # No current step but has steps — start from first
                    next_step_id = ordered_steps[0].id if len(ordered_steps) > 1 else None

            uc = ApproveStatusFormUseCase(
                self.repo,
                self.execution_engine,
                self.attachment_committer,
                self.event_publisher
            )
            cmd = ApproveFormCommand(
                form_id=form.id,
                approved_by=request.user.id,
                approved_at=timezone.now(),
                next_step_id=next_step_id,
                execution_action=catalog.execution_action if catalog else 'UPDATE_STATUS'
            )
            uc.execute(cmd)
            
            is_final = next_step_id is None
            msg = 'تم الاعتماد النهائي للطلب بنجاح. تم تحديث حالة الفرد.' if is_final else 'تم الاعتماد وتمرير المعاملة للمرحلة التالية.'
            return Response({'success': True, 'message': msg, 'is_final': is_final})
        except ValueError as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

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
            from systems.services.models import ServiceCatalog

            # ── 1. DB first: if ServiceCatalog has a custom fields_schema, use it ──
            service = (
                ServiceCatalog.objects.filter(form_type=ft).first()
                or ServiceCatalog.objects.filter(code=ft).first()
            )
            if service and service.fields_schema and service.fields_schema.get('sections'):
                schema_data = service.fields_schema.copy()
                # Merge attachments from attachments_schema if present
                db_attachments = [
                    {
                        'doc_type': att.get('key', att.get('doc_type', '')),
                        'label': att.get('label', att.get('name', '')),
                        'required': att.get('required', True),
                    }
                    for att in (service.attachments_schema or [])
                ]
                if db_attachments:
                    schema_data['attachments'] = db_attachments
                return Response({'success': True, 'data': schema_data})

            # ── 2. Fallback: use FormRegistry as default seed ──
            if FormRegistry.exists(ft):
                return Response({'success': True, 'data': FormRegistry.schema(ft)})

            return Response(
                {'success': False, 'error': f'نوع غير صالح: {ft}'},
                status=status.HTTP_400_BAD_REQUEST,
            )
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
