"""
Security Admin - واجهة إدارة الأمان
═══════════════════════════════════════
⚠️ Role, UserProfile → authorization/admin.py
⚠️ UserSession → accounts/admin.py
⚠️ AuditLog, LoginAuditLog → audit/admin.py
"""
from django.contrib import admin
from .models import (
    DualAuthorizationRequest,
    MetricsSnapshot, SystemSetting
)


@admin.register(DualAuthorizationRequest)
class DualAuthorizationRequestAdmin(admin.ModelAdmin):
    list_display = [
        'action_type', 'status', 'requester', 'approver',
        'target_object_id', 'requested_at'
    ]
    list_filter = ['status', 'action_type']
    search_fields = ['target_object_id', 'requester__username']
    readonly_fields = [
        'requested_at', 'approved_at', 'executed_at',
    ]


@admin.register(MetricsSnapshot)
class MetricsSnapshotAdmin(admin.ModelAdmin):
    list_display = ['metric_type', 'collected_at']
    list_filter = ['metric_type']
    readonly_fields = ['collected_at']


@admin.register(SystemSetting)
class SystemSettingAdmin(admin.ModelAdmin):
    list_display = ['key', 'category', 'is_sensitive', 'updated_at']
    list_filter = ['category', 'is_sensitive']
    search_fields = ['key', 'description']
