"""
Session Model — جلسات المستخدم (Hybrid JWT + Session Layer)
═══════════════════════════════════════════════════════════════
Redis = Fast Layer (session cache, token lookup, activity tracking)
PostgreSQL = Source of Truth (persistent truth, fallback)

كل refresh token يُخزّن كـ hash (SHA-256) في الجلسة.
عند كل refresh: يتم تدوير التوكن (rotation) لمنع Replay Attack.
"""
import uuid
import hashlib
from typing import Optional

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserSession(models.Model):
    """
    جلسة المستخدم — تمثل اتصال فعلي من جهاز معين.

    لماذا لا نعتمد على JWT فقط؟
        - لأن JWT وحده لا يكفي للتحكم المؤسسي.
        - نحتاج: revoke session, logout all devices,
          detect suspicious login, control max sessions, rotate tokens.

    التدفق:
        Client → Refresh Token → Redis lookup →
        If valid: rotate token + update session
        Else: DB fallback
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_('المعرف'),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sessions',
        verbose_name=_('المستخدم'),
    )
    session_id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
        db_index=True,
        verbose_name=_('معرف الجلسة'),
        help_text=_('يُضمّن في Access Token كـ claim'),
    )

    # ── Refresh Token (Stateful) ──
    refresh_token_hash = models.CharField(
        max_length=128,
        db_index=True,
        verbose_name=_('هاش Refresh Token'),
        help_text=_('SHA-256 hash — لا نخزّن التوكن الأصلي أبداً'),
    )

    # ── Device Information ──
    device_name = models.CharField(
        max_length=200,
        blank=True,
        default='',
        verbose_name=_('اسم الجهاز'),
        help_text=_('مثل: iPhone 15, Windows PC'),
    )
    browser = models.CharField(
        max_length=200,
        blank=True,
        default='',
        verbose_name=_('المتصفح'),
        help_text=_('مثل: Chrome 120, Safari 17'),
    )
    os = models.CharField(
        max_length=200,
        blank=True,
        default='',
        verbose_name=_('نظام التشغيل'),
        help_text=_('مثل: Windows 11, iOS 17, Android 14'),
    )
    ip_address = models.GenericIPAddressField(
        verbose_name=_('عنوان IP'),
    )
    user_agent = models.TextField(
        blank=True,
        default='',
        verbose_name=_('User Agent'),
    )

    # ── Lifecycle ──
    last_activity = models.DateTimeField(
        default=timezone.now,
        verbose_name=_('آخر نشاط'),
        help_text=_('يُحدَّث مع كل طلب عبر Middleware'),
    )
    expires_at = models.DateTimeField(
        verbose_name=_('تنتهي في'),
        help_text=_('بعد هذا التاريخ الجلسة غير صالحة'),
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('نشطة'),
    )
    revoked_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('ألغيت في'),
        help_text=_('إذا تم إلغاؤها يدوياً أو بسبب خمول'),
    )
    revoke_reason = models.CharField(
        max_length=50,
        blank=True,
        default='',
        verbose_name=_('سبب الإلغاء'),
        help_text=_('مثل: manual, inactivity, logout, security'),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('تاريخ الإنشاء'),
    )

    class Meta:
        db_table = 'accounts_user_session'
        verbose_name = _('جلسة مستخدم')
        verbose_name_plural = _('جلسات المستخدمين')
        ordering = ['-last_activity']
        indexes = [
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['refresh_token_hash']),
            models.Index(fields=['last_activity']),
            models.Index(fields=['expires_at']),
            models.Index(fields=['is_active', 'expires_at']),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(expires_at__gt=models.F('created_at')),
                name='session_expires_after_creation',
            ),
        ]

    def __str__(self) -> str:
        device = self.device_name or self.ip_address
        status = 'نشطة' if self.is_active else 'ملغاة'
        return f"{self.user} — {device} ({status})"

    # ── Token Hashing ──

    @staticmethod
    def hash_token(token: str) -> str:
        """تحويل refresh token إلى SHA-256 hash."""
        return hashlib.sha256(token.encode('utf-8')).hexdigest()

    def verify_token(self, raw_token: str) -> bool:
        """التحقق من صحة refresh token بمقارنة الهاش."""
        return self.refresh_token_hash == self.hash_token(raw_token)

    def update_token_hash(self, new_raw_token: str) -> None:
        """تحديث هاش التوكن بعد الـ rotation."""
        self.refresh_token_hash = self.hash_token(new_raw_token)
        self.save(update_fields=['refresh_token_hash'])

    # ── Lifecycle Management ──

    @property
    def is_expired(self) -> bool:
        """هل انتهت صلاحية الجلسة."""
        return timezone.now() > self.expires_at

    @property
    def is_valid(self) -> bool:
        """هل الجلسة صالحة (نشطة + غير منتهية)."""
        return self.is_active and not self.is_expired

    @property
    def inactivity_seconds(self) -> int:
        """عدد الثواني منذ آخر نشاط."""
        delta = timezone.now() - self.last_activity
        return int(delta.total_seconds())

    def touch(self) -> None:
        """تحديث آخر نشاط — يُستدعى من Middleware."""
        self.last_activity = timezone.now()
        self.save(update_fields=['last_activity'])

    def revoke(self, reason: str = 'manual') -> None:
        """إلغاء الجلسة."""
        self.is_active = False
        self.revoked_at = timezone.now()
        self.revoke_reason = reason
        self.save(update_fields=['is_active', 'revoked_at', 'revoke_reason'])

    # ── Redis Cache Keys ──

    @property
    def redis_key(self) -> str:
        """مفتاح Redis لهذه الجلسة."""
        return f"session:{self.session_id}"

    @property
    def redis_token_key(self) -> str:
        """مفتاح Redis للبحث عبر token hash."""
        return f"token:{self.refresh_token_hash}"

    def to_redis_dict(self) -> dict:
        """تحويل الجلسة لبيانات Redis (لتخزينها كـ Hash)."""
        return {
            'session_id': str(self.session_id),
            'user_id': str(self.user_id),
            'refresh_token_hash': self.refresh_token_hash,
            'is_active': '1' if self.is_active else '0',
            'expires_at': self.expires_at.isoformat(),
            'last_activity': self.last_activity.isoformat(),
            'ip_address': self.ip_address,
            'device_name': self.device_name,
        }

    @classmethod
    def from_redis_dict(cls, data: dict) -> Optional['UserSession']:
        """إعادة بناء بيانات الجلسة من Redis dict (للقراءة السريعة)."""
        if not data:
            return None
        from django.utils.dateparse import parse_datetime
        session = cls()
        session.session_id = uuid.UUID(data.get('session_id', ''))
        session.user_id = data.get('user_id', '')
        session.refresh_token_hash = data.get('refresh_token_hash', '')
        session.is_active = data.get('is_active') == '1'
        session.ip_address = data.get('ip_address', '')
        session.device_name = data.get('device_name', '')
        expires = data.get('expires_at')
        if expires:
            session.expires_at = parse_datetime(expires)
        activity = data.get('last_activity')
        if activity:
            session.last_activity = parse_datetime(activity)
        return session
