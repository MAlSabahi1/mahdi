"""
PermissionGroup Model — مجموعات الصلاحيات
═══════════════════════════════════════════
تجميع الصلاحيات في مجموعات لتسهيل الإدارة من الـ UI.

أمثلة المجموعات:
    Users, Personnel, Documents, Finance,
    Reports, Security, Audit, Settings

الاستخدام:
    GET /api/v1/authorization/permissions/grouped/
    → يُعيد الصلاحيات مُجمَّعة حسب المجموعة لعرضها في Admin UI.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models.base import TimeStampedModel


class PermissionGroup(TimeStampedModel):
    """
    مجموعة صلاحيات — لتنظيم عرض الصلاحيات في واجهة الإدارة.

    المسؤوليات:
        - تجميع الصلاحيات المتعلقة بنظام فرعي واحد
        - ترتيب العرض في Admin UI
        - أيقونة لكل مجموعة (للـ Frontend)
    """
    code = models.CharField(
        max_length=50, unique=True, db_index=True,
        verbose_name=_('الرمز'),
        help_text=_('مثل: users, personnel, reports, security'),
    )
    name = models.CharField(
        max_length=100,
        verbose_name=_('الاسم بالعربي'),
        help_text=_('مثل: المستخدمين، شؤون الأفراد'),
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('الوصف'),
    )
    icon = models.CharField(
        max_length=50, default='shield',
        verbose_name=_('الأيقونة'),
        help_text=_('اسم الأيقونة للـ Frontend: users, shield, file-text'),
    )
    display_order = models.IntegerField(
        default=0,
        verbose_name=_('ترتيب العرض'),
        help_text=_('رقم أقل = يظهر أولاً'),
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('نشطة'),
    )

    class Meta:
        db_table = 'authorization_permission_group'
        verbose_name = _('مجموعة صلاحيات')
        verbose_name_plural = _('مجموعات الصلاحيات')
        ordering = ['display_order', 'name']

    def __str__(self) -> str:
        return f"{self.name} ({self.code})"

    def get_permissions_count(self) -> int:
        """عدد الصلاحيات في هذه المجموعة."""
        return self.permissions.filter(is_active=True).count()
