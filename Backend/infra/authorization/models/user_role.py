"""
UserRole Model — ربط المستخدم بالأدوار
═══════════════════════════════════════════
User ↔ Role (M2M عبر Through Table)

القواعد:
    - المستخدم يحمل أدواراً متعددة
    - كل ربط يُسجّل: من أسنده، متى، تنتهي متى
    - الأدوار المنتهية (expired) لا تُحسب
"""
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.models.base import TimeStampedModel
from infra.authorization.models.role import Role


class UserRole(TimeStampedModel):
    """
    ربط مستخدم بدور.

    يدعم:
        - أدوار متعددة لكل مستخدم
        - أدوار مؤقتة (expires_at)
        - تتبع من أسند الدور
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='authorization_roles',
        verbose_name=_('المستخدم'),
    )
    role = models.ForeignKey(
        Role, on_delete=models.CASCADE,
        related_name='user_assignments',
        verbose_name=_('الدور'),
    )
    is_active = models.BooleanField(
        default=True, verbose_name=_('نشط'),
    )
    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='authz_role_assignments_given',
        verbose_name=_('أُسند بواسطة'),
    )
    assigned_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('تاريخ الإسناد'),
    )
    expires_at = models.DateTimeField(
        null=True, blank=True,
        verbose_name=_('تنتهي في'),
        help_text=_('اتركه فارغاً لدور دائم'),
    )
    notes = models.TextField(
        blank=True,
        verbose_name=_('ملاحظات'),
    )

    class Meta:
        db_table = 'authorization_user_role'
        verbose_name = _('دور مستخدم')
        verbose_name_plural = _('أدوار المستخدمين')
        unique_together = [['user', 'role']]
        indexes = [
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['role']),
            models.Index(fields=['expires_at']),
        ]

    def __str__(self) -> str:
        return f"{self.user} ← {self.role.code}"

    @property
    def is_expired(self) -> bool:
        """هل الدور منتهي الصلاحية."""
        if self.expires_at is None:
            return False
        return timezone.now() > self.expires_at

    @property
    def is_effective(self) -> bool:
        """هل الدور فعّال (نشط + غير منتهي + الدور نفسه نشط)."""
        return (
            self.is_active
            and not self.is_expired
            and self.role.is_active
        )
