from OpenSoftCoreV4.common.models.Currency import Currency
from OpenSoftCoreV4.utils.abstract_models.soft_delete_model import SoftDeleteModel
from OpenSoftCoreV4.utils.abstract_models.ex_id_model import ExIdModel
from django.db import models
from django.utils.translation import gettext_lazy as _

# from system_management.models.Specialization import Specialization
# from system_management.models.StudeySystem import StudySystem


class ServiceERPSettings(ExIdModel, SoftDeleteModel):
    specialization_id = models.IntegerField(_("كورس - فصل - تخصص"))
    study_system_id = models.IntegerField(_("النظام الدراسي"),null=True,blank=True)
    fk_org_service_config = models.ForeignKey(
        'd_services.OrganizationServiceConfig',
        on_delete=models.CASCADE,
        related_name='service_specialization_settings',
        verbose_name=_('الخدمة')
    )
    fk_currency = models.ForeignKey(
        Currency,
        on_delete=models.PROTECT,
        verbose_name=_('عملة الرسوم'),
        null=True,
        blank=True
    )
    service_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_('رسوم الخدمة')
    )


    # for erp integration
    is_donor_invoice_allowed = models.BooleanField(
        default=True,
        verbose_name=_('تتيح خيار المنحة')
    )
    is_discount_allowed = models.BooleanField(
        default=True,
        verbose_name=_('تتيح خيار الخصم')
    )
    erp_product_id = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_('معرف المنتج في نظام ERP')
    )
    erp_product_name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_('اسم المنتج في نظام ERP')
    )
    erp_product_for_discount_id = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_('معرف المنتج للخصم في نظام ERP')
    )
    erp_product_for_discount_name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_('اسم المنتج للخصم في نظام ERP')
    )
    erp_product_for_internal_donors_id = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_('معرف المنتج  للمنح الداخليه في نظام ERP')
    )
    erp_product_for_internal_donors_name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_('اسم المنتج  للمنح الداخليه في نظام ERP')    
    )

    erp_project_id = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_('معرف المشروع في نظام ERP')
    )
    erp_project_name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_('اسم المشروع في نظام ERP')
    )
    erp_activity_id = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_('معرف النشاط في نظام ERP')
    )
    erp_activity_name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_('اسم النشاط في نظام ERP')
    )
    erp_cost_center_id = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_('معرف مركز التكلفة في نظام ERP')
    )
    erp_cost_center_name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_('اسم مركز التكلفة في نظام ERP')
    )
    def _str_(self):
        return f'{self.fk_org_service_config.fk_service} - {self.specialization_id} - {self.study_system_id}'
    class Meta:
        verbose_name = _('إعدادات الخدمة لنظام ال ERP')
        verbose_name_plural = _('إعدادات الخدمات لنظام ال ERP')
        constraints = [
            models.UniqueConstraint(
                fields=['specialization_id', 'fk_org_service_config'],
                name='unique_specialization_stat_no_delete',
                condition=models.Q(is_deleted=False),
            )
        ]
        indexes = [
            models.Index(fields=['specialization_id', 'fk_org_service_config']),
        ]

