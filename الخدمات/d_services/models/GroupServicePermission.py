"""
نموذج صلاحية مجموعة الخدمة - Group Service Permission Model
ربط الصلاحيات المحددة للمجموعات
"""
from django.db import models
from OpenSoftCoreV4.usermanager.models.Group import CustomGroup
from django.utils.translation import gettext_lazy as _

from utils.core.base_sync_model import BaseSyncModel


class GroupServicePermission(BaseSyncModel):
    fk_group = models.ForeignKey(
        CustomGroup,
        on_delete=models.CASCADE,
        related_name='service_permissions',
        verbose_name=_('المجموعة')
    )
    fk_permission = models.ForeignKey(
        'ServicePermission',
        on_delete=models.CASCADE,
        related_name='group_assignments',
        verbose_name=_('صلاحية الخدمة')
    )

    def __str__(self):
        return f'{self.fk_group.name_ar} - {self.fk_permission}'

    class Meta(BaseSyncModel.Meta):
        verbose_name = _('صلاحية مجموعة الخدمة')
        verbose_name_plural = _('صلاحيات مجموعات الخدمات')
        constraints = BaseSyncModel.Meta.constraints + [
            models.UniqueConstraint(
                fields=['fk_group', 'fk_permission', "source_system"],
                condition=models.Q(is_deleted=False),
                name='unique_group_service_permission',
            ),
        ]
