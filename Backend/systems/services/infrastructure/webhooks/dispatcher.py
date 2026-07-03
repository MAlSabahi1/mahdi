"""
Webhook Dispatch System - نظام إشعارات Webhook
المرحلة 4: إرسال إشعارات HTTP عند حدوث أحداث معينة
"""
import hashlib
import hmac
import json
import logging
from datetime import datetime

import requests
from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)

# الأحداث المدعومة
WEBHOOK_EVENTS = [
    ('rejection.created', 'تم رفض تغيير'),
    ('staging.ready', 'كشوفة جاهزة للمراجعة'),
    ('import.completed', 'اكتمل الاستيراد'),
    ('reconciliation.completed', 'اكتملت المطابقة'),
    ('report.ready', 'تقرير جاهز للتحميل'),
    ('dual_auth.pending', 'طلب تفويض مزدوج جديد'),
]


def compute_webhook_signature(payload_bytes, secret):
    """حساب توقيع HMAC-SHA256 للـ payload"""
    return hmac.new(
        secret.encode('utf-8'),
        payload_bytes,
        hashlib.sha256
    ).hexdigest()


def dispatch_webhook(event_type, data, directorate_id=None):
    """
    إرسال webhook لجميع الـ URLs المسجلة لهذا الحدث
    
    Args:
        event_type: نوع الحدث (مثل 'rejection.created')
        data: بيانات الحدث (dict)
        directorate_id: معرف الإدارة (اختياري - للتصفية)
    """
    from systems.services.models import WebhookConfig
    
    configs = WebhookConfig.objects.filter(
        is_active=True,
        events__contains=[event_type],
    )
    
    if directorate_id:
        from django.db.models import Q
        configs = configs.filter(
            Q(central_department_id=directorate_id) | 
            Q(central_department__isnull=True)
        )
    
    payload = {
        'event': event_type,
        'timestamp': timezone.now().isoformat(),
        'data': data,
    }
    payload_bytes = json.dumps(payload, ensure_ascii=False, default=str).encode('utf-8')
    
    results = []
    for config in configs:
        try:
            signature = compute_webhook_signature(payload_bytes, config.secret)
            
            response = requests.post(
                config.url,
                data=payload_bytes,
                headers={
                    'Content-Type': 'application/json; charset=utf-8',
                    'X-Webhook-Signature': f'sha256={signature}',
                    'X-Webhook-Event': event_type,
                },
                timeout=10,
            )
            
            # تسجيل النتيجة
            config.last_triggered_at = timezone.now()
            config.last_response_code = response.status_code
            config.save(update_fields=['last_triggered_at', 'last_response_code'])
            
            results.append({
                'url': config.url,
                'status': response.status_code,
                'success': 200 <= response.status_code < 300,
            })
            
        except requests.RequestException as e:
            logger.warning(f'Webhook delivery failed to {config.url}: {e}')
            config.last_response_code = 0
            config.save(update_fields=['last_response_code'])
            results.append({
                'url': config.url,
                'status': 0,
                'success': False,
                'error': str(e),
            })
    
    return results
