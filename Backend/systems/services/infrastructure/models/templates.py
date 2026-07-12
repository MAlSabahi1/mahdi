"""
Infrastructure Models: Templates
══════════════════════════════════
ReportTemplate + CustomFormTemplate + CustomReportTemplate
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from core.models import TimeStampedModel

User = get_user_model()


class ReportTemplate(TimeStampedModel):
    """قوالب التقارير"""

    TEMPLATE_TYPE_CHOICES = [
        ('personnel_summary',   _('ملخص الأفراد')),
        ('department_strength', _('قوة الإدارات')),
        ('monthly_changes',     _('التغييرات الشهرية')),
        ('rejections_report',   _('تقرير المرفوضات')),
    ]

    name            = models.CharField(max_length=200, verbose_name=_('اسم القالب'))
    slug            = models.SlugField(unique=True, verbose_name=_('الرمز'))
    description     = models.TextField(blank=True, verbose_name=_('الوصف'))
    template_type   = models.CharField(
        max_length=50, choices=TEMPLATE_TYPE_CHOICES,
        verbose_name=_('نوع القالب')
    )
    default_filters = models.JSONField(
        default=dict, blank=True,
        verbose_name=_('المعايير الافتراضية')
    )
    is_active = models.BooleanField(default=True, verbose_name=_('نشط'))

    class Meta:
        app_label = 'services'
        db_table = 'services_report_template'
        verbose_name = _('قالب تقرير')
        verbose_name_plural = _('قوالب التقارير')
        ordering = ['name']

    def __str__(self):
        return self.name


class CustomFormTemplate(TimeStampedModel):
    """
    استمارة مخصصة يُنشئها مدير النظام.
    تظهر تلقائياً في FormRegistry بدون كود.
    """
    form_type = models.SlugField(
        unique=True, max_length=50,
        verbose_name=_('معرّف الاستمارة'),
        help_text=_('مثال: wounded, transferred — بالإنجليزية بدون مسافات')
    )
    label         = models.CharField(max_length=200, verbose_name=_('اسم الاستمارة'))
    target_status = models.CharField(
        max_length=100, verbose_name=_('الحالة المستهدفة'),
        help_text=_('اسم الحالة الخدمية التي ينتقل إليها الفرد')
    )
    description = models.TextField(blank=True, verbose_name=_('الوصف'))
    fields = models.JSONField(
        default=list, verbose_name=_('حقول بيانات الحالة'),
        help_text=_('[{"key":"...", "label":"...", "type":"text|date|select|textarea", "required":true, "options":["أ","ب"]}]')
    )
    attachments = models.JSONField(
        default=list, verbose_name=_('المرفقات المطلوبة'),
        help_text=_('[{"doc_type":"...", "label":"...", "required":true}]')
    )
    min_documents = models.PositiveIntegerField(default=1,  verbose_name=_('أقل عدد مرفقات'))
    max_documents = models.PositiveIntegerField(default=10, verbose_name=_('أقصى عدد مرفقات'))
    is_active     = models.BooleanField(default=True, verbose_name=_('مفعّلة'))
    created_by    = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='custom_forms', verbose_name=_('أنشأها')
    )

    class Meta:
        app_label = 'services'
        db_table = 'services_custom_form_template'
        verbose_name = _('استمارة مخصصة')
        verbose_name_plural = _('الاستمارات المخصصة')
        ordering = ['label']

    def __str__(self):
        return self.label


class CustomReportTemplate(TimeStampedModel):
    """
    نموذج تقرير مخصص يُنشئه مدير النظام.
    يظهر تلقائياً في ReportRegistry بدون كود.
    الترقيم يبدأ من 26.
    """
    model_number = models.PositiveIntegerField(
        unique=True, verbose_name=_('رقم النموذج'),
        help_text=_('يبدأ من 26 — الأرقام 1-25 محجوزة')
    )
    title = models.CharField(max_length=200, verbose_name=_('عنوان النموذج'))

    REPORT_TYPES = [
        ('detail',       _('تفصيلي')),
        ('aggregation',  _('خلاصة عددية')),
        ('status_based', _('حسب الحالة')),
    ]
    report_type    = models.CharField(
        max_length=20, choices=REPORT_TYPES, default='detail',
        verbose_name=_('نوع التقرير')
    )
    category       = models.CharField(max_length=50,  verbose_name=_('التصنيف'))
    parent_section = models.CharField(max_length=100, verbose_name=_('القسم الرئيسي'))
    sub_section    = models.CharField(max_length=100, blank=True, verbose_name=_('القسم الفرعي'))
    columns = models.JSONField(
        default=list, verbose_name=_('أعمدة الجدول'),
        help_text=_('[{"key":"rank", "label":"الرتبة", "source":"personnel.current_rank.name"}]')
    )
    base_filter = models.JSONField(
        default=dict, blank=True, verbose_name=_('فلتر البيانات'),
        help_text=_('{\"current_status__name\": \"...\"} — فلتر ORM')
    )
    is_active  = models.BooleanField(default=True, verbose_name=_('مفعّل'))
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='custom_reports', verbose_name=_('أنشأه')
    )

    class Meta:
        app_label = 'services'
        db_table = 'services_custom_report_template'
        verbose_name = _('نموذج تقرير مخصص')
        verbose_name_plural = _('النماذج المخصصة')
        ordering = ['model_number']

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.model_number and self.model_number < 26:
            raise ValidationError({'model_number': _('الأرقام 1-25 محجوزة للنماذج الأساسية')})

    def save(self, *args, **kwargs):
        if not self.model_number:
            last = CustomReportTemplate.objects.order_by('-model_number').first()
            self.model_number = (last.model_number + 1) if last else 26
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"نموذج {self.model_number} — {self.title}"


class DocumentFormTemplate(TimeStampedModel):
    """
    قالب استمارة ديناميكي (يتم تصميمه عبر الواجهة).
    يحتوي على ترويسة، محتوى (CKEditor)، وتذييل، مع إمكانية إدراج حقول ديناميكية وصور.
    """
    name = models.CharField(max_length=200, verbose_name=_('اسم الاستمارة'))
    slug = models.SlugField(unique=True, max_length=100, verbose_name=_('الرمز (Slug)'))
    category = models.CharField(max_length=100, verbose_name=_('التصنيف'), default='رسمية')
    is_preset = models.BooleanField(default=False, verbose_name=_('قالب جاهز (Preset)'))
    is_active = models.BooleanField(default=True, verbose_name=_('مفعّل'))

    # Header
    header_columns = models.PositiveSmallIntegerField(default=3, verbose_name=_('أعمدة الترويسة'))
    header_blocks = models.JSONField(
        default=list, verbose_name=_('محتوى الترويسة'),
        help_text=_('مصفوفة من النصوص (HTML) لكل عمود')
    )

    # Body
    body_content = models.TextField(blank=True, verbose_name=_('محتوى الاستمارة الرئيسي'))

    # Footer
    footer_columns = models.PositiveSmallIntegerField(default=1, verbose_name=_('أعمدة التذييل'))
    footer_blocks = models.JSONField(
        default=list, verbose_name=_('محتوى التذييل'),
        help_text=_('مصفوفة من النصوص (HTML) لكل عمود')
    )

    # Metadata
    page_size = models.CharField(max_length=20, default='A4', verbose_name=_('حجم الصفحة'))
    orientation = models.CharField(max_length=20, default='portrait', verbose_name=_('اتجاه الصفحة'))

    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='document_form_templates', verbose_name=_('أنشأه')
    )

    class Meta:
        app_label = 'services'
        db_table = 'services_document_form_template'
        verbose_name = _('استمارة ديناميكية')
        verbose_name_plural = _('الاستمارات الديناميكية')
        ordering = ['name']

    def __str__(self):
        return self.name
