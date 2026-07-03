"""
Infrastructure Models: Event Log
═════════════════════════════════
ServiceEventLog — سجل أحداث الخدمة (بديل الأعمدة الزمنية)
"""
import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from core.models import TimeStampedModel, SecurityAdministration
from systems.personnel.models import PersonnelMaster
from infra.storage.models import Document

User = get_user_model()


class ServiceEventLog(TimeStampedModel):
    """سجل الأحداث - بديل الأعمدة الزمنية"""
    personnel = models.ForeignKey(
        PersonnelMaster,
        on_delete=models.PROTECT,
        related_name='events',
        verbose_name=_('الفرد')
    )
    security_admin = models.ForeignKey(
        SecurityAdministration,
        on_delete=models.SET_NULL,
        null=True,
        related_name='service_events',
        verbose_name=_('إدارة الأمن')
    )
    event_date = models.DateField(verbose_name=_('تاريخ الحدث'))
    service_month = models.CharField(max_length=7, verbose_name=_('شهر الخدمة'))  # YYYY-MM
    field_name = models.CharField(max_length=50, verbose_name=_('اسم الحقل'))
    old_value = models.TextField(blank=True, verbose_name=_('القيمة القديمة'))
    new_value = models.TextField(verbose_name=_('القيمة الجديدة'))
    order_document = models.ForeignKey(
        Document,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='events',
        verbose_name=_('المستند')
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_events',
        verbose_name=_('أنشئ بواسطة')
    )

    class Meta:
        app_label = 'services'
        db_table = 'services_event_log'
        verbose_name = _('حدث')
        verbose_name_plural = _('الأحداث')
        ordering = ['-event_date', '-created_at']
        indexes = [
            models.Index(fields=['personnel', 'service_month']),
            models.Index(fields=['service_month', 'field_name']),
            models.Index(fields=['event_date']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['personnel', 'service_month', 'field_name', 'event_date'],
                name='unique_event_per_day'
            )
        ]

    def __str__(self):
        return f"{self.personnel.military_number} - {self.field_name} - {self.service_month}"
