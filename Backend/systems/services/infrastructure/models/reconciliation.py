"""
Infrastructure Models: Reconciliation
══════════════════════════════════════
ReconciliationTask — مهمة المطابقة الشهرية
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from core.models import TimeStampedModel, SecurityAdministration

User = get_user_model()


class ReconciliationTask(TimeStampedModel):
    """مهمة المطابقة"""

    TASK_TYPE_CHOICES = [
        ('attendance',    _('مطابقة حضور')),
        ('payroll',       _('مطابقة راتب')),
        ('qualification', _('مطابقة مؤهلات')),
    ]

    STATUS_CHOICES = [
        ('pending',   _('قيد التنفيذ')),
        ('completed', _('مكتمل')),
        ('failed',    _('فشل')),
    ]

    name = models.CharField(max_length=200, verbose_name=_('اسم المهمة'))
    security_admin = models.ForeignKey(
        SecurityAdministration,
        on_delete=models.SET_NULL,
        null=True,
        related_name='reconciliation_tasks',
        verbose_name=_('إدارة الأمن')
    )
    task_type = models.CharField(
        max_length=20,
        choices=TASK_TYPE_CHOICES,
        verbose_name=_('نوع المطابقة')
    )
    source_file = models.FileField(
        upload_to='reconciliation/%Y/%m/',
        verbose_name=_('ملف المصدر')
    )
    key_field = models.CharField(max_length=50, verbose_name=_('حقل الربط'))
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name=_('الحالة')
    )
    result = models.JSONField(null=True, blank=True, verbose_name=_('النتيجة'))
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='reconciliation_tasks',
        verbose_name=_('أنشئ بواسطة')
    )

    class Meta:
        app_label = 'services'
        db_table = 'services_reconciliation_task'
        verbose_name = _('مهمة مطابقة')
        verbose_name_plural = _('مهام المطابقة')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['task_type']),
        ]

    def __str__(self):
        return f"{self.name} - {self.status}"
