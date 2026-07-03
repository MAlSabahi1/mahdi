"""
Security Models - نماذج الأمان
═══════════════════════════════
النماذج الأمنية الخاصة بـ security app.

ملاحظة مهمة:
    Role, UserProfile, Permission → انتقلت إلى authorization/
    AuditLog, LoginAuditLog → انتقلت إلى audit/
    يمكن استيرادها من هنا للتوافق الخلفي.
"""
import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

User = get_user_model()

# ══════════════════════════════════════════════════════════════════════════════
# Re-exports — للتوافق الخلفي (RBAC انتقل إلى authorization)
# ══════════════════════════════════════════════════════════════════════════════
from infra.authorization.models import (  # noqa: F401
    Permission,
    Role,
    RolePermission,
    UserProfile,
    UserRole,
)
from infra.audit.models import AuditLog, LoginAuditLog  # noqa: F401

# ── Legacy: قائمة الصلاحيات القديمة (ستُستبدل بجدول Permission) ──
SYSTEM_PERMISSIONS = [
    ('view_personnel', 'عرض الأفراد'),
    ('edit_personnel_basic', 'تعديل البيانات الأساسية'),
    ('edit_personnel_status', 'تعديل الحالة الخدمية'),
    ('delete_personnel', 'حذف فرد (يتطلب تفويض مزدوج)'),
    ('export_sheet', 'تصدير كشوفات'),
    ('import_sheet', 'رفع كشوفات'),
    ('review_staging', 'مراجعة التغييرات المقترحة'),
    ('approve_change', 'اعتماد التغييرات'),
    ('reject_change', 'رفض التغييرات'),
    ('create_reconciliation', 'إنشاء مهام مطابقة'),
    ('resolve_reconciliation', 'حل اختلافات المطابقة'),
    ('close_month', 'إقفال الشهر'),
    ('override_lock', 'إلغاء إقفال الشهر (يتطلب تفويض مزدوج)'),
    ('view_audit_log', 'عرض سجل التدقيق'),
    ('verify_audit_signatures', 'التحقق من توقيعات التدقيق'),
    ('view_reports', 'عرض التقارير'),
    ('print_reports', 'طباعة التقارير'),
    ('export_reports', 'تصدير التقارير'),
    ('manage_users', 'إدارة المستخدمين والأدوار'),
    ('manage_roles', 'إنشاء وتعديل الأدوار'),
    ('manage_dictionaries', 'إدارة القواميس'),
    ('manage_settings', 'إدارة الإعدادات العامة'),
    ('manage_backups', 'إدارة النسخ الاحتياطي'),
    ('approve_dual_auth', 'الموافقة على طلبات التفويض المزدوج'),
    ('view_dual_auth', 'عرض طلبات التفويض المزدوج'),
    ('view_security_dashboard', 'عرض لوحة المراقبة الأمنية'),
    ('view_shadow_tables', 'عرض تاريخ الجداول'),
    ('request_correction', 'طلب تصحيح بيانات (نموذج 23)'),
    ('approve_correction', 'الموافقة على تصحيح بيانات'),
]

FOUR_EYES_PERMISSIONS = [
    'delete_personnel',
    'override_lock',
]


# ══════════════════════════════════════════════════════════════════════════════
# نماذج خاصة بـ security (تبقى هنا)
# ══════════════════════════════════════════════════════════════════════════════

class DualAuthorizationRequest(models.Model):
    """
    طلب تفويض مزدوج (Four-Eyes)

    العمليات فائقة الحساسية تتطلب موافقة مستخدمين اثنين.
    """
    ACTION_TYPE_CHOICES = [
        ('DELETE_PERSONNEL', _('حذف فرد نهائياً')),
        ('UNLOCK_MONTH', _('إلغاء إقفال شهر')),
        ('MODIFY_SUPER_ADMIN', _('تعديل صلاحيات مدير النظام')),
        ('CHANGE_ENCRYPTION_KEY', _('تغيير مفتاح التشفير')),
        ('BULK_DELETE', _('حذف جماعي')),
        ('RESTORE_BACKUP', _('استعادة نسخة احتياطية')),
    ]
    STATUS_CHOICES = [
        ('pending', _('قيد الانتظار')),
        ('approved', _('موافق عليه')),
        ('rejected', _('مرفوض')),
        ('expired', _('منتهي الصلاحية')),
        ('cancelled', _('ملغي')),
        ('executed', _('تم التنفيذ')),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    requester = models.ForeignKey(User, on_delete=models.CASCADE,
                                   related_name='dual_auth_requests', verbose_name=_('الطالب'))
    approver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='dual_auth_approvals', verbose_name=_('الموافق'))
    action_type = models.CharField(max_length=30, choices=ACTION_TYPE_CHOICES, verbose_name=_('نوع العملية'))
    target_object_type = models.CharField(max_length=100, verbose_name=_('نوع الكائن المستهدف'))
    target_object_id = models.CharField(max_length=100, verbose_name=_('معرف الكائن المستهدف'))
    request_data = models.JSONField(default=dict, verbose_name=_('بيانات الطلب'))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name=_('الحالة'))
    requested_at = models.DateTimeField(auto_now_add=True, verbose_name=_('تاريخ الطلب'))
    expires_at = models.DateTimeField(verbose_name=_('تنتهي في'))
    approved_at = models.DateTimeField(null=True, blank=True, verbose_name=_('تاريخ الموافقة'))
    executed_at = models.DateTimeField(null=True, blank=True, verbose_name=_('تاريخ التنفيذ'))
    rejection_reason = models.TextField(blank=True, verbose_name=_('سبب الرفض'))
    execution_result = models.JSONField(null=True, blank=True, verbose_name=_('نتيجة التنفيذ'))

    class Meta:
        db_table = 'security_dual_auth_request'
        verbose_name = _('طلب تفويض مزدوج')
        verbose_name_plural = _('طلبات التفويض المزدوج')
        ordering = ['-requested_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['action_type', 'status']),
            models.Index(fields=['requester', 'status']),
            models.Index(fields=['expires_at']),
        ]

    def __str__(self):
        return f"{self.get_action_type_display()} - {self.status}"

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timezone.timedelta(days=7)
        super().save(*args, **kwargs)

    def is_expired(self) -> bool:
        return timezone.now() > self.expires_at

    def can_be_approved_by(self, user) -> bool:
        if user.pk == self.requester_id:
            return False
        try:
            return user.profile.has_permission('approve_dual_auth')
        except Exception:
            return False


# ══════════════════════════════════════════════════════════════
# UserSession → انتقل إلى accounts.models.session.UserSession
# النسخة الجديدة تدعم JWT + Redis + Token Rotation
# ══════════════════════════════════════════════════════════════



class MetricsSnapshot(models.Model):
    """لقطة إحصائيات أمنية"""
    METRIC_TYPE_CHOICES = [
        ('login_failures', _('محاولات دخول فاشلة')),
        ('active_sessions', _('جلسات نشطة')),
        ('pending_dual_auth', _('طلبات تفويض معلقة')),
        ('shadow_table_sizes', _('أحجام جداول الظل')),
        ('atomic_transactions', _('إحصائيات المعاملات الذرية')),
        ('slow_queries', _('أبطأ الاستعلامات')),
        ('audit_integrity', _('سلامة سجل التدقيق')),
        ('system_health', _('صحة النظام العامة')),
    ]
    metric_type = models.CharField(max_length=30, choices=METRIC_TYPE_CHOICES, verbose_name=_('نوع المقياس'))
    data = models.JSONField(verbose_name=_('البيانات'))
    collected_at = models.DateTimeField(auto_now_add=True, verbose_name=_('تاريخ التجميع'))

    class Meta:
        db_table = 'security_metrics_snapshot'
        verbose_name = _('لقطة إحصائيات')
        verbose_name_plural = _('لقطات الإحصائيات')
        ordering = ['-collected_at']
        indexes = [
            models.Index(fields=['metric_type', 'collected_at']),
            models.Index(fields=['collected_at']),
        ]

    def __str__(self):
        return f"{self.get_metric_type_display()} - {self.collected_at}"


class SystemSetting(models.Model):
    """إعدادات النظام العامة"""
    key = models.CharField(max_length=100, unique=True, verbose_name=_('المفتاح'))
    value = models.JSONField(verbose_name=_('القيمة'))
    description = models.TextField(blank=True, verbose_name=_('الوصف'))
    category = models.CharField(max_length=50, default='general', choices=[
        ('general', _('عام')), ('security', _('الأمان')),
        ('import_export', _('التصدير والاستيراد')),
        ('notifications', _('الإشعارات')), ('performance', _('الأداء')),
    ], verbose_name=_('التصنيف'))
    is_sensitive = models.BooleanField(default=False, verbose_name=_('حساس'))
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                    related_name='updated_settings', verbose_name=_('عُدّل بواسطة'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('تاريخ التحديث'))

    class Meta:
        db_table = 'security_system_setting'
        verbose_name = _('إعداد النظام')
        verbose_name_plural = _('إعدادات النظام')
        ordering = ['category', 'key']
        indexes = [models.Index(fields=['category'])]

    def __str__(self):
        return f"{self.key} = {self.value}"

    @classmethod
    def get_value(cls, key: str, default=None):
        try:
            return cls.objects.get(key=key).value
        except cls.DoesNotExist:
            return default

    @classmethod
    def set_value(cls, key: str, value, user=None, description=''):
        obj, _ = cls.objects.update_or_create(
            key=key, defaults={'value': value, 'updated_by': user, 'description': description or key})
        return obj
