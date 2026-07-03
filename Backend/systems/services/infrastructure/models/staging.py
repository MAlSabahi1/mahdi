"""
Infrastructure Models: Staging
═══════════════════════════════
StagingRecord — منطقة الفحص المؤقتة
"""
import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from core.models import TimeStampedModel, SecurityAdministration
from systems.personnel.models import PersonnelMaster

User = get_user_model()


class StagingRecord(TimeStampedModel):
    """منطقة الفحص المؤقتة"""

    STATUS_CHOICES = [
        ('pending',  _('قيد المراجعة')),
        ('approved', _('موافق عليه')),
        ('rejected', _('مرفوض')),
    ]

    SEVERITY_CHOICES = [
        ('low',  _('منخفض - لا يحتاج مستند')),
        ('high', _('عالي - يحتاج مستند')),
    ]

    personnel = models.ForeignKey(
        PersonnelMaster,
        on_delete=models.CASCADE,
        related_name='staging_records',
        verbose_name=_('الفرد')
    )
    security_admin = models.ForeignKey(
        SecurityAdministration,
        on_delete=models.SET_NULL,
        null=True,
        related_name='staging_records',
        verbose_name=_('إدارة الأمن')
    )
    upload_batch_id = models.UUIDField(
        default=uuid.uuid4,
        verbose_name=_('معرف دفعة الرفع')
    )
    proposed_change = models.JSONField(verbose_name=_('التغيير المقترح'))
    notes = models.TextField(blank=True, verbose_name=_('ملاحظات'))
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name=_('الحالة')
    )
    severity = models.CharField(
        max_length=10,
        choices=SEVERITY_CHOICES,
        default='low',
        verbose_name=_('الأهمية')
    )
    requires_document     = models.BooleanField(default=False, verbose_name=_('يتطلب مستند'))
    name_mismatch         = models.BooleanField(default=False, verbose_name=_('اختلاف في الاسم'))
    rank_mismatch         = models.BooleanField(default=False, verbose_name=_('اختلاف في الرتبة'))
    national_id_mismatch  = models.BooleanField(default=False, verbose_name=_('اختلاف في الرقم الوطني'))
    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_staging_records',
        verbose_name=_('راجع بواسطة')
    )
    reviewed_at = models.DateTimeField(null=True, blank=True, verbose_name=_('تاريخ المراجعة'))

    class Meta:
        app_label = 'services'
        db_table = 'services_staging_record'
        verbose_name = _('سجل مؤقت')
        verbose_name_plural = _('السجلات المؤقتة')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['personnel', 'status']),
            models.Index(fields=['upload_batch_id']),
            models.Index(fields=['severity']),
        ]

    def __str__(self):
        return f"{self.personnel.military_number} - {self.status}"
