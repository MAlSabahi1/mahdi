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
            'personnel__central_department', 'personnel__branch',
            'personnel__division', 'personnel__unit',
            'personnel__security_admin',
            'personnel__birth_governorate', 'personnel__birth_district',
            'personnel__birth_sub_district', 'personnel__birth_village',
            'personnel__residence_governorate', 'personnel__residence_district',
            'personnel__residence_sub_district', 'personnel__residence_village',
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
            
        approval_type = getattr(catalog, 'approval_type', 'internal') if catalog else 'internal'
        execution_action = getattr(catalog, 'execution_action', 'UPDATE_STATUS') if catalog else 'UPDATE_STATUS'

        return {
            'id': form.pk,
            'form_type': form.form_type,
            'form_type_display': form_type_display,
            'service_type': service_type,
            'approval_type': approval_type,
            'is_external': approval_type == 'external',
            'execution_action': execution_action,
            'status': form.status,
            'status_display': form.get_status_display(),
            'personnel': {
                'military_number': p.military_number,
                'full_name': p.full_name,
                'rank': p.current_rank.name if p.current_rank else '',
                'rank_name': p.current_rank.name if p.current_rank else '',
                'rank_id': p.current_rank.id if p.current_rank else None,
                'national_id': p.national_id or '',
                'birth_date': str(p.birth_date) if p.birth_date else '',
                'join_date': str(p.join_date) if p.join_date else '',
                # الهيكل التنظيمي
                'security_admin': p.security_admin.name if getattr(p, 'security_admin', None) else '',
                'security_admin_name': p.security_admin.name if getattr(p, 'security_admin', None) else '',
                'central_department': p.central_department.name if getattr(p, 'central_department', None) else '',
                'central_department_name': p.central_department.name if getattr(p, 'central_department', None) else '',
                'branch_name': p.branch.name if getattr(p, 'branch', None) else '',
                'division_name': p.division.name if getattr(p, 'division', None) else '',
                'unit_name': p.unit.name if getattr(p, 'unit', None) else '',
                # بيانات الهوية
                'id_issue_date': str(p.id_issue_date) if getattr(p, 'id_issue_date', None) else '',
                'id_issue_place': p.id_issue_place if getattr(p, 'id_issue_place', None) else '',
                # بيانات الميلاد (أسماء نصية كاملة: محافظة - مديرية - عزلة - قرية)
                'birth_governorate_name': p.birth_governorate.name_ar if getattr(p, 'birth_governorate', None) else '',
                'birth_district_name': p.birth_district.name_ar if getattr(p, 'birth_district', None) else '',
                'birth_sub_district_name': p.birth_sub_district.name_ar if getattr(p, 'birth_sub_district', None) else '',
                'birth_village_name': p.birth_village.name_ar if getattr(p, 'birth_village', None) else '',
                # بيانات الإقامة (أسماء نصية كاملة)
                'residence_governorate_name': p.residence_governorate.name_ar if getattr(p, 'residence_governorate', None) else '',
                'residence_district_name': p.residence_district.name_ar if getattr(p, 'residence_district', None) else '',
                'residence_sub_district_name': p.residence_sub_district.name_ar if getattr(p, 'residence_sub_district', None) else '',
                'residence_village_name': p.residence_village.name_ar if getattr(p, 'residence_village', None) else '',
            } if p else None,
            'from_status': form.from_status.name if form.from_status else None,
            'to_status': form.to_status.name if form.to_status else None,
            'to_status_id': form.to_status_id,
            'effective_date': form.effective_date,
            'form_data': form.form_data,
            'notes': form.notes,
            'required_attachments': form.required_attachments,
            'attachments': list(form.attachments.values('id', 'document_type', 'file', 'status', 'personnel_id', 'context_type')),
            'attachments_complete': form.attachments_complete,
            'submitted_by': getattr(form.submitted_by, 'username', None),
            'submitted_at': form.submitted_at,
            'is_printed': form.is_printed,
            'ministry_approval_doc_id': form.ministry_approval_doc_id,
            'ministry_approval_doc_url': form.ministry_approval_doc.file.url if form.ministry_approval_doc and hasattr(form.ministry_approval_doc, 'file') and form.ministry_approval_doc.file else None,
            'current_step_name': form.current_step.stage.name_ar if getattr(form, 'current_step', None) and getattr(form.current_step, 'stage', None) else None,
            'current_step_id': form.current_step_id,
            'all_steps': all_steps,
            'current_step_index': current_step_index,
            'workflow_log': form.workflow_log,
            'rejection_reason': form.rejection_reason,
            'priority': form.priority,
            'sla_deadline': form.sla_deadline,
            'is_overdue': form.is_overdue,
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
        elif is_dynamic:
            from systems.services.models import ServiceCatalog
            catalog = ServiceCatalog.objects.filter(code=form_type).first() or ServiceCatalog.objects.filter(form_type=form_type).first()
            if catalog and catalog.execution_config and catalog.execution_config.get('to_status_id'):
                to_status_obj = ServiceStatus.objects.filter(pk=catalog.execution_config.get('to_status_id')).first()
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
        
        # ── التحقق الأمني والمنطقي (لمنع التكرار) ──
        # 1. التحقق الاستباقي من تعارض الأرقام لتجنب الفشل في التنفيذ النهائي
        n_id = form_data.get('national_id')
        old_mil = form_data.get('old_military_number')
        
        if n_id and PersonnelMaster.objects.filter(national_id=n_id).exclude(pk=personnel.pk).exists():
            return Response({'success': False, 'error': 'الرقم الوطني المُدخل مسجل مسبقاً لفرد آخر في النظام.'}, status=status.HTTP_400_BAD_REQUEST)
            
        if old_mil and PersonnelMaster.objects.filter(old_military_number=old_mil).exclude(pk=personnel.pk).exists():
            owner = PersonnelMaster.objects.filter(old_military_number=old_mil).exclude(pk=personnel.pk).first()
            return Response({'success': False, 'error': f'الرقم العسكري القديم مستخدم بالفعل للفرد: {owner.full_name}'}, status=status.HTTP_400_BAD_REQUEST)

        # 2. التحقق من الحالة الحالية (إذا كان يملكها مسبقاً)
        if to_status_obj and personnel.current_status_id == to_status_obj.id:
            return Response({'success': False, 'error': f'الفرد لديه هذه الحالة ({to_status_obj.name}) مسبقاً في النظام'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 3. التحقق إذا كان الفرد شهيد أو متوفى (لا يقبل أي معاملات باستثناء العودة للخدمة)
        if personnel.current_status and any(word in personnel.current_status.name for word in ['شهيد', 'متوفى']):
            if form_type not in ['returned_to_service', 'correction']:
                return Response({'success': False, 'error': f'لا يمكن إنشاء هذه المعاملة لأن الفرد مسجل كـ ({personnel.current_status.name}) في النظام.'}, status=status.HTTP_400_BAD_REQUEST)

        # 2. التحقق من وجود معاملة سابقة قيد الإجراء لنفس النوع ونفس الفرد
        existing_pending = StatusChangeForm.objects.filter(
            personnel=personnel,
            form_type=form_type,
            status__in=['draft', 'in_progress', 'pending_services', 'pending_hr', 'pending_director', 'returned']
        ).first()
        
        if existing_pending:
            return Response({'success': False, 'error': f'يوجد معاملة سابقة من نفس النوع قيد الإجراء (رقم: {existing_pending.id})'}, status=status.HTTP_400_BAD_REQUEST)

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
                service_catalog=ServiceCatalog.objects.filter(code=form_type).first() or ServiceCatalog.objects.filter(form_type=form_type).first(),
            )

            doc_ids = d.get('document_ids', [])
            if doc_ids:
                docs = Document.objects.filter(id__in=doc_ids)
                form.attachments.set(docs)
                form.attachments_complete = len(docs) >= min_docs
                form.save(update_fields=['attachments_complete'])

                # ── ربط المرفقات بالفرد مباشرة ──
                for doc in docs:
                    if not doc.personnel_id:
                        doc.personnel = personnel
                        doc.context_type = 'StatusChangeForm'
                        doc.context_id = str(form.id)
                        doc.save(update_fields=['personnel_id', 'context_type', 'context_id'])

            # ── تسجيل الحدث في Timeline ──
            from systems.services.models import FormEventLog
            FormEventLog.objects.create(
                form=form,
                action='created',
                to_status='draft',
                performed_by=request.user,
                notes=f'تم إنشاء مسودة {label_msg} للفرد {personnel.full_name}'
            )

        # ── بعد نجاح المعاملة — تسجيل التدقيق (يُنفَّذ فقط بعد commit) ──
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
            from systems.services.models import ServiceCatalog, FormEventLog
            catalog = ServiceCatalog.objects.filter(code=form.form_type).first() or ServiceCatalog.objects.filter(form_type=form.form_type).first()
            if not catalog:
                return Response({'success': False, 'error': 'لم يتم العثور على الخدمة'}, status=400)

            # ── تحديد الخطوة الأولى من مسار سير العمل ──
            first_step_id = None
            ordered_steps = list(catalog.workflow_steps.order_by('order'))
            if ordered_steps:
                first_step_id = ordered_steps[0].id

            uc = SubmitStatusFormUseCase(self.repo)
            cmd = SubmitFormCommand(
                form_id=form.id,
                submitted_by=request.user.id,
                submitted_at=timezone.now(),
                first_step_id=first_step_id,
            )
            uc.execute(cmd)

            # ── تحديث current_step في النموذج مباشرة (لأن الـ repo يحدث بالـ filter().update) ──
            if first_step_id:
                StatusChangeForm.objects.filter(id=form.id).update(current_step_id=first_step_id)

            # ── تسجيل الحدث في Timeline ──
            FormEventLog.objects.create(
                form=form,
                action='submitted',
                from_status='draft',
                to_status='in_progress',
                performed_by=request.user,
                notes=f'تم تقديم الطلب — المرحلة الأولى: {ordered_steps[0].stage.name_ar if ordered_steps else "غير محدد"}'
            )

            return Response({'success': True, 'message': 'تم التقديم بنجاح. بانتظار الاعتماد.'})
        except ValueError as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def mark_printed(self, request, pk=None):
        """تسجيل الطباعة — يُسمح من أي حالة نشطة (مسودة، قيد الإجراء، مُرجع)"""
        try:
            form = self.get_object()
            if form.status in ['approved', 'rejected']:
                return Response({'success': False, 'error': 'لا يمكن طباعة معاملة معتمدة أو مرفوضة بهذه الطريقة'}, status=400)

            form.is_printed = True
            form.save(update_fields=['is_printed'])

            # ── تسجيل حدث الطباعة في Timeline ──
            from systems.services.models import FormEventLog
            FormEventLog.objects.create(
                form=form,
                action='printed',
                performed_by=request.user,
                notes=f'تمت طباعة الاستمارة بواسطة {request.user.get_full_name() or request.user.username}'
            )
            return Response({'success': True, 'message': 'تم تسجيل الطباعة بنجاح', 'is_printed': True})
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=400)

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        try:
            form = self.get_object()
            if getattr(form, 'status', None) != 'in_progress':
                return Response({'success': False, 'error': 'الطلب ليس في مرحلة قيد الإجراء'}, status=400)

            from systems.services.models import ServiceCatalog, FormEventLog
            catalog = ServiceCatalog.objects.filter(code=form.form_type).first() or ServiceCatalog.objects.filter(form_type=form.form_type).first()

            if not catalog:
                return Response({'success': False, 'error': 'لم يتم العثور على الخدمة في الدليل. لا يمكن الاعتماد.'}, status=400)

            # ── حماية الشهيد/المتوفى من أي اعتماد نهائي غير منطقي ──
            if form.personnel and form.personnel.current_status:
                ps_name = form.personnel.current_status.name
                if any(w in ps_name for w in ['شهيد', 'متوفى']):
                    if form.form_type not in ['returned_to_service', 'correction']:
                        return Response({'success': False, 'error': f'الفرد مسجّل كـ ({ps_name}). لا يمكن اعتماد هذه المعاملة.'}, status=400)

            # ── التحقق من الخدمات الخارجية (external) ──
            if catalog and getattr(catalog, 'approval_type', '') == 'external':
                if not form.is_printed:
                    return Response({'success': False, 'error': 'يجب طباعة الاستمارة وإرسالها للوزارة أولاً قبل الاعتماد.'}, status=400)

                ministry_doc_id = request.data.get('ministry_document_id')
                if not ministry_doc_id:
                    return Response({'success': False, 'error': 'يجب إرفاق مستند موافقة الوزارة.'}, status=400)

                # منع تكرار مستند الوزارة
                if form.ministry_approval_doc_id and form.ministry_approval_doc_id != int(ministry_doc_id):
                    return Response({'success': False, 'error': 'مستند الوزارة مرفق مسبقاً. لا يمكن استبداله.'}, status=400)

                from infra.storage.models import Document
                doc = Document.objects.filter(id=ministry_doc_id).first()
                if not doc:
                    return Response({'success': False, 'error': 'المستند المرفق غير صالح.'}, status=400)

                form.ministry_approval_doc = doc
                form.attachments.add(doc)
                form.save(update_fields=['ministry_approval_doc'])

            # ── تحديد الخطوة التالية من مسار سير العمل ──
            next_step_id = None
            current_step_name = 'غير محدد'
            next_step_name = None

            ordered_steps = list(catalog.workflow_steps.select_related('stage').order_by('order'))
            if not ordered_steps:
                return Response({'success': False, 'error': 'لا يوجد مسار سير عمل معرّف لهذه الخدمة. يرجى إعداد المراحل أولاً.'}, status=400)

            if form.current_step_id:
                current_idx = next((i for i, s in enumerate(ordered_steps) if s.id == form.current_step_id), -1)
                if current_idx >= 0:
                    current_step_name = ordered_steps[current_idx].stage.name_ar
                    if current_idx < len(ordered_steps) - 1:
                        next_step_id = ordered_steps[current_idx + 1].id
                        next_step_name = ordered_steps[current_idx + 1].stage.name_ar
                    # else: آخر خطوة → next_step_id = None → اعتماد نهائي
            else:
                # لا توجد خطوة حالية لكن يوجد مسار — نبدأ من الأولى ثم ننتقل للثانية
                current_step_name = ordered_steps[0].stage.name_ar
                if len(ordered_steps) > 1:
                    next_step_id = ordered_steps[1].id
                    next_step_name = ordered_steps[1].stage.name_ar
                # else: خطوة واحدة فقط → اعتماد نهائي

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
                execution_action=catalog.execution_action if catalog else 'UPDATE_STATUS',
                execution_config=catalog.execution_config if catalog else {},
            )
            uc.execute(cmd)

            is_final = next_step_id is None

            # ── تحديث current_step في النموذج ──
            StatusChangeForm.objects.filter(id=form.id).update(
                current_step_id=next_step_id
            )

            # ── تسجيل الحدث في Timeline ──
            approver_name = request.user.get_full_name() or request.user.username

            if is_final:
                FormEventLog.objects.create(
                    form=form,
                    action='approved',
                    from_status='in_progress',
                    to_status='approved',
                    performed_by=request.user,
                    notes=f'✅ اعتماد نهائي — بواسطة: {approver_name}. المرحلة: {current_step_name}. تم تحديث حالة الفرد في السجل.'
                )
            else:
                FormEventLog.objects.create(
                    form=form,
                    action='approved',
                    from_status='in_progress',
                    to_status='in_progress',
                    performed_by=request.user,
                    notes=f'✓ اعتماد بواسطة: {approver_name} — تم اعتماد مرحلة ({current_step_name}) وتمرير المعاملة إلى مرحلة ({next_step_name})'
                )

            msg = 'تم الاعتماد النهائي للطلب بنجاح. تم تحديث حالة الفرد.' if is_final else f'تم الاعتماد وتمرير المعاملة إلى مرحلة: {next_step_name}.'
            return Response({'success': True, 'message': msg, 'is_final': is_final})
        except ValueError as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        try:
            form = self.get_object()
            reason = request.data.get('reason', 'تم الرفض')

            uc = RejectStatusFormUseCase(self.repo, self.event_publisher)
            cmd = RejectFormCommand(
                form_id=form.id,
                reason=reason,
                rejected_by=request.user.id
            )
            uc.execute(cmd)

            # ── تسجيل الحدث في Timeline ──
            from systems.services.models import FormEventLog
            FormEventLog.objects.create(
                form=form,
                action='rejected',
                from_status='in_progress',
                to_status='rejected',
                performed_by=request.user,
                notes=f'سبب الرفض: {reason}'
            )

            # ملاحظة: RejectionLog مرتبط بـ StagingRecord (نظام الاستيراد) وليس بالاستمارات.
            # الرفض مسجّل في: FormEventLog (أعلاه) + AuditService.log_form_rejected (عبر DjangoEventPublisher)

            # ── حذف المرفقات المرتبطة بالطلب المرفوض (بناءً على طلب العميل) ──
            try:
                # حذف الملفات الفسيزيائية والسجلات من قاعدة البيانات
                form.attachments.all().delete()
                form.attachments_complete = False
                form.save(update_fields=['attachments_complete'])
            except Exception as e:
                pass # تجاهل في حال كان هناك قيود على الحذف

            return Response({'success': True, 'message': 'تم رفض الاستمارة وحذف مرفقاتها المرتبطة'})
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
    @action(detail=False, methods=['get'])
    def export(self, request):
        qs = self.get_queryset()
        # ── تحضير خريطة أسماء الأنواع الديناميكية ──
        from systems.services.models import ServiceCatalog
        catalog_map = {}
        for sc in ServiceCatalog.objects.values('code', 'form_type', 'name_ar'):
            catalog_map[sc['code']] = sc['name_ar']
            if sc['form_type']:
                catalog_map[sc['form_type']] = sc['name_ar']

        rows = []
        for i, f in enumerate(qs, 1):
            p = f.personnel
            # حل الاسم: من Catalog أولاً، ثم من choices، ثم الكود الخام
            ft_display = catalog_map.get(f.form_type) or dict(f.FORM_TYPE_CHOICES).get(f.form_type) or f.form_type
            rows.append({
                'seq': i,
                'rank': p.current_rank.name if p and p.current_rank else '',
                'military_number': p.military_number if p else '',
                'full_name': p.full_name if p else '',
                'form_type': ft_display,
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
