from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from core.models import TimeStampedModel

User = get_user_model()

class BIDataSource(TimeStampedModel):
    """
    مصادر البيانات لمنصة ذكاء الأعمال (BI).
    يمكن أن يكون Source عبارة عن Database View, ORM Model, أو Materialized View.
    """
    SOURCE_TYPES = [
        ('orm_model', _('نموذج ORM')),
        ('db_view', _('عرض قاعدة بيانات (View)')),
        ('raw_sql', _('استعلام مباشر (Raw SQL)')),
    ]

    name = models.CharField(max_length=200, verbose_name=_('اسم المصدر'))
    source_type = models.CharField(max_length=50, choices=SOURCE_TYPES, default='orm_model', verbose_name=_('نوع المصدر'))
    target = models.CharField(
        max_length=255, 
        verbose_name=_('الهدف'), 
        help_text=_('اسم الجدول، الـ View، أو مسار الـ ORM Model (مثال: personnel.PersonnelMaster)')
    )
    description = models.TextField(blank=True, verbose_name=_('الوصف'))
    is_active = models.BooleanField(default=True, verbose_name=_('مفعّل'))

    class Meta:
        app_label = 'services'
        db_table = 'services_bi_datasource'
        verbose_name = _('مصدر بيانات BI')
        verbose_name_plural = _('مصادر بيانات BI')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.get_source_type_display()})"


class EnterpriseReportTemplate(TimeStampedModel):
    """
    القالب الشامل لتقارير BI المؤسسية
    يحتوي على JSON Schema عملاق (config_schema) لتخزين كافة تفاصيل:
    - الأعمدة (Columns & Formatting)
    - الفلاتر المتداخلة (Nested Filters)
    - طريقة العرض (Layouts: Table, Pivot, Summary)
    - التجميعات والمعادلات (Aggregations & Calculated Columns)
    """
    title = models.CharField(max_length=255, verbose_name=_('عنوان التقرير'))
    slug = models.SlugField(unique=True, verbose_name=_('الرمز المرجعي'))
    description = models.TextField(blank=True, verbose_name=_('وصف التقرير'))
    
    data_source = models.ForeignKey(
        BIDataSource, 
        on_delete=models.PROTECT, 
        related_name='enterprise_reports', 
        verbose_name=_('مصدر البيانات')
    )
    
    config_schema = models.JSONField(
        default=dict, 
        verbose_name=_('مخطط التكوين (JSON Schema)'),
        help_text=_('يحتوي على Columns, Filters, Layout, Permissions')
    )
    
    is_active = models.BooleanField(default=True, verbose_name=_('مفعّل'))
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='created_enterprise_reports', verbose_name=_('أنشأه')
    )

    class Meta:
        app_label = 'services'
        db_table = 'services_enterprise_report_template'
        verbose_name = _('تقرير BI مؤسسي')
        verbose_name_plural = _('تقارير BI مؤسسية')
        ordering = ['-created_at']

    def __str__(self):
        return self.title
