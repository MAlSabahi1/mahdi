"""
Security Middleware - وسيط الأمان
═════════════════════════════════════
1. CurrentUserMiddleware: يضبط current_user في PostgreSQL لجداول الظل
2. SessionTrackingMiddleware: تتبع نشاط الجلسة

⚠️ AuditContextMiddleware → انتقل إلى accounts/middleware/audit_context.py
"""
from django.utils import timezone
from django.db import connection


class CurrentUserMiddleware:
    """
    يضبط متغير مؤقت في PostgreSQL لمعرفة المستخدم الحالي.
    يُستخدم بواسطة Triggers جداول الظل.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if hasattr(request, 'user') and request.user.is_authenticated:
            try:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SET LOCAL myapp.current_user = %s",
                        [str(request.user.pk)]
                    )
            except Exception:
                pass

        response = self.get_response(request)
        return response


class SessionTrackingMiddleware:
    """تتبع آخر نشاط للمستخدم وتحديث الجلسة."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if (hasattr(request, 'user') and
            request.user.is_authenticated and
            hasattr(request, 'session') and
            request.session.session_key):

            from infra.accounts.models import UserSession
            try:
                UserSession.objects.filter(
                    session_key=request.session.session_key,
                    is_active=True
                ).update(last_activity=timezone.now())
            except Exception:
                pass
        return response
