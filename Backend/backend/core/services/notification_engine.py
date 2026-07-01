"""
Notification Engine — محرك الإشعارات المركزي الموحد
الواجهة الوحيدة (Facade) التي يجب أن تتصل بها كل الأنظمة الفرعية لإرسال أي إشعار.
"""
import logging
from typing import List, Dict, Any, Optional
from core.services.notification_channels import (
    InAppChannel, 
    InternalQueueChannel
)

logger = logging.getLogger('notifications')

class NotificationEngine:
    """
    محرك الإشعارات المركزي.
    يقوم بفرز وتوجيه الطلبات إلى القنوات المناسبة بناءً على المدخلات.
    """
    
    # خريطة القنوات المتاحة في النظام المحلي
    AVAILABLE_CHANNELS = {
        'in_app': InAppChannel(),
        'internal_queue': InternalQueueChannel(),
    }

    @classmethod
    def send(
        cls, 
        notification_type: str, 
        target_user_id: Any, 
        title: str, 
        message: str,
        triggered_by_id: Optional[Any] = None,
        priority: str = 'normal',
        channels: List[str] = None,
        extra_kwargs: Dict[str, Any] = None
    ) -> Dict[str, bool]:
        """
        إرسال إشعار موحد.
        
        Args:
            notification_type: نوع الإشعار (مثلاً STATUS_CHANGE)
            target_user_id: الـ ID للمستخدم المستهدف
            title: عنوان الإشعار
            message: نص الإشعار
            triggered_by_id: الـ ID للمستخدم المسبب للإشعار (اختياري)
            priority: الأولوية ('low', 'normal', 'high', 'urgent')
            channels: قائمة القنوات المطلوبة (e.g., ['in_app', 'sms']). Default: ['in_app']
            extra_kwargs: بيانات إضافية (action_url, related_object_type, extra_data)
        
        Returns:
            Dict: تقرير بنجاح/فشل الإرسال لكل قناة، مثلاً: {'in_app': True, 'sms': True}
        """
        if channels is None:
            channels = ['in_app']
            
        if extra_kwargs is None:
            extra_kwargs = {}
            
        notification_data = {
            'notification_type': notification_type,
            'target_user_id': target_user_id,
            'triggered_by_id': triggered_by_id,
            'title': title,
            'message': message,
            'priority': priority,
            **extra_kwargs
        }
        
        results = {}
        for channel_name in channels:
            channel = cls.AVAILABLE_CHANNELS.get(channel_name)
            if not channel:
                logger.warning(f"NotificationEngine: Channel '{channel_name}' is not registered.")
                results[channel_name] = False
                continue
            
            # محاولة الإرسال
            try:
                success = channel.send(notification_data)
                results[channel_name] = success
            except Exception as e:
                logger.error(f"NotificationEngine: Failed to send via {channel_name}. Error: {str(e)}")
                results[channel_name] = False
                
        return results

    @classmethod
    def send_async(cls, *args, **kwargs):
        """
        إرسال غير متزامن عبر Celery لمنع تأخير الـ HTTP Response.
        """
        from core.tasks import process_notification_task
        process_notification_task.delay(*args, **kwargs)
