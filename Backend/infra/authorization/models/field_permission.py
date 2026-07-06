"""
FieldPermission Model — قيود الحقول الحساسة
═══════════════════════════════════════════════
Field-Level Security: تحديد أي حقول يمكن للمستخدم رؤيتها/تعديلها.

أمثلة:
    module=personnel, field=salary → view=personnel.view_salary.all
    module=personnel, field=bank_account → view=personnel.view_bank.all

التطبيق:
    FieldSecurityMixin في الـ Serializer يقرأ هذا الجدول
    ويحذف الحقول التي لا يملك المستخدم صلاحية رؤيتها.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models.base import TimeStampedModel


class FieldPermission(TimeStampedModel):
    """
    تعريف حقل حساس + الصلاحيات المطلوبة لرؤيته/تعديله.

    المسؤوليات:
        - تعريف الحقول الحساسة لكل نظام فرعي
        - ربط كل حقل بصلاحية عرض وصلاحية تعديل
        - تحديد هل الحقل حساس (يُسجّل الوصول إليه)
    """
    module = models.CharField(
        max_length=50,
        verbose_name=_('النظام الفرعي'),
        help_text=_('مثل: personnel, services, finance'),
    )
    field_name = models.CharField(
        max_length=100,
        verbose_name=_('اسم الحقل'),
        help_text=_('اسم الحقل في الـ Serializer: salary, bank_account, military_number'),
    )
    label = models.CharField(
        max_length=200,
        verbose_name=_('الوصف بالعربي'),
        help_text=_('مثل: الراتب، الحساب البنكي'),
    )
    view_permission = models.CharField(
        max_length=100,
        verbose_name=_('صلاحية العرض'),
        help_text=_('كود الصلاحية المطلوبة للعرض: personnel.view_salary.all'),
    )
    edit_permission = models.CharField(
        max_length=100, blank=True, default='',
        verbose_name=_('صلاحية التعديل'),
        help_text=_('كود الصلاحية المطلوبة للتعديل: personnel.edit_salary.all'),
    )
    is_sensitive = models.BooleanField(
        default=True,
        verbose_name=_('حقل حساس'),
        help_text=_('الحقول الحساسة يُسجّل الوصول إليها في سجل التدقيق'),
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('نشط'),
    )

    class Meta:
        db_table = 'authorization_field_permission'
        verbose_name = _('صلاحية حقل')
        verbose_name_plural = _('صلاحيات الحقول')
        unique_together = [['module', 'field_name']]
        ordering = ['module', 'field_name']
        indexes = [
            models.Index(fields=['module']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self) -> str:
        return f"{self.module}.{self.field_name} — {self.label}"
