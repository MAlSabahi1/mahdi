"""
نموذج سجل مزامنة الخدمات — Service Sync Log
يتتبع حالة مزامنة كل خدمة من النظام الفرعي إلى البوابة
يعمل على جانب النظام الفرعي فقط
"""
from django.db import models
from django.utils.translation import gettext_lazy as _


class ServiceSyncStatus(models.IntegerChoices):
    """حالات المزامنة"""
    NOT_SYNCED = 1, _("لم تتم المزامنة")
    SUCCESS = 2, _("تمت المزامنة بنجاح")
    FAILED = 3, _("فشلت المزامنة")


class ServiceSync(models.Model):
    """
    سجل مزامنة الخدمات — يُنشأ تلقائياً عند إنشاء خدمة جديدة
    """
    fk_service = models.OneToOneField(
        'd_services.Service',
        on_delete=models.CASCADE,
        related_name='sync_record',
        verbose_name=_('الخدمة')
    )
    service_name = models.CharField(
        max_length=255,
        blank=True,
        default='',
        verbose_name=_('اسم الخدمة'),
        help_text=_('اسم مقروء للعرض')
    )
    status = models.PositiveSmallIntegerField(
        choices=ServiceSyncStatus.choices,
        default=ServiceSyncStatus.NOT_SYNCED,
        verbose_name=_('حالة المزامنة')
    )
    error_message = models.TextField(
        blank=True,
        default='',
        verbose_name=_('رسالة الخطأ'),
        help_text=_('تفاصيل الخطأ عند فشل المزامنة')
    )
    last_synced_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('آخر محاولة مزامنة')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('تاريخ التسجيل')
    )

    class Meta:
        verbose_name = _('سجل مزامنة خدمة')
        verbose_name_plural = _('سجلات مزامنة الخدمات')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.service_name} — {self.get_status_display()}'
