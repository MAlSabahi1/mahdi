"""
Notification Channels — قنوات الإرسال لمحرك الإشعارات
مصممة لدعم بيئة محلية (Intranet/Offline) بشكل كامل.
"""
import logging
from abc import ABC, abstractmethod

logger = logging.getLogger('notifications')

class BaseNotificationChannel(ABC):
    """الواجهة الأساسية لأي قناة إشعارات"""
    
    @abstractmethod
    def send(self, notification_data: dict) -> bool:
        """
        إرسال الإشعار عبر القناة.
        يجب أن تعيد True إذا تم الإرسال بنجاح، و False في حالة الفشل.
        """
        pass


class InAppChannel(BaseNotificationChannel):
    """
    قناة الإشعارات الداخلية للتطبيق.
    تقوم بإنشاء سجل في قاعدة البيانات (NotificationRecord).
    """
    def send(self, notification_data: dict) -> bool:
        try:
            from core.models.notification import NotificationRecord
            NotificationRecord.objects.create(
                notification_type=notification_data.get('notification_type', 'SYSTEM'),
                title=notification_data.get('title', ''),
                message=notification_data.get('message', ''),
                priority=notification_data.get('priority', 'normal'),
                target_user_id=notification_data.get('target_user_id'),
                triggered_by_id=notification_data.get('triggered_by_id'),
                related_object_type=notification_data.get('related_object_type', ''),
                related_object_id=notification_data.get('related_object_id', ''),
                action_url=notification_data.get('action_url', ''),
                extra_data=notification_data.get('extra_data', {})
            )
            return True
        except Exception as e:
            logger.error(f"InAppChannel Error: {str(e)}")
            return False


class InternalQueueChannel(BaseNotificationChannel):
    """
    قناة مخصصة للرسائل الداخلية بين الأنظمة.
    يمكن أن تضع رسالة في Celery Queue ليعالجها خدمة أخرى لاحقاً.
    """
    def send(self, notification_data: dict) -> bool:
        logger.info(f"InternalQueueChannel received event: {notification_data.get('notification_type')}")
        # مستقبلاً: إرسال الحدث إلى Celery/RabbitMQ كـ Message
        return True
