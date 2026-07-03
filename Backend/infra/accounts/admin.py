"""
Accounts Admin — لوحة إدارة المستخدمين
═══════════════════════════════════════════
تسجيل النماذج في Django Admin.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from infra.accounts.models.user import User
from infra.accounts.models.session import UserSession
from infra.accounts.models.security import SecurityProfile


class SecurityProfileInline(admin.StackedInline):
    """عرض ملف الأمان داخل صفحة المستخدم."""
    model = SecurityProfile
    can_delete = False
    verbose_name = _('ملف الأمان')
    verbose_name_plural = _('ملف الأمان')
    readonly_fields = (
        'failed_login_attempts', 'is_locked', 'locked_until',
        'last_failed_ip', 'last_failed_at', 'password_changed_at',
        'last_known_ip', 'created_at', 'updated_at',
    )
    fieldsets = (
        (_('حالة القفل'), {
            'fields': (
                'is_locked', 'locked_until', 'failed_login_attempts',
                'last_failed_ip', 'last_failed_at',
            ),
        }),
        (_('كلمة المرور'), {
            'fields': (
                'password_changed_at', 'must_change_password',
            ),
        }),
        (_('آخر نشاط معروف'), {
            'fields': (
                'last_known_ip', 'last_known_user_agent',
            ),
        }),
    )


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """إدارة المستخدمين المخصصة."""
    inlines = [SecurityProfileInline]

    list_display = (
        'username', 'full_name', 'email', 'phone',
        'is_active', 'is_staff', 'last_login', 'created_at',
    )
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'created_at')
    search_fields = ('username', 'full_name', 'email', 'phone')
    ordering = ('-created_at',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('البيانات الشخصية'), {
            'fields': ('full_name', 'email', 'phone'),
        }),
        (_('الصلاحيات'), {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions',
            ),
        }),
        (_('التواريخ'), {
            'fields': ('last_login', 'date_joined', 'created_at', 'updated_at'),
        }),
    )
    readonly_fields = ('created_at', 'updated_at', 'last_login', 'date_joined')

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'full_name', 'phone', 'email', 'password1', 'password2'),
        }),
    )


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    """عرض الجلسات في لوحة الإدارة."""
    list_display = (
        'user', 'device_name', 'browser', 'os',
        'ip_address', 'is_active', 'last_activity', 'created_at',
    )
    list_filter = ('is_active', 'os', 'browser', 'created_at')
    search_fields = ('user__username', 'user__full_name', 'ip_address', 'device_name')
    readonly_fields = (
        'session_id', 'refresh_token_hash', 'user_agent',
        'created_at', 'revoked_at', 'revoke_reason',
    )
    ordering = ('-last_activity',)

    fieldsets = (
        (_('الجلسة'), {
            'fields': ('user', 'session_id', 'is_active', 'revoked_at', 'revoke_reason'),
        }),
        (_('الجهاز'), {
            'fields': ('device_name', 'browser', 'os', 'ip_address', 'user_agent'),
        }),
        (_('التوقيت'), {
            'fields': ('last_activity', 'expires_at', 'created_at'),
        }),
        (_('الأمان'), {
            'fields': ('refresh_token_hash',),
            'classes': ('collapse',),
        }),
    )

    def has_add_permission(self, request):
        return False


@admin.register(SecurityProfile)
class SecurityProfileAdmin(admin.ModelAdmin):
    """عرض ملفات الأمان في لوحة الإدارة."""
    list_display = (
        'user', 'is_locked', 'failed_login_attempts',
        'must_change_password', 'last_known_ip', 'updated_at',
    )
    list_filter = ('is_locked', 'must_change_password')
    search_fields = ('user__username', 'user__full_name', 'last_known_ip')
    readonly_fields = (
        'failed_login_attempts', 'last_failed_ip', 'last_failed_at',
        'password_changed_at', 'last_known_ip', 'last_known_user_agent',
        'created_at', 'updated_at',
    )

    actions = ['unlock_accounts']

    @admin.action(description=_('فك قفل الحسابات المحددة'))
    def unlock_accounts(self, request, queryset):
        for profile in queryset.filter(is_locked=True):
            profile.unlock()
        self.message_user(request, _('تم فك قفل الحسابات المحددة.'))
