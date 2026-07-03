"""
Core Workflow Models - محرك الحالات والانتقالات
═══════════════════════════════════════════════════
قواعد انتقال الحالات الخدمية — يتم تعريفها من واجهة الأدمن.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from .base import TimeStampedModel


class StateTransitionRule(TimeStampedModel):
    """قواعد انتقال الحالات - محرك الحالات الديناميكي

    يسمح لمدير النظام بتعريف القواعد من الواجهة:
    - أي حالة يمكن الانتقال إليها من حالة معينة
    - هل يتطلب الانتقال مرفقاً رسمياً
    - هل يتطلب تفويضاً مزدوجاً
    - ما الحد الأدنى لأولوية الدور المطلوب
    """
    from_status = models.ForeignKey(
        'core.ServiceStatus',
        on_delete=models.CASCADE,
        related_name='transitions_from',
        verbose_name=_('من حالة')
    )
    to_status = models.ForeignKey(
        'core.ServiceStatus',
        on_delete=models.CASCADE,
        related_name='transitions_to',
        verbose_name=_('إلى حالة')
    )
    requires_document = models.BooleanField(
        default=False,
        verbose_name=_('يتطلب مرفق'),
        help_text=_('هل يجب رفع مستند رسمي لإتمام الانتقال')
    )
    required_document_types = models.JSONField(
        default=list,
        blank=True,
        verbose_name=_('أنواع المرفقات المطلوبة'),
        help_text=_('مثل: ["death_cert", "ministry_order", "medical_report"]')
    )
    requires_dual_auth = models.BooleanField(
        default=False,
        verbose_name=_('يتطلب تفويض مزدوج'),
        help_text=_('عمليات فائقة الحساسية مثل الاستشهاد والوفاة')
    )
    requires_status_change_form = models.BooleanField(
        default=False,
        verbose_name=_('يتطلب استمارة إثبات حالة'),
        help_text=_('مثل استمارة وفاة أو تقاعد')
    )
    min_role_priority = models.IntegerField(
        default=0,
        verbose_name=_('الحد الأدنى لأولوية الدور'),
        help_text=_('0=أي مستخدم مصرح, 50=رئيس خدمات, 100=مدير نظام')
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('نشط')
    )
    notes = models.TextField(
        blank=True,
        verbose_name=_('ملاحظات'),
        help_text=_('وصف القاعدة أو الإشارة للأمر الوزاري')
    )

    class Meta:
        db_table = 'core_state_transition_rule'
        verbose_name = _('قاعدة انتقال حالة')
        verbose_name_plural = _('قواعد انتقال الحالات')
        unique_together = [['from_status', 'to_status']]
        ordering = ['from_status', 'to_status']
        indexes = [
            models.Index(fields=['from_status']),
            models.Index(fields=['to_status']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.from_status.name} → {self.to_status.name}"
