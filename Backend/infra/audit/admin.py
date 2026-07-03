"""
Audit Admin — لوحة إدارة التدقيق
"""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from infra.audit.models.audit_log import AuditLog
from infra.audit.models.login_audit import LoginAuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = (
        'timestamp', 'username', 'action', 'model_name', 'object_id',
        'severity', 'module', 'is_verified_display',
    )
    list_filter = ('action', 'severity', 'module', 'is_archived')
    search_fields = ('username', 'model_name', 'object_id', 'change_reason')
    date_hierarchy = 'timestamp'
    ordering = ('-timestamp',)
    readonly_fields = (
        'user', 'username', 'action', 'model_name', 'object_id',
        'old_data', 'new_data', 'change_reason', 'ip_address',
        'user_agent', 'session_key', 'severity', 'module',
        'timestamp', 'signature', 'is_archived',
    )

    # Immutable — لا إضافة ولا حذف من الأدمن
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def is_verified_display(self, obj):
        return '✅' if obj.verify() else '⚠️'
    is_verified_display.short_description = _('سليم')


@admin.register(LoginAuditLog)
class LoginAuditLogAdmin(admin.ModelAdmin):
    list_display = (
        'timestamp', 'username_attempted', 'action', 'ip_address',
        'failure_reason',
    )
    list_filter = ('action', 'failure_reason')
    search_fields = ('username_attempted', 'ip_address')
    date_hierarchy = 'timestamp'
    ordering = ('-timestamp',)
    readonly_fields = (
        'user', 'username_attempted', 'action', 'ip_address',
        'user_agent', 'failure_reason', 'extra_data',
        'session_key', 'geo_location', 'timestamp',
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
