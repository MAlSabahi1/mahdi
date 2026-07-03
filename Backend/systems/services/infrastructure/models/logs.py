"""
Infrastructure Models: Logs
═════════════════════════════
ExportLog + RejectionLog — سجلات التصدير والرفض
"""
import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from core.models import TimeStampedModel, SecurityAdministration
from systems.personnel.models import PersonnelMaster
from .staging import StagingRecord

User = get_user_model()


class ExportLog(TimeStampedModel):
    """سجل التصدير - لتوثيق عمليات تصدير القوالب"""

    STATUS_CHOICES = [
        ('pending',  _('قيد الانتظار')),
        ('returned', _('تم الإرجاع')),
        ('expired',  _('منتهي الصلاحية')),
    ]

    export_id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
        verbose_name=_('معرف التصدير')
    )
    central_department = models.ForeignKey(
        'core.CentralDepartment',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='export_logs',
        verbose_name=_('الإدارة المركزية')
    )
    security_admin = models.ForeignKey(
        SecurityAdministration,
        on_delete=models.SET_NULL,
        null=True,
        related_name='export_logs',
        verbose_name=_('إدارة الأمن')
    )
    service_month    = models.CharField(max_length=7, verbose_name=_('شهر الخدمة'))  # YYYY-MM
    exported_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='exports',
        verbose_name=_('صدّر بواسطة')
    )
    file_hash        = models.CharField(max_length=64, verbose_name=_('Hash الملف'))
    row_uuids        = models.JSONField(verbose_name=_('UUIDs الصفوف'))
    editable_columns = models.JSONField(verbose_name=_('الأعمدة القابلة للتعديل'))
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name=_('الحالة')
    )

    class Meta:
        app_label = 'services'
        db_table = 'services_export_log'
        verbose_name = _('سجل تصدير')
        verbose_name_plural = _('سجلات التصدير')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['export_id']),
            models.Index(fields=['central_department', 'service_month']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        name = self.central_department.name if self.central_department else 'N/A'
        return f"{name} - {self.service_month}"


class RejectionLog(TimeStampedModel):
    """سجل الرفوضات - لتوثيق التغييرات المرفوضة"""

    staging_record = models.ForeignKey(
        StagingRecord,
        on_delete=models.CASCADE,
        related_name='rejections',
        verbose_name=_('السجل المؤقت')
    )
    central_department = models.ForeignKey(
        'core.CentralDepartment',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='rejections',
        verbose_name=_('الإدارة المركزية')
    )
    security_admin = models.ForeignKey(
        SecurityAdministration,
        on_delete=models.SET_NULL,
        null=True,
        related_name='rejections',
        verbose_name=_('إدارة الأمن')
    )
    service_month    = models.CharField(max_length=7, verbose_name=_('شهر الخدمة'))
    personnel = models.ForeignKey(
        PersonnelMaster,
        on_delete=models.PROTECT,
        related_name='rejections',
        verbose_name=_('الفرد')
    )
    proposed_status  = models.TextField(verbose_name=_('الحالة المقترحة'))
    rejection_reason = models.TextField(verbose_name=_('سبب الرفض'))
    rejected_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='rejections',
        verbose_name=_('رفض بواسطة')
    )
    rejected_at = models.DateTimeField(auto_now_add=True, verbose_name=_('تاريخ الرفض'))

    class Meta:
        app_label = 'services'
        db_table = 'services_rejection_log'
        verbose_name = _('سجل رفض')
        verbose_name_plural = _('سجلات الرفوضات')
        ordering = ['-rejected_at']
        indexes = [
            models.Index(fields=['central_department', 'service_month']),
            models.Index(fields=['rejected_at']),
        ]

    def __str__(self):
        return f"{self.personnel.military_number} - {self.service_month}"
