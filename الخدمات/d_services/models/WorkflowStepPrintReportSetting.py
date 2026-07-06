"""
نموذج إعدادات طباعة خطوة سير العمل - Workflow Step Print Report Setting Model
ربط إعدادات الطباعة بخطوات سير العمل حسب المنظمة
"""
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from OpenSoftCoreV4.utils.abstract_models.soft_delete_model import SoftDeleteModel
from OpenSoftCoreV4.utils.abstract_models.ex_id_model import ExIdModel


class WorkflowStepPrintReportSetting(ExIdModel, SoftDeleteModel):
    """
    إعدادات طباعة خطوة سير العمل
    - fk_org_service_config: إعدادات الخدمة للمنظمة
    - fk_workflow_step: خطوة سير العمل
    - fk_print_report_setting_for_output: إعدادات الطباعة للمخرج
    - fk_print_report_setting_for_input: إعدادات الطباعة للمدخل
    """
    fk_org_service_config = models.ForeignKey(
        'OrganizationServiceConfig',
        on_delete=models.CASCADE,
        related_name='workflow_step_print_settings',
        verbose_name=_('إعدادات الخدمة للمنظمة')
    )
    fk_workflow_step = models.ForeignKey(
        'ServiceWorkflowStep',
        on_delete=models.CASCADE,
        related_name='print_report_settings',
        verbose_name=_('خطوة سير العمل')
    )
    fk_print_report_setting_for_output = models.ForeignKey(
        'common.PrintReportSetting',
        on_delete=models.SET_NULL,
        related_name='workflow_step_output_settings',
        verbose_name=_('إعدادات الطباعة للمخرج'),
        null=True,
        blank=True
    )
    fk_print_report_setting_for_input = models.ForeignKey(
        'common.PrintReportSetting',
        on_delete=models.SET_NULL,
        related_name='workflow_step_input_settings',
        verbose_name=_('إعدادات الطباعة للمدخل'),
        null=True,
        blank=True
    )

    def clean(self):
        from django.core.exceptions import ValidationError
        
        # التحقق من أن إعدادات الطباعة تابعة لنفس المنظمة
        org = self.fk_org_service_config.fk_organization
        
        if self.fk_print_report_setting_for_input:
            if self.fk_print_report_setting_for_input.fk_branch != org:
                raise ValidationError({
                    'fk_print_report_setting_for_input': _('إعدادات الطباعة للمدخل يجب أن تكون تابعة لنفس المنظمة')
                })
        
        if self.fk_print_report_setting_for_output:
            if self.fk_print_report_setting_for_output.fk_branch != org:
                raise ValidationError({
                    'fk_print_report_setting_for_output': _('إعدادات الطباعة للمخرج يجب أن تكون تابعة لنفس المنظمة')
                })
        
        # التحقق من أن خطوة سير العمل تابعة لنفس الخدمة
        if self.fk_workflow_step.fk_service != self.fk_org_service_config.fk_service:
            raise ValidationError({
                'fk_workflow_step': _('خطوة سير العمل يجب أن تكون تابعة لنفس الخدمة')
            })

    def __str__(self):
        return f'{self.fk_workflow_step} - {self.fk_org_service_config.fk_organization}'

    class Meta:
        verbose_name = _('إعدادات طباعة خطوة سير العمل')
        verbose_name_plural = _('إعدادات طباعة خطوات سير العمل')
        constraints = [
            models.UniqueConstraint(
                fields=['fk_org_service_config', 'fk_workflow_step'],
                name='unique_org_config_workflow_step_print',
                condition=Q(is_deleted=False),
            ),
        ]







