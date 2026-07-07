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

    def execute_action(self, personnel_id: int, form_id: str, action_type: str, to_status_id: int = None) -> None:
        from systems.personnel.models import PersonnelMaster
        from systems.services.infrastructure.models.status_change import StatusChangeForm
        
        with transaction.atomic():
            if action_type == 'UPDATE_STATUS' and to_status_id:
                PersonnelMaster.objects.filter(pk=personnel_id).update(
                    current_status_id=to_status_id,
                    updated_at=timezone.now(),
                )
            elif action_type == 'UPDATE_RANK':
                # منطق تحديث الرتبة مستقبلاً (يتطلب بيانات الرتبة من الاستمارة)
                pass
            elif action_type == 'SECURITY_RESTRICT':
                # منطق إضافة قيد أمني
                pass
            elif action_type == 'NONE':
                # توثيق فقط
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
