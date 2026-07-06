"""
نموذج مرحلة سير العمل - Workflow Stage Model
تعريف عام لجميع المراحل الممكنة في النظام
"""
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from OpenSoftCoreV4.utils.abstract_models.soft_delete_model import SoftDeleteModel
from OpenSoftCoreV4.utils.abstract_models.ex_id_model import ExIdModel

from d_services.choices.choices import WorkflowStageTypeChoice


class WorkflowStage(ExIdModel, SoftDeleteModel):
    """
    مرحلة سير العمل - Workflow Stage
    تعريف عام لجميع المراحل الممكنة في النظام
    """
    name_ar = models.CharField(
        max_length=100,
        verbose_name=_('اسم المرحلة (عربي)')
    )
    name_en = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_('اسم المرحلة (إنجليزي)')
    )
    stage_type = models.CharField(
        max_length=100,
        choices=WorkflowStageTypeChoice.choices,
        verbose_name=_('نوع المرحلة')
    )
    is_final_stage = models.BooleanField(
        default=False,
        verbose_name=_('مرحلة نهائية')
    )
    is_execution_stage = models.BooleanField(
        default=False,
        verbose_name=_('مرحلة تنفيذ')
    )
    expected_duration_days = models.PositiveIntegerField(
        default=1,
        verbose_name=_('الوقت المتوقع (بالأيام) لتنفيذ هذا الإجراء')
    )

    def __str__(self):
        return f'{self.name_ar}'

    class Meta:
        verbose_name = _('مرحلة سير العمل')
        verbose_name_plural = _('مراحل سير العمل')
        constraints = [
            models.UniqueConstraint(
                fields=['name_ar'],
                name='unique_workflow_stage_name_ar',
                condition=Q(is_deleted=False),
            ),
        ]
