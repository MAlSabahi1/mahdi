"""
Role Service — إدارة الأدوار
═══════════════════════════════
CRUD + Cache Invalidation.

القاعدة الذهبية:
    عند تعديل أي صلاحية لدور → مسح كاش جميع مستخدمي هذا الدور.
"""
import logging
from typing import Any, Dict, List, Optional

from django.contrib.auth import get_user_model
from django.db import transaction

from infra.authorization.cache.permission_cache import PermissionCache
from infra.authorization.models.permission import Permission
from infra.authorization.models.role import Role, RolePermission
from infra.authorization.models.user_role import UserRole

logger = logging.getLogger('authorization.role')

User = get_user_model()


class RoleServiceError(Exception):
    def __init__(self, message: str, code: str = 'role_error', status_code: int = 400):
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(self.message)


class RoleService:
    """
    إدارة الأدوار — CRUD + Cache Invalidation.
    """

    # ══════════════════════════════════════════════════════════════
    # CRUD
    # ══════════════════════════════════════════════════════════════

    @staticmethod
    def create_role(
        name: str,
        code: str,
        description: str = '',
        priority: int = 0,
        created_by: Optional[Any] = None,
    ) -> Role:
        """إنشاء دور جديد."""
        if Role.objects.filter(code=code).exists():
            raise RoleServiceError('رمز الدور مستخدم بالفعل', code='code_exists')

        role = Role.objects.create(
            name=name,
            code=code,
            description=description,
            priority=priority,
            created_by=created_by,
        )
        logger.info(
            f"[RoleService] Role created: {code} "
            f"by {getattr(created_by, 'username', 'system')}"
        )
        return role

    @staticmethod
    def update_role(
        role_id: int,
        data: Dict[str, Any],
        updated_by: Optional[Any] = None,
    ) -> Role:
        """تحديث دور."""
        try:
            role = Role.objects.get(pk=role_id)
        except Role.DoesNotExist:
            raise RoleServiceError('الدور غير موجود', code='not_found', status_code=404)

        allowed = {'name', 'description', 'is_active', 'priority'}
        update_fields = []
        for field, value in data.items():
            if field in allowed:
                setattr(role, field, value)
                update_fields.append(field)

        if update_fields:
            role.save(update_fields=update_fields)
            logger.info(f"[RoleService] Role updated: {role.code} fields={update_fields}")

        return role

    @staticmethod
    def delete_role(role_id: int) -> None:
        """حذف دور (غير نظامي فقط)."""
        try:
            role = Role.objects.get(pk=role_id)
        except Role.DoesNotExist:
            raise RoleServiceError('الدور غير موجود', code='not_found', status_code=404)

        if role.is_system_role:
            raise RoleServiceError('لا يمكن حذف دور نظامي', code='system_role')

        role.is_active = False
        role.save(update_fields=['is_active'])

        # مسح كاش جميع مستخدمي الدور
        PermissionCache.invalidate_role_users(role.pk)
        logger.info(f"[RoleService] Role deactivated: {role.code}")

    # ══════════════════════════════════════════════════════════════
    # إدارة الصلاحيات (Permission ↔ Role)
    # ══════════════════════════════════════════════════════════════

    @staticmethod
    def assign_permission(
        role_id: int,
        permission_code: str,
        granted_by: Optional[Any] = None,
    ) -> None:
        """منح صلاحية لدور + مسح الكاش."""
        try:
            role = Role.objects.get(pk=role_id)
        except Role.DoesNotExist:
            raise RoleServiceError('الدور غير موجود', code='role_not_found', status_code=404)

        try:
            permission = Permission.objects.get(code=permission_code, is_active=True)
        except Permission.DoesNotExist:
            raise RoleServiceError(
                f'الصلاحية غير موجودة: {permission_code}',
                code='permission_not_found',
            )

        with transaction.atomic():
            RolePermission.objects.get_or_create(
                role=role,
                permission=permission,
                defaults={'granted_by': granted_by},
            )

        # 🔴 Cache Invalidation — القاعدة الذهبية
        PermissionCache.invalidate_role_users(role.pk)
        logger.info(f"[RoleService] Permission assigned: {role.code} ← {permission_code}")

    @staticmethod
    def revoke_permission(role_id: int, permission_code: str) -> None:
        """سحب صلاحية من دور + مسح الكاش."""
        deleted, _ = RolePermission.objects.filter(
            role_id=role_id,
            permission__code=permission_code,
        ).delete()

        if deleted > 0:
            PermissionCache.invalidate_role_users(role_id)
            logger.info(f"[RoleService] Permission revoked from role {role_id}: {permission_code}")

    @staticmethod
    def set_role_permissions(
        role_id: int,
        permission_codes: List[str],
        granted_by: Optional[Any] = None,
    ) -> None:
        """تعيين كامل صلاحيات الدور (يستبدل القائمة الحالية)."""
        try:
            role = Role.objects.get(pk=role_id)
        except Role.DoesNotExist:
            raise RoleServiceError('الدور غير موجود', code='not_found', status_code=404)

        permissions = Permission.objects.filter(
            code__in=permission_codes, is_active=True
        )
        found_codes = set(permissions.values_list('code', flat=True))
        missing = set(permission_codes) - found_codes
        if missing:
            raise RoleServiceError(
                f'صلاحيات غير موجودة: {", ".join(missing)}',
                code='permissions_not_found',
            )

        with transaction.atomic():
            RolePermission.objects.filter(role=role).delete()
            RolePermission.objects.bulk_create([
                RolePermission(
                    role=role,
                    permission=perm,
                    granted_by=granted_by,
                ) for perm in permissions
            ])

        # Cache Invalidation
        PermissionCache.invalidate_role_users(role.pk)
        logger.info(
            f"[RoleService] Permissions set for {role.code}: "
            f"{len(permission_codes)} permissions"
        )

    # ══════════════════════════════════════════════════════════════
    # إدارة User ↔ Role
    # ══════════════════════════════════════════════════════════════

    @staticmethod
    def assign_role_to_user(
        user_id: str,
        role_id: int,
        assigned_by: Optional[Any] = None,
        expires_at=None,
        notes: str = '',
    ) -> UserRole:
        """إسناد دور لمستخدم + مسح الكاش."""
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise RoleServiceError('المستخدم غير موجود', code='user_not_found', status_code=404)

        try:
            role = Role.objects.get(pk=role_id, is_active=True)
        except Role.DoesNotExist:
            raise RoleServiceError('الدور غير موجود', code='role_not_found', status_code=404)

        user_role, created = UserRole.objects.update_or_create(
            user=user, role=role,
            defaults={
                'is_active': True,
                'assigned_by': assigned_by,
                'expires_at': expires_at,
                'notes': notes,
            },
        )

        # Cache Invalidation
        PermissionCache.invalidate_user(str(user_id))
        logger.info(
            f"[RoleService] Role assigned: {user} ← {role.code} "
            f"by {getattr(assigned_by, 'username', 'system')}"
        )
        return user_role

    @staticmethod
    def revoke_role_from_user(user_id: str, role_id: int) -> None:
        """إلغاء دور من مستخدم + مسح الكاش."""
        UserRole.objects.filter(
            user_id=user_id, role_id=role_id,
        ).update(is_active=False)

        PermissionCache.invalidate_user(str(user_id))
        logger.info(f"[RoleService] Role revoked: user={user_id} role={role_id}")

    # ══════════════════════════════════════════════════════════════
    # قراءة
    # ══════════════════════════════════════════════════════════════

    @staticmethod
    def list_roles(active_only: bool = True) -> list:
        """قائمة الأدوار."""
        qs = Role.objects.all()
        if active_only:
            qs = qs.filter(is_active=True)
        return list(qs.order_by('-priority', 'name'))

    @staticmethod
    def get_role_detail(role_id: int) -> Dict:
        """تفاصيل دور مع صلاحياته."""
        try:
            role = Role.objects.get(pk=role_id)
        except Role.DoesNotExist:
            raise RoleServiceError('الدور غير موجود', code='not_found', status_code=404)

        return {
            'role': role,
            'permissions': role.get_all_permission_codes(),
            'users_count': UserRole.objects.filter(
                role=role, is_active=True
            ).count(),
        }
