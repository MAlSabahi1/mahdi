import logging
from celery import shared_task

logger = logging.getLogger('notifications')

@shared_task(name='core.process_notification_task')
def process_notification_task(*args, **kwargs):
    """
    مهمة Celery لمعالجة إرسال الإشعارات بشكل غير متزامن.
    تستدعي NotificationEngine.send في الخلفية.
    """
    from core.services.notification_engine import NotificationEngine
    try:
        results = NotificationEngine.send(*args, **kwargs)
        logger.info(f"Async Notification Processed. Results: {results}")
        return results
    except Exception as e:
        logger.error(f"Error in process_notification_task: {str(e)}")
        raise
