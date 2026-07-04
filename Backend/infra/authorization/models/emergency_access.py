"""
EmergencyAccess Model — الوصول الطارئ (Break Glass)
═══════════════════════════════════════════════════════
صلاحيات طوارئ تُمنح مؤقتاً عند الضرورة القصوى.

القواعد:
    - يُمنح فقط من مستخدم يملك صلاحية emergency.grant
    - مدة أقصى 24 ساعة (إلزامي)
    - يُسجّل بالكامل في Audit Log بمستوى CRITICAL
    - يُراجع إلزامياً بعد الانتهاء
    - ينتهي تلقائياً

التدفق:
    1. المدير يمنح وصول طوارئ → الحالة: active
    2. المستخدم يستخدم الصلاحيات → كل عملية تُسجّل
    3. الوقت ينتهي → الحالة: expired
    4. المدقق يراجع → الحالة: reviewed
"""
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.models.base import TimeStampedModel


class EmergencyStatus(models.TextChoices):
    """حالة الوصول الطارئ."""
    ACTIVE = 'active', _('نشط')
    EXPIRED = 'expired', _('منتهي')
    REVOKED = 'revoked', _('ملغي')
    REVIEWED = 'reviewed', _('تمت المراجعة')


class EmergencyAccess(TimeStampedModel):
    """
    وصول طارئ (Break Glass) — صلاحيات مؤقتة مع تدقيق كامل.

    المسؤوليات:
        - منح صلاحيات طوارئ مؤقتة
        - تسجيل كامل لكل عملية تحت الطوارئ
        - انتهاء تلقائي بعد المدة المحددة
        - مراجعة إلزامية بعد الانتهاء
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='emergency_accesses',
        verbose_name=_('المستخدم'),
    )
    granted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='emergency_grants',
        verbose_name=_('مُنح بواسطة'),
    )

    # السبب والصلاحيات
    reason = models.TextField(
        verbose_name=_('سبب الطوارئ'),
        help_text=_('إلزامي — يُعرض في التدقيق'),
    )
    permissions = models.ManyToManyField(
        'authorization.Permission',
        related_name='emergency_accesses',
        verbose_name=_('الصلاحيات الممنوحة'),
    )

    # التوقيت
    granted_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('تاريخ المنح'),
    )
    expires_at = models.DateTimeField(
        verbose_name=_('ينتهي في'),
        help_text=_('أقصى مدة: 24 ساعة'),
    )

    # الحالة
    status = models.CharField(
        max_length=20,
        choices=EmergencyStatus.choices,
        default=EmergencyStatus.ACTIVE,
        verbose_name=_('الحالة'),
    )

    # الإلغاء المبكر
    revoked_at = models.DateTimeField(
        null=True, blank=True,
        verbose_name=_('تاريخ الإلغاء'),
    )
    revoked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='emergency_revocations',
        verbose_name=_('ألغاه'),
    )

    # المراجعة
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='emergency_reviews',
        verbose_name=_('راجعه'),
    )
    reviewed_at = models.DateTimeField(
        null=True, blank=True,
        verbose_name=_('تاريخ المراجعة'),
    )
    audit_notes = models.TextField(
        blank=True,
        verbose_name=_('ملاحظات التدقيق'),
        help_text=_('ملاحظات المراجع بعد انتهاء الطوارئ'),
    )

    class Meta:
        db_table = 'authorization_emergency_access'
        verbose_name = _('وصول طارئ')
        verbose_name_plural = _('وصول الطوارئ')
        ordering = ['-granted_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['status', 'expires_at']),
            models.Index(fields=['granted_by']),
        ]

    def __str__(self) -> str:
        return f"🚨 {self.user} — {self.get_status_display()} ({self.reason[:50]})"

    @property
    def is_expired(self) -> bool:
        return timezone.now() > self.expires_at

    @property
    def is_effective(self) -> bool:
        """هل الوصول الطارئ فعّال الآن."""
        return self.status == EmergencyStatus.ACTIVE and not self.is_expired

    @property
    def needs_review(self) -> bool:
        """هل يحتاج مراجعة (منتهي ولم يُراجع بعد)."""
        return (
            self.status in (EmergencyStatus.EXPIRED, EmergencyStatus.REVOKED)
            and self.reviewed_by is None
        )

    def get_permission_codes(self) -> list:
        """أكواد الصلاحيات الممنوحة."""
        return list(
            self.permissions.filter(is_active=True)
            .values_list('code', flat=True)
        )
