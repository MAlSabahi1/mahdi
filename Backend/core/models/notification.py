"""
Core Notification Models - الإشعارات المركزية
═══════════════════════════════════════════════════
نظام إشعارات موحد يخدم كل الأنظمة الفرعية.
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from .base import TimeStampedModel

User = get_user_model()


class NotificationRecord(TimeStampedModel):
    """
    إشعار مركزي — يخدم كل الأنظمة الفرعية.

    أنواع الإشعارات:
    - STAGING_SUBMITTED: تم رفع كشف جديد
    - RECONCILIATION_NEEDED: هناك اختلافات بحاجة حل
    - STATUS_CHANGE: تم تغيير حالة فرد
    - DUAL_AUTH_REQUIRED: بحاجة موافقة تفويض مزدوج
    - MONTH_CLOSED: تم إقفال الشهر
    - SYSTEM: إشعار نظامي عام
    """
    NOTIFICATION_TYPE_CHOICES = [
        ('STAGING_SUBMITTED', _('كشف جديد')),
        ('RECONCILIATION_NEEDED', _('مطابقة مطلوبة')),
        ('STATUS_CHANGE', _('تغيير حالة')),
        ('DUAL_AUTH_REQUIRED', _('تفويض مزدوج مطلوب')),
        ('DUAL_AUTH_APPROVED', _('تفويض مزدوج مُعتمد')),
        ('DUAL_AUTH_REJECTED', _('تفويض مزدوج مرفوض')),
        ('MONTH_CLOSED', _('إقفال شهر')),
        ('IMPORT_COMPLETED', _('اكتمال استيراد')),
        ('EXPORT_COMPLETED', _('اكتمال تصدير')),
        ('SYSTEM', _('إشعار نظامي')),
        ('WARNING', _('تحذير')),
        ('ERROR', _('خطأ')),
    ]
    PRIORITY_CHOICES = [
        ('low', _('منخفض')),
        ('normal', _('عادي')),
        ('high', _('مرتفع')),
        ('urgent', _('عاجل')),
    ]

    notification_type = models.CharField(max_length=30, choices=NOTIFICATION_TYPE_CHOICES,
                                          verbose_name=_('النوع'))
    title = models.CharField(max_length=200, verbose_name=_('العنوان'))
    message = models.TextField(verbose_name=_('الرسالة'))
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES,
                                default='normal', verbose_name=_('الأولوية'))
    target_user = models.ForeignKey(User, on_delete=models.CASCADE,
                                     related_name='notifications', verbose_name=_('المستخدم المستهدف'))
    triggered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                      related_name='triggered_notifications', verbose_name=_('المُرسل'))
    is_read = models.BooleanField(default=False, verbose_name=_('مقروء'))
    read_at = models.DateTimeField(null=True, blank=True, verbose_name=_('تاريخ القراءة'))
    related_object_type = models.CharField(max_length=100, blank=True, verbose_name=_('نوع الكائن'))
    related_object_id = models.CharField(max_length=100, blank=True, verbose_name=_('معرف الكائن'))
    action_url = models.CharField(max_length=500, blank=True, verbose_name=_('رابط الإجراء'))
    extra_data = models.JSONField(null=True, blank=True, verbose_name=_('بيانات إضافية'))

    class Meta:
        db_table = 'core_notification'
        verbose_name = _('إشعار')
        verbose_name_plural = _('الإشعارات')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['target_user', 'is_read']),
            models.Index(fields=['notification_type']),
            models.Index(fields=['created_at']),
            models.Index(fields=['priority']),
        ]

    def __str__(self):
        return f"[{self.notification_type}] {self.title}"

    def mark_as_read(self):
        if not self.is_read:
            from django.utils import timezone
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=['is_read', 'read_at'])
