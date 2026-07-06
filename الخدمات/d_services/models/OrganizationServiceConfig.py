"""
نموذج إعدادات خدمة المنظمة - Organization Service Config Model
إعدادات خاصة بالخدمة على مستوى كل منظمة
"""
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from OpenSoftCoreV4.utils.abstract_models.soft_delete_model import SoftDeleteModel
from OpenSoftCoreV4.utils.abstract_models.ex_id_model import ExIdModel
from OpenSoftCoreV4.common.models.Branch import Organization
from OpenSoftCoreV4.common.models.Currency import Currency
from d_services.choices.choices import InstallmentPeriodChoice


class OrganizationServiceConfig(ExIdModel, SoftDeleteModel):
    """
    إعدادات خدمة المنظمة - Organization Service Config
    إعدادات خاصة بالخدمة على مستوى كل منظمة
    """
    fk_service = models.ForeignKey(
        'Service',
        on_delete=models.CASCADE,
        related_name='org_configs',
        verbose_name=_('الخدمة')
    )
    fk_organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='service_configs',
        verbose_name=_('المنظمة')
    )
    
    # إعدادات الدفع
    is_installment_allowed = models.BooleanField(
        default=False,
        verbose_name=_('تتيح خيار التقسيط')
    )
    installments_count = models.IntegerField(
        default=1,
        verbose_name=_('عدد التقسيطات')
    )
    is_paid = models.BooleanField(
        default=True,
        verbose_name=_('خدمة مدفوعة')
    )
    free_limit_per_year = models.PositiveIntegerField(
        default=0,
        verbose_name=_('الحد الأقصى للطلبات المجانية سنوياً')
    )
    fk_currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        related_name='service_configs',
        verbose_name=_('العملة'),
        null=True,
        blank=True
    )
    fee_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name=_('مبلغ الرسوم')
    )
    fk_print_report_setting_for_input = models.ForeignKey(
        'common.PrintReportSetting',
        on_delete=models.CASCADE,
        related_name='service_configs_input',
        verbose_name=_('إعدادات الطباعة لاستمارة الطلب'),
        null=True,
        blank=True
    )
    fk_print_report_setting_for_output = models.ForeignKey(
        'common.PrintReportSetting',
        on_delete=models.CASCADE,
        related_name='service_configs_output',
        verbose_name=_('إعدادات الطباعة لمخرج الطلب'),
        null=True,
        blank=True
    )
    installment_period = models.CharField(
        max_length=100,
        choices=InstallmentPeriodChoice.choices,
        null=True,
        blank=True,
        verbose_name=_('الفترة الزمنية للقسط')
    )
    # إعدادات الترقيم
    request_prefix = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_('بادئة ترقيم الطلبات')
    )
    
    # حالة التفعيل
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('مفعلة')
    )
    
    # حقول القفل
    is_locked = models.BooleanField(
        default=False,
        verbose_name=_('مقفلة من التعديل')
    )
    locked_reason = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('سبب القفل')
    )
    locked_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('وقت القفل')
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
    # end for erp integration

    def clean(self):
        from django.core.exceptions import ValidationError
        
        if self.fk_print_report_setting_for_input:
            if self.fk_print_report_setting_for_input.fk_branch != self.fk_organization:
                raise ValidationError({
                    'fk_print_report_setting_for_input': _('إعدادات الطباعة لاستمارة الطلب يجب أن تابعة لنفس المنظمة')
                })

        if self.fk_print_report_setting_for_output:
            if self.fk_print_report_setting_for_output.fk_branch != self.fk_organization:
                raise ValidationError({
                    'fk_print_report_setting_for_output': _('إعدادات الطباعة لمخرج الطلب يجب أن تابعة لنفس المنظمة')
                })

    def __str__(self):
        return f'{self.fk_service.code} - {self.fk_organization}'

    class Meta:
        verbose_name = _('إعدادات خدمة المنظمة')
        verbose_name_plural = _('إعدادات خدمات المنظمات')
        constraints = [
            models.UniqueConstraint(
                fields=['fk_service', 'fk_organization'],
                condition=Q(is_deleted=False),
                name='unique_service_org_config',
            ),
        ]
