"""
نموذج مزامنة طلبات الخدمة - Service Request Sync Model
تتبع حالة مزامنة كل طلب لكل نظام (مدارس/جامعات/معاهد)
نفس نمط ObjectSync في الكور
"""
from django.db import models
from django.utils.translation import gettext_lazy as _

from OpenSoftCoreV4.utils.abstract_models.soft_delete_model import SoftDeleteModel


class ServiceRequestSyncStatus(models.IntegerChoices):
    """حالات المزامنة"""
    NOT_SYNCED = 1, _("لم تتم المزامنة")
    SYNCED = 2, _("تمت المزامنة")
    MODIFIED_AFTER_SYNC = 3, _("تم التعديل بعد المزامنة")
    CANNOT_SYNC = 4, _("لا يمكن المزامنة لهذا النظام")
    FAILED = 5, _("فشلت المزامنة")


class ServiceRequestSync(SoftDeleteModel):
    """
    تتبع حالة مزامنة طلب خدمة لكل نظام فرعي
    يُنشأ تلقائياً عند إنشاء طلب في البوابة
    """
    fk_service_request = models.OneToOneField(
        'd_services.ServiceRequest',
        on_delete=models.CASCADE,
        related_name='sync_status',
        verbose_name=_('الطلب')
    )
    portal_request_id = models.CharField(
        max_length=100,
        db_index=True,
        verbose_name=_('معرف الطلب في البوابة'),
        help_text=_('المعرف الأصلي للطلب في نظام البوابة')
    )

    # ── Per-system sync status ────────────────────────────────────────
    school = models.PositiveSmallIntegerField(
        choices=ServiceRequestSyncStatus.choices,
        default=ServiceRequestSyncStatus.CANNOT_SYNC,
        verbose_name=_('نظام المدارس'),
    )
    university = models.PositiveSmallIntegerField(
        choices=ServiceRequestSyncStatus.choices,
        default=ServiceRequestSyncStatus.CANNOT_SYNC,
        verbose_name=_('نظام الجامعات'),
    )
    institute = models.PositiveSmallIntegerField(
        choices=ServiceRequestSyncStatus.choices,
        default=ServiceRequestSyncStatus.CANNOT_SYNC,
        verbose_name=_('نظام المعاهد'),
    )

    # ── Per-system error messages ─────────────────────────────────────
    school_error = models.TextField(
        blank=True, default='',
        verbose_name=_('خطأ نظام المدارس'),
    )
    university_error = models.TextField(
        blank=True, default='',
        verbose_name=_('خطأ نظام الجامعات'),
    )
    institute_error = models.TextField(
        blank=True, default='',
        verbose_name=_('خطأ نظام المعاهد'),
    )

    last_sync_attempt = models.DateTimeField(
        null=True, blank=True,
        verbose_name=_('آخر محاولة مزامنة'),
    )

    class Meta:
        verbose_name = _('مزامنة طلب خدمة')
        verbose_name_plural = _('مزامنة طلبات الخدمة')
        indexes = [
            models.Index(fields=['school'], name='idx_srs_school'),
            models.Index(fields=['university'], name='idx_srs_university'),
            models.Index(fields=['institute'], name='idx_srs_institute'),
        ]

    def __str__(self):
        return f'Sync({self.portal_request_id})'
