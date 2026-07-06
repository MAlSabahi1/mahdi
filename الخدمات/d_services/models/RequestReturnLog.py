"""
نموذج سجل إرجاع الطلب - Request Return Log Model
لتسجيل عمليات إرجاع الطلبات بين المراحل أو إلى الطالب
"""
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from OpenSoftCoreV4.utils.abstract_models.soft_delete_model import SoftDeleteModel
from OpenSoftCoreV4.utils.abstract_models.ex_id_model import ExIdModel

from d_services.choices.choices import ReturnReasonChoice


class RequestReturnLog(ExIdModel, SoftDeleteModel):
    """
    سجل إرجاع الطلب - Request Return Log
    لتسجيل عمليات إرجاع الطلبات بين المراحل أو إلى الطالب
    """
    fk_request = models.ForeignKey(
        'ServiceRequest',
        on_delete=models.CASCADE,
        related_name='return_logs',
        verbose_name=_('الطلب')
    )
    fk_from_stage = models.ForeignKey(
        'ServiceWorkflowStep',
        on_delete=models.PROTECT,
        related_name='return_from_logs',
        verbose_name=_('من المرحلة')
    )
    fk_to_stage = models.ForeignKey(
        'ServiceWorkflowStep',
        on_delete=models.PROTECT,
        related_name='return_to_logs',
        verbose_name=_('إلى المرحلة'),
        null=True,
        blank=True
    )
    return_reason = models.CharField(
        max_length=30,
        choices=ReturnReasonChoice.choices,
        verbose_name=_('سبب الإرجاع')
    )
    return_reason_details = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('تفاصيل سبب الإرجاع')
    )
    returned_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('وقت الإرجاع')
    )
    fk_returned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='returned_requests',
        verbose_name=_('تم الإرجاع بواسطة'),
        null=True,
        blank=True
    )
    is_resolved = models.BooleanField(
        default=False,
        verbose_name=_('تم حل المشكلة')
    )
    resolution_notes = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('ملاحظات الحل')
    )
    resolved_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('وقت الحل')
    )

    def __str__(self):
        return f'{self.fk_request.request_number} - {self.return_reason}'

    class Meta:
        verbose_name = _('سجل إرجاع الطلب')
        verbose_name_plural = _('سجلات إرجاع الطلبات')
        ordering = ['-returned_at']
