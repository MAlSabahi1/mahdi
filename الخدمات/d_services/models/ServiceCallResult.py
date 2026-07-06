from d_services.models.ServiceRequest import ServiceRequest
from utils.core.sync_abstract_model import SyncAbastractModel
from config.imports.core_models import SoftDeleteModel
from django.db import models
from django.utils.translation import gettext_lazy as _

class ServiceCallResult(SyncAbastractModel, SoftDeleteModel):
    fk_service_request = models.ForeignKey(
        ServiceRequest,
        on_delete=models.CASCADE, 
        related_name="requests",
    )

    func = models.CharField(
        max_length=255, 
        verbose_name=_("الحقل")
    )

    result = models.JSONField(_("الناتج"), null=True, blank=True)

    def __str__(self):
        return f'{self.external_id}'


    class Meta:
        verbose_name = _('تفاصيل طلب الخدمه')
        verbose_name_plural = _('تفاصيل طلب الخدمه')
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['external_id', "func"],
                name='unique_ex_func'
            ),
        ]
