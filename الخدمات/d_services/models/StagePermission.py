"""
نموذج صلاحية المرحلة - Stage Permission Model
تحديد المستخدمين أو الأدوار المسموح لهم بالعمل على خطوة معينة
"""
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class StagePermission(models.Model):
    fk_workflow_step_permission = models.ForeignKey(
        'ServiceWorkFlowStepPermission',
        on_delete=models.CASCADE,
        related_name='stage_permissions',
        verbose_name=_('خطوة سير العمل')
    )
    fk_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='stage_permissions',
        verbose_name=_('المستخدم'),
    )
    role_name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_('اسم الدور')
    )
    role_id = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_('معرف الدور')
    )

    def __str__(self):
        if self.fk_user:
            return f'{self.fk_workflow_step_permission} - {self.fk_user}'
        return f'{self.fk_workflow_step_permission} - {self.role_name}'

    class Meta:
        verbose_name = _('صلاحية المرحلة')
        verbose_name_plural = _('صلاحيات المراحل')
