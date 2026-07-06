
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from OpenSoftCoreV4.utils.abstract_models.soft_delete_model import SoftDeleteModel
from OpenSoftCoreV4.utils.abstract_models.ex_id_model import ExIdModel


class StageChecklistItem(ExIdModel, SoftDeleteModel):
    """
    عنصر قائمة التحقق للمرحلة
    يمثل عنصر واحد في قائمة التحقق التي يجب إكمالها قبل إتمام المرحلة
    """
    fk_request_action = models.ForeignKey(
        'RequestAction',
        on_delete=models.CASCADE,
        related_name='checklist_items',
        verbose_name=_('إجراء الطلب')
    )
    
    # بيانات العنصر
    title = models.CharField(
        max_length=255,
        verbose_name=_('عنوان العنصر')
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('وصف العنصر')
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name=_('ترتيب العنصر')
    )
    
    # حالة الإكمال
    is_checked = models.BooleanField(
        default=False,
        verbose_name=_('تم الإكمال')
    )
    is_required = models.BooleanField(
        default=True,
        verbose_name=_('إلزامي')
    )
    
    # التتبع
    checked_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('وقت الإكمال')
    )
    fk_checked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='checked_checklist_items',
        verbose_name=_('تم الإكمال بواسطة'),
        null=True,
        blank=True
    )
    
    def __str__(self):
        status = '✓' if self.is_checked else '○'
        return f'{status} {self.title}'
    
    def check_item(self, user):
        """تعليم العنصر كمكتمل"""
        from django.utils import timezone
        self.is_checked = True
        self.checked_at = timezone.now()
        self.fk_checked_by = user
        self.save()
    
    def uncheck_item(self):
        """إلغاء تعليم العنصر"""
        self.is_checked = False
        self.checked_at = None
        self.fk_checked_by = None
        self.save()
    
    class Meta:
        verbose_name = _('عنصر قائمة التحقق')
        verbose_name_plural = _('عناصر قائمة التحقق')
        ordering = ['fk_request_action', 'order']


class WorkflowStepChecklistTemplate(SoftDeleteModel):
    """
    قالب قائمة التحقق لخطوة سير العمل
    يحدد عناصر قائمة التحقق الافتراضية لكل خطوة
    """
    fk_org_service_config = models.ForeignKey(
        'OrganizationServiceConfig',
        on_delete=models.CASCADE,
        related_name='checklist_templates',
        verbose_name=_('الخدمة')
    )
    fk_workflow_step = models.ForeignKey(
        'ServiceWorkflowStep',
        on_delete=models.CASCADE,
        related_name='checklist_templates',
        verbose_name=_('خطوة سير العمل')
    )
    
    title = models.CharField(
        max_length=255,
        verbose_name=_('عنوان العنصر')
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('وصف العنصر')
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name=_('ترتيب العنصر')
    )
    is_required = models.BooleanField(
        default=True,
        verbose_name=_('إلزامي')
    )
    
    def __str__(self):
        req = '⚠️' if self.is_required else ''
        return f'{req} {self.title}'
    
    class Meta:
        verbose_name = _('قالب قائمة التحقق')
        verbose_name_plural = _('قوالب قوائم التحقق')
        ordering = ['fk_workflow_step', 'order']
