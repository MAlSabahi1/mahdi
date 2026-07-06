"""
نموذج طلب الخدمة - Service Request Model
الجدول الرئيسي لتخزين بيانات كل طلب خدمة مقدم من المستخدم
"""
import datetime
import json
import uuid
from datetime import timedelta
from decimal import Decimal

from django.utils import timezone

from d_services.choices.choices import GrantStatusChoice
from d_services.choices.choices import DiscountStatusChoice
from django.db import models
from django.db.models import Q
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from OpenSoftCoreV4.utils.abstract_models.soft_delete_model import SoftDeleteModel
from OpenSoftCoreV4.utils.abstract_models.ex_id_model import ExIdModel
from OpenSoftCoreV4.common.models.Branch import Organization

from d_services.choices.choices import (
    ServiceStatusChoice,
    PaymentStatusChoice,
    RequestSourceChoice,
    PriorityChoice,
)
from d_services.choices.choices import (
    TargetAudienceComponentChoice,
    BaseComponentChoice,
    OutputTemplateTypeChoice,
    InputTemplateTypeChoice,
)
from d_services.models.OrganizationServiceConfig import OrganizationServiceConfig
from d_services.models.ServiceInstallmentPlan import ServiceInstallmentPlan
from middleware_system.models.Invoice import ERPInvoice, PartnerType
from utils.core.base_sync_model import BaseSyncModel

class ServiceRequest(BaseSyncModel):
    # معرف المنظمة
    fk_organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name='service_requests',
        verbose_name=_('المنظمة'),
        null=True,
        blank=True
    )
    
    # البيانات الأساسية
    request_number = models.CharField(
        max_length=50,
        verbose_name=_('رقم الطلب')
    )
    fk_service = models.ForeignKey(
        'Service',
        on_delete=models.PROTECT,
        related_name='requests',
        verbose_name=_('الخدمة')
    )
    
    fk_service_version = models.ForeignKey(
        'ServiceVersion',
        on_delete=models.PROTECT,
        related_name='requests',
        verbose_name=_('إصدار الخدمة'),
        null=True,
        blank=True
    )
    
    # بيانات الإدخال (JSON)
    version_data = models.JSONField(
        null=True,
        blank=True,
        verbose_name=_('بيانات حقول الإصدار')
    )
    target_audience_component = models.CharField(
        max_length=100,
        choices=TargetAudienceComponentChoice.choices,
        verbose_name=_('اختيار الجمهور المستهدف')
    )
    target_audience_data = models.JSONField(
        verbose_name=_('بيانات الجمهور المستهدف')
    )
    base_audience_component = models.CharField(
        max_length=100,
        choices=BaseComponentChoice.choices,
        verbose_name=_('اختيار المكون الأساسي')
    )
    base_component_data = models.JSONField(
        verbose_name=_('بيانات المكون الأساسي')
    )
    
    # التواريخ
    requested_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('تاريخ تقديم الطلب')
    )
    start_request_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('تاريخ البدء')
    )
    final_delivery_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('تاريخ التسليم النهائي')
    )
    
    # الحالة
    status = models.CharField(
        max_length=100,
        choices=ServiceStatusChoice.choices,
        default=ServiceStatusChoice.PENDING,
        verbose_name=_('حالة الطلب')
    )
    has_approvals = models.BooleanField(
        default=False,
        verbose_name=_('يتطلب موافقات')
    )
    
    # إعدادات المخرجات
    output_template_type = models.CharField(
        max_length=100,
        choices=OutputTemplateTypeChoice.choices,
        null=True,
        blank=True,
        verbose_name=_('نوع نموذج المخرج')
    )
    input_template_type = models.CharField(
        max_length=100,
        choices=InputTemplateTypeChoice.choices,
        null=True,
        blank=True,
        verbose_name=_('نموذج استمارة الطلب')
    )
    
    output_data_function = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('دالة جلب بيانات المخرج')
    )
    input_data_function = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('دالة جلب بيانات الاستماره')
    )
    # إعدادات المخرجات
    output_document = models.FileField(
        upload_to='requests/outputs/',
        null=True,
        blank=True,
        verbose_name=_('ملف المخرج النهائي')
    )
    input_document = models.FileField(
        upload_to='requests/inputs/',
        null=True,
        blank=True,
        verbose_name=_('ملف المدخل')
    )
    
    # مصدر الطلب ومقدمه
    request_source = models.CharField(
        max_length=100,
        choices=RequestSourceChoice.choices,
        default=RequestSourceChoice.PLATFORM,
        verbose_name=_('مصدر الطلب')
    )
    fk_requester = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='submitted_service_requests',
        verbose_name=_('مقدم الطلب'),
    )
    priority = models.CharField(
        max_length=100,
        choices=PriorityChoice.choices,
        default=PriorityChoice.NORMAL,
        verbose_name=_('الأولوية')
    )
    requester_image = models.ImageField(
        upload_to='requests/requester_images/',
        null=True,
        blank=True,
        verbose_name=_('صورة مقدم الطلب')
    )
    requester_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('اسم مقدم الطلب')
    )
    requester_description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('وصف مقدم الطلب')
    )
    requester_id = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_('معرف مقدم الطلب'),
        db_index=True
    )
    discount_status = models.CharField(
        max_length=100,
        choices=DiscountStatusChoice.choices,
        default=DiscountStatusChoice.NO_DISCOUNT,
        verbose_name=_('حالة الخصم')
    )
    discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        verbose_name=_('نسبة الخصم (%)')
    )
    discounted_fee = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name=_('الرسوم بعد الخصم')
    )
    discounted_fee_reason = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('سبب الخصم')
    )
    discount_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name=_('قيمة الخصم')
    )
    discount_reason = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('سبب الخصم')
    )
    discount_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('وقت الخصم')
    )
    discount_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='discounted_service_requests',
        verbose_name=_('تم الخصم بواسطة'),
        null=True,
        blank=True
    )
    discount_rejected_reason = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('سبب رفض الخصم')
    )
    discount_rejected_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('وقت رفض الخصم')
    )
    discount_rejected_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='rejected_discounted_service_requests',
        verbose_name=_('تم رفض الخصم بواسطة'),
        null=True,
        blank=True
    )
    discount_canceled_reason = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('سبب إلغاء الخصم')
    )
    discount_canceled_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('وقت إلغاء الخصم')
    )
    discount_canceled_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='canceled_discounted_service_requests',
        verbose_name=_('تم إلغاء الخصم بواسطة'),
        null=True,
        blank=True
    )

    # البيانات المالية
    total_fee = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name=_('إجمالي الرسوم')
    )
    amount_paid = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name=_('المبلغ المدفوع')
    )
    remaining_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name=_('المبلغ المتبقي')
    )
    student_invoice_number = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("رقم فاتورة الطالب")
    )
    grant_invoice_number = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("رقم فاتورة الجهة المانحة")
    )
    payment_status = models.CharField(
        max_length=50,
        choices=PaymentStatusChoice.choices,
        default=PaymentStatusChoice.UNPAID,
        verbose_name=_('حالة الدفع')
    )
    # for erp integration
    partner_data = models.JSONField(
        null=True,
        blank=True,
        default=dict,
        verbose_name=_("بيانات الشريك")
    )
    is_donor_invoice_allowed = models.BooleanField(
        default=True,
        verbose_name=_('تتيح خيار فاتورة الجهات المانحة')
    )
    ###################################
    """يتم تخزين المعرفات الخاصة بالمنح المتاحة للطالب (صاحب الطلب للخدمة)"""
    available_grant_sources_ids = models.JSONField(
        default=list,
        verbose_name=_("معرفات الجهات المانحة المتاحة")
    )
    ####################################

    is_discount_allowed = models.BooleanField(
        default=True,
        verbose_name=_('تتيح خيار الخصم')
    )
    is_internal_donors = models.BooleanField(
        default=False,
        verbose_name=_('منحه داخليه')
    )
    currency = models.CharField(
        max_length=20,
        null=True,
        blank=True,
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
    # بيانات المنحة
    grant_status = models.CharField(
        max_length=100,
        choices=GrantStatusChoice.choices,
        default=GrantStatusChoice.NO_GRANT,
        verbose_name=_('حالة المنحة')
    )   
    fk_grant_source = models.ForeignKey(
        'GrantSource',
        on_delete=models.SET_NULL,
        related_name='service_requests',
        verbose_name=_('مصدر المنحة'),
        null=True,
        blank=True
    )
    grant_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name=_('مبلغ المنحة')
    )
    grant_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        verbose_name=_('نسبة المنحة (%)')
    )
    grant_assigned_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('تاريخ تعيين المنحة')
    )
    grant_assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='assigned_grants',
        verbose_name=_('تم تعيين المنحة بواسطة'),
        null=True,
        blank=True
    )
    grant_cancel_reason = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('سبب إلغاء المنحة')
    )
    grant_cancel_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('وقت إلغاء المنحة')
    )
    grant_cancel_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='cancelled_grants',
        verbose_name=_('تم إلغاء المنحة بواسطة'),
        null=True,
        blank=True
    )
    grant_rejected_reason = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('سبب رفض المنحة')
    )
    grant_rejected_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('وقت رفض المنحة')
    )
    grant_rejected_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='rejected_grants',
        verbose_name=_('تم رفض المنحة بواسطة'),
        null=True,
        blank=True
    )
    
    
    # لقطات JSON للمراحل والشروط
    workflow_stages_snapshot = models.JSONField(
        null=True,
        blank=True,
        verbose_name=_('لقطة مراحل سير العمل')
    )
    prerequisites_snapshot = models.JSONField(
        null=True,
        blank=True,
        verbose_name=_('لقطة الشروط')
    )
    
    # حقول التحكم
    is_locked = models.BooleanField(
        default=False,
        verbose_name=_('مقفول من التعديل')
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
    is_locked_from_service = models.BooleanField(
        default=False,
        verbose_name=_('مقفول من التعديل بواسطة الخدمة')
    ) 
    reject_reason = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('سبب الرفض')
    )
    reject_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('وقت الرفض')
    )
    cancel_reason = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('سبب الإلغاء')
    )
    cancelled_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('وقت الإلغاء')
    )


    func_call_results = models.ManyToOneRel(
        'fk_service_request',
        "d_services.ServiceCallResult", 
        field_name='func_call_results'
    )

    @property
    def is_allowed_change_financial(self):
        """التحقق اذا كان بالامكان التعديل على البيانات المالية بعد انشاء الفواتير"""
        installments = self.installments.filter(student_invoice_number__isnull=False).distinct()
        if self.student_invoice_number:
            return False
        if installments.exists():
            return False
        return True



    @property
    def org_service_config(self):
        """الحصول على اعدادات المنظمة"""
        return OrganizationServiceConfig.objects.get(
            fk_organization=self.fk_organization,
            fk_service=self.fk_service,
        )
    @property
    def due_amount(self):
        due_amount = self.total_fee
        if self.discount_amount > 0:
            due_amount -= self.discount_amount
        if self.grant_amount > 0:
            due_amount -= self.grant_amount
        return round(due_amount,2)

    @property
    def invoices_data(self):
        """الحصول على بيانات فواتير الطلب من النظام الوسيط"""
        return sorted(self.get_invoices_data(), key=lambda i: i['partner_type'])


    def __str__(self):
        return f'{self.request_number}'

    def get_invoices_data(self):
        """ الحصول على بيانات الفواتير الخاصة بطلب الخدمة"""
        date_today = datetime.date.today()
        # grant_ratio = self.grant_percentage / 100 if self.grant_percentage else None
        org_service_config = self.org_service_config
        installments_plan = org_service_config.installment_plans.all()
        if not installments_plan.exists():
            invoices_data = []
            if self.due_amount >0:
                invoices_data.append(
                    self.add_invoice_data(
                        self.external_id,
                        1,
                        self.due_amount,
                        is_installment=False,
                        partner_data=self.partner_data,
                        due_date=date_today,
                        currency=self.currency
                    )
                )

            if self.grant_amount >0:
                invoices_data.append(
                    self.add_invoice_data(
                        self.external_id,
                        2,
                        self.grant_amount,
                        is_installment=False,
                        partner_data=self.fk_grant_source.partner_data,
                        due_date=date_today,
                        currency=self.currency
                    )
                )
            if self.discount_amount >0:
                invoices_data.append(
                    self.add_invoice_data(
                        self.external_id,
                        3,
                        self.discount_amount,
                        is_installment=False,
                        partner_data=self.partner_data,
                        due_date=date_today,
                        currency=self.currency
                    )
                )
            return invoices_data
        return []

    def add_invoice_data(self,source_id,partner_type,amount,is_installment=False,partner_data=None,due_date=None,currency=None):
        invoice_number=None
        partner_type__display= PartnerType(partner_type).label if partner_type else None
        if partner_type==PartnerType.STUDENT:
            invoice_number = self.student_invoice_number
        elif partner_type==PartnerType.DONOR:
            invoice_number = self.grant_invoice_number
        return {
            'source_id': source_id,
            'organization_id': self.fk_organization.id if self.fk_organization else None,
            'is_installment': is_installment,
            'partner_type': partner_type,
            'partner_type__display':partner_type__display ,
            'amount': amount,
            'partner_data': partner_data,
            'due_date': due_date,
            'currency': currency,
            'invoice_number': invoice_number,
            'is_paid':self.payment_status == 'paid',
            'erp_cost_center_id': self.erp_cost_center_id,
            'erp_product_id': self.erp_product_id,
            'erp_product_for_discount_id': self.erp_product_for_discount_id,
            'erp_product_for_internal_donors_id': self.erp_product_for_internal_donors_id,
            'erp_project_id': self.erp_project_id,
            'erp_activity_id': self.erp_activity_id,
        }




    class Meta(BaseSyncModel.Meta):
        verbose_name = _('طلب الخدمة')
        verbose_name_plural = _('طلبات الخدمات')
        ordering = ['-requested_at']
        constraints = BaseSyncModel.Meta.constraints + [
            # models.UniqueConstraint(
            #     fields=['request_number','fk_organization', 'fk_service', 'source_system'],
            #     name='unique_service_request_number_organization',
            #     condition=Q(is_deleted=False),
            # ),
            # models.UniqueConstraint(
            #     fields=['student_invoice_number', 'fk_service', 'source_system'],
            #     name='student_invoice_number_no_delete',
            #     condition=Q(is_deleted=False),
            # ),
            # models.UniqueConstraint(
            #     fields=['grant_invoice_number', 'fk_service', 'source_system'],
            #     name='grant_invoice_number_no_delete',
            #     condition=Q(is_deleted=False),
            # ),
        ]
        indexes = BaseSyncModel.Meta.indexes + [
            models.Index(fields=['fk_service', 'fk_organization', 'status'], name='idx_sr_svc_org_status'),
            models.Index(fields=['fk_organization', 'status'], name='idx_sr_org_status'),
            models.Index(fields=['fk_requester', 'status'], name='idx_sr_requester_status'),
            models.Index(fields=['requested_at'], name='idx_sr_requested_at'),
            models.Index(fields=['status', 'is_locked'], name='idx_sr_status_locked'),
            models.Index(fields=['payment_status'], name='idx_sr_payment_status'),
            models.Index(fields=['grant_status'], name='idx_sr_grant_status'),
            models.Index(fields=['discount_status'], name='idx_sr_discount_status'),
        ]
