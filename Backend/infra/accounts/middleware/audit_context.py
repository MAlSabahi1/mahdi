"""
Audit Context Middleware — سياق التدقيق
═══════════════════════════════════════════
يستخرج بيانات الطلب (IP, User Agent, Session) ويخزنها في Thread-local
لاستخدامها تلقائياً في سجلات التدقيق (AuditLog).
"""
from django.http import HttpRequest, HttpResponse
from core.utils.audit_context import set_audit_context, clear_audit_context


class AuditContextMiddleware:
    """
    تخزين بيانات الطلب في الذاكرة المؤقتة للـ Thread.
    يُستخدم بواسطة AuditLog.save() للجلب التلقائي للـ IP و User Agent.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        # 1. استخراج IP
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0].strip()
        else:
            ip_address = request.META.get('REMOTE_ADDR')

        # 2. استخراج User Agent
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        # 3. استخراج الجلسة والمستخدم
        session_key = None
        if hasattr(request, 'session') and request.session.session_key:
            session_key = request.session.session_key

        user = None
        if hasattr(request, 'user') and request.user.is_authenticated:
            user = request.user

        # وضع البيانات في السياق
        set_audit_context(
            ip_address=ip_address,
            user_agent=user_agent,
            session_key=session_key,
            user=user,
        )

        try:
            response = self.get_response(request)
            return response
        finally:
            # تنظيف السياق دائماً لمنع تسرب البيانات بين الطلبات
            clear_audit_context()
