
from django.db import models
from django.utils.translation import gettext_lazy as _

from d_services.choices.choices import ServicePermissionType
from utils.core.base_sync_model import BaseSyncModel
class ServicePermission(BaseSyncModel):
    
    fk_service = models.ForeignKey(
        'Service',
        on_delete=models.CASCADE,
        related_name='permissions',
        verbose_name=_('الخدمة')
    )
    permission_type = models.CharField(
        choices=ServicePermissionType.choices,
        max_length=100,
        verbose_name=_('نوع الصلاحية')
    )

    def __str__(self):
        return f'{self.fk_service.code} - {self.permission_type}'

    class Meta(BaseSyncModel.Meta):
        verbose_name = _('صلاحية الخدمة')
        verbose_name_plural = _('صلاحيات الخدمات')
        constraints = BaseSyncModel.Meta.constraints +  [
            models.UniqueConstraint(
                fields=['fk_service', 'permission_type', 'source_system'],
                name='unique_service_permission_type',
            ),
        ]
