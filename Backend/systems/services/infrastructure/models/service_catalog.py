"""
Infrastructure Models: Service Catalog and Configurations
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import TimeStampedModel


class ServiceCatalog(TimeStampedModel):
    """تعريف الخدمة ديناميكياً — مستوحى من Service + ServiceVersion"""
    
    CATEGORY_CHOICES = [
        ('military', _('حركات الأفراد والتعيينات')),
        ('financial', _('الخدمات المالية والرواتب')),
        ('disciplinary', _('شؤون الانضباط والإجراءات')),
        ('other', _('أخرى')),
    ]

    APPROVAL_TYPE_CHOICES = [
        ('internal', _('موافقة داخلية')),
        ('external', _('موافقة خارجية')),
        ('none', _('لا تتطلب موافقة')),
    ]

    SERVICE_TYPE_CHOICES = [
        ('form', _('استمارة')),
        ('correction', _('تصحيح بيانات')),
        ('rank_settlement', _('ترقية / تسوية رتبة')),
        ('disciplinary', _('جزاء تأديبي')),
        ('security', _('أمان ومزامنة')),
        ('other', _('أخرى')),
    ]

    code = models.CharField(max_length=20, unique=True, verbose_name=_('كود الخدمة'))
    name_ar = models.CharField(max_length=255, verbose_name=_('اسم الخدمة'))
    description = models.TextField(blank=True, default='', verbose_name=_('وصف الخدمة'))
    category = models.CharField(
        max_length=50, 
        choices=CATEGORY_CHOICES,
        default='other',
        verbose_name=_('فئة الخدمة')
    )
    icon = models.CharField(max_length=50, verbose_name=_('أيقونة الخدمة (Lucide)'))
    form_type = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name=_('نوع الاستمارة المرتبطة'))
    
    # نوع الموافقة المطلوبة
    approval_type = models.CharField(
        max_length=20,
        choices=APPROVAL_TYPE_CHOICES,
        default='internal',
        verbose_name=_('نوع الموافقة'),
        help_text=_('هل الطلب يحتاج موافقة داخلية (مدير) أو خارجية (وزارة) أو لا يحتاج'),
    )
    
    # تصنيف نوع الخدمة (لتبويبات دليل الخدمات)
    service_type = models.CharField(
        max_length=30,
        choices=SERVICE_TYPE_CHOICES,
        default='form',
        verbose_name=_('تصنيف الخدمة'),
        help_text=_('يحدد التبويب الذي تظهر فيه الخدمة في دليل الخدمات'),
    )
    
    # إعدادات
    is_active = models.BooleanField(default=True, verbose_name=_('مفعلة'))
    requires_approval = models.BooleanField(default=True, verbose_name=_('تتطلب موافقات'))
    is_repeatable = models.BooleanField(default=True, verbose_name=_('قابلة للتكرار'))
    is_locked = models.BooleanField(default=False, verbose_name=_('مقفلة'))
    lock_reason = models.TextField(blank=True, default='', verbose_name=_('سبب القفل'))
    
    # SLA 
    expected_duration_hours = models.IntegerField(default=48, verbose_name=_('المدة المتوقعة (ساعات)'))
    
    # بيانات العرض
    attachments_count = models.IntegerField(default=0, verbose_name=_('عدد المرفقات المتوقعة'))
    target_audience = models.CharField(max_length=100, default='الكل', verbose_name=_('الفئة المستهدفة'))
    
    # حقول الاستمارة
    fields_schema = models.JSONField(default=dict, blank=True, verbose_name=_('مخطط الحقول (JSON)'))
    
    sort_order = models.IntegerField(default=0, verbose_name=_('الترتيب'))

    class Meta:
        app_label = 'services'
        db_table = 'services_service_catalog'
        verbose_name = _('دليل خدمة')
        verbose_name_plural = _('دليل الخدمات')
        ordering = ['sort_order', '-created_at']

    def __str__(self):
        return f'{self.code} - {self.name_ar}'


class ServicePrerequisite(TimeStampedModel):
    """شروط مسبقة للخدمة — مستوحى من ServicePrerequisite"""
    
    VALIDATION_CHOICES = [
        ('age_min', _('الحد الأدنى للعمر')),
        ('age_max', _('الحد الأقصى للعمر')),
        ('service_years_min', _('الحد الأدنى لسنوات الخدمة')),
        ('status_check', _('التحقق من الحالة الحالية')),
        ('custom', _('تحقق مخصص')),
    ]

    service = models.ForeignKey(
        ServiceCatalog, 
        on_delete=models.CASCADE, 
        related_name='prerequisites',
        verbose_name=_('الخدمة')
    )
    name_ar = models.CharField(max_length=255, verbose_name=_('اسم الشرط'))
    description = models.TextField(blank=True, verbose_name=_('الوصف'))
    validation_type = models.CharField(max_length=50, choices=VALIDATION_CHOICES, verbose_name=_('نوع التحقق'))
    validation_value = models.CharField(max_length=255, verbose_name=_('القيمة المطلوبة'))
    is_mandatory = models.BooleanField(default=True, verbose_name=_('إلزامي'))
    order = models.IntegerField(default=0, verbose_name=_('الترتيب'))

    class Meta:
        app_label = 'services'
        db_table = 'services_service_prerequisite'
        verbose_name = _('شرط مسبق')
        verbose_name_plural = _('الشروط المسبقة')
        ordering = ['service', 'order']

    def __str__(self):
        return f'{self.service.code} - {self.name_ar}'


class ChecklistTemplate(TimeStampedModel):
    """قالب Checklist لكل مرحلة — مستوحى من WorkflowStepChecklistTemplate"""
    
    service = models.ForeignKey(
        ServiceCatalog, 
        on_delete=models.CASCADE, 
        related_name='checklist_templates',
        verbose_name=_('الخدمة')
    )
    stage = models.CharField(max_length=50, verbose_name=_('مرحلة الاعتماد'))
    title = models.CharField(max_length=255, verbose_name=_('عنوان العنصر'))
    description = models.TextField(blank=True, verbose_name=_('الوصف'))
    is_required = models.BooleanField(default=True, verbose_name=_('إلزامي'))
    order = models.IntegerField(default=0, verbose_name=_('الترتيب'))

    class Meta:
        app_label = 'services'
        db_table = 'services_checklist_template'
        verbose_name = _('قالب عنصر تحقق')
        verbose_name_plural = _('قوالب عناصر التحقق')
        ordering = ['service', 'stage', 'order']

    def __str__(self):
        return f'{self.service.code} [{self.stage}] - {self.title}'
