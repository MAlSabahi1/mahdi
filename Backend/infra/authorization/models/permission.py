"""
Permission Model — صلاحية مُهيكلة
═══════════════════════════════════
module.action.scope

5 مستويات:
    1. page    — هل يدخل الصفحة
    2. component — هل يرى الزر/القائمة
    3. action  — هل ينفذ العملية
    4. data    — أي بيانات يراها (scope)
    5. field   — أي حقول يراها/يعدلها
"""
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models.base import TimeStampedModel


class PermissionCategory(models.TextChoices):
    """تصنيف الصلاحية حسب المستوى."""
    PAGE = 'page', _('صفحة')
    COMPONENT = 'component', _('عنصر واجهة')
    ACTION = 'action', _('إجراء')
    DATA = 'data', _('نطاق بيانات')
    FIELD = 'field', _('حقل')


class Permission(TimeStampedModel):
    """
    صلاحية مُهيكلة — module.action.scope.

    أمثلة:
        users.view.all         → رؤية جميع المستخدمين
        personnel.view.department → رؤية أفراد القسم فقط
        personnel.edit_salary.all → تعديل الراتب (field permission)
        services.approve.all   → الموافقة على الخدمات
    """
    code = models.CharField(
        max_length=100, unique=True, db_index=True,
        verbose_name=_('الكود'),
        help_text=_('يُبنى تلقائياً: module.action.scope'),
    )
    module = models.CharField(
        max_length=50, verbose_name=_('الشاشة'),
        help_text=_('مثل: users, personnel, services, reports, system'),
    )
    action = models.CharField(
        max_length=50, verbose_name=_('الفعل'),
        help_text=_('مثل: view, create, edit, delete, approve, export'),
    )
    scope = models.CharField(
        max_length=50, default='all', verbose_name=_('النطاق'),
        help_text=_('مثل: all, own, department, governorate'),
    )
    label = models.CharField(
        max_length=200, verbose_name=_('الوصف بالعربي'),
    )
    description = models.TextField(
        blank=True, verbose_name=_('شرح تفصيلي'),
    )
    category = models.CharField(
        max_length=20,
        choices=PermissionCategory.choices,
        default=PermissionCategory.ACTION,
        verbose_name=_('تصنيف الصلاحية'),
        help_text=_('المستوى: صفحة، عنصر، إجراء، بيانات، حقل'),
    )
    is_active = models.BooleanField(
        default=True, verbose_name=_('نشطة'),
    )
    is_system = models.BooleanField(
        default=True, verbose_name=_('صلاحية نظامية'),
        help_text=_('الصلاحيات النظامية لا يمكن حذفها'),
    )
    requires_dual_auth = models.BooleanField(
        default=False, verbose_name=_('تتطلب تفويض مزدوج'),
    )
    group = models.ForeignKey(
        'authorization.PermissionGroup',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='permissions',
        verbose_name=_('مجموعة الصلاحيات'),
        help_text=_('يُحدد تلقائياً بواسطة seed_permissions حسب الوحدة (module)'),
    )

    class Meta:
        db_table = 'authorization_permission'
        verbose_name = _('صلاحية')
        verbose_name_plural = _('الصلاحيات')
        ordering = ['module', 'action', 'scope']
        unique_together = [['module', 'action', 'scope']]
        indexes = [
            models.Index(fields=['module']),
            models.Index(fields=['is_active']),
            models.Index(fields=['module', 'action']),
            models.Index(fields=['category']),
            models.Index(fields=['code']),
        ]

    def __str__(self) -> str:
        return f"{self.code} — {self.label}"

    def save(self, *args, **kwargs):
        # بناء الكود تلقائياً
        expected = f"{self.module}.{self.action}.{self.scope}"
        if not self.code or self.code != expected:
            self.code = expected
        super().save(*args, **kwargs)

    @classmethod
    def get_module_choices(cls) -> list:
        """الأنظمة الفرعية المتاحة."""
        return list(
            cls.objects.filter(is_active=True)
            .values_list('module', flat=True)
            .distinct()
        )

    @classmethod
    def get_by_category(cls, category: str):
        """جلب الصلاحيات حسب التصنيف."""
        return cls.objects.filter(is_active=True, category=category)
