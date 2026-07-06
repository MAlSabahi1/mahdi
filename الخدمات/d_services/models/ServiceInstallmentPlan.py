"""
نموذج خطة تقسيط الخدمة - Service Installment Plan Model
تفاصيل خطة التقسيط المتاحة للخدمة
"""
from decimal import Decimal

from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from OpenSoftCoreV4.utils.abstract_models.soft_delete_model import SoftDeleteModel
from OpenSoftCoreV4.utils.abstract_models.ex_id_model import ExIdModel

from d_services.choices.choices import InstallmentPeriodChoice


class ServiceInstallmentPlan(ExIdModel, SoftDeleteModel):
    """
    خطة تقسيط الخدمة - Service Installment Plan
    تفاصيل خطة التقسيط المتاحة للخدمة
    """
    fk_org_service_config = models.ForeignKey(
        'OrganizationServiceConfig',
        on_delete=models.CASCADE,
        related_name='installment_plans',
        verbose_name=_('الخدمة')
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name=_('مبلغ القسط')
    )
    order = models.PositiveIntegerField(
        verbose_name=_('ترتيب القسط')
    )
    due_days_from_request = models.PositiveIntegerField(
        verbose_name=_('أيام الاستحقاق من تاريخ الطلب')
    )

    @property
    def percentage(self):
        """الحصول على نسبة الخصم من خلال مبلغ الخدمة ومبلغ القسط"""
        percentage = Decimal(self.amount / self.fk_org_service_config.fee_amount)
        return percentage


    def __str__(self):
        return f'{self.fk_org_service_config.fk_service.code} - قسط {self.order}'

    class Meta:
        verbose_name = _('خطة تقسيط الخدمة')
        verbose_name_plural = _('خطط تقسيط الخدمات')
        ordering = ['fk_org_service_config', 'order']
        constraints = [
            models.UniqueConstraint(
                fields=['fk_org_service_config', 'order'],
                name='unique_service_installment_order',
                condition=Q(is_deleted=False),
            ),
        ]
