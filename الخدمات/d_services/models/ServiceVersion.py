"""
نموذج إصدار الخدمة - Service Version Model
لتخزين البيانات الإضافية الخاصة بكل خدمة
"""
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from OpenSoftCoreV4.utils.abstract_models.soft_delete_model import SoftDeleteModel
from OpenSoftCoreV4.utils.abstract_models.ex_id_model import ExIdModel

from d_services.choices.choices import ComponentTypeChoice


class ServiceVersion(ExIdModel, SoftDeleteModel):
    """
    إصدار الخدمة - Service Version
    لتخزين البيانات الإضافية الخاصة بكل خدمة والتي يتم إدخالها عبر واجهات المستخدم
    """
    fk_service = models.ForeignKey(
        'Service',
        on_delete=models.CASCADE,
        related_name='versions',
        verbose_name=_('الخدمة')
    )
    
    version_name = models.CharField(
        max_length=100,
        verbose_name=_('اسم الإصدار')
    )
    component_type = models.CharField(
        max_length=50,
        choices=ComponentTypeChoice.choices,
        default=ComponentTypeChoice.FORM,
        verbose_name=_('نوع واجهة الإدخال')
    )
    is_current = models.BooleanField(
        default=False,
        verbose_name=_('الإصدار الحالي')
    )
    fields_schema = models.JSONField(
        verbose_name=_('مخطط الحقول (JSON)')
    )
    
    # حقول التحكم
    is_locked = models.BooleanField(
        default=False,
        verbose_name=_('مقفول من التعديل')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('تاريخ الإنشاء')
    )

    def __str__(self):
        return f'{self.fk_service.code} - {self.version_name}'

    class Meta:
        verbose_name = _('إصدار الخدمة')
        verbose_name_plural = _('إصدارات الخدمات')
        ordering = ['fk_service', '-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['fk_service', 'version_name'],
                name='unique_service_version_name',
                condition=Q(is_deleted=False),
            ),
            models.UniqueConstraint(
                fields=['fk_service', 'is_current'],
                name='unique_service_version_is_current',
                condition=Q(is_deleted=False) & Q(is_current=True),
            ),
        ]
