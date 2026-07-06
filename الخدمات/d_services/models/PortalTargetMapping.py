"""
نموذج ربط حقول البوابة - Portal Target Mapping Model
تخزين خريطة التحويل بين حقول Target في البوابة و QAS لكل خدمة
"""
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from OpenSoftCoreV4.utils.abstract_models.soft_delete_model import SoftDeleteModel
from d_services.choices.choices import ResolveByChoice


class PortalTargetMapping(SoftDeleteModel):
    """
    ربط حقول Target بين البوابة ونظام الخدمات
    مشترك لكل المنظمات - مرتبط بالخدمة مباشرة
    """
    fk_service = models.ForeignKey(
        'd_services.Service',
        on_delete=models.CASCADE,
        related_name='portal_target_mappings',
        verbose_name=_('الخدمة')
    )

    # حقل QAS (من JSON schema)
    qas_field_name = models.CharField(
        max_length=100,
        verbose_name=_('اسم الحقل في QAS'),
        help_text=_('مثال: fk_college, fk_student_batch')
    )
    qas_model_name = models.CharField(
        max_length=100,
        verbose_name=_('اسم الموديل في QAS'),
        help_text=_('مثال: College, StudentBatch')
    )

    # حقل البوابة
    portal_field_name = models.CharField(
        max_length=100,
        verbose_name=_('اسم الحقل في البوابة'),
        help_text=_('مثال: college_ex_id, student_ex_id')
    )

    # طريقة التحويل
    resolve_by = models.CharField(
        max_length=50,
        choices=ResolveByChoice.choices,
        default=ResolveByChoice.EX_ID,
        verbose_name=_('طريقة التحويل'),
        help_text=_('كيف يتم البحث عن السجل في QAS')
    )
    resolve_field = models.CharField(
        max_length=100,
        default='ex_id',
        verbose_name=_('حقل البحث في QAS'),
        help_text=_('الحقل المستخدم للبحث في الموديل، مثال: ex_id, code')
    )
    custom_resolver = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('دالة تحويل مخصصة'),
        help_text=_('اسم الدالة المخصصة (فقط إذا كانت طريقة التحويل = دالة مخصصة)')
    )

    is_main_target = models.BooleanField(
        default=False,
        verbose_name=_('الحقل الرئيسي للهدف')
    )
    field_order = models.IntegerField(
        default=0,
        verbose_name=_('ترتيب الحقل')
    )

    def __str__(self):
        return f'{self.fk_service.code} → {self.qas_field_name} ← {self.portal_field_name}'

    class Meta:
        verbose_name = _('ربط حقل بوابة')
        verbose_name_plural = _('ربط حقول البوابة')
        ordering = ['field_order']
        constraints = [
            models.UniqueConstraint(
                fields=['fk_service', 'qas_field_name'],
                name='unique_portal_mapping_service_field',
                condition=Q(is_deleted=False),
            ),
        ]
        indexes = [
            models.Index(fields=['fk_service'], name='idx_portal_mapping_service'),
        ]
