"""
Infrastructure Models: Form Notes, Logs, Returns, and Checklists
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from core.models import TimeStampedModel
from .status_change import StatusChangeForm

User = get_user_model()


class FormNote(TimeStampedModel):
    """ملاحظات متعددة على الطلب — مستوحى من RequestNote"""
    form = models.ForeignKey(
        StatusChangeForm, 
        on_delete=models.CASCADE, 
        related_name='form_notes',
        verbose_name=_('الطلب')
    )
    content = models.TextField(verbose_name=_('محتوى الملاحظة'))
    created_by = models.ForeignKey(
        User, 
        on_delete=models.PROTECT, 
        related_name='form_notes_created',
        verbose_name=_('أضيفت بواسطة')
    )

    class Meta:
        app_label = 'services'
        db_table = 'services_form_note'
        verbose_name = _('ملاحظة على الطلب')
        verbose_name_plural = _('ملاحظات الطلبات')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.form.id} - {self.content[:50]}'


class FormEventLog(TimeStampedModel):
    """سجل أحداث الطلب (Timeline) — مستوحى من WorkflowLog + RequestLog"""
    
    ACTION_CHOICES = [
        ('created', _('إنشاء')),
        ('submitted', _('تقديم')),
        ('approved', _('اعتماد')),
        ('rejected', _('رفض')),
        ('returned', _('إرجاع')),
        ('note_added', _('إضافة ملاحظة')),
        ('updated', _('تحديث بيانات')),
        ('checklist_checked', _('إكمال تحقق')),
    ]
    
    SLA_CHOICES = [
        ('on_time', _('في الوقت')),
        ('at_risk', _('معرض للخطر')),
        ('overdue', _('متأخر')),
        ('na', _('غير متاح')),
    ]

    form = models.ForeignKey(
        StatusChangeForm, 
        on_delete=models.CASCADE, 
        related_name='event_logs',
        verbose_name=_('الطلب')
    )
    action = models.CharField(
        max_length=30, 
        choices=ACTION_CHOICES,
        verbose_name=_('الإجراء')
    )
    from_status = models.CharField(max_length=50, null=True, blank=True, verbose_name=_('من حالة'))
    to_status = models.CharField(max_length=50, null=True, blank=True, verbose_name=_('إلى حالة'))
    performed_by = models.ForeignKey(
        User, 
        on_delete=models.PROTECT,
        verbose_name=_('تم بواسطة')
    )
    notes = models.TextField(blank=True, verbose_name=_('ملاحظات'))
    
    # SLA Fields
    expected_duration_hours = models.IntegerField(null=True, blank=True, verbose_name=_('المدة المتوقعة (ساعات)'))
    actual_duration_hours = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, verbose_name=_('المدة الفعلية (ساعات)'))
    sla_status = models.CharField(max_length=20, choices=SLA_CHOICES, default='na', verbose_name=_('حالة SLA'))
    is_overdue = models.BooleanField(default=False, verbose_name=_('متأخر'))

    class Meta:
        app_label = 'services'
        db_table = 'services_form_event_log'
        verbose_name = _('سجل حدث')
        verbose_name_plural = _('سجلات الأحداث')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.form.id} - {self.get_action_display()}'


class FormReturnLog(TimeStampedModel):
    """سجل إرجاع الطلب — مستوحى من RequestReturnLog"""
    
    RETURN_REASON_CHOICES = [
        ('missing_attachments', _('نقص المرفقات')),
        ('incorrect_data', _('بيانات غير صحيحة')),
        ('incomplete_form', _('نموذج غير مكتمل')),
        ('other', _('أخرى')),
    ]

    form = models.ForeignKey(
        StatusChangeForm, 
        on_delete=models.CASCADE, 
        related_name='return_logs',
        verbose_name=_('الطلب')
    )
    return_reason = models.CharField(
        max_length=30, 
        choices=RETURN_REASON_CHOICES,
        verbose_name=_('سبب الإرجاع')
    )
    return_details = models.TextField(blank=True, verbose_name=_('تفاصيل السبب'))
    from_status = models.CharField(max_length=50, verbose_name=_('من مرحلة'))
    to_status = models.CharField(max_length=50, verbose_name=_('إلى مرحلة'))
    returned_by = models.ForeignKey(
        User, 
        on_delete=models.PROTECT,
        related_name='returned_forms',
        verbose_name=_('أُرجع بواسطة')
    )
    is_resolved = models.BooleanField(default=False, verbose_name=_('تم حل المشكلة'))
    resolution_notes = models.TextField(blank=True, verbose_name=_('ملاحظات الحل'))
    resolved_at = models.DateTimeField(null=True, blank=True, verbose_name=_('تاريخ الحل'))

    class Meta:
        app_label = 'services'
        db_table = 'services_form_return_log'
        verbose_name = _('سجل إرجاع')
        verbose_name_plural = _('سجلات الإرجاع')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.form.id} - {self.get_return_reason_display()}'


class FormChecklist(TimeStampedModel):
    """قائمة تحقق لكل مرحلة — مستوحى من StageChecklistItem"""
    form = models.ForeignKey(
        StatusChangeForm, 
        on_delete=models.CASCADE, 
        related_name='checklist_items',
        verbose_name=_('الطلب')
    )
    title = models.CharField(max_length=255, verbose_name=_('عنوان العنصر'))
    description = models.TextField(blank=True, verbose_name=_('الوصف'))
    stage = models.CharField(max_length=50, verbose_name=_('مرحلة الاعتماد'))
    is_required = models.BooleanField(default=True, verbose_name=_('إلزامي'))
    is_checked = models.BooleanField(default=False, verbose_name=_('مكتمل'))
    checked_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name=_('اكتمل بواسطة')
    )
    checked_at = models.DateTimeField(null=True, blank=True, verbose_name=_('تاريخ الإكمال'))
    order = models.IntegerField(default=0, verbose_name=_('الترتيب'))

    class Meta:
        app_label = 'services'
        db_table = 'services_form_checklist'
        verbose_name = _('عنصر تحقق')
        verbose_name_plural = _('قوائم التحقق')
        ordering = ['form', 'stage', 'order']

    def __str__(self):
        return f'{self.form.id} - {self.title}'
