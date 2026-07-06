"""
نموذج خطوة سير عمل الخدمة - Service Workflow Step Model
تحديد تسلسل المراحل الخاص بخدمة معينة
"""
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from OpenSoftCoreV4.utils.abstract_models.soft_delete_model import SoftDeleteModel
from OpenSoftCoreV4.utils.abstract_models.ex_id_model import ExIdModel
from d_services.choices.choices import OutputTemplateTypeChoice, InputTemplateTypeChoice
from d_services.apis.external_methods.base import validate_function_name

class ServiceWorkflowStep(ExIdModel, SoftDeleteModel):
    """
    خطوة سير عمل الخدمة - Service Workflow Step
    تحديد تسلسل المراحل (Workflow) الخاص بخدمة معينة
    """
    fk_service = models.ForeignKey(
        'Service',
        on_delete=models.CASCADE,
        related_name='workflow_steps',
        verbose_name=_('الخدمة')
    )
    fk_stage = models.ForeignKey(
        'WorkflowStage',
        on_delete=models.PROTECT,
        related_name='service_steps',
        verbose_name=_('المرحلة العامة')
    )
    order = models.PositiveIntegerField(
        verbose_name=_('ترتيب الخطوة')
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('وصف الخطوة')
    )
    is_final_step = models.BooleanField(
        default=False,
        verbose_name=_('خطوة نهائية')
    )
    is_execution_step = models.BooleanField(
        default=False,
        verbose_name=_('خطوة تنفيذ')
    )
    
    # إعدادات المخرجات المخصصة
    has_custom_output = models.BooleanField(
        default=False,
        verbose_name=_('لها مخرج خاص')
    )
    has_approval = models.BooleanField(
        default=False,
        verbose_name=_('يتطلب موافقه')
    )
    custom_output_template = models.CharField(
        max_length=255,
        choices=OutputTemplateTypeChoice.choices,
        null=True,
        blank=True,
        verbose_name=_('نموذج المخرج الخاص')
    )
    custom_output_function = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('دالة المخرج الخاص'),
        # validators=[validate_function_name]
    )
    has_custom_input = models.BooleanField(default=False, verbose_name='لها مدخل خاص')
    custom_input_template = models.CharField(
        max_length=255,
        choices=InputTemplateTypeChoice.choices,
        null=True,
        blank=True,
        verbose_name=_('نموذج المدخل الخاص')
    )
    custom_input_function = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('دالة المدخل الخاص'),
        # validators=[validate_function_name]
    )
    
    # الأوقات
    start_offset_days = models.PositiveIntegerField(
        default=0,
        verbose_name=_('أيام بدء المرحلة من تاريخ الطلب')
    )
    delivery_offset_days = models.PositiveIntegerField(
        default=1,
        verbose_name=_('أيام التسليم من تاريخ الطلب')
    )
    
    # إجراء التنفيذ
    execution_procedure_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('اسم إجراء التنفيذ'),
        # validators=[validate_function_name]
    )
    icon = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_('أيقونة الخطوة'),
        help_text=_('اسم الأيقونة مثل: mdi-check, mdi-clock')
    )

    def __str__(self):
        return f'{self.fk_service.code} - {self.fk_stage.name_ar} ({self.order})'

    class Meta:
        verbose_name = _('خطوة سير عمل الخدمة')
        verbose_name_plural = _('خطوات سير عمل الخدمات')
        ordering = ['fk_service', 'order']
        constraints = [
            models.UniqueConstraint(
                fields=['fk_service', 'order'],
                name='unique_service_workflow_order',
                condition=Q(is_deleted=False),
            ),
        ]
# make signal to save permissoin for this steps with check 
