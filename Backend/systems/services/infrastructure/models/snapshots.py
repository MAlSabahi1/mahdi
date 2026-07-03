"""
Infrastructure Models: Snapshots
══════════════════════════════════
MonthlySnapshot + DirectorateCompliance — اللقطات الشهرية ومتابعة الالتزام
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import TimeStampedModel, SecurityAdministration


class MonthlySnapshot(TimeStampedModel):
    """اللقطة الشهرية"""
    security_admin = models.ForeignKey(
        SecurityAdministration,
        on_delete=models.SET_NULL,
        null=True,
        related_name='monthly_snapshots',
        verbose_name=_('إدارة الأمن')
    )
    central_department = models.ForeignKey(
        'core.CentralDepartment',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='monthly_snapshots',
        verbose_name=_('الإدارة المركزية')
    )
    service_month = models.CharField(
        max_length=7,
        verbose_name=_('شهر الخدمة')
    )  # YYYY-MM
    data   = models.JSONField(verbose_name=_('البيانات'))
    locked = models.BooleanField(default=False, verbose_name=_('مقفل'))

    class Meta:
        app_label = 'services'
        db_table = 'services_monthly_snapshot'
        verbose_name = _('لقطة شهرية')
        verbose_name_plural = _('اللقطات الشهرية')
        ordering = ['-service_month']
        constraints = [
            models.UniqueConstraint(
                fields=['security_admin', 'central_department', 'service_month'],
                name='unique_snapshot_per_org_month'
            )
        ]
        indexes = [
            models.Index(fields=['service_month']),
            models.Index(fields=['locked']),
        ]

    def __str__(self):
        return f"Snapshot {self.service_month} - {'🔒' if self.locked else '🔓'}"


class DirectorateCompliance(TimeStampedModel):
    """متابعة التزام الإدارات"""

    central_department = models.ForeignKey(
        'core.CentralDepartment',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='compliance_records',
        verbose_name=_('الإدارة المركزية')
    )
    security_admin = models.ForeignKey(
        SecurityAdministration,
        on_delete=models.SET_NULL,
        null=True,
        related_name='compliance_records',
        verbose_name=_('إدارة الأمن')
    )
    service_month             = models.CharField(max_length=7, verbose_name=_('شهر الخدمة'))
    submitted_at              = models.DateTimeField(null=True, blank=True, verbose_name=_('تاريخ التسليم'))
    error_count               = models.IntegerField(default=0,   verbose_name=_('عدد الأخطاء'))
    rejected_changes_count    = models.IntegerField(default=0,   verbose_name=_('عدد التغييرات المرفوضة'))
    late_days                 = models.IntegerField(default=0,   verbose_name=_('أيام التأخير'))
    quality_score             = models.IntegerField(default=100, verbose_name=_('درجة الجودة'))

    class Meta:
        app_label = 'services'
        db_table = 'services_directorate_compliance'
        verbose_name = _('التزام إدارة')
        verbose_name_plural = _('التزام الإدارات')
        ordering = ['-service_month', 'central_department']
        constraints = [
            models.UniqueConstraint(
                fields=['security_admin', 'central_department', 'service_month'],
                name='unique_compliance_per_org_month'
            )
        ]
        indexes = [
            models.Index(fields=['service_month']),
            models.Index(fields=['quality_score']),
        ]

    def __str__(self):
        name = self.central_department.name if self.central_department else 'N/A'
        return f"{name} - {self.service_month} - {self.quality_score}%"
