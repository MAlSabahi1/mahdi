"""
نموذج إجراء الطلب - Request Action Model
لتسجيل جميع الإجراءات التي تتم على الطلب أثناء مروره بمراحل سير العمل
"""

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from OpenSoftCoreV4.utils.abstract_models.soft_delete_model import SoftDeleteModel
from OpenSoftCoreV4.utils.abstract_models.ex_id_model import ExIdModel
from OpenSoftCoreV4.common.models.Branch import Organization

from d_services.choices.choices import StageStatusChoice
from d_services.choices.choices import OutputTemplateTypeChoice
from d_services.choices.choices import InputTemplateTypeChoice
from utils.core.sync_abstract_model import SyncAbastractModel

class RequestAction(SyncAbastractModel, SoftDeleteModel):
    """
    إجراء الطلب - Request Action
    لتسجيل جميع الإجراءات التي تتم على الطلب أثناء مروره بمراحل سير العمل
    """
    fk_request = models.ForeignKey( 'ServiceRequest',on_delete=models.CASCADE,related_name='actions',verbose_name=_('الطلب'))
    fk_workflow_step = models.ForeignKey(
        'ServiceWorkflowStep',
        on_delete=models.PROTECT,
        related_name='actions',
        verbose_name=_('خطوة سير العمل')
    )
    
    # معلومات الخطوة
    is_final_step = models.BooleanField(
        default=False,
        verbose_name=_('خطوة نهائية')
    )
    is_execution_step = models.BooleanField(
        default=False,
        verbose_name=_('خطوة تنفيذ')
    )
    has_custom_output = models.BooleanField(
        default=False,
        verbose_name=_('لها مخرج خاص')
    )
    has_custom_input = models.BooleanField(default=False,verbose_name='لها مدخل خاص')
    has_approval = models.BooleanField(default=False, verbose_name=_('يتطلب موافقه'))
    is_approved = models.BooleanField(
        default=False,
        verbose_name=_('تم الموافقة عليه')
    )
    is_executed = models.BooleanField(
        default=False,
        verbose_name=_('تم التنفيذ عليه')
    )
    
    custom_output_template = models.CharField(
        max_length=255,
        choices=OutputTemplateTypeChoice.choices,
        null=True,
        blank=True,
        verbose_name=_('نموذج المخرج الخاص')
    )
    custom_input_template = models.CharField(
        max_length=255,
        choices=InputTemplateTypeChoice.choices,
        null=True,
        blank=True,
        verbose_name=_('نموذج المدخل الخاص')
    )
    output_file = models.FileField(
        upload_to='requests/action_outputs/',
        null=True,
        blank=True,
        verbose_name=_('ملف المخرج')
    )
    input_file = models.FileField(
        upload_to='requests/action_outputs/',
        null=True,
        blank=True,
        verbose_name=_('ملف الاستمارة')
    )

    
    # الملاحظات
    notes = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('الملاحظات')
    )
    note_recorded_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('وقت تسجيل الملاحظة')
    )



    fk_started_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='started_actions',
        verbose_name=_('تم البدء بواسطة'),
        null=True,
        blank=True
    )
    start_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('وقت البدء')
    )
    fk_executed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='executed_actions',
        verbose_name=_('تم التنفيذ بواسطة'),
        null=True,
        blank=True
    )
    executed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('وقت التنفيذ')
    )
    fk_completed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='completed_actions',
        verbose_name=_('تم الانتهاء بواسطة'),
        null=True,
        blank=True
    )
    delivery_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('وقت التسليم')
    )
    fk_approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='approved_actions',
        verbose_name=_('تمت الموافقة بواسطة'),
        null=True,
        blank=True
    )
    approved_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("وقت الموافقة")
    )
    fk_rejected_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='rejected_actions',
        verbose_name=_('تم الرفض بواسطة'),
        null=True,
        blank=True
    )
    rejected_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("وقت الرفض")
    )
    reject_reason = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('سبب الرفض')
    )
    fk_cancelled_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='cancelled_actions',
        verbose_name=_('تم الالغاء بواسطة'),
        null=True,
        blank=True
    )
    cancelled_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("وقت الالغاء")
    )
    fk_returned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='returned_actions',
        verbose_name=_('تم الإرجاع بواسطة'),
        null=True,
        blank=True
    )
    returned_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("وقت الإرجاع")
    )
    returned_reason = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('سبب الارجاع')
    )
    fk_moved_to_next_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='moved_actions',
        verbose_name=_('نقل للمرحلة التالية بواسطة'),
        null=True,
        blank=True
    )
    moved_to_next_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("وقت الانتقال الى المرحله التاليه")
    )
    # حالة المرحلة
    stage_status = models.CharField(
        max_length=100,
        choices=StageStatusChoice.choices,
        default=StageStatusChoice.PENDING,
        verbose_name=_('حالة المرحلة')
    )
    
    # بيانات وصفية إضافية
    stage_metadata = models.JSONField(
        verbose_name=_('بيانات وصفية للمرحلة')
    )
    is_current = models.BooleanField(
        default=False,
        verbose_name=_('المرحلة الحالية')
    )
    order = models.PositiveIntegerField(
        verbose_name=_('ترتيب الإجراء')
    )
    def __str__(self):
        return f'{self.fk_request.request_number if self.fk_request else None} - {self.fk_workflow_step}'

    class Meta:
        verbose_name = _('إجراء الطلب')
        verbose_name_plural = _('إجراءات الطلبات')
        ordering = ['fk_request', 'fk_workflow_step__order']
        indexes = [
            models.Index(fields=['fk_request', 'is_current'], name='idx_action_request_current'),
            models.Index(fields=['fk_workflow_step', 'stage_status'], name='idx_action_step_status'),
            models.Index(fields=['fk_request', 'stage_status'], name='idx_action_request_status'),
            models.Index(fields=['is_current', 'stage_status'], name='idx_action_current_status'),
        ]
