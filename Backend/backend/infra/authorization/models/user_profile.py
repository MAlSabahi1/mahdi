"""
UserProfile Model — ملف المستخدم التنظيمي
════════════════════════════════════════════
يربط المستخدم بالهيكل التنظيمي + الدور الأساسي.

القواعد:
    - بدون أمان (SecurityProfile في accounts)
    - بدون business logic
    - Data Scope يعتمد على: security_admin, central_department/branch/district_police
"""
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models.base import TimeStampedModel
from infra.authorization.models.role import Role


class UserProfile(TimeStampedModel):
    """
    ملف المستخدم التنظيمي.

    المسؤوليات:
        - ربط المستخدم بالهيكل التنظيمي (محافظة → إدارة → قسم)
        - الدور الأساسي للمستخدم
        - نطاق البيانات (Data Scope)
        - تفضيلات المستخدم
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='authz_profile',
        verbose_name=_('المستخدم'),
    )
    role = models.ForeignKey(
        Role, on_delete=models.PROTECT,
        related_name='primary_users',
        verbose_name=_('الدور الأساسي'),
    )

    # ── الهيكل التنظيمي الأمني ──
    security_admin = models.ForeignKey(
        'core.SecurityAdministration', on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='auth_staff_profiles',
        verbose_name=_('إدارة أمن المحافظة'),
    )
    central_department = models.ForeignKey(
        'core.CentralDepartment', on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='auth_staff_profiles',
        verbose_name=_('الإدارة المركزية'),
    )
    branch = models.ForeignKey(
        'core.Branch', on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='auth_staff_profiles',
        verbose_name=_('الفرع'),
    )
    district_police = models.ForeignKey(
        'core.DistrictPolice', on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='auth_staff_profiles',
        verbose_name=_('أمن المديرية'),
    )
    division = models.ForeignKey(
        'core.Division', on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='auth_staff_profiles',
        verbose_name=_('القسم'),
    )
    unit = models.ForeignKey(
        'core.Unit', on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='auth_staff_profiles',
        verbose_name=_('الوحدة'),
    )


    # ── نطاق الإشراف ──
    supervised_security_admins = models.ManyToManyField(
        'core.SecurityAdministration',
        blank=True,
        related_name='auth_supervisors',
        verbose_name=_('إدارات الأمن المُشرف عليها'),
    )
    supervises_all = models.BooleanField(
        default=False,
        verbose_name=_('يشرف على جميع الإدارات'),
    )

    # ── تفضيلات ──
    language = models.CharField(
        max_length=5, default='ar',
        choices=[('ar', _('العربية')), ('en', _('الإنجليزية'))],
        verbose_name=_('اللغة'),
    )
    admin_notes = models.TextField(
        blank=True, verbose_name=_('ملاحظات المدير'),
    )

    class Meta:
        db_table = 'authorization_user_profile'
        verbose_name = _('ملف مستخدم')
        verbose_name_plural = _('ملفات المستخدمين')
        indexes = [
            models.Index(fields=['role']),
            models.Index(fields=['security_admin']),
        ]

    def __str__(self) -> str:
        return f"{self.user} ({self.role.name})"

    # ── Data Scope (ABAC) ──

    def has_security_admin_scope(self, security_admin_id: int) -> bool:
        """هل يمكنه الوصول لبيانات إدارة أمن هذه المحافظة؟"""
        if self.user.is_superuser or self.supervises_all:
            return True
        if self.supervised_security_admins.filter(pk=security_admin_id).exists():
            return True
        return self.security_admin_id == security_admin_id

    def get_accessible_security_admin_ids(self) -> list:
        """قائمة إدارات الأمن التي يمكنه الوصول إليها."""
        from core.models.organization import SecurityAdministration
        if self.user.is_superuser or self.supervises_all:
            return list(SecurityAdministration.objects.values_list('pk', flat=True))
        sa_ids = set()
        if self.security_admin_id:
            sa_ids.add(self.security_admin_id)
        sa_ids.update(
            self.supervised_security_admins.values_list('pk', flat=True)
        )
        return list(sa_ids)
