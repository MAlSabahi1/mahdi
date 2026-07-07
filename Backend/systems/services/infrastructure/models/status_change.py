"""
Infrastructure Models: Status Change Form
══════════════════════════════════════════
StatusChangeForm — الاستمارات الـ11 الرسمية لإثبات الحالة
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from core.models import TimeStampedModel, SecurityAdministration
from systems.personnel.models import PersonnelMaster
from infra.storage.models import Document

User = get_user_model()


class StatusChangeForm(TimeStampedModel):
    """استمارة إثبات حالة - الـ 11 استمارة الرسمية

    كل تغيير حالة حساس (وفاة، شهيد، تقاعد، إلخ) يتطلب:
    1. ملء استمارة رسمية بالبيانات المطلوبة
    2. إرفاق المستندات الإلزامية
    3. دورة اعتماد ثلاثية: قسم الخدمات ← مدير الموارد البشرية ← المدير العام
    """

    FORM_TYPE_CHOICES = [
        ('retirement_age',  _('بلوغ السن القانوني')),
        ('death',           _('وفاة')),
        ('missing',         _('مفقود')),
        ('medical_unfit',   _('عدم لياقة صحية')),
        ('end_of_service',  _('إنهاء مدة')),
        ('retired',         _('محال للتقاعد')),
        ('imprisoned',      _('مسجون')),
        ('escort',          _('مرافق / معيات')),
        ('martyr',          _('شهيد')),
        ('study_leave',     _('مفرغ للدراسة')),
        ('seconded',        _('منتدب')),
    ]

    STATUS_CHOICES = [
        ('draft',             _('مسودة')),
        ('in_progress',       _('قيد الإجراء')),
        ('approved',          _('معتمد')),
        ('rejected',          _('مرفوض')),
        ('returned',          _('مُرجع — بحاجة لتعديل')),
    ]
    
    PRIORITY_CHOICES = [
        ('low', _('منخفضة')),
        ('normal', _('عادية')),
        ('high', _('عالية')),
        ('urgent', _('عاجلة')),
    ]

    personnel = models.ForeignKey(
        PersonnelMaster,
        on_delete=models.PROTECT,
        related_name='status_change_forms',
        verbose_name=_('الفرد')
    )
    security_admin = models.ForeignKey(
        SecurityAdministration,
        on_delete=models.SET_NULL,
        null=True,
        related_name='status_change_forms',
        verbose_name=_('إدارة الأمن')
    )
    form_type = models.CharField(
        max_length=100,
        verbose_name=_('نوع الاستمارة')
    )
    form_data = models.JSONField(
        default=dict,
        verbose_name=_('بيانات الاستمارة'),
        help_text=_('البيانات التفصيلية حسب نوع الاستمارة')
    )

    # الحالة السابقة والجديدة
    from_status = models.ForeignKey(
        'core.ServiceStatus',
        on_delete=models.PROTECT,
        null=True,
        related_name='forms_from',
        verbose_name=_('الحالة السابقة')
    )
    to_status = models.ForeignKey(
        'core.ServiceStatus',
        on_delete=models.PROTECT,
        null=True,
        related_name='forms_to',
        verbose_name=_('الحالة الجديدة')
    )
    effective_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('تاريخ النفاذ')
    )

    # حالة الاستمارة
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name=_('حالة الاستمارة')
    )
    
    # حقول جديدة (دمج نظام الخدمات)
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='normal',
        verbose_name=_('الأولوية')
    )
    sla_deadline = models.DateTimeField(null=True, blank=True, verbose_name=_('الموعد النهائي (SLA)'))
    is_overdue = models.BooleanField(default=False, verbose_name=_('متأخر'))
    service_catalog = models.ForeignKey(
        'services.ServiceCatalog',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='forms',
        verbose_name=_('دليل الخدمة المرتبط')
    )

    # دورة الاعتماد الديناميكية
    submitted_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        related_name='submitted_forms', verbose_name=_('مقدم الطلب')
    )
    submitted_at = models.DateTimeField(null=True, blank=True, verbose_name=_('تاريخ التقديم'))
    
    current_step = models.ForeignKey(
        'services.ServiceWorkflowStep',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pending_forms',
        verbose_name=_('المرحلة الحالية')
    )
    
    workflow_log = models.JSONField(
        default=list,
        verbose_name=_('سجل الاعتمادات'),
        help_text=_('سجل ديناميكي لمن اعتمد الاستمارة في كل مرحلة ومتى')
    )
    
    is_printed = models.BooleanField(
        default=False,
        verbose_name=_('تمت الطباعة')
    )
    ministry_approval_doc = models.ForeignKey(
        Document,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ministry_approvals',
        verbose_name=_('مستند موافقة الوزارة')
    )

    rejection_reason = models.TextField(blank=True, verbose_name=_('سبب الرفض'))
    rejected_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='rejected_forms', verbose_name=_('رفض بواسطة')
    )

    # المرفقات
    required_attachments = models.JSONField(
        default=list,
        verbose_name=_('المرفقات المطلوبة'),
        help_text=_('قائمة أنواع المرفقات الإلزامية')
    )
    attachments = models.ManyToManyField(
        Document,
        blank=True,
        related_name='status_change_forms',
        verbose_name=_('المرفقات')
    )
    attachments_complete = models.BooleanField(
        default=False,
        verbose_name=_('المرفقات مكتملة')
    )

    notes = models.TextField(blank=True, verbose_name=_('ملاحظات'))

    class Meta:
        app_label = 'services'
        db_table = 'services_status_change_form'
        verbose_name = _('استمارة إثبات حالة')
        verbose_name_plural = _('استمارات إثبات الحالة')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['form_type', 'status']),
            models.Index(fields=['personnel', 'status']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.get_form_type_display()} - {self.personnel} - {self.get_status_display()}"
