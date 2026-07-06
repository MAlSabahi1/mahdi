from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from OpenSoftCoreV4.utils.abstract_models.soft_delete_model import SoftDeleteModel


class AudienceConditionVerification(SoftDeleteModel):

    fk_request = models.ForeignKey(
        'ServiceRequest',
        on_delete=models.CASCADE,
        related_name='condition_verifications',
        verbose_name=_('الطلب')
    )
    fk_prerequisite = models.ForeignKey(
        'ServicePrerequisite',
        on_delete=models.PROTECT,
        related_name='verifications',
        verbose_name=_('الشرط')
    )
    is_satisfied = models.BooleanField(
        default=False,
        verbose_name=_('تم تحقق الشرط')
    )
    verification_result = models.JSONField(
        default=dict,
        verbose_name=_('نتائج التحقق')
    )
    verified_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('وقت التحقق')
    )
    fk_verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='verified_conditions',
        verbose_name=_('تم التحقق بواسطة'),
        null=True,
        blank=True
    )
    notes = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('ملاحظات')
    )

    def __str__(self):
        status = "✓" if self.is_satisfied else "✗"
        return f'{self.fk_request.request_number} - {self.fk_prerequisite.name_ar} - {status}'

    class Meta:
        verbose_name = _('التحقق من شروط الجمهور')
        verbose_name_plural = _('سجلات التحقق من الشروط')
        ordering = ['fk_request', 'fk_prerequisite__order']
