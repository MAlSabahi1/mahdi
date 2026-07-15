from django.db import models
from django.utils.translation import gettext_lazy as _
from .base import TimeStampedModel

class SystemSetting(TimeStampedModel):
    """
    نموذج الإعدادات العامة للنظام - Global System Settings
    يخزن الإعدادات الحيوية مثل سن التقاعد، الإجازات، وغيرها لتجنب تثبيتها في الكود.
    """
    CATEGORY_CHOICES = [
        ('retirement', _('إعدادات التقاعد')),
        ('promotions', _('إعدادات الترقيات')),
        ('services', _('إعدادات الخدمات')),
        ('holidays', _('إعدادات الإجازات')),
        ('system', _('إعدادات عامة للنظام')),
    ]
    
    TYPE_CHOICES = [
        ('int', _('رقم صحيح')),
        ('float', _('رقم عشري')),
        ('bool', _('منطقي (صح/خطأ)')),
        ('str', _('نص')),
        ('json', _('بيانات معقدة (JSON)')),
    ]

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, verbose_name=_('التصنيف'))
    key = models.CharField(max_length=100, unique=True, verbose_name=_('المفتاح البرمجي'))
    title = models.CharField(max_length=200, verbose_name=_('العنوان (للعرض)'))
    description = models.TextField(blank=True, verbose_name=_('الوصف المساعد'))
    
    value_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='str', verbose_name=_('نوع القيمة'))
    value = models.TextField(verbose_name=_('القيمة'))
    
    is_active = models.BooleanField(default=True, verbose_name=_('مفعل'))

    class Meta:
        db_table = 'core_system_setting'
        verbose_name = _('إعداد النظام')
        verbose_name_plural = _('إعدادات النظام')
        ordering = ['category', 'title']

    def __str__(self):
        return f"[{self.get_category_display()}] {self.title} = {self.value}"

    @property
    def typed_value(self):
        """Return the value cast to its proper Python type based on value_type."""
        if self.value_type == 'int':
            return int(self.value)
        elif self.value_type == 'float':
            return float(self.value)
        elif self.value_type == 'bool':
            return self.value.lower() in ['true', '1', 'yes', 't']
        elif self.value_type == 'json':
            import json
            try:
                return json.loads(self.value)
            except json.JSONDecodeError:
                return {}
        return self.value

    @classmethod
    def get_setting(cls, key, default=None):
        """Helper method to easily fetch a setting value by key."""
        try:
            setting = cls.objects.get(key=key, is_active=True)
            return setting.typed_value
        except cls.DoesNotExist:
            return default
