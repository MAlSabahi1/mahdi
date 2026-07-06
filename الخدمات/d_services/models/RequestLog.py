"""
نموذج سجل الطلب - Request Log Model
لتسجيل جميع التغييرات على حالة وبيانات طلبات الخدمة
Enhanced with smart tracking fields, alerts, and performance indexes
"""
import uuid
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from OpenSoftCoreV4.utils.abstract_models.soft_delete_model import SoftDeleteModel

from d_services.choices.choices import LogActionChoice, LogSeverityChoice


class RequestLog(SoftDeleteModel):
    """
    سجل الطلب - Request Log
    لتسجيل جميع التغييرات على حالة وبيانات طلبات الخدمة
    """
    # ========================================
    # الحقول الأساسية - Core Fields
    # ========================================
    fk_request = models.ForeignKey(
        'ServiceRequest',
        on_delete=models.CASCADE,
        related_name='logs',
        verbose_name=_('الطلب')
    )
    action = models.CharField(
        max_length=30,
        choices=LogActionChoice.choices,
        verbose_name=_('الإجراء')
    )
    fk_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='request_logs',
        verbose_name=_('المستخدم'),
        null=True,
        blank=True
    )
    
    # ========================================
    # حقول التغييرات - Change Tracking Fields
    # ========================================
    changes = models.JSONField(
        default=dict,
        verbose_name=_('التغييرات'),
        help_text=_('ملخص التغييرات')
    )
    old_values = models.JSONField(
        default=dict,
        verbose_name=_('القيم السابقة')
    )
    new_values = models.JSONField(
        default=dict,
        verbose_name=_('القيم الجديدة')
    )
    affected_fields = models.JSONField(
        default=list,
        verbose_name=_('الحقول المتأثرة'),
        help_text=_('قائمة أسماء الحقول التي تم تغييرها')
    )
    
    # ========================================
    # حقول الحالة - Status Fields
    # ========================================
    old_status = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        verbose_name=_('الحالة السابقة')
    )
    new_status = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        verbose_name=_('الحالة الجديدة')
    )
    old_payment_status = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        verbose_name=_('حالة الدفع السابقة')
    )
    new_payment_status = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        verbose_name=_('حالة الدفع الجديدة')
    )
    
    # ========================================
    # حقول التتبع المتقدم - Advanced Tracking
    # ========================================
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('الوقت')
    )
    session_id = models.UUIDField(
        null=True,
        blank=True,
        verbose_name=_('معرف الجلسة'),
        help_text=_('UUID للجلسة لتجميع العمليات المرتبطة')
    )
    request_id = models.UUIDField(
        default=uuid.uuid4,
        verbose_name=_('معرف الطلب HTTP'),
        help_text=_('UUID فريد لكل عملية')
    )
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name=_('عنوان IP')
    )
    user_agent = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('معلومات المتصفح')
    )
    request_path = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        verbose_name=_('مسار الطلب')
    )
    request_method = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        verbose_name=_('نوع الطلب')
    )
    duration_ms = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_('مدة العملية (مللي ثانية)')
    )
    
    # ========================================
    # حقول الملاحظات والتنبيهات - Notes & Alerts
    # ========================================
    notes = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('ملاحظات')
    )
    severity = models.CharField(
        max_length=100,
        choices=LogSeverityChoice.choices,
        default=LogSeverityChoice.INFO,
        verbose_name=_('مستوى الأهمية')
    )
    is_flagged = models.BooleanField(
        default=False,
        verbose_name=_('تم التعليم'),
        help_text=_('هل يتطلب هذا السجل انتباه خاص؟')
    )
    flag_reason = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('سبب التعليم')
    )
    
    # ========================================
    # حقول المراجعة - Review Fields
    # ========================================
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_request_logs',
        verbose_name=_('تمت المراجعة بواسطة')
    )
    reviewed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('وقت المراجعة')
    )
    review_notes = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('ملاحظات المراجعة')
    )
    
    # ========================================
    # حقول السياق الإضافية - Additional Context
    # ========================================
    related_stage = models.ForeignKey(
        'RequestAction',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='related_logs',
        verbose_name=_('المرحلة ذات الصلة')
    )
    rollback_data = models.JSONField(
        default=dict,
        verbose_name=_('بيانات التراجع'),
        help_text=_('بيانات لإمكانية التراجع عن التغيير')
    )
    extra_data = models.JSONField(
        default=dict,
        verbose_name=_('بيانات إضافية'),
        help_text=_('أي بيانات إضافية مخصصة')
    )

    def __str__(self):
        return f'{self.fk_request.request_number} - {self.action} - {self.timestamp}'

    class Meta:
        verbose_name = _('سجل الطلب')
        verbose_name_plural = _('سجلات الطلبات')
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['fk_request', 'action', '-timestamp'], name='reqlog_req_action_ts_idx'),
            models.Index(fields=['fk_user', '-timestamp'], name='reqlog_user_ts_idx'),
            models.Index(fields=['old_status', 'new_status'], name='reqlog_status_change_idx'),
            models.Index(fields=['severity', '-timestamp'], name='reqlog_severity_ts_idx'),
            models.Index(fields=['is_flagged', '-timestamp'], name='reqlog_flagged_ts_idx'),
            models.Index(fields=['session_id'], name='reqlog_session_idx'),
            models.Index(fields=['-timestamp'], name='reqlog_ts_idx'),
        ]

    # ========================================
    # خصائص محسوبة - Computed Properties
    # ========================================
    @property
    def action_display(self):
        """عرض الإجراء بشكل مقروء"""
        return self.get_action_display()
    
    @property
    def severity_display(self):
        """عرض مستوى الأهمية بشكل مقروء"""
        return self.get_severity_display()
    
    @property
    def is_status_change(self):
        """هل هذا تغيير حالة؟"""
        return self.old_status != self.new_status and self.new_status is not None
    
    @property
    def is_critical(self):
        """هل السجل حرج؟"""
        return self.severity in [LogSeverityChoice.ERROR, LogSeverityChoice.CRITICAL]
    
    @property
    def needs_review(self):
        """هل يحتاج السجل للمراجعة؟"""
        return self.is_flagged and self.reviewed_at is None
    
    @property
    def changes_count(self):
        """عدد التغييرات"""
        return len(self.affected_fields) if self.affected_fields else 0

    # ========================================
    # دوال مساعدة - Helper Methods
    # ========================================
    def mark_reviewed(self, user, notes=None):
        """تعليم السجل كمراجع"""
        self.reviewed_by = user
        self.reviewed_at = timezone.now()
        if notes:
            self.review_notes = notes
        self.save(update_fields=['reviewed_by', 'reviewed_at', 'review_notes'])
    
    def flag(self, reason=None):
        """تعليم السجل للانتباه"""
        self.is_flagged = True
        if reason:
            self.flag_reason = reason
        self.save(update_fields=['is_flagged', 'flag_reason'])
    
    def unflag(self):
        """إزالة التعليم"""
        self.is_flagged = False
        self.flag_reason = None
        self.save(update_fields=['is_flagged', 'flag_reason'])
    
    def add_note(self, note, append=True):
        """إضافة ملاحظة"""
        if append and self.notes:
            self.notes = f"{self.notes}\n---\n{note}"
        else:
            self.notes = note
        self.save(update_fields=['notes'])

    @classmethod
    def get_recent_by_request(cls, request_id, limit=10):
        """جلب آخر السجلات لطلب معين"""
        return cls.objects.filter(
            fk_request_id=request_id,
            is_deleted=False
        ).select_related('fk_user', 'reviewed_by', 'related_stage')[:limit]
    
    @classmethod
    def get_status_changes(cls, request_id):
        """جلب تغييرات الحالة فقط"""
        return cls.objects.filter(
            fk_request_id=request_id,
            is_deleted=False
        ).exclude(
            new_status__isnull=True
        ).select_related('fk_user')
    
    @classmethod
    def get_timeline(cls, request_id):
        """جلب سجل الطلب كـ timeline"""
        return cls.objects.filter(
            fk_request_id=request_id,
            is_deleted=False
        ).select_related('fk_user', 'related_stage').order_by('timestamp')
    
    @classmethod
    def get_flagged(cls, request_id=None):
        """جلب السجلات المعلمة"""
        qs = cls.objects.filter(is_deleted=False, is_flagged=True)
        if request_id:
            qs = qs.filter(fk_request_id=request_id)
        return qs.select_related('fk_user', 'fk_request')
    
    @classmethod
    def get_by_action(cls, action, request_id=None, limit=50):
        """جلب السجلات حسب نوع الإجراء"""
        qs = cls.objects.filter(is_deleted=False, action=action)
        if request_id:
            qs = qs.filter(fk_request_id=request_id)
        return qs.select_related('fk_user', 'fk_request')[:limit]
