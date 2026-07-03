"""
Authorization Models Package
═════════════════════════════
from infra.authorization.models import Permission, Role, UserRole, UserProfile
"""
from .permission import Permission, PermissionCategory
from .role import Role, RolePermission
from .user_role import UserRole
from .user_profile import UserProfile

__all__ = [
    'Permission', 'PermissionCategory',
    'Role', 'RolePermission',
    'UserRole',
    'UserProfile',
]
