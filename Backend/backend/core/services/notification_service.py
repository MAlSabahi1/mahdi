"""
Notification Service — خدمة الإشعارات المباشرة
═══════════════════════════════════════════════
واجهة صريحة لإرسال الإشعارات. تستخدم NotificationEngine الموجود داخلياً.
كل استدعاء واضح ومباشر — بدون أحداث مخفية.
"""
import logging
from typing import Any, Optional

logger = logging.getLogger('notifications')


class NotificationService:
    """
    خدمة إشعارات مركزية — نقطة الدخول الوحيدة لإرسال أي إشعار.
    
    الاستخدام:
        NotificationService.notify_status_change(personnel, form)
        NotificationService.notify_form_rejected(form, reason)
    """

    @staticmethod
    def _send(
        notification_type: str,
        target_user: Any,
        title: str,
        message: str,
        priority: str = 'normal',
        personnel: Any = None,
    ) -> None:
        """
        الدالة الأساسية لإرسال الإشعارات.
        تُنشئ NotificationRecord مباشرةً في قاعدة البيانات.
        """
        from core.models.notification import NotificationRecord

        try:
            kwargs = {
                'notification_type': notification_type,
                'target_user': target_user,
                'title': title,
                'message': message,
                'priority': priority,
            }
            if personnel is not None:
                kwargs['personnel'] = personnel

            NotificationRecord.objects.create(**kwargs)
            logger.debug(
                f"[NotificationService] Sent '{notification_type}' to "
                f"{getattr(target_user, 'username', target_user)}"
            )
        except Exception as e:
            # الإشعار لا يجب أن يكسر العملية الأساسية
            logger.error(f"[NotificationService] Failed to send '{notification_type}': {e}")

    @staticmethod
    def notify_status_change(personnel: Any, form: Any) -> None:
        """إشعار صاحب الطلب بأن حالة الفرد تم تغييرها بنجاح."""
        if not form or not getattr(form, 'submitted_by', None):
            return

        NotificationService._send(
            notification_type='status_change_approved',
            target_user=form.submitted_by,
            personnel=personnel,
            priority='high',
            title=f'تم اعتماد {form.get_form_type_display()} — {personnel.full_name}',
            message=f'تمت الموافقة على الاستمارة ({personnel.military_number})',
        )

    @staticmethod
    def notify_form_rejected(form: Any, reason: str) -> None:
        """إشعار صاحب الطلب بأن الاستمارة تم رفضها."""
        if not form or not getattr(form, 'submitted_by', None):
            return

        NotificationService._send(
            notification_type='status_change_rejected',
            target_user=form.submitted_by,
            personnel=getattr(form, 'personnel', None),
            priority='medium',
            title=f'رفض {form.get_form_type_display()} — {form.personnel.full_name}',
            message=f'السبب: {reason}',
        )

    @staticmethod
    def notify_workflow_approved(instance: Any) -> None:
        """إشعار منشئ الطلب بأن المسار تم اعتماده بالكامل."""
        initiator = getattr(instance, 'initiator', None)
        if not initiator:
            return

        workflow_name = instance.workflow.name if hasattr(instance, 'workflow') else 'مسار عمل'
        NotificationService._send(
            notification_type='workflow_approved',
            target_user=initiator,
            priority='high',
            title=f'تم اعتماد طلبك: {workflow_name}',
            message='تم الانتهاء من دورة الاعتماد للطلب الخاص بك بنجاح.',
        )
