"""
Authorization Admin — لوحة إدارة كل طبقات الصلاحيات
═══════════════════════════════════════════════════════
"""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from infra.authorization.models.permission import Permission
from infra.authorization.models.permission_group import PermissionGroup
from infra.authorization.models.role import Role, RolePermission
from infra.authorization.models.user_role import UserRole
from infra.authorization.models.user_profile import UserProfile
from infra.authorization.models.field_permission import FieldPermission
from infra.authorization.models.record_acl import RecordACL
from infra.authorization.models.policy import AccessPolicy
from infra.authorization.models.delegation import Delegation
from infra.authorization.models.emergency_access import EmergencyAccess


# ── Inlines ──

class RolePermissionInline(admin.TabularInline):
    model = RolePermission
    extra = 1
    autocomplete_fields = ['permission']
    readonly_fields = ('granted_by', 'created_at')


class UserRoleInline(admin.TabularInline):
    model = UserRole
    fk_name = 'user'
    extra = 0
    autocomplete_fields = ['role']
    readonly_fields = ('assigned_by', 'assigned_at')


# ── الطبقة 3: مجموعات الصلاحيات ──

@admin.register(PermissionGroup)
class PermissionGroupAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'icon', 'display_order', 'is_active', 'get_count')
    list_filter = ('is_active',)
    search_fields = ('code', 'name')
    ordering = ('display_order',)

    def get_count(self, obj):
        return obj.permissions.filter(is_active=True).count()
    get_count.short_description = _('عدد الصلاحيات')


# ── الطبقة 1: الصلاحيات ──

@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('code', 'label', 'module', 'action', 'scope', 'category', 'is_active')
    list_filter = ('module', 'category', 'is_active', 'is_system')
    search_fields = ('code', 'label', 'description')
    ordering = ('module', 'action', 'scope')
    readonly_fields = ('code',)
    # ملاحظة: حقل group سيُضاف لنموذج Permission في migration لاحقة

    fieldsets = (
        (None, {'fields': ('module', 'action', 'scope', 'code')}),
        (_('الوصف'), {'fields': ('label', 'description', 'category')}),
        (_('الإعدادات'), {'fields': ('is_active', 'is_system', 'requires_dual_auth')}),
    )


# ── الطبقة 2: الأدوار ──

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'priority', 'is_active', 'is_system_role', 'permissions_count')
    list_filter = ('is_active', 'is_system_role')
    search_fields = ('name', 'code', 'description')
    inlines = [RolePermissionInline]
    ordering = ('-priority', 'name')

    def permissions_count(self, obj):
        return obj.permissions.count()
    permissions_count.short_description = _('عدد الصلاحيات')


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'is_active', 'assigned_by', 'assigned_at', 'expires_at')
    list_filter = ('is_active', 'role')
    search_fields = ('user__username', 'user__full_name', 'role__name')
    autocomplete_fields = ['user', 'role']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'security_admin', 'central_department', 'branch', 'district_police')
    list_filter = ('role', 'security_admin')
    search_fields = ('user__username', 'user__full_name')
    autocomplete_fields = ['user', 'role', 'security_admin', 'central_department', 'branch', 'district_police', 'division', 'unit']


# ── الطبقة 6: صلاحيات الحقول ──

@admin.register(FieldPermission)
class FieldPermissionAdmin(admin.ModelAdmin):
    list_display = ('module', 'field_name', 'label', 'view_permission', 'edit_permission', 'is_sensitive', 'is_active')
    list_filter = ('module', 'is_sensitive', 'is_active')
    search_fields = ('field_name', 'label')
    ordering = ('module', 'field_name')


# ── الطبقة 5: قيود السجلات ──

@admin.register(RecordACL)
class RecordACLAdmin(admin.ModelAdmin):
    list_display = ('content_type', 'object_id', 'access_type', 'target_user', 'target_role', 'is_active', 'expires_at')
    list_filter = ('access_type', 'is_active', 'content_type')
    search_fields = ('object_id', 'reason')
    autocomplete_fields = ['target_user', 'target_role']


# ── الطبقة 8: السياسات ──

@admin.register(AccessPolicy)
class AccessPolicyAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'permission_code', 'effect', 'priority', 'is_active')
    list_filter = ('effect', 'is_active')
    search_fields = ('name', 'code', 'permission_code')
    ordering = ('-priority',)


# ── الطبقة 11: التفويضات ──

@admin.register(Delegation)
class DelegationAdmin(admin.ModelAdmin):
    list_display = ('delegator', 'delegate', 'role', 'status', 'starts_at', 'ends_at')
    list_filter = ('status',)
    search_fields = ('delegator__username', 'delegate__username', 'reason')
    autocomplete_fields = ['delegator', 'delegate', 'role']


# ── الطبقة 12: الوصول الطارئ ──

@admin.register(EmergencyAccess)
class EmergencyAccessAdmin(admin.ModelAdmin):
    list_display = ('user', 'granted_by', 'status', 'reason', 'granted_at', 'expires_at', 'needs_review')
    list_filter = ('status',)
    search_fields = ('user__username', 'reason')
    autocomplete_fields = ['user', 'granted_by']
    readonly_fields = ('granted_at',)
