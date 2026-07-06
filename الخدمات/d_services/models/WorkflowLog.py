"""
نموذج سجل سير العمل - Workflow Log Model
لتسجيل انتقال الطلب بين مراحل سير العمل والإجراءات المتخذة
Enhanced with SLA tracking, performance metrics, and alerts
"""
import uuid
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from OpenSoftCoreV4.utils.abstract_models.soft_delete_model import SoftDeleteModel

from d_services.choices.choices import LogSeverityChoice, SLAStatusChoice, LogActionChoice


class WorkflowLog(SoftDeleteModel):
    """
    سجل سير العمل - Workflow Log
    لتسجيل انتقال الطلب بين مراحل سير العمل والإجراءات المتخذة
    """
    # ========================================
    # الحقول الأساسية - Core Fields
    # ========================================
    fk_request = models.ForeignKey(
        'ServiceRequest',
        on_delete=models.CASCADE,
        related_name='workflow_logs',
        verbose_name=_('الطلب')
    )
    fk_from_stage = models.ForeignKey(
        'ServiceWorkflowStep',
        on_delete=models.PROTECT,
        related_name='outgoing_logs',
        verbose_name=_('من المرحلة'),
        null=True,
        blank=True
    )
    fk_to_stage = models.ForeignKey(
        'ServiceWorkflowStep',
        on_delete=models.PROTECT,
        related_name='incoming_logs',
        verbose_name=_('إلى المرحلة'),
        null=True,
        blank=True
    )
    fk_request_action = models.ForeignKey(
        'RequestAction',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='workflow_logs',
        verbose_name=_('إجراء الطلب')
    )
    fk_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='workflow_logs',
        verbose_name=_('المستخدم'),
        null=True,
        blank=True
    )
    
    # ========================================
    # حقول الإجراء - Action Fields
    # ========================================
    action = models.CharField(
        max_length=30,
        choices=LogActionChoice.choices,
        default=LogActionChoice.MOVE,
        verbose_name=_('نوع الإجراء')
    )
    action_taken = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_('الإجراء المتخذ')
    )
    
    # ========================================
    # حقول التوقيت - Timing Fields
    # ========================================
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('الوقت')
    )
    session_id = models.UUIDField(
        null=True,
        blank=True,
        verbose_name=_('معرف الجلسة')
    )
    started_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('وقت بدء المرحلة')
    )
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('وقت إكمال المرحلة')
    )
    duration_ms = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_('مدة العملية (مللي ثانية)')
    )
    
    # ========================================
    # حقول SLA والأداء - SLA & Performance Fields
    # ========================================
    sla_status = models.CharField(
        max_length=100,
        choices=SLAStatusChoice.choices,
        default=SLAStatusChoice.NOT_APPLICABLE,
        verbose_name=_('حالة SLA')
    )
    expected_duration_hours = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name=_('المدة المتوقعة (ساعات)')
    )
    actual_duration_hours = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_('المدة الفعلية (ساعات)')
    )
    is_overdue = models.BooleanField(
        default=False,
        verbose_name=_('متأخر'),
        help_text=_('هل تجاوزت المرحلة الوقت المحدد؟')
    )
    overdue_hours = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_('ساعات التأخير')
    )
    
    # ========================================
    # حقول الملاحظات والتنبيهات - Notes & Alerts
    # ========================================
    notes = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('ملاحظات')
    )
    decision_notes = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('ملاحظات القرار'),
        help_text=_('تفاصيل القرار المتخذ')
    )
    severity = models.CharField(
        max_length=100,
        choices=LogSeverityChoice.choices,
        default=LogSeverityChoice.INFO,
        verbose_name=_('مستوى الأهمية')
    )
    is_flagged = models.BooleanField(
        default=False,
        verbose_name=_('تم التعليم')
    )
    flag_reason = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('سبب التعليم')
    )
    
    # ========================================
    # حقول البيانات الإضافية - Additional Data
    # ========================================
    input_data = models.JSONField(
        default=dict,
        verbose_name=_('بيانات المدخلات'),
        help_text=_('البيانات التي تم إدخالها في هذه المرحلة')
    )
    output_data = models.JSONField(
        default=dict,
        verbose_name=_('بيانات المخرجات'),
        help_text=_('البيانات الناتجة من هذه المرحلة')
    )
    extra_data = models.JSONField(
        default=dict,
        verbose_name=_('بيانات إضافية')
    )

    def __str__(self):
        return f'{self.fk_request.request_number} - {self.fk_from_stage} → {self.fk_to_stage}'

    class Meta:
        verbose_name = _('سجل سير العمل')
        verbose_name_plural = _('سجلات سير العمل')
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['fk_request', '-timestamp'], name='wflog_req_ts_idx'),
            models.Index(fields=['fk_user', '-timestamp'], name='wflog_user_ts_idx'),
            models.Index(fields=['is_overdue', 'sla_status'], name='wflog_sla_idx'),
            models.Index(fields=['action', '-timestamp'], name='wflog_action_ts_idx'),
            models.Index(fields=['is_flagged', '-timestamp'], name='wflog_flagged_ts_idx'),
            models.Index(fields=['session_id'], name='wflog_session_idx'),
        ]

    # ========================================
    # خصائص محسوبة - Computed Properties
    # ========================================
    @property
    def action_display(self):
        """عرض الإجراء بشكل مقروء"""
        return self.get_action_display()
    
    @property
    def sla_status_display(self):
        """عرض حالة SLA بشكل مقروء"""
        return self.get_sla_status_display()
    
    @property
    def stage_duration(self):
        """مدة المرحلة"""
        if self.started_at and self.completed_at:
            delta = self.completed_at - self.started_at
            return delta.total_seconds() / 3600  # hours
        return None
    
    @property
    def is_transition(self):
        """هل هذا انتقال بين مراحل؟"""
        return self.fk_from_stage != self.fk_to_stage
    
    @property
    def from_stage_name(self):
        """اسم المرحلة المصدر"""
        if self.fk_from_stage and hasattr(self.fk_from_stage, 'fk_stage'):
            return self.fk_from_stage.fk_stage.name_ar
        return None
    
    @property
    def to_stage_name(self):
        """اسم المرحلة الهدف"""
        if self.fk_to_stage and hasattr(self.fk_to_stage, 'fk_stage'):
            return self.fk_to_stage.fk_stage.name_ar
        return None

    # ========================================
    # دوال مساعدة - Helper Methods
    # ========================================
    def calculate_sla_status(self):
        """حساب حالة SLA"""
        if not self.expected_duration_hours or not self.actual_duration_hours:
            return SLAStatusChoice.NOT_APPLICABLE
        
        if self.actual_duration_hours <= self.expected_duration_hours:
            return SLAStatusChoice.ON_TIME
        elif self.actual_duration_hours <= self.expected_duration_hours * 1.25:
            return SLAStatusChoice.AT_RISK
        else:
            return SLAStatusChoice.OVERDUE
    
    def mark_overdue(self, hours=None):
        """تعليم المرحلة كمتأخرة"""
        self.is_overdue = True
        if hours:
            self.overdue_hours = hours
        self.sla_status = SLAStatusChoice.OVERDUE
        self.save(update_fields=['is_overdue', 'overdue_hours', 'sla_status'])
    
    def flag(self, reason=None):
        """تعليم السجل للانتباه"""
        self.is_flagged = True
        if reason:
            self.flag_reason = reason
        self.save(update_fields=['is_flagged', 'flag_reason'])
    
    def add_note(self, note, append=True):
        """إضافة ملاحظة"""
        if append and self.notes:
            self.notes = f"{self.notes}\n---\n{note}"
        else:
            self.notes = note
        self.save(update_fields=['notes'])

    @classmethod
    def get_timeline(cls, request_id):
        """جلب سجل سير العمل كـ timeline"""
        return cls.objects.filter(
            fk_request_id=request_id,
            is_deleted=False
        ).select_related(
            'fk_user', 'fk_from_stage', 'fk_to_stage', 'fk_request_action'
        ).order_by('timestamp')
    
    @classmethod
    def get_overdue(cls, request_id=None):
        """جلب المراحل المتأخرة"""
        qs = cls.objects.filter(is_deleted=False, is_overdue=True)
        if request_id:
            qs = qs.filter(fk_request_id=request_id)
        return qs.select_related('fk_user', 'fk_request', 'fk_from_stage', 'fk_to_stage')
    
    @classmethod
    def get_by_stage(cls, stage_id, limit=50):
        """جلب السجلات لمرحلة معينة"""
        return cls.objects.filter(
            is_deleted=False
        ).filter(
            models.Q(fk_from_stage_id=stage_id) | models.Q(fk_to_stage_id=stage_id)
        ).select_related('fk_user', 'fk_request')[:limit]
    
    @classmethod
    def get_performance_summary(cls, request_id):
        """ملخص أداء المراحل لطلب معين"""
        logs = cls.objects.filter(
            fk_request_id=request_id,
            is_deleted=False,
            actual_duration_hours__isnull=False
        ).values('fk_to_stage__fk_stage__name_ar').annotate(
            avg_duration=models.Avg('actual_duration_hours'),
            max_duration=models.Max('actual_duration_hours'),
            overdue_count=models.Count('id', filter=models.Q(is_overdue=True))
        )
        return list(logs)
