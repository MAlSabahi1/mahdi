"""
نموذج قسط الطلب - Request Installment Model
تفاصيل الأقساط المستحقة على طلب معين
"""
import datetime
import uuid
from decimal import Decimal

from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from OpenSoftCoreV4.utils.abstract_models.soft_delete_model import SoftDeleteModel
from OpenSoftCoreV4.utils.abstract_models.ex_id_model import ExIdModel

from d_services.choices.choices import PaymentStatusChoice
from utils.core.sync_abstract_model import SyncAbastractModel


class RequestInstallment(ExIdModel, SyncAbastractModel, SoftDeleteModel):
    """
    قسط الطلب - Request Installment
    تفاصيل الأقساط المستحقة على طلب معين
    """
    fk_request = models.ForeignKey(
        'ServiceRequest',
        on_delete=models.CASCADE,
        related_name='installments',
        verbose_name=_('الطلب')
    )
    period = models.CharField(
        max_length=50,
        verbose_name=_('الفترة الزمنية')
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name=_('مبلغ القسط')
    )
    order = models.PositiveIntegerField(
        verbose_name=_('ترتيب القسط')
    )
    due_date = models.DateField(
        verbose_name=_('تاريخ الاستحقاق')
    )
    payment_status = models.CharField(
        max_length=50,
        choices=PaymentStatusChoice.choices,
        default=PaymentStatusChoice.UNPAID,
        verbose_name=_('حالة الدفع')
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
    paid_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('تاريخ الدفع')
    )
    @property
    def grant_amount(self):
        """الحصول على مبلغ المنحة من نسبة المنحة ومبلغ القسط"""
        grant_ratio = round(self.fk_request.grant_percentage / 100,2) if self.fk_request.grant_percentage else None
        if grant_ratio and grant_ratio>0:
            return round(Decimal(self.amount * grant_ratio),2)
        return 0.00

    @property
    def discount_amount(self):
        """الحصول على مبلغ الخصم من نسبة الخصم ومبلغ القسط"""
        discount_ratio = round(self.fk_request.discount_percentage / 100 ,2) if self.fk_request.discount_percentage else None
        if discount_ratio and discount_ratio > 0:
            return round(Decimal(self.amount * discount_ratio))
        return 0.00

    @property
    def due_amount(self):
        """الحصول على المبلغ الاجمالي المستحق بعد الخصم والمنحة"""
        due_amount = self.amount
        if self.fk_request.discount_percentage > 0:
            due_amount -= self.discount_amount
        if self.fk_request.grant_percentage > 0:
            due_amount -= self.grant_amount
        return round(due_amount,2)

    def __str__(self):
        return f'{self.fk_request.request_number} - قسط {self.order}'

    def get_invoices_data(self):
        """ الحصول على بيانات الفواتير الخاصة بطلب الخدمة"""
        date_today = datetime.date.today()
        request_obj = self.fk_request
        org_service_config = self.fk_request.org_service_config
        service_currency = org_service_config.fk_currency.code if hasattr(org_service_config, 'fk_currency') else None
        installments_plan = org_service_config.installment_plans.all()
        if installments_plan.exists():
            invoices_data = []
            if self.due_amount >0:
                invoices_data.append(
                    request_obj.add_invoice_data(
                        self.ex_id,
                        1,
                        self.due_amount,
                        is_installment=True,
                        partner_data=request_obj.partner_data,
                        due_date=date_today,
                        currency=service_currency
                    )
                )
            if self.grant_amount > 0:
                invoices_data.append(
                    request_obj.add_invoice_data(
                        self.ex_id,
                        2,
                        self.grant_amount,
                        is_installment=True,
                        partner_data=request_obj.fk_grant_source.partner_data,
                        due_date=date_today,
                        currency=service_currency
                    )
                )
            if self.discount_amount>0:
                invoices_data.append(
                    request_obj.add_invoice_data(
                        self.ex_id,
                        3,
                        self.discount_amount,
                        is_installment=True,
                        partner_data=request_obj.partner_data,
                        due_date=date_today,
                        currency=service_currency
                    )
                )
            return invoices_data
        return []

    class Meta:
        verbose_name = _('قسط الطلب')
        verbose_name_plural = _('أقساط الطلبات')
        ordering = ['fk_request', 'order']
        constraints = [
            models.UniqueConstraint(
                fields=['fk_request', 'order'],
                name='unique_request_installment_order',
                condition=Q(is_deleted=False),
            ),
            models.UniqueConstraint(
                fields=['ex_id'],
                name='unique_request_installment_ex_id',
                condition=Q(is_deleted=False),
            ),
            models.UniqueConstraint(
                fields=['student_invoice_number'],
                name='installment_student_invoice_number_no_delete',
                condition=Q(is_deleted=False),
            ),
            models.UniqueConstraint(
                fields=['grant_invoice_number'],
                name='installment_grant_invoice_number_no_delete',
                condition=Q(is_deleted=False),
            ),
        ]
