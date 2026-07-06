"""
Permission Checker - Unified permission validation utilities
"""
from typing import Optional
from django.utils.translation import gettext_lazy as _

from d_services.utils.exception_handler import PermissionDeniedException
from d_services.models.GroupServicePermission import GroupServicePermission


class PermissionChecker:
    """Centralized permission checking for service operations"""
    
    @staticmethod
    def require_superuser(user) -> None:
        """Require user to be a superuser"""
        if not user.is_superuser:
            raise PermissionDeniedException(
                message=_('فقط المسؤول يمكنه تنفيذ هذا الإجراء'),
                hint=_('هذه العملية تتطلب صلاحيات المسؤول')
            )
    
    @staticmethod
    def require_manager(user) -> None:
        """Require user to be an organization manager"""
        if not getattr(user, 'is_manager', False):
            raise PermissionDeniedException(
                message=_('ليس لديك صلاحيات'),
                hint=_('هذه العملية تتطلب صلاحيات مدير المنظمة')
            )
    
    @staticmethod
    def require_superuser_or_manager(user) -> None:
        """Require user to be either superuser or manager"""
        if not user.is_superuser and not getattr(user, 'is_manager', False):
            raise PermissionDeniedException(
                message=_('ليس لديك صلاحيات'),
                hint=_('هذه العملية تتطلب صلاحيات المسؤول أو مدير المنظمة')
            )
    
    @staticmethod
    def check_service_permission(user, service_id: int, permission_type: str) -> bool:
        """Check if user has specific service permission"""
        if user.is_superuser:
            return True
        
        user_groups = user.groups.all()
        return GroupServicePermission.objects.filter(
            fk_group__in=user_groups,
            fk_permission__fk_service_id=service_id,
            fk_permission__permission_type=permission_type
        ).exists()
    
    @staticmethod
    def require_service_permission(user, service_id: int, permission_type: str) -> None:
        """Require user to have specific service permission"""
        if not PermissionChecker.check_service_permission(user, service_id, permission_type):
            raise PermissionDeniedException(
                message=_('ليس لديك صلاحية تنفيذ هذا الإجراء'),
                details={'required_permission': permission_type},
                hint=_('تواصل مع مدير النظام للحصول على الصلاحية المطلوبة')
            )
    
    @staticmethod
    def get_user_organization(user):
        """Get user's organization or raise exception"""
        user_org = getattr(user, 'fk_organization', None)
        if not user_org:
            raise PermissionDeniedException(
                message=_('المستخدم غير مرتبط بمنظمة'),
                hint=_('يجب ربط حسابك بمنظمة للاستمرار')
            )
        return user_org
