"""
نموذج ملاحظات الطلب - Request Note Model
ملاحظات يضيفها المستخدمون على الطلبات
"""
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from OpenSoftCoreV4.utils.abstract_models.soft_delete_model import SoftDeleteModel
from OpenSoftCoreV4.utils.abstract_models.ex_id_model import ExIdModel

from utils.core.sync_abstract_model import SyncAbastractModel


class RequestNote(SyncAbastractModel, SoftDeleteModel):
    """ملاحظة على طلب الخدمة"""
    
    fk_request = models.ForeignKey(
        'ServiceRequest',
        on_delete=models.CASCADE,
        related_name='notes',
        verbose_name=_('الطلب')
    )
    content = models.TextField(
        verbose_name=_('محتوى الملاحظة')
    )
    fk_created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='request_notes',
        verbose_name=_('أضيفت بواسطة')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('تاريخ الإضافة')
    )

    def __str__(self):
        return f'{self.fk_request.request_number} - {self.content[:50]}'

    class Meta:
        verbose_name = _('ملاحظة على الطلب')
        verbose_name_plural = _('ملاحظات الطلبات')
        ordering = ['-created_at']
