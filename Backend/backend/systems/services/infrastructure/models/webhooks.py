"""
Infrastructure Models: Webhooks
═════════════════════════════════
WebhookConfig — تكوين إشعارات الويب هوكس
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from core.models import TimeStampedModel

User = get_user_model()


class WebhookConfig(TimeStampedModel):
    """تكوين Webhook لإشعار الأنظمة الخارجية"""

    EVENT_CHOICES = [
        ('rejection.created',        _('رفض تغيير')),
        ('staging.ready',            _('كشوفة جاهزة')),
        ('import.completed',         _('اكتمال الاستيراد')),
        ('reconciliation.completed', _('اكتمال المطابقة')),
        ('report.ready',             _('تقرير جاهز')),
        ('dual_auth.pending',        _('تفويض مزدوج جديد')),
    ]

    url = models.URLField(
        verbose_name=_('عنوان URL'),
        help_text=_('نقطة نهاية HTTPS لإرسال الإشعارات')
    )
    secret = models.CharField(
        max_length=128,
        verbose_name=_('المفتاح السري'),
        help_text=_('مفتاح HMAC للتوقيع')
    )
    events = models.JSONField(
        default=list,
        verbose_name=_('الأحداث المفعّلة'),
    )
    central_department = models.ForeignKey(
        'core.CentralDepartment',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='webhook_configs',
        verbose_name=_('الإدارة المركزية'),
        help_text=_('فارغ = جميع الإدارات')
    )
    is_active = models.BooleanField(default=True, verbose_name=_('مفعّل'))
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        related_name='webhook_configs', verbose_name=_('أنشئ بواسطة')
    )
    last_triggered_at    = models.DateTimeField(null=True, blank=True, verbose_name=_('آخر تشغيل'))
    last_response_code   = models.IntegerField(null=True, blank=True, verbose_name=_('آخر كود استجابة'))

    class Meta:
        app_label = 'services'
        db_table = 'services_webhook_config'
        verbose_name = _('إعداد Webhook')
        verbose_name_plural = _('إعدادات Webhook')

    def __str__(self):
        return f"{self.url} - {'✅' if self.is_active else '❌'}"
