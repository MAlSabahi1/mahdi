"""
نموذج متطلبات الخدمة - Service Prerequisite Model
الشروط التي يجب التحقق منها قبل السماح بتقديم طلب الخدمة
"""
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from OpenSoftCoreV4.utils.abstract_models.soft_delete_model import SoftDeleteModel
from OpenSoftCoreV4.utils.abstract_models.ex_id_model import ExIdModel
from d_services.choices.choices import PrerequisiteStatusChoice
from d_services.apis.external_methods.base import validate_function_name


class ServicePrerequisite(ExIdModel, SoftDeleteModel):
    """
    متطلب الخدمة - Service Prerequisite
    الشروط التي يجب التحقق منها قبل السماح بتقديم طلب الخدمة
    """
    fk_service = models.ForeignKey(
        'Service',
        on_delete=models.CASCADE,
        related_name='prerequisites',
        verbose_name=_('الخدمة')
    )
    name_ar = models.CharField(
        max_length=255,
        verbose_name=_('اسم الشرط بالعربي')
    )
    name_en = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('اسم الشرط بالانجليزي')
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('وصف الشرط')
    )
    status = models.CharField(
        max_length=100,
        choices=PrerequisiteStatusChoice.choices,
        default=PrerequisiteStatusChoice.MANDATORY,
        verbose_name=_('حالة الشرط')
    )
    validation_procedure_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('اسم إجراء التحقق'),
        validators=[validate_function_name]
    )
    order = models.PositiveIntegerField(
        default=1,
        verbose_name=_('ترتيب الشرط')
    )

    def __str__(self):
        return f'{self.fk_service.code} - {self.name_ar}'

    class Meta:
        verbose_name = _('متطلب الخدمة')
        verbose_name_plural = _('متطلبات الخدمات')
        ordering = ['fk_service', 'order']
