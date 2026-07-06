
from django.db import models
from django.utils.translation import gettext_lazy as _
from OpenSoftCoreV4.utils.abstract_models.ex_id_model import ExIdModel

from d_services.choices.choices import ActionPermissionType
class ServiceWorkFlowStepPermission(ExIdModel, models.Model):
    
    fk_workflow_step = models.ForeignKey(
        'ServiceWorkflowStep',
        on_delete=models.CASCADE,
        related_name='permissions',
        verbose_name=_('خطوة سير العمل')
    )
    permission_type = models.CharField(
        choices=ActionPermissionType.choices,
        max_length=100,
        verbose_name=_('نوع الصلاحية')
    )

    def __str__(self):
        return f'{self.fk_workflow_step } - {self.permission_type}'

    class Meta:
        verbose_name = _('صلاحية خطوة سير العمل')
        verbose_name_plural = _('صلاحيات خطوات سير العمل')
        constraints = [
            models.UniqueConstraint(
                fields=['fk_workflow_step', 'permission_type'],
                name='unique_workflow_step_permission_type',
            ),
        ]
