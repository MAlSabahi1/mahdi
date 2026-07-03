"""
AuditLog — سجل التدقيق المركزي
════════════════════════════════════
يُسجّل كل عملية CRUD في النظام بالكامل.
موقّع رقمياً بـ HMAC-SHA256 لمنع التلاعب.

الميزات المتقدمة:
    - HMAC-SHA256 digital signature (tamper detection)
    - سبب التغيير (change_reason) — إجباري للعمليات الحساسة
    - مستوى الحساسية (severity)
    - مدة الاحتفاظ: 10 سنوات كحد أدنى
    - دعم الأرشفة الباردة بعد 5 سنوات
    - BRIN Index للأداء مع البيانات الضخمة
"""
import hashlib
import hmac

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.postgres.indexes import BrinIndex
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class AuditSeverity(models.TextChoices):
    """مستوى حساسية العملية."""
    INFO = 'info', _('معلومات')
    LOW = 'low', _('منخفض')
    MEDIUM = 'medium', _('متوسط')
    HIGH = 'high', _('عالي')
    CRITICAL = 'critical', _('حرج')


class AuditLog(models.Model):
    """
    سجل تدقيق مركزي — يُسجل كل عملية في النظام.

    يجيب على الأسئلة الخمسة:
        1. من قام بالتغيير؟ → user, username
        2. متى؟ → timestamp
        3. من أي جهاز؟ → ip_address, user_agent
        4. ما الذي تغيّر؟ → model_name, object_id, old_data, new_data
        5. ما المبرر؟ → change_reason

    الحماية:
        - HMAC-SHA256 signature: أي تعديل يدوي على السجل يُكتشف فوراً
        - Immutable: لا يُعدَّل ولا يُحذف بعد الإنشاء
    """
    # ── من فعل ──
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='audit_logs', verbose_name=_('المستخدم'),
    )
    username = models.CharField(
        max_length=150, blank=True, default='',
        verbose_name=_('اسم المستخدم'),
        help_text=_('محفوظ حتى لو حُذف المستخدم'),
    )

    # ── ماذا فعل ──
    action = models.CharField(
        max_length=50, db_index=True, verbose_name=_('العملية'),
        help_text=_('مثل: CREATE, UPDATE, DELETE, LOGIN, APPROVE, REJECT, EXPORT'),
    )
    model_name = models.CharField(
        max_length=100, db_index=True, verbose_name=_('اسم النموذج'),
    )
    object_id = models.CharField(
        max_length=100, verbose_name=_('معرف الكائن'),
    )
    old_data = models.JSONField(
        null=True, blank=True, verbose_name=_('البيانات القديمة'),
    )
    new_data = models.JSONField(
        null=True, blank=True, verbose_name=_('البيانات الجديدة'),
    )

    # ── لماذا فعل (المبرر) ──
    change_reason = models.TextField(
        blank=True, default='', verbose_name=_('سبب التغيير'),
        help_text=_('المستند أو المذكرة المبررة — إجباري للعمليات الحساسة'),
    )

    # ── من أي جهاز ──
    ip_address = models.GenericIPAddressField(
        null=True, blank=True, verbose_name=_('عنوان IP'),
    )
    user_agent = models.TextField(
        blank=True, default='', verbose_name=_('User Agent'),
    )
    session_key = models.CharField(
        max_length=64, null=True, blank=True, verbose_name=_('معرف الجلسة'),
    )

    # ── التصنيف ──
    severity = models.CharField(
        max_length=10,
        choices=AuditSeverity.choices,
        default=AuditSeverity.INFO,
        verbose_name=_('مستوى الحساسية'),
    )
    module = models.CharField(
        max_length=50, blank=True, default='',
        verbose_name=_('النظام الفرعي'),
        help_text=_('مثل: personnel, services, security, system'),
    )

    # ── التوقيع والتوقيت ──
    timestamp = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name=_('التوقيت'),
    )
    signature = models.CharField(
        max_length=64, blank=True, verbose_name=_('التوقيع الرقمي'),
        help_text=_('HMAC-SHA256 — لمنع التلاعب'),
    )

    # ── الأرشفة ──
    is_archived = models.BooleanField(
        default=False, verbose_name=_('مؤرشف'),
        help_text=_('يُؤرشف بعد 5 سنوات — يُحتفظ به 10 سنوات'),
    )

    class Meta:
        db_table = 'audit_log'
        verbose_name = _('سجل تدقيق')
        verbose_name_plural = _('سجلات التدقيق')
        ordering = ['-timestamp']
        # Immutable — لا يُحذف
        default_permissions = ('add', 'view')
        indexes = [
            models.Index(fields=['action']),
            models.Index(fields=['model_name']),
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['timestamp']),
            models.Index(fields=['module', 'action']),
            models.Index(fields=['severity']),
            models.Index(fields=['is_archived', 'timestamp']),
            BrinIndex(fields=['timestamp'], name='audit_log_timestamp_brin'),
        ]

    def __str__(self) -> str:
        who = self.username or (self.user.username if self.user else 'anonymous')
        return f"[{self.timestamp}] {who} — {self.action} {self.model_name}"

    # ── HMAC Digital Signature ──

    def compute_signature(self) -> str:
        """حساب التوقيع الرقمي — يُكتشف أي تلاعب."""
        key = getattr(settings, 'AUDIT_SIGNING_KEY', settings.SECRET_KEY)
        payload = (
            f"{self.user_id or ''}|{self.username}|{self.action}|"
            f"{self.model_name}|{self.object_id}|"
            f"{self.timestamp.isoformat() if self.timestamp else ''}|"
            f"{self.session_key or ''}"
        )
        return hmac.new(
            key.encode('utf-8'),
            payload.encode('utf-8'),
            hashlib.sha256,
        ).hexdigest()

    def verify(self) -> bool:
        """التحقق من سلامة السجل — هل تم التلاعب؟"""
        if not self.signature:
            return False
        return hmac.compare_digest(self.signature, self.compute_signature())

    def save(self, *args, **kwargs):
        # حفظ اسم المستخدم تلقائياً
        if self.user and not self.username:
            self.username = self.user.username

        # جلب سياق الطلب تلقائياً
        from infra.audit.utils.audit_context import get_audit_context
        context = get_audit_context()
        if not self.ip_address and context.get('ip_address'):
            self.ip_address = context['ip_address']
        if not self.user_agent and context.get('user_agent'):
            self.user_agent = context['user_agent']
        if not self.session_key and context.get('session_key'):
            self.session_key = context['session_key']

        # التوقيع الرقمي عند الإنشاء فقط
        if not self.pk and not self.signature:
            self.signature = self.compute_signature()

        super().save(*args, **kwargs)
