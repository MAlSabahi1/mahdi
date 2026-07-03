"""
Activity Tracking Middleware — تتبع نشاط المستخدم
═══════════════════════════════════════════════════════
كل Request:
    - تحديث last_activity في Redis (سريع)
    - إذا 30 دقيقة بدون نشاط → session revoke تلقائي

يعمل مع JWT Authentication — يستخرج session_id من Access Token.
"""
import logging
from typing import Optional

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.utils import timezone

logger = logging.getLogger('accounts.middleware.activity')

INACTIVITY_TIMEOUT: int = getattr(settings, 'SESSION_INACTIVITY_TIMEOUT', 1800)

# مسارات لا تحتاج تتبع نشاط
EXEMPT_PATHS = (
    '/api/v1/auth/login/',
    '/api/v1/auth/refresh/',
    '/admin/',
    '/api/v1/schema/',
    '/api/v1/docs/',
    '/api/v1/redoc/',
)


class ActivityTrackingMiddleware:
    """
    Middleware لتتبع نشاط المستخدم وإلغاء الجلسات الخاملة.

    التدفق:
        1. استخراج session_id من JWT Access Token
        2. تحديث last_activity في Redis (سريع — لا DB lookup)
        3. فحص الخمول: إذا > 30 دقيقة → revoke session + رد 401
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        # تخطي المسارات المستثناة
        if any(request.path.startswith(p) for p in EXEMPT_PATHS):
            return self.get_response(request)

        # تخطي المستخدمين غير المصادقين
        if not hasattr(request, 'user') or not request.user.is_authenticated:
            return self.get_response(request)

        # استخراج session_id من JWT
        session_id = self._extract_session_id(request)
        if session_id:
            # تخزين session_id في request للاستخدام لاحقاً
            request._session_id = session_id

            # فحص الخمول أولاً
            from infra.accounts.services.session_service import SessionService
            is_inactive = SessionService.check_inactivity(session_id)

            if is_inactive:
                from rest_framework.response import Response
                from django.http import JsonResponse
                logger.info(
                    f"[ActivityMiddleware] Session revoked due to inactivity: "
                    f"{session_id} user={request.user.username}"
                )
                return JsonResponse(
                    {
                        'success': False,
                        'error': 'انتهت الجلسة بسبب عدم النشاط. يرجى تسجيل الدخول مجدداً.',
                        'code': 'session_inactive',
                    },
                    status=401,
                )

            # تحديث النشاط
            SessionService.update_activity(session_id)

        response = self.get_response(request)
        return response

    @staticmethod
    def _extract_session_id(request: HttpRequest) -> Optional[str]:
        """استخراج session_id من JWT Access Token."""
        try:
            from rest_framework_simplejwt.authentication import JWTAuthentication
            jwt_auth = JWTAuthentication()
            header = jwt_auth.get_header(request)
            if not header:
                return None
            raw_token = jwt_auth.get_raw_token(header)
            if not raw_token:
                return None
            validated = jwt_auth.get_validated_token(raw_token)
            return validated.get('session_id')
        except Exception:
            return None
