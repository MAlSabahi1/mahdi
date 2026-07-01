"""
Request Signing Middleware - التحقق من توقيع الطلبات
المرحلة 4: HMAC-SHA256 لمنع هجمات إعادة التشغيل (Replay attacks)

الهيدرات المطلوبة للعمليات الحساسة:
- X-Request-Signature: HMAC-SHA256 hash
- X-Request-Timestamp: Unix timestamp
- X-Request-Nonce: UUID فريد لكل طلب
"""
import hashlib
import hmac
import time
import json
import logging

from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)

# العمليات التي تتطلب توقيع
SENSITIVE_PATHS = [
    '/api/v1/users/',
    '/api/v1/dual-auth/',
    '/api/v1/settings/',
]

# مدة صلاحية التوقيع (5 دقائق)
SIGNATURE_MAX_AGE = 300

# مدة حفظ nonce لمنع إعادة الاستخدام (10 دقائق)
NONCE_CACHE_TTL = 600


class RequestSigningMiddleware(MiddlewareMixin):
    """
    Middleware للتحقق من توقيع الطلبات الحساسة
    
    يتحقق من:
    1. وجود هيدر التوقيع
    2. صحة التوقيع (HMAC-SHA256)
    3. عدم انتهاء صلاحية الطلب
    4. عدم إعادة استخدام nonce (منع Replay attacks)
    """
    
    def process_request(self, request):
        # تجاهل في وضع التطوير إذا لم يتم تفعيل التوقيع
        if settings.DEBUG and not getattr(settings, 'ENFORCE_REQUEST_SIGNING', False):
            return None
        
        # فقط العمليات الكتابية على المسارات الحساسة
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return None
        
        is_sensitive = any(
            request.path.startswith(path) for path in SENSITIVE_PATHS
        )
        if not is_sensitive:
            return None
        
        # استخراج الهيدرات
        signature = request.META.get('HTTP_X_REQUEST_SIGNATURE', '')
        timestamp = request.META.get('HTTP_X_REQUEST_TIMESTAMP', '')
        nonce = request.META.get('HTTP_X_REQUEST_NONCE', '')
        
        if not all([signature, timestamp, nonce]):
            return JsonResponse({
                'success': False,
                'error': 'طلب غير موقع. يجب تضمين X-Request-Signature و X-Request-Timestamp و X-Request-Nonce',
                'code': 'SIGNATURE_REQUIRED',
            }, status=400)
        
        # فحص صلاحية التوقيت
        try:
            req_time = int(timestamp)
            if abs(time.time() - req_time) > SIGNATURE_MAX_AGE:
                return JsonResponse({
                    'success': False,
                    'error': 'الطلب منتهي الصلاحية',
                    'code': 'SIGNATURE_EXPIRED',
                }, status=400)
        except (ValueError, TypeError):
            return JsonResponse({
                'success': False,
                'error': 'timestamp غير صالح',
                'code': 'INVALID_TIMESTAMP',
            }, status=400)
        
        # فحص nonce (منع إعادة التشغيل)
        nonce_key = f'request_nonce:{nonce}'
        if cache.get(nonce_key):
            return JsonResponse({
                'success': False,
                'error': 'الطلب مكرر (nonce مستخدم)',
                'code': 'NONCE_REUSED',
            }, status=400)
        
        # التحقق من التوقيع
        signing_key = getattr(settings, 'REQUEST_SIGNING_KEY', settings.SECRET_KEY)
        body = request.body or b''
        message = f'{timestamp}.{nonce}.{body.decode("utf-8", errors="replace")}'
        
        expected_signature = hmac.new(
            signing_key.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256,
        ).hexdigest()
        
        if not hmac.compare_digest(signature, expected_signature):
            logger.warning(
                f'Invalid request signature from {request.META.get("REMOTE_ADDR")} '
                f'for {request.method} {request.path}'
            )
            return JsonResponse({
                'success': False,
                'error': 'توقيع الطلب غير صحيح',
                'code': 'INVALID_SIGNATURE',
            }, status=403)
        
        # حفظ nonce لمنع إعادة الاستخدام
        cache.set(nonce_key, True, NONCE_CACHE_TTL)
        
        return None
