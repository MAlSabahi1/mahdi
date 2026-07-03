"""
Audit Context — Thread-local context لبيانات الطلب
════════════════════════════════════════════════════════
يُخزّن IP, User-Agent, Session Key تلقائياً من Middleware.
يُستخدم في AuditLog.save() لملء الحقول تلقائياً.
"""
import threading

_thread_local = threading.local()


def set_audit_context(
    ip_address: str = None,
    user_agent: str = None,
    session_key: str = None,
    user=None,
) -> None:
    """تعيين سياق التدقيق — يُستدعى من Middleware."""
    _thread_local.audit_context = {
        'ip_address': ip_address,
        'user_agent': user_agent,
        'session_key': session_key,
        'user': user,
    }


def get_audit_context() -> dict:
    """جلب سياق التدقيق — يُستدعى من AuditLog.save()."""
    return getattr(_thread_local, 'audit_context', {})


def clear_audit_context() -> None:
    """مسح السياق — يُستدعى في نهاية الطلب."""
    _thread_local.audit_context = {}
