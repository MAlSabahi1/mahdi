"""
Security Permissions — Legacy RBAC/ABAC Engine
════════════════════════════════════════════════
⚠️  محرك الصلاحيات الرئيسي انتقل إلى authorization/ app.
    هذا الملف يُعيد تصدير الواجهات للتوافق الخلفي.

    الاستخدام الجديد:
        from infra.authorization.services.permission_service import PermissionService
        from infra.authorization.mixins.permission_mixin import ServicePermission
"""
import warnings

# ══════════════════════════════════════════════════════════════
# Re-exports من authorization (للتوافق الخلفي)
# ══════════════════════════════════════════════════════════════

from rest_framework import permissions as drf_permissions
from django.core.exceptions import PermissionDenied
from django.db.models import QuerySet


def get_user_profile(user):
    """جلب ملف المستخدم — يستخدم authz_profile."""
    try:
        return user.authz_profile
    except Exception:
        return None


def has_permission(user, permission_code: str) -> bool:
    """
    فحص صلاحية المستخدم (RBAC).
    ⚠️ يُفضل استخدام: PermissionService.has_permission(user, code)
    """
    if not user or not user.is_authenticated:
        return False
    try:
        if hasattr(user, 'security_profile') and user.security_profile.check_lock_state():
            return False
    except Exception:
        pass
    if user.is_superuser:
        return True

    from infra.authorization.services.permission_service import PermissionService
    return PermissionService.has_permission(user, permission_code)


def has_directorate_scope(user, directorate_id: int) -> bool:
    """
    فحص النطاق: هل المستخدم يملك حق الوصول لإدارة أمن محافظة معينة؟
    directorate_id هنا = security_administration_id في النموذج الجديد.
    """
    if not user or not user.is_authenticated:
        return False
    try:
        if hasattr(user, 'security_profile') and user.security_profile.check_lock_state():
            return False
    except Exception:
        pass
    if user.is_superuser:
        return True
    profile = get_user_profile(user)
    if not profile:
        return False
    # UserProfile الجديد يستخدم security_admin بدلاً من directorate
    return profile.has_security_admin_scope(directorate_id)


# للتوافق الخلفي
has_department_scope = has_directorate_scope


def has_governorate_scope(user, governorate_id: int) -> bool:
    """فحص النطاق: هل المستخدم يملك حق الوصول لمحافظة معينة."""
    if user.is_superuser:
        return True
    profile = get_user_profile(user)
    if not profile:
        return False
    # supervises_all في UserProfile الجديد بدلاً من supervises_all_directorates
    if getattr(profile, 'supervises_all', False):
        return True
    return getattr(profile, 'security_admin_id', None) is None


def has_permission_for_directorate(user, permission_code: str,
                                   directorate_id: int) -> bool:
    """فحص مركب: الصلاحية + النطاق معاً."""
    return (has_permission(user, permission_code) and
            has_directorate_scope(user, directorate_id))


# للتوافق الخلفي
has_permission_for_department = has_permission_for_directorate


def check_permission(user, permission_code: str):
    """فحص صلاحية مع رمي استثناء عند الفشل."""
    if not has_permission(user, permission_code):
        raise PermissionDenied(f'ليس لديك صلاحية: {permission_code}')


def check_permission_for_directorate(user, permission_code: str,
                                     directorate_id: int):
    """فحص مركب مع رمي استثناء."""
    check_permission(user, permission_code)
    if not has_directorate_scope(user, directorate_id):
        raise PermissionDenied('ليس لديك صلاحية على هذه الإدارة/المديرية')


# للتوافق الخلفي
check_permission_for_department = check_permission_for_directorate


def requires_four_eyes(permission_code: str) -> bool:
    """هل الصلاحية تتطلب تفويض مزدوج؟"""
    from infra.security.models import FOUR_EYES_PERMISSIONS
    return permission_code in FOUR_EYES_PERMISSIONS


# ══════════════════════════════════════════════════════════════
# مرشح النطاق (Directorate Scope Filter)
# ══════════════════════════════════════════════════════════════

def filter_by_directorate_scope(user, queryset: QuerySet,
                                directorate_field: str = 'directorate') -> QuerySet:
    """
    تصفية QuerySet حسب نطاق المستخدم.
    ⚠️ يُفضل استخدام: PermissionService.get_scoped_queryset()
    """
    if user.is_superuser:
        return queryset
    profile = get_user_profile(user)
    if not profile:
        return queryset.none()
    # UserProfile الجديد: get_accessible_security_admin_ids بدلاً من get_accessible_directorate_ids
    dir_ids = profile.get_accessible_security_admin_ids()
    if not dir_ids:
        return queryset.none()
    return queryset.filter(**{f'{directorate_field}__in': dir_ids})


# للتوافق الخلفي
filter_by_department_scope = filter_by_directorate_scope


def filter_by_governorate_scope(user, queryset: QuerySet,
                                governorate_field: str = 'governorate') -> QuerySet:
    """تصفية QuerySet حسب المحافظة."""
    if user.is_superuser:
        return queryset
    profile = get_user_profile(user)
    if not profile:
        return queryset.none()
    if profile.governorate_id is None:
        if getattr(profile, 'supervises_all_directorates', False):
            return queryset
        return queryset.none()
    return queryset.filter(**{f'{governorate_field}_id': profile.governorate_id})


# ══════════════════════════════════════════════════════════════
# DRF Permission Classes — Delegate to authorization
# ══════════════════════════════════════════════════════════════

class ABACPermission(drf_permissions.BasePermission):
    """
    DRF Permission class — RBAC + ABAC.
    ⚠️ يُفضل استخدام: authorization.mixins.ServicePermission
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        required = getattr(view, 'required_permission', None)
        if required is None:
            return True
        if isinstance(required, dict):
            action = getattr(view, 'action', request.method.lower())
            perm = required.get(action)
            if perm is None:
                return True
            if isinstance(perm, (list, tuple, set)):
                from infra.authorization.services.permission_service import PermissionService
                return PermissionService.has_any_permission(request.user, *perm)
            return has_permission(request.user, perm)
        
        if isinstance(required, (list, tuple, set)):
            from infra.authorization.services.permission_service import PermissionService
            return PermissionService.has_any_permission(request.user, *required)
            
        return has_permission(request.user, required)

    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        gov_id = None
        if hasattr(obj, 'governorate_id'):
            gov_id = obj.governorate_id
        elif hasattr(obj, 'personnel') and hasattr(obj.personnel, 'governorate_id'):
            gov_id = obj.personnel.governorate_id
        if gov_id is not None:
            if not has_governorate_scope(request.user, gov_id):
                return False
        dept_id = None
        if hasattr(obj, 'directorate_id'):
            dept_id = obj.directorate_id
        elif hasattr(obj, 'department_id'):
            dept_id = obj.department_id
        elif hasattr(obj, 'personnel'):
            dept_id = getattr(obj.personnel, 'directorate_id', None)
        if dept_id is not None:
            return has_directorate_scope(request.user, dept_id)
        return True


class IsAdminPermission(drf_permissions.BasePermission):
    """صلاحية مدير النظام فقط."""
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return (request.user.is_superuser or
                has_permission(request.user, 'manage_users'))


class HasSpecificPermission(drf_permissions.BasePermission):
    """DRF Permission class لصلاحية محددة."""
    def __init__(self, permission_code: str):
        self.permission_code = permission_code

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return has_permission(request.user, self.permission_code)


# ══════════════════════════════════════════════════════════════
# Decorators
# ══════════════════════════════════════════════════════════════

def permission_required(permission_code: str):
    """ديكوريتور يتحقق من الصلاحية."""
    from functools import wraps

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user = kwargs.get('user')
            if user is None and len(args) > 0:
                obj = args[0]
                if hasattr(obj, 'user'):
                    user = obj.user
                elif hasattr(obj, 'request') and hasattr(obj.request, 'user'):
                    user = obj.request.user
            if user is None:
                raise PermissionDenied('لا يمكن تحديد المستخدم')
            check_permission(user, permission_code)
            return func(*args, **kwargs)
        return wrapper
    return decorator
