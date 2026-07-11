"""
Permission Service — محرك الصلاحيات
═══════════════════════════════════════
نقطة الدخول الوحيدة لكل فحوص الصلاحيات.

القاعدة الذهبية:
    Redis Cache أولاً → DB Fallback → Redis Warm
    لا DB Query مباشرة في الكود العادي.

الاستخدام:
    from infra.authorization.services.permission_service import PermissionService
    if PermissionService.has_permission(user, Perms.USERS_VIEW):
        ...
"""
import logging
from typing import Dict, List, Optional, Set

from django.contrib.auth import get_user_model
from django.db import models

from infra.authorization.cache.permission_cache import PermissionCache

logger = logging.getLogger('authorization.permission')

User = get_user_model()


class PermissionService:
    """
    محرك الصلاحيات — يقرأ من Redis Cache.

    المسؤوليات:
        - has_permission / has_any / has_all
        - get_user_permissions (لإرسالها للـ Frontend)
        - get_user_roles
        - بناء الكاش (warm) عند الحاجة
    """

    # ══════════════════════════════════════════════════════════════
    # فحص الصلاحيات (الأهم)
    # ══════════════════════════════════════════════════════════════

    @staticmethod
    def has_permission(user, permission_code: str) -> bool:
        """
        هل المستخدم يملك هذه الصلاحية؟

        التدفق:
            1. superuser → True دائماً
            2. Redis Cache lookup
            3. إذا الكاش فارغ → DB Query → Warm Cache
        """
        if not user or not user.is_authenticated:
            return False
        if user.is_superuser:
            return True

        user_id = str(user.pk)

        # 1. Redis Cache
        cached = PermissionCache.has_permission(user_id, permission_code)
        if cached is not None:
            return cached

        # 2. Cache miss → DB → Warm
        permissions = PermissionService._load_from_db(user)
        PermissionCache.warm_cache(user_id, permissions)

        return permission_code in permissions

    @staticmethod
    def has_any_permission(user, *codes: str) -> bool:
        """هل يملك أي صلاحية من القائمة؟"""
        if not user or not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        perms = PermissionService.get_user_permissions(user)
        return bool(set(codes) & perms)

    @staticmethod
    def has_all_permissions(user, *codes: str) -> bool:
        """هل يملك جميع الصلاحيات في القائمة؟"""
        if not user or not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        perms = PermissionService.get_user_permissions(user)
        return set(codes).issubset(perms)

    # ══════════════════════════════════════════════════════════════
    # جلب الصلاحيات (للـ Frontend)
    # ══════════════════════════════════════════════════════════════

    @staticmethod
    def get_user_permissions(user) -> Set[str]:
        """
        جلب جميع صلاحيات المستخدم.
        يُستخدم لإرسالها للـ Frontend عند Login.
        """
        if not user or not user.is_authenticated:
            return set()
        if user.is_superuser:
            from infra.authorization.models.permission import Permission
            return set(
                Permission.objects.filter(is_active=True)
                .values_list('code', flat=True)
            )

        user_id = str(user.pk)

        # Redis Cache
        cached = PermissionCache.get_permissions(user_id)
        if cached is not None:
            return cached

        # Cache miss → DB → Warm
        permissions = PermissionService._load_from_db(user)
        PermissionCache.warm_cache(user_id, permissions)

        return permissions

    @staticmethod
    def get_user_permissions_list(user) -> List[str]:
        """نسخة List (مرتّبة) — للـ API Response."""
        return sorted(PermissionService.get_user_permissions(user))

    @staticmethod
    def get_user_roles(user) -> List[Dict]:
        """
        جلب أدوار المستخدم — لعرضها في الـ Frontend.

        Returns:
            [{'code': 'admin', 'name': 'مدير النظام', 'is_primary': True}, ...]
        """
        if not user or not user.is_authenticated:
            return []

        roles = []

        # الدور الأساسي
        try:
            profile = user.authz_profile
            roles.append({
                'code': profile.role.code,
                'name': profile.role.name,
                'is_primary': True,
            })
        except Exception:
            pass

        # الأدوار الإضافية
        from infra.authorization.models.user_role import UserRole
        from django.utils import timezone

        additional = UserRole.objects.filter(
            user=user, is_active=True
        ).select_related('role').filter(
            role__is_active=True,
        )
        for ur in additional:
            if not ur.is_expired:
                roles.append({
                    'code': ur.role.code,
                    'name': ur.role.name,
                    'is_primary': False,
                    'expires_at': ur.expires_at.isoformat() if ur.expires_at else None,
                })

        return roles

    # ══════════════════════════════════════════════════════════════
    # Data Scope (ABAC — المستوى 4)
    # ══════════════════════════════════════════════════════════════

    @staticmethod
    def check_data_scope(user, permission_code: str, obj=None) -> bool:
        """
        فحص نطاق البيانات (ABAC).

        القاعدة:
            personnel.view.all            → يرى الكل
            personnel.view.security_admin → يرى إدارة أمنه فقط
        """
        if not PermissionService.has_permission(user, permission_code):
            return False

        # استخراج scope من الكود
        parts = permission_code.split('.')
        scope = parts[2] if len(parts) >= 3 else 'all'

        if scope == 'all':
            return True

        if obj is None:
            return True  # لا كائن للفحص

        try:
            profile = user.authz_profile
        except Exception:
            return False

        if scope == 'security_admin':
            sa_id = getattr(obj, 'security_admin_id', None)
            if sa_id is None:
                return True
            return profile.has_security_admin_scope(sa_id)

        if scope == 'own':
            owner_id = getattr(obj, 'user_id', None) or getattr(obj, 'created_by_id', None)
            return owner_id == user.pk

        return False

    @staticmethod
    def get_scoped_queryset(user, queryset, permission_code: str):
        """
        فلترة QuerySet حسب نطاق البيانات.

        مثال:
            qs = PermissionService.get_scoped_queryset(
                user, Personnel.objects.all(), 'personnel.view.*'
            )
        """
        if user.is_superuser:
            return queryset

        scope = 'all'
        
        # إذا تم تمرير .* نبحث عن أعلى صلاحية يمتلكها المستخدم
        if permission_code.endswith('.*'):
            base = permission_code[:-2]
            if PermissionService.has_permission(user, f'{base}.all'):
                scope = 'all'
            elif PermissionService.has_permission(user, f'{base}.security_admin'):
                scope = 'security_admin'
            elif PermissionService.has_permission(user, f'{base}.own'):
                scope = 'own'
            else:
                return queryset.none()
        else:
            parts = permission_code.split('.')
            scope = parts[2] if len(parts) >= 3 else 'all'

        if scope == 'all':
            return queryset

        try:
            profile = user.authz_profile
        except Exception:
            return queryset.none()

        if scope == 'security_admin':
            sa_ids = profile.get_accessible_security_admin_ids()
            return queryset.filter(security_admin_id__in=sa_ids)

        if scope == 'own':
            return queryset.filter(
                models.Q(user_id=user.pk) | models.Q(created_by_id=user.pk)
            )

        return queryset

    # ══════════════════════════════════════════════════════════════
    # بناء الكاش من DB
    # ══════════════════════════════════════════════════════════════

    @staticmethod
    def _load_from_db(user) -> Set[str]:
        """
        جلب كل صلاحيات المستخدم من DB.
        يُستدعى فقط عند cache miss.
        """
        from infra.authorization.models.user_role import UserRole

        all_perms: Set[str] = set()

        # 1. الدور الأساسي
        try:
            profile = user.authz_profile
            primary_perms = profile.role.get_all_permission_codes()
            all_perms.update(primary_perms)
        except Exception:
            pass

        # 2. الأدوار الإضافية
        additional_roles = UserRole.objects.filter(
            user=user, is_active=True
        ).select_related('role')

        for ur in additional_roles:
            if ur.is_effective:
                role_perms = ur.role.get_all_permission_codes()
                all_perms.update(role_perms)

        logger.debug(
            f"[PermissionService] Loaded {len(all_perms)} permissions "
            f"from DB for {user}"
        )

        return all_perms

    # ══════════════════════════════════════════════════════════════
    # إعادة بناء الكاش (يُستدعى بعد Login)
    # ══════════════════════════════════════════════════════════════

    @staticmethod
    def warm_user_cache(user) -> Set[str]:
        """بناء كاش الصلاحيات — يُستدعى من AuthService عند Login."""
        permissions = PermissionService._load_from_db(user)
        PermissionCache.warm_cache(str(user.pk), permissions)
        return permissions
