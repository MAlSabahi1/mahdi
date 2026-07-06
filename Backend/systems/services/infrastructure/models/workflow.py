"""
Infrastructure Models: Dynamic Workflow Engine
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import TimeStampedModel
from systems.services.infrastructure.models.service_catalog import ServiceCatalog

class WorkflowStage(TimeStampedModel):
    """
    المرحلة العامة في سير العمل - Workflow Stage
    مثل: الموارد البشرية، الخدمات، الشؤون المالية، المدير العام
    """
    code = models.CharField(max_length=50, unique=True, verbose_name=_('كود المرحلة'))
    name_ar = models.CharField(max_length=255, verbose_name=_('اسم المرحلة'))
    description = models.TextField(blank=True, verbose_name=_('وصف المرحلة'))
    icon = models.CharField(max_length=50, blank=True, verbose_name=_('أيقونة المرحلة'))
    is_active = models.BooleanField(default=True, verbose_name=_('مفعلة'))

    class Meta:
        app_label = 'services'
        db_table = 'services_workflow_stage'
        verbose_name = _('مرحلة سير العمل')
        verbose_name_plural = _('مراحل سير العمل')

    def __str__(self):
        return self.name_ar


class ServiceWorkflowStep(TimeStampedModel):
    """
    خطوة سير عمل الخدمة - Service Workflow Step
    تحديد تسلسل المراحل (Workflow) الخاص بخدمة معينة
    """
    service = models.ForeignKey(
        ServiceCatalog,
        on_delete=models.CASCADE,
        related_name='workflow_steps',
        verbose_name=_('الخدمة')
    )
    stage = models.ForeignKey(
        WorkflowStage,
        on_delete=models.PROTECT,
        related_name='service_steps',
        verbose_name=_('المرحلة العامة')
    )
    order = models.PositiveIntegerField(verbose_name=_('ترتيب الخطوة'))
    description = models.TextField(null=True, blank=True, verbose_name=_('وصف الخطوة'))
    is_final_step = models.BooleanField(default=False, verbose_name=_('خطوة نهائية (اعتماد نهائي)'))
    is_execution_step = models.BooleanField(default=False, verbose_name=_('خطوة تنفيذ (إصدار)'))
    
    # إعدادات الموافقة
    requires_approval = models.BooleanField(default=True, verbose_name=_('تتطلب موافقة'))
    
    class Meta:
        app_label = 'services'
        db_table = 'services_service_workflow_step'
        verbose_name = _('خطوة سير عمل الخدمة')
        verbose_name_plural = _('خطوات سير عمل الخدمات')
        ordering = ['service', 'order']
        constraints = [
            models.UniqueConstraint(
                fields=['service', 'order'],
                name='unique_service_workflow_order'
            )
        ]

    def __str__(self):
        return f'{self.service.code} - {self.stage.name_ar} ({self.order})'
