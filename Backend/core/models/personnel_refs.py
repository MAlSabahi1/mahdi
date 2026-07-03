"""
Core Personnel Reference Models - البيانات المرجعية للأفراد
═══════════════════════════════════════════════════════════════
الرتب، الحالات الخدمية، الفئات الوظيفية، المسميات، المؤهلات، المناصب، تصنيفات القوة
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from .base import TimeStampedModel


class Rank(TimeStampedModel):
    """الرتبة العسكرية"""
    name = models.CharField(max_length=50, unique=True, verbose_name=_('اسم الرتبة'))
    order = models.IntegerField(unique=True, verbose_name=_('الترتيب'))
    is_officer = models.BooleanField(default=False, verbose_name=_('ضابط'))

    class Meta:
        db_table = 'core_rank'
        verbose_name = _('رتبة')
        verbose_name_plural = _('الرتب')
        ordering = ['order']
        indexes = [
            models.Index(fields=['order']),
        ]

    def __str__(self):
        return self.name


class ServiceStatus(TimeStampedModel):
    """الحالة الخدمية"""

    CLASSIFICATION_CHOICES = [
        ('active_full', _('قوة عاملة فعلية')),
        ('active_part', _('قوة عاملة غير فعلية')),
        ('inactive_temp', _('قوة غير عاملة مؤقتاً')),
        ('inactive_perm', _('قوة غير عاملة نهائياً')),
    ]

    name = models.CharField(max_length=100, unique=True, verbose_name=_('اسم الحالة'))
    classification = models.CharField(
        max_length=20,
        choices=CLASSIFICATION_CHOICES,
        verbose_name=_('التصنيف')
    )
    receives_salary = models.BooleanField(default=True, verbose_name=_('يستحق راتب'))
    requires_document = models.BooleanField(default=False, verbose_name=_('يتطلب مستند'))
    is_permanent_deactivation = models.BooleanField(
        default=False,
        verbose_name=_('خروج نهائي')
    )

    class Meta:
        db_table = 'core_service_status'
        verbose_name = _('حالة خدمية')
        verbose_name_plural = _('الحالات الخدمية')
        ordering = ['name']
        indexes = [
            models.Index(fields=['classification']),
        ]

    def __str__(self):
        return self.name


class JobCategory(TimeStampedModel):
    """الفئة الوظيفية"""
    name = models.CharField(max_length=50, unique=True, verbose_name=_('اسم الفئة'))

    class Meta:
        db_table = 'core_job_category'
        verbose_name = _('فئة وظيفية')
        verbose_name_plural = _('الفئات الوظيفية')
        ordering = ['name']

    def __str__(self):
        return self.name


class JobTitle(TimeStampedModel):
    """المسمى الوظيفي"""
    name = models.CharField(max_length=100, unique=True, verbose_name=_('المسمى الوظيفي'))
    category = models.ForeignKey(
        JobCategory,
        on_delete=models.PROTECT,
        related_name='job_titles',
        verbose_name=_('الفئة')
    )
    description = models.TextField(blank=True, verbose_name=_('الوصف'))

    class Meta:
        db_table = 'core_job_title'
        verbose_name = _('مسمى وظيفي')
        verbose_name_plural = _('المسميات الوظيفية')
        ordering = ['category', 'name']
        indexes = [
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return f"{self.name} ({self.category.name})"


class Qualification(TimeStampedModel):
    """المؤهل الدراسي"""
    name = models.CharField(max_length=50, unique=True, verbose_name=_('المؤهل'))
    order = models.IntegerField(unique=True, verbose_name=_('الترتيب'))

    class Meta:
        db_table = 'core_qualification'
        verbose_name = _('مؤهل دراسي')
        verbose_name_plural = _('المؤهلات الدراسية')
        ordering = ['order']

    def __str__(self):
        return self.name


class Position(TimeStampedModel):
    """المنصب الإداري - منفصل عن المسمى الوظيفي

    المنصب مرتبط بالفئة الوظيفية:
    - المناصب الإدارية (مدير إدارة، رئيس قسم) → فئة إداري فقط
    - بعض المناصب الميدانية (قائد سرية، قائد كتيبة) → فئة ميداني
    - allowed_categories فارغ = مسموح لأي فئة
    """
    name = models.CharField(max_length=100, unique=True, verbose_name=_('المنصب'))
    level = models.IntegerField(
        verbose_name=_('المستوى الإداري'),
        help_text=_('1=أعلى مستوى (وزير)، 10=أدنى مستوى')
    )
    requires_rank = models.ForeignKey(
        'core.Rank',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='positions',
        verbose_name=_('الرتبة المطلوبة'),
        help_text=_('الحد الأدنى من الرتبة المطلوبة لهذا المنصب')
    )
    allowed_categories = models.JSONField(
        default=list,
        blank=True,
        verbose_name=_('الفئات المسموحة'),
        help_text=_('مثل: ["إداري", "ميداني"] — فارغ = مسموح لأي فئة')
    )

    class Meta:
        db_table = 'core_position'
        verbose_name = _('منصب')
        verbose_name_plural = _('المناصب')
        ordering = ['level', 'name']
        indexes = [
            models.Index(fields=['level']),
        ]

    def __str__(self):
        return self.name


class ForceType(TimeStampedModel):
    """تصنيف القوة - حسب الدليل الإرشادي"""

    CATEGORY_CHOICES = [
        ('basic', _('أساسي')),
        ('committee', _('لجان')),
        ('newcomer', _('مستجدين')),
    ]

    RANK_TYPE_CHOICES = [
        ('officer', _('ضباط')),
        ('personnel', _('أفراد')),
        ('both', _('كلاهما')),
    ]

    name = models.CharField(max_length=100, unique=True, verbose_name=_('اسم التصنيف'))
    code = models.CharField(max_length=20, unique=True, verbose_name=_('الكود'))
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        verbose_name=_('الفئة')
    )
    rank_type = models.CharField(
        max_length=20,
        choices=RANK_TYPE_CHOICES,
        verbose_name=_('نوع الرتبة')
    )
    is_outside_payroll = models.BooleanField(
        default=False,
        verbose_name=_('خارج الصرف')
    )
    description = models.TextField(blank=True, verbose_name=_('الوصف'))
    order = models.IntegerField(default=0, verbose_name=_('الترتيب'))

    class Meta:
        db_table = 'core_force_type'
        verbose_name = _('تصنيف القوة')
        verbose_name_plural = _('تصنيفات القوة')
        ordering = ['order', 'name']
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['rank_type']),
        ]

    def __str__(self):
        return self.name


class VariableType(TimeStampedModel):
    """
    قاموس القيم الشائعة للمتغيرات الشهرية (اختياري)
    ═══════════════════════════════════════════════════
    المتغير الشهري هو نص حر يكتبه رئيس الخدمات.
    هذا القاموس فقط لتسهيل الاختيار السريع من قيم متكررة شائعة
    بدل إعادة كتابتها كل مرة.

    عند الاستيراد من الإكسل القديم: يتم مطابقة النص مع legacy_aliases
    لربطه تلقائياً بقيمة موحدة.

    أمثلة على القيم:
    - "يتم تنزيلهم من خدمات المحافظة الأولى_لاتوجد عليهم عهد"
    - "مواصلة_قوة عاملة غير فعلية"
    - "قوة فعلية"
    - "ينزل بسبب التكرار في نفس الوحدة"
    """

    code = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name=_('الرمز'),
        help_text=_('رمز فريد بالإنجليزية — مثال: download_from_marib')
    )
    name = models.CharField(
        max_length=300,
        unique=True,
        verbose_name=_('النص الموحد'),
        help_text=_('الصياغة الرسمية الموحدة التي ستظهر في الكشوفات')
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('الوصف'),
        help_text=_('شرح مختصر لمتى يُستخدم هذا المتغير')
    )
    legacy_aliases = models.JSONField(
        default=list,
        blank=True,
        verbose_name=_('المسميات القديمة'),
        help_text=_('صياغات مختلفة من الإكسل القديم تشير لنفس المعنى — للمطابقة التلقائية عند الاستيراد')
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('مفعّل')
    )
    order = models.IntegerField(
        default=0,
        verbose_name=_('الترتيب')
    )

    class Meta:
        db_table = 'core_variable_type'
        verbose_name = _('قيمة متغير شهري شائعة')
        verbose_name_plural = _('القيم الشائعة للمتغيرات الشهرية')
        ordering = ['order', 'name']
        indexes = [
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return self.name
