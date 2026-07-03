"""
Authorization Admin — لوحة إدارة الصلاحيات والأدوار
═══════════════════════════════════════════════════════
"""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from infra.authorization.models.permission import Permission
from infra.authorization.models.role import Role, RolePermission
from infra.authorization.models.user_role import UserRole
from infra.authorization.models.user_profile import UserProfile


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


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('code', 'label', 'module', 'action', 'scope', 'category', 'is_active')
    list_filter = ('module', 'category', 'is_active', 'is_system')
    search_fields = ('code', 'label', 'description')
    ordering = ('module', 'action', 'scope')
    readonly_fields = ('code',)

    fieldsets = (
        (None, {'fields': ('module', 'action', 'scope', 'code')}),
        (_('الوصف'), {'fields': ('label', 'description', 'category')}),
        (_('الإعدادات'), {'fields': ('is_active', 'is_system', 'requires_dual_auth')}),
    )


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
