"""
RecordACL Model — قيود الوصول على مستوى السجل الفردي
═══════════════════════════════════════════════════════
Record-Level Security: منع/سماح لمستخدم أو دور بالوصول لسجل بعينه.

أمثلة:
    - ملف الفرد رقم 101 → مقيّد (سري)
    - مستند رقم 2024-05 → ممنوع على المستخدم X

التدفق:
    PermissionService.has_permission() → True
    RecordACLService.check_access(user, obj) → False (deny rule)
    → النتيجة: ممنوع
"""
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.models.base import TimeStampedModel


class AccessType(models.TextChoices):
    """نوع القيد: سماح أو منع."""
    ALLOW = 'allow', _('سماح')
    DENY = 'deny', _('منع')


class RecordACL(TimeStampedModel):
    """
    قيد وصول على سجل فردي.

    القواعد:
        - deny يتغلب على allow (Deny-First)
        - يمكن تقييد مستخدم أو دور أو كليهما
        - القيود المنتهية (expires_at) لا تُحسب
        - يُسجَّل من وضع القيد ومتى (للتدقيق)
    """
    # الكائن المستهدف (Generic FK)
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE,
        verbose_name=_('نوع السجل'),
        help_text=_('مثل: PersonnelMaster, Document'),
    )
    object_id = models.CharField(
        max_length=100,
        verbose_name=_('معرف السجل'),
    )
    content_object = GenericForeignKey('content_type', 'object_id')

    # المستهدف بالقيد (مستخدم أو دور أو كلاهما)
    target_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='record_acls',
        verbose_name=_('المستخدم'),
        help_text=_('اتركه فارغاً لتطبيق القيد على الجميع'),
    )
    target_role = models.ForeignKey(
        'authorization.Role',
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='record_acls',
        verbose_name=_('الدور'),
        help_text=_('اتركه فارغاً لعدم تقييد دور'),
    )

    # تفاصيل القيد
    access_type = models.CharField(
        max_length=10,
        choices=AccessType.choices,
        default=AccessType.DENY,
        verbose_name=_('نوع القيد'),
    )
    permission_code = models.CharField(
        max_length=100, blank=True, default='',
        verbose_name=_('الصلاحية المقيّدة'),
        help_text=_('اتركه فارغاً لتقييد كل العمليات على هذا السجل'),
    )
    reason = models.TextField(
        verbose_name=_('سبب القيد'),
    )

    # من وضع القيد ومتى ينتهي
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='created_record_acls',
        verbose_name=_('أُنشئ بواسطة'),
    )
    expires_at = models.DateTimeField(
        null=True, blank=True,
        verbose_name=_('تنتهي في'),
        help_text=_('اتركه فارغاً لقيد دائم'),
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('نشط'),
    )

    class Meta:
        db_table = 'authorization_record_acl'
        verbose_name = _('قيد وصول سجل')
        verbose_name_plural = _('قيود الوصول على السجلات')
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['target_user', 'is_active']),
            models.Index(fields=['target_role', 'is_active']),
            models.Index(fields=['is_active', 'expires_at']),
        ]

    def __str__(self) -> str:
        target = self.target_user or self.target_role or 'الجميع'
        return f"{self.access_type}: {target} → {self.content_type}#{self.object_id}"

    @property
    def is_expired(self) -> bool:
        """هل القيد منتهي الصلاحية."""
        if self.expires_at is None:
            return False
        return timezone.now() > self.expires_at

    @property
    def is_effective(self) -> bool:
        """هل القيد فعّال (نشط + غير منتهي)."""
        return self.is_active and not self.is_expired
