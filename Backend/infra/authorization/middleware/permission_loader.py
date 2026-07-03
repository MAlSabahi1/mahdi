"""
Permission Loader Middleware — تحميل الصلاحيات من Redis
═══════════════════════════════════════════════════════════
كل Request:
    1. يتحقق هل الكاش موجود
    2. إذا لا → يُعيد بناءه من DB
    3. يُرفق الصلاحيات في request._permissions للسرعة
"""
import logging

from django.conf import settings
from django.http import HttpRequest, HttpResponse

logger = logging.getLogger('authorization.middleware')

EXEMPT_PATHS = (
    '/api/v1/auth/login/',
    '/api/v1/auth/refresh/',
    '/admin/',
    '/api/v1/schema/',
    '/api/v1/docs/',
    '/api/v1/redoc/',
)


class PermissionLoaderMiddleware:
    """
    Middleware يُحمّل صلاحيات المستخدم في كل Request.
    يضعها في request._permissions لتجنب cache lookup متكرر.
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

        # تحميل الصلاحيات
        try:
            from infra.authorization.services.permission_service import PermissionService
            permissions = PermissionService.get_user_permissions(request.user)
            request._permissions = permissions
        except Exception as e:
            logger.debug(f"[PermissionLoader] Failed to load permissions: {e}")
            request._permissions = set()

        return self.get_response(request)
