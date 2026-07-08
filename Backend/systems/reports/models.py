from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class ExportRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', _('قيد المراجعة')
        APPROVED = 'APPROVED', _('تمت الموافقة')
        REJECTED = 'REJECTED', _('مرفوض')
        EXPIRED = 'EXPIRED', _('منتهي الصلاحية')

    report_id = models.CharField(max_length=50, verbose_name=_('معرف التقرير'))
    report_name = models.CharField(max_length=255, verbose_name=_('اسم التقرير'))
    
    requested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='export_requests',
        verbose_name=_('مقدم الطلب')
    )
    reason = models.TextField(verbose_name=_('سبب التصدير'))
    
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name=_('الحالة')
    )
    
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_exports',
        verbose_name=_('المعتمد')
    )
    approval_notes = models.TextField(
        null=True, 
        blank=True, 
        verbose_name=_('ملاحظات المراجعة')
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('تاريخ الطلب'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('تاريخ التحديث'))
    expires_at = models.DateTimeField(null=True, blank=True, verbose_name=_('تاريخ انتهاء الصلاحية'))

    class Meta:
        verbose_name = _('طلب تصدير')
        verbose_name_plural = _('طلبات التصدير')
        ordering = ['-created_at']

    def __str__(self):
        return f"طلب تصدير {self.report_name} بواسطة {self.requested_by}"
