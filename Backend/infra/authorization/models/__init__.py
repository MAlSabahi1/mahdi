"""
Authorization Models Package
═════════════════════════════════
كل نماذج نظام الصلاحيات — 12 طبقة أمنية.

الاستيراد:
    from infra.authorization.models import Permission, Role, Delegation, ...
"""
from .permission_group import PermissionGroup
from .permission import Permission, PermissionCategory
from .role import Role, RolePermission
from .user_role import UserRole
from .user_profile import UserProfile
from .field_permission import FieldPermission
from .record_acl import RecordACL, AccessType
from .policy import AccessPolicy, PolicyEffect
from .delegation import Delegation, DelegationStatus
from .emergency_access import EmergencyAccess, EmergencyStatus

__all__ = [
    # الطبقة 1-2: الصلاحيات والأدوار
    'Permission', 'PermissionCategory',
    'Role', 'RolePermission',
    'UserRole',
    'UserProfile',
    # الطبقة 3: مجموعات الصلاحيات (للعرض في Admin UI)
    'PermissionGroup',
    # الطبقة 5: Record-Level Security
    'RecordACL', 'AccessType',
    # الطبقة 6: Field-Level Security
    'FieldPermission',
    # الطبقة 8: Dynamic Policies (ABAC Engine)
    'AccessPolicy', 'PolicyEffect',
    # الطبقة 11: Delegation (التفويض المؤقت)
    'Delegation', 'DelegationStatus',
    # الطبقة 12: Emergency Access (Break Glass)
    'EmergencyAccess', 'EmergencyStatus',
]
