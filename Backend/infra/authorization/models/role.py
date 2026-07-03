"""
Role Model — الأدوار الوظيفية
═══════════════════════════════
Role → RolePermission → Permission

القواعد:
    - الدور يجمع مجموعة صلاحيات
    - لا صلاحيات مباشرة داخل User (خطأ معماري)
    - Through Table (RolePermission) للتتبع الكامل
"""
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models.base import TimeStampedModel
from infra.authorization.models.permission import Permission


class Role(TimeStampedModel):
    """
    الدور الوظيفي — يجمع مجموعة صلاحيات.

    أمثلة:
        مدير النظام, رئيس خدمات, مدخل بيانات, مراجع, مشرف إداري
    """
    name = models.CharField(
        max_length=100, unique=True,
        verbose_name=_('اسم المجموعة'),
    )
    code = models.CharField(
        max_length=50, unique=True, db_index=True,
        verbose_name=_('الرمز الداخلي'),
        help_text=_('مثل: admin, service_head, data_entry'),
    )
    description = models.TextField(
        blank=True, verbose_name=_('الوصف'),
    )
    is_active = models.BooleanField(
        default=True, verbose_name=_('نشط'),
    )
    is_system_role = models.BooleanField(
        default=False, verbose_name=_('مجموعة نظامية'),
        help_text=_('المجموعات النظامية لا يمكن حذفها'),
    )
    priority = models.IntegerField(
        default=0, verbose_name=_('الأولوية'),
        help_text=_('رقم أعلى = أولوية أعلى — لحل التعارضات'),
    )
    permissions = models.ManyToManyField(
        Permission,
        through='RolePermission',
        related_name='roles',
        blank=True,
        verbose_name=_('الصلاحيات'),
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='authz_created_roles',
        verbose_name=_('أنشئ بواسطة'),
    )

    class Meta:
        db_table = 'authorization_role'
        verbose_name = _('مجموعة')
        verbose_name_plural = _('المجموعات')
        ordering = ['-priority', 'name']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self) -> str:
        return self.name

    # ── Permission Checks (DB-level — للـ Admin فقط) ──

    def has_permission(self, permission_code: str) -> bool:
        """فحص صلاحية (DB query — استخدم PermissionService في الكود)."""
        from infra.authorization.registry.permissions import LEGACY_TO_NEW_MAPPING
        mapped_code = LEGACY_TO_NEW_MAPPING.get(permission_code, permission_code)
        return self.permissions.filter(
            code=mapped_code, is_active=True
        ).exists()

    def has_any_permission(self, *codes: str) -> bool:
        from infra.authorization.registry.permissions import LEGACY_TO_NEW_MAPPING
        mapped_codes = [LEGACY_TO_NEW_MAPPING.get(c, c) for c in codes]
        return self.permissions.filter(
            code__in=mapped_codes, is_active=True
        ).exists()


    def get_all_permission_codes(self) -> list:
        """جلب كل أكواد الصلاحيات."""
        return sorted(
            self.permissions.filter(is_active=True)
            .values_list('code', flat=True)
        )

    @classmethod
    def get_available_permissions(cls) -> list:
        return list(
            Permission.objects.filter(is_active=True)
            .values('code', 'label', 'module', 'action', 'scope', 'category')
        )


class RolePermission(TimeStampedModel):
    """
    جدول وسيط: Role ↔ Permission.
    يُسجّل من منح الصلاحية ومتى (للتدقيق).
    """
    role = models.ForeignKey(
        Role, on_delete=models.CASCADE,
        related_name='role_permissions',
    )
    permission = models.ForeignKey(
        Permission, on_delete=models.CASCADE,
        related_name='role_permissions',
    )
    granted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name=_('مُنحت بواسطة'),
    )

    class Meta:
        db_table = 'authorization_role_permission'
        verbose_name = _('صلاحية مجموعة')
        verbose_name_plural = _('صلاحيات المجموعات')
        unique_together = [['role', 'permission']]

    def __str__(self) -> str:
        return f"{self.role.code} → {self.permission.code}"
