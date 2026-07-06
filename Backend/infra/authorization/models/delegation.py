"""
Delegation Model — التفويض
═══════════════════════════════
تفويض صلاحيات من مستخدم لآخر لفترة محددة.

مثال:
    مدير في إجازة يُفوِّض صلاحياته لمستخدم X
    من 1 يوليو إلى 10 يوليو
    ثم تنتهي تلقائياً.

القواعد:
    - المُفوِّض يجب أن يملك الصلاحيات التي يُفوِّضها
    - التفويض مؤقت (starts_at → ends_at إلزامي)
    - يمكن تفويض دور كامل أو صلاحيات محددة
    - يمكن إلغاء التفويض مبكراً
    - يُسجّل في Audit Log
"""
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.models.base import TimeStampedModel


class DelegationStatus(models.TextChoices):
    """حالة التفويض."""
    ACTIVE = 'active', _('نشط')
    EXPIRED = 'expired', _('منتهي')
    REVOKED = 'revoked', _('ملغي')
    PENDING = 'pending', _('قيد الانتظار')


class Delegation(TimeStampedModel):
    """
    تفويض صلاحيات — User → User.

    المسؤوليات:
        - تفويض دور كامل أو صلاحيات محددة
        - ضبط فترة التفويض (starts_at, ends_at)
        - إلغاء مبكر
        - تتبع من فوّض ومن استلم ومن وافق
    """
    delegator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='delegations_given',
        verbose_name=_('المُفوِّض'),
        help_text=_('المستخدم الذي يمنح صلاحياته'),
    )
    delegate = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='delegations_received',
        verbose_name=_('المُفوَّض إليه'),
        help_text=_('المستخدم الذي يستلم الصلاحيات'),
    )

    # ما يُفوَّض: دور أو صلاحيات محددة
    role = models.ForeignKey(
        'authorization.Role',
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='delegations',
        verbose_name=_('الدور المُفوَّض'),
        help_text=_('اتركه فارغاً لتفويض صلاحيات محددة بدلاً من دور كامل'),
    )
    permissions = models.ManyToManyField(
        'authorization.Permission',
        blank=True,
        related_name='delegations',
        verbose_name=_('صلاحيات محددة'),
        help_text=_('اتركها فارغة إذا تم تحديد دور — ستُفوَّض كل صلاحيات الدور'),
    )

    # الفترة الزمنية
    reason = models.TextField(
        verbose_name=_('سبب التفويض'),
    )
    starts_at = models.DateTimeField(
        verbose_name=_('يبدأ من'),
    )
    ends_at = models.DateTimeField(
        verbose_name=_('ينتهي في'),
    )

    # الحالة والتتبع
    status = models.CharField(
        max_length=20,
        choices=DelegationStatus.choices,
        default=DelegationStatus.PENDING,
        verbose_name=_('الحالة'),
    )
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='delegation_approvals',
        verbose_name=_('وافق عليه'),
        help_text=_('فارغ = تفويض ذاتي لا يحتاج موافقة'),
    )
    revoked_at = models.DateTimeField(
        null=True, blank=True,
        verbose_name=_('تاريخ الإلغاء'),
    )
    revoked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='delegation_revocations',
        verbose_name=_('ألغاه'),
    )
    notes = models.TextField(
        blank=True,
        verbose_name=_('ملاحظات'),
    )

    class Meta:
        db_table = 'authorization_delegation'
        verbose_name = _('تفويض')
        verbose_name_plural = _('التفويضات')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['delegator', 'status']),
            models.Index(fields=['delegate', 'status']),
            models.Index(fields=['status', 'starts_at', 'ends_at']),
            models.Index(fields=['ends_at']),
        ]

    def __str__(self) -> str:
        return f"{self.delegator} → {self.delegate} ({self.get_status_display()})"

    @property
    def is_expired(self) -> bool:
        """هل التفويض منتهي الصلاحية."""
        return timezone.now() > self.ends_at

    @property
    def is_started(self) -> bool:
        """هل بدأ وقت التفويض."""
        return timezone.now() >= self.starts_at

    @property
    def is_effective(self) -> bool:
        """هل التفويض فعّال الآن (نشط + بدأ + لم ينتهِ)."""
        return (
            self.status == DelegationStatus.ACTIVE
            and self.is_started
            and not self.is_expired
        )

    def get_delegated_permission_codes(self) -> list:
        """جلب أكواد الصلاحيات المُفوَّضة."""
        if self.role_id:
            # تفويض دور كامل
            return self.role.get_all_permission_codes()
        # صلاحيات محددة
        return list(
            self.permissions.filter(is_active=True)
            .values_list('code', flat=True)
        )
