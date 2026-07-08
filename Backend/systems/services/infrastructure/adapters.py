"""
Infrastructure: Status Change Adapters
═════════════════════════════════════════
تطبيق الـ Protocols المُعرّفة في application/use_cases.
هنا يُسمح باستخدام Django و Services الخارجية.
"""
from __future__ import annotations
from django.db import transaction
from django.utils import timezone

from ..domain.entities.status_change_form import StatusChangeFormEntity


class DjangoExecutionActionEngine:
    """
    محرك الإجراءات التنفيذية للخدمات:
    ينفذ تغييرات على قاعدة البيانات بناءً على نوع الإجراء (execution_action) المحدد في الخدمة.
    """

    def execute_action(self, personnel_id: int, form_id: str, action_type: str, execution_config: dict, to_status_id: int = None) -> None:
        from systems.personnel.models import PersonnelMaster
        from systems.services.infrastructure.models.status_change import StatusChangeForm
        
        with transaction.atomic():
            if action_type == 'UPDATE_STATUS':
                # Use to_status_id from execution_config if provided (dynamic), else fallback to form.to_status_id (legacy/static)
                target_status = execution_config.get('to_status_id') or to_status_id
                if target_status:
                    PersonnelMaster.objects.filter(pk=personnel_id).update(
                        current_status_id=target_status,
                        updated_at=timezone.now(),
                    )
            elif action_type == 'UPDATE_RANK':
                # منطق تحديث الرتبة
                form = StatusChangeForm.objects.filter(id=form_id).first()
                if form and form.form_data:
                    new_rank_val = form.form_data.get('to_rank')
                    if new_rank_val:
                        from systems.personnel.models import Rank
                        rank_obj = None
                        if str(new_rank_val).isdigit():
                            rank_obj = Rank.objects.filter(pk=new_rank_val).first()
                        if not rank_obj:
                            rank_obj = Rank.objects.filter(name=new_rank_val).first()
                        if rank_obj:
                            PersonnelMaster.objects.filter(pk=personnel_id).update(
                                current_rank=rank_obj,
                                updated_at=timezone.now()
                            )

            elif action_type == 'PERSONNEL_TO_OFFICER':
                # تسوية وضع من فرد إلى ضابط (ترقية مع تغيير الرقم العسكري)
                form = StatusChangeForm.objects.filter(id=form_id).first()
                if form and form.form_data:
                    new_rank_val = form.form_data.get('to_rank')
                    new_mil_num = form.form_data.get('new_military_number')
                    if new_rank_val and new_mil_num:
                        from systems.personnel.models import Rank
                        rank_obj = None
                        if str(new_rank_val).isdigit():
                            rank_obj = Rank.objects.filter(pk=new_rank_val).first()
                        if not rank_obj:
                            rank_obj = Rank.objects.filter(name=new_rank_val).first()
                        if rank_obj:
                            PersonnelMaster.objects.filter(pk=personnel_id).update(
                                current_rank=rank_obj,
                                military_number=new_mil_num,
                                updated_at=timezone.now()
                            )
            elif action_type == 'SECURITY_RESTRICT' or action_type == 'SECURITY_SYNC':
                # منطق إضافة قيد أمني
                pass
            elif action_type.startswith('CORRECTION_'):
                # التحديث الأوتوماتيكي لبيانات السجل (تصحيح بيانات)
                form = StatusChangeForm.objects.filter(id=form_id).first()
                if form and form.form_data:
                    update_fields = {}
                    if action_type == 'CORRECTION_NAME' and 'correct_name' in form.form_data:
                        update_fields['full_name'] = form.form_data['correct_name']
                    elif action_type == 'CORRECTION_MILITARY_NUM' and 'correct_military_number' in form.form_data:
                        update_fields['military_number'] = form.form_data['correct_military_number']
                    elif action_type == 'CORRECTION_NATIONAL_ID' and 'correct_national_id' in form.form_data:
                        update_fields['national_id'] = form.form_data['correct_national_id']
                    
                    if update_fields:
                        update_fields['updated_at'] = timezone.now()
                        PersonnelMaster.objects.filter(pk=personnel_id).update(**update_fields)

            elif action_type.startswith('DISCIPLINARY_'):
                # منطق الجزاءات التأديبية
                pass
                
            elif action_type == 'NONE':
                # توثيق فقط - لا يوجد تحديث آلي على الجداول الرئيسية
                pass


class DjangoEventPublisher:
    """
    نشر الأحداث بعد الاعتماد أو الرفض.
    مطابق لـ: transaction.on_commit(lambda: (AuditService, NotificationService, ServiceEventService))
    يُنفَّذ فقط بعد commit قاعدة البيانات الفعلي.
    """

    def publish_approved(self, form: StatusChangeFormEntity, approved_by_id: int) -> None:
        """يُستدعى بعد الاعتماد النهائي من المدير."""

        def _execute():
            try:
                from infra.audit.services.audit_service import AuditService
                from core.services.notification_service import NotificationService
                from core.services.service_event_service import ServiceEventService
                from systems.personnel.models import PersonnelMaster
                from systems.services.infrastructure.models.status_change import StatusChangeForm

                personnel = PersonnelMaster.objects.get(pk=form.personnel_id)
                db_form   = StatusChangeForm.objects.get(id=form.id)

                from infra.accounts.models import User
                approved_by_user = User.objects.filter(id=approved_by_id).first()

                AuditService.log_status_change(
                    personnel, db_form.from_status, db_form.to_status, approved_by_user, db_form
                )
                NotificationService.notify_status_change(personnel, db_form)
                ServiceEventService.record_status_change(
                    personnel, db_form.from_status, db_form.to_status, approved_by_user
                )
            except Exception as exc:
                import logging
                logging.getLogger(__name__).error(
                    f"EventPublisher.publish_approved failed for form {form.id}: {exc}"
                )

        transaction.on_commit(_execute)

    def publish_rejected(self, form: StatusChangeFormEntity, reason: str) -> None:
        """يُستدعى بعد الرفض."""

        def _execute():
            try:
                from infra.audit.services.audit_service import AuditService
                from core.services.notification_service import NotificationService
                from infra.accounts.models import User
                from systems.services.infrastructure.models.status_change import StatusChangeForm

                db_form  = StatusChangeForm.objects.get(id=form.id)
                rejector = User.objects.filter(id=form.rejected_by_id).first()

                AuditService.log_form_rejected(rejector, db_form, reason)
                NotificationService.notify_form_rejected(db_form, reason)
            except Exception as exc:
                import logging
                logging.getLogger(__name__).error(
                    f"EventPublisher.publish_rejected failed for form {form.id}: {exc}"
                )

        transaction.on_commit(_execute)

class DjangoAttachmentCommitter:
    """
    تثبيت مرفقات الاستمارة.
    """
    def commit_form_attachments(self, form_id: str) -> None:
        from systems.services.infrastructure.models.status_change import StatusChangeForm
        from systems.services.application.services.attachment_service import AttachmentService
        
        form = StatusChangeForm.objects.get(id=form_id)
        doc_ids = list(form.attachments.values_list('id', flat=True))
        if doc_ids:
            AttachmentService.commit_documents(doc_ids)
