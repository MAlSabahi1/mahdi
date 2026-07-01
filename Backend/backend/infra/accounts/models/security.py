"""
Security Model — ملف أمان المستخدم
═════════════════════════════════════
مفصول عن User لأن الأمان مسؤولية مختلفة.
يحتوي على: محاولات دخول فاشلة، إقفال الحساب، سياسات كلمة المرور.

القاعدة المطبقة:
    5 failed attempts → lock 15 minutes
"""
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


# ── ثوابت سياسات الأمان ──
MAX_FAILED_ATTEMPTS: int = 5
LOCKOUT_DURATION_MINUTES: int = 15


class SecurityProfile(models.Model):
    """
    ملف الأمان — كل ما يتعلق بحماية حساب المستخدم.

    لا يُخلط بـ User (الهوية) أو Session (الحالة الحالية).
    هذا مسؤول عن: القفل، سياسات كلمة المرور، كشف السلوك المشبوه.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='security_profile',
        verbose_name=_('المستخدم'),
    )

    # ── Login Attempts & Lockout ──
    failed_login_attempts = models.PositiveIntegerField(
        default=0,
        verbose_name=_('محاولات الدخول الفاشلة'),
    )
    is_locked = models.BooleanField(
        default=False,
        verbose_name=_('مقفل'),
        help_text=_('يُقفل تلقائياً بعد 5 محاولات فاشلة'),
    )
    locked_until = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('مقفل حتى'),
    )
    last_failed_ip = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name=_('آخر IP فاشل'),
    )
    last_failed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('آخر محاولة فاشلة'),
    )

    # ── Password Policies ──
    password_changed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('آخر تغيير كلمة مرور'),
    )
    must_change_password = models.BooleanField(
        default=False,
        verbose_name=_('يجب تغيير كلمة المرور'),
        help_text=_('يُفعّل عند إعادة تعيين كلمة المرور بواسطة المدير'),
    )
    password_history = models.JSONField(
        default=list,
        blank=True,
        verbose_name=_('سجل كلمات المرور'),
        help_text=_('هاشات آخر 5 كلمات مرور لمنع إعادة الاستخدام'),
    )

    # ── Suspicious Activity ──
    last_known_ip = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name=_('آخر IP معروف'),
        help_text=_('آخر IP ناجح — للكشف عن تغيير الموقع'),
    )
    last_known_user_agent = models.TextField(
        blank=True,
        default='',
        verbose_name=_('آخر User Agent معروف'),
    )

    # ── Timestamps ──
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('تاريخ الإنشاء'),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('تاريخ التحديث'),
    )

    class Meta:
        db_table = 'accounts_security_profile'
        verbose_name = _('ملف أمان')
        verbose_name_plural = _('ملفات الأمان')
        indexes = [
            models.Index(fields=['is_locked']),
            models.Index(fields=['last_failed_at']),
        ]

    def __str__(self) -> str:
        status = 'مقفل' if self.is_locked else 'نشط'
        return f"{self.user} — {status}"

    # ── Lockout Logic ──

    def record_failed_attempt(self, ip_address: str) -> None:
        """
        تسجيل محاولة دخول فاشلة.
        إذا وصلت المحاولات لـ 5: يُقفل الحساب 15 دقيقة.
        """
        self.failed_login_attempts += 1
        self.last_failed_ip = ip_address
        self.last_failed_at = timezone.now()

        if self.failed_login_attempts >= MAX_FAILED_ATTEMPTS:
            self.is_locked = True
            self.locked_until = timezone.now() + timezone.timedelta(
                minutes=LOCKOUT_DURATION_MINUTES
            )

        self.save(update_fields=[
            'failed_login_attempts', 'last_failed_ip',
            'last_failed_at', 'is_locked', 'locked_until',
        ])

    def record_successful_login(self, ip_address: str, user_agent: str) -> None:
        """
        تسجيل دخول ناجح — يُعيد تعيين عداد المحاولات الفاشلة.
        يُحدّث آخر IP و User Agent المعروفين.
        """
        self.failed_login_attempts = 0
        self.is_locked = False
        self.locked_until = None
        self.last_failed_ip = None
        self.last_failed_at = None
        self.last_known_ip = ip_address
        self.last_known_user_agent = user_agent
        self.save(update_fields=[
            'failed_login_attempts', 'is_locked', 'locked_until',
            'last_failed_ip', 'last_failed_at',
            'last_known_ip', 'last_known_user_agent',
        ])

    def check_lock_state(self) -> bool:
        """
        فحص حالة القفل — يُعيد True إذا الحساب مقفل.
        يُفك القفل تلقائياً إذا انتهت مدة الإقفال.
        """
        if not self.is_locked:
            return False

        if self.locked_until and timezone.now() > self.locked_until:
            self.unlock()
            return False

        return True

    def unlock(self) -> None:
        """فك قفل الحساب وإعادة تعيين العداد."""
        self.is_locked = False
        self.locked_until = None
        self.failed_login_attempts = 0
        self.last_failed_ip = None
        self.last_failed_at = None
        self.save(update_fields=[
            'is_locked', 'locked_until', 'failed_login_attempts',
            'last_failed_ip', 'last_failed_at',
        ])

    # ── Password Policies ──

    def record_password_change(self, password_hash: str) -> None:
        """
        تسجيل تغيير كلمة المرور.
        يحتفظ بآخر 5 هاشات لمنع إعادة الاستخدام.
        """
        self.password_changed_at = timezone.now()
        self.must_change_password = False

        history = self.password_history or []
        history.insert(0, password_hash)
        self.password_history = history[:5]

        self.save(update_fields=[
            'password_changed_at', 'must_change_password', 'password_history',
        ])

    def is_password_reused(self, password_hash: str) -> bool:
        """فحص هل كلمة المرور مُستخدمة سابقاً."""
        return password_hash in (self.password_history or [])

    # ── Suspicious Login Detection ──

    def is_suspicious_login(self, ip_address: str, user_agent: str) -> bool:
        """
        كشف تسجيل دخول مشبوه — تغيير IP أو User Agent.
        لا يمنع الدخول، لكن يُسجّل في Audit Log.
        """
        if not self.last_known_ip:
            return False

        ip_changed = (self.last_known_ip != ip_address)
        ua_changed = (
            self.last_known_user_agent
            and self.last_known_user_agent != user_agent
        )

        return ip_changed and ua_changed

    @property
    def lockout_remaining_seconds(self) -> int:
        """الوقت المتبقي على انتهاء القفل بالثواني."""
        if not self.is_locked or not self.locked_until:
            return 0
        remaining = (self.locked_until - timezone.now()).total_seconds()
        return max(0, int(remaining))
