"""
Security Signals - إشارات الأمان
═══════════════════════════════════
تسجيل أحداث تسجيل الدخول/الخروج عبر AuditService.

ملاحظة: إدارة UserSession تتم عبر accounts.services.SessionService
         ولا تحتاج تدخل من Signals (JWT-based).
"""
from django.contrib.auth.signals import (
    user_logged_in, user_logged_out, user_login_failed
)
from django.dispatch import receiver


@receiver(user_logged_in)
def on_user_logged_in(sender, request, user, **kwargs):
    """تحديث معلومات الجلسة عند الدخول الناجح."""
    ip = _get_client_ip(request)
    user_agent = request.META.get('HTTP_USER_AGENT', '') if request else ''

    # إعادة تعيين محاولات الفاشلة وتحديث معلومات الدخول الآمن
    from infra.accounts.services.security_service import SecurityService
    SecurityService.record_successful_login(user, ip or '127.0.0.1', user_agent)

    # تحديث معلومات الجلسة في UserProfile
    try:
        profile = user.authz_profile
        profile.last_login_ip = ip
        profile.last_login_user_agent = user_agent[:500]
        profile.save(update_fields=['last_login_ip', 'last_login_user_agent'])
    except Exception:
        pass

    # تسجيل عبر AuditService
    from infra.audit.services.audit_service import AuditService
    AuditService.log_login(
        user=user, username=user.username,
        action='LOGIN_SUCCESS',
    )

    # ⚠️ UserSession يُدار عبر accounts.services.SessionService
    # لا نُنشئ جلسة هنا — SessionService.create_session() يفعل ذلك مع JWT


@receiver(user_logged_out)
def on_user_logged_out(sender, request, user, **kwargs):
    """تسجيل خروج المستخدم."""
    if user is None:
        return

    from infra.audit.services.audit_service import AuditService
    AuditService.log_login(
        user=user, username=user.username,
        action='LOGOUT',
    )

    # ⚠️ إلغاء الجلسة يتم عبر SessionService.revoke_session()
    # لا نتدخل هنا — AuthService.logout() يفعل ذلك


@receiver(user_login_failed)
def on_user_login_failed(sender, credentials, request, **kwargs):
    """تسجيل محاولة دخول فاشلة + قفل الحساب."""
    from django.contrib.auth import get_user_model
    User = get_user_model()

    username = credentials.get('username', '')
    ip = _get_client_ip(request) if request else None
    user_agent = ''
    if request:
        user_agent = request.META.get('HTTP_USER_AGENT', '')

    # تحديد سبب الفشل
    user_obj = None
    failure_reason = 'invalid_password'
    try:
        user_obj = User.objects.get(username=username)
        from infra.accounts.services.security_service import SecurityService
        if SecurityService.check_lock_state(user_obj).is_locked:
            failure_reason = 'account_locked'
    except User.DoesNotExist:
        failure_reason = 'user_not_found'

    # تسجيل عبر AuditService
    from infra.audit.services.audit_service import AuditService
    AuditService.log_login(
        user=user_obj, username=username,
        action='LOGIN_FAILED',
        failure_reason=failure_reason,
    )

    # تحديث محاولات الدخول الفاشلة + قفل الحساب
    if user_obj:
        from infra.accounts.services.security_service import SecurityService
        prev_locked = SecurityService.check_lock_state(user_obj).is_locked
        SecurityService.record_failed_login(username, ip or '127.0.0.1')
        now_locked = SecurityService.check_lock_state(user_obj).is_locked
        if now_locked and not prev_locked:
            AuditService.log_login(
                user=user_obj, username=username,
                action='ACCOUNT_LOCKED',
            )


# ══════════════════════════════════════════════════════════════
# Helper
# ══════════════════════════════════════════════════════════════

def _get_client_ip(request):
    """استخراج IP العميل."""
    if not request:
        return None
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')
