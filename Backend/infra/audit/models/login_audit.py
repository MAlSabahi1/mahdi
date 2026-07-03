"""
LoginAuditLog — سجل تدقيق تسجيل الدخول
═══════════════════════════════════════════
منفصل عن AuditLog لأداء أفضل وتحليل أمني مخصص.

يُسجل كل محاولة:
    - دخول ناجح/فاشل
    - خروج
    - تجديد توكن
    - قفل/فتح حساب
    - تغيير/إعادة تعيين كلمة مرور
"""
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.postgres.indexes import BrinIndex
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class LoginAction(models.TextChoices):
    """أنواع أحداث تسجيل الدخول."""
    LOGIN_SUCCESS = 'LOGIN_SUCCESS', _('دخول ناجح')
    LOGIN_FAILED = 'LOGIN_FAILED', _('دخول فاشل')
    LOGOUT = 'LOGOUT', _('خروج')
    TOKEN_REFRESH = 'TOKEN_REFRESH', _('تجديد توكن')
    ACCOUNT_LOCKED = 'ACCOUNT_LOCKED', _('قفل حساب')
    ACCOUNT_UNLOCKED = 'ACCOUNT_UNLOCKED', _('فتح حساب')
    PASSWORD_CHANGED = 'PASSWORD_CHANGED', _('تغيير كلمة مرور')
    PASSWORD_RESET = 'PASSWORD_RESET', _('إعادة تعيين كلمة مرور')
    SESSION_REVOKED = 'SESSION_REVOKED', _('إلغاء جلسة')
    SUSPICIOUS_LOGIN = 'SUSPICIOUS_LOGIN', _('دخول مشبوه')


class FailureReason(models.TextChoices):
    """أسباب فشل تسجيل الدخول."""
    NONE = '', _('لا يوجد')
    INVALID_PASSWORD = 'invalid_password', _('كلمة مرور خاطئة')
    ACCOUNT_LOCKED = 'account_locked', _('حساب مغلق')
    ACCOUNT_DISABLED = 'account_disabled', _('حساب معطل')
    USER_NOT_FOUND = 'user_not_found', _('مستخدم غير موجود')
    TWO_FACTOR_FAILED = 'two_factor_failed', _('فشل التحقق الثنائي')
    SESSION_EXPIRED = 'session_expired', _('جلسة منتهية')
    TOKEN_INVALID = 'token_invalid', _('توكن غير صالح')


class LoginAuditLog(models.Model):
    """
    سجل تدقيق تسجيل الدخول — تحليل أمني مخصص.

    حالة استخدام:
        إذا تغيرت حالة فرد من "عامل" إلى "منقطع"،
        يستطيع مدير النظام معرفة:
            من قام بالتغيير؟ متى؟ من أي جهاز؟
    """
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='login_audit_logs', verbose_name=_('المستخدم'),
    )
    username_attempted = models.CharField(
        max_length=150, verbose_name=_('اسم المستخدم المُدخل'),
    )
    action = models.CharField(
        max_length=20, choices=LoginAction.choices,
        verbose_name=_('الحدث'),
    )
    ip_address = models.GenericIPAddressField(
        null=True, blank=True, verbose_name=_('عنوان IP'),
    )
    user_agent = models.TextField(
        blank=True, default='', verbose_name=_('User Agent'),
    )
    failure_reason = models.CharField(
        max_length=30, choices=FailureReason.choices,
        blank=True, default='', verbose_name=_('سبب الفشل'),
    )
    extra_data = models.JSONField(
        null=True, blank=True, verbose_name=_('بيانات إضافية'),
    )
    session_key = models.CharField(
        max_length=64, null=True, blank=True, verbose_name=_('معرف الجلسة'),
    )
    geo_location = models.CharField(
        max_length=100, blank=True, default='',
        verbose_name=_('الموقع الجغرافي'),
        help_text=_('يُحسب من IP إذا متاح'),
    )
    timestamp = models.DateTimeField(
        auto_now_add=True, verbose_name=_('التوقيت'),
    )

    class Meta:
        db_table = 'audit_login_log'
        verbose_name = _('سجل دخول')
        verbose_name_plural = _('سجلات الدخول')
        ordering = ['-timestamp']
        default_permissions = ('add', 'view')
        indexes = [
            models.Index(fields=['action', 'timestamp']),
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['ip_address']),
            models.Index(fields=['timestamp']),
            models.Index(fields=['username_attempted']),
            models.Index(fields=['failure_reason']),
            BrinIndex(fields=['timestamp'], name='login_audit_timestamp_brin'),
        ]

    def __str__(self) -> str:
        return f"[{self.timestamp}] {self.username_attempted} — {self.get_action_display()}"

    def save(self, *args, **kwargs):
        from infra.audit.utils.audit_context import get_audit_context
        context = get_audit_context()
        if not self.ip_address and context.get('ip_address'):
            self.ip_address = context['ip_address']
        if not self.user_agent and context.get('user_agent'):
            self.user_agent = context['user_agent']
        if not self.session_key and context.get('session_key'):
            self.session_key = context['session_key']
        super().save(*args, **kwargs)
