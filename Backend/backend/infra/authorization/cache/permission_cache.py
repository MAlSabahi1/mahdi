"""
Permission Cache — كاش الصلاحيات في Redis
══════════════════════════════════════════════
لا DB Query لكل Permission Check — Redis أولاً.

المفتاح: user_permissions:{user_id}
القيمة:  Set[str] من أكواد الصلاحيات

يُحدّث تلقائياً عند:
    - تعديل صلاحيات دور (role_service)
    - إسناد/إلغاء دور (role_service)
    - تسجيل دخول جديد (auth_service)
"""
import logging
from typing import Optional, Set

from django.core.cache import cache

logger = logging.getLogger('authorization.cache')

# ── ثوابت ──
PERMISSION_CACHE_TTL: int = 3600  # ساعة واحدة
PERMISSION_CACHE_PREFIX: str = 'user_permissions'


class PermissionCache:
    """
    Redis Permission Cache Layer.

    التدفق:
        Request → Redis Lookup → إذا موجود: return
                                 إذا لا: DB Query → Redis Store → return
    """

    # ══════════════════════════════════════════════════════════════
    # القراءة
    # ══════════════════════════════════════════════════════════════

    @staticmethod
    def get_permissions(user_id: str) -> Optional[Set[str]]:
        """
        جلب صلاحيات المستخدم من Redis.
        Returns None إذا الكاش فارغ (يحتاج warm).
        """
        cache_key = f"{PERMISSION_CACHE_PREFIX}:{user_id}"
        try:
            cached = cache.get(cache_key)
            if cached is not None and isinstance(cached, (list, set)):
                return set(cached)
            return None
        except Exception as e:
            logger.debug(f"[PermissionCache] Redis read failed: {e}")
            return None

    @staticmethod
    def has_permission(user_id: str, permission_code: str) -> Optional[bool]:
        """
        فحص صلاحية واحدة من Redis.
        Returns None إذا الكاش فارغ.
        """
        perms = PermissionCache.get_permissions(user_id)
        if perms is None:
            return None
        return permission_code in perms

    # ══════════════════════════════════════════════════════════════
    # الكتابة
    # ══════════════════════════════════════════════════════════════

    @staticmethod
    def warm_cache(user_id: str, permissions: Set[str]) -> None:
        """
        بناء/تحديث كاش الصلاحيات.
        يُستدعى عند: Login, Role Change, Permission Change.
        """
        cache_key = f"{PERMISSION_CACHE_PREFIX}:{user_id}"
        try:
            cache.set(cache_key, list(permissions), PERMISSION_CACHE_TTL)
            logger.debug(
                f"[PermissionCache] Warmed cache for user {user_id}: "
                f"{len(permissions)} permissions"
            )
        except Exception as e:
            logger.error(f"[PermissionCache] Redis write failed: {e}")

    # ══════════════════════════════════════════════════════════════
    # الإلغاء (Cache Invalidation)
    # ══════════════════════════════════════════════════════════════

    @staticmethod
    def invalidate_user(user_id: str) -> None:
        """مسح كاش مستخدم واحد — يُجبر على إعادة الحساب."""
        cache_key = f"{PERMISSION_CACHE_PREFIX}:{user_id}"
        try:
            cache.delete(cache_key)
            logger.info(f"[PermissionCache] Invalidated cache for user {user_id}")
        except Exception as e:
            logger.debug(f"[PermissionCache] Redis delete failed: {e}")

    @staticmethod
    def invalidate_role_users(role_id: int) -> None:
        """
        مسح كاش جميع مستخدمي دور معين.
        يُستدعى عند: تعديل صلاحيات الدور.
        
        هذا هو الحل لمعضلة Cache Invalidation المذكورة في permishn.md.
        """
        from infra.authorization.models.user_role import UserRole
        from infra.authorization.models.user_profile import UserProfile

        # المستخدمون الذين لديهم هذا الدور كأساسي
        primary_user_ids = list(
            UserProfile.objects.filter(role_id=role_id)
            .values_list('user_id', flat=True)
        )
        # المستخدمون الذين لديهم هذا الدور كإضافي
        additional_user_ids = list(
            UserRole.objects.filter(role_id=role_id, is_active=True)
            .values_list('user_id', flat=True)
        )

        all_user_ids = set(primary_user_ids + additional_user_ids)

        for uid in all_user_ids:
            PermissionCache.invalidate_user(str(uid))

        logger.info(
            f"[PermissionCache] Invalidated cache for role {role_id}: "
            f"{len(all_user_ids)} users affected"
        )

    @staticmethod
    def invalidate_all() -> None:
        """مسح كل كاش الصلاحيات — للطوارئ فقط."""
        try:
            # نستخدم pattern delete إذا متاح
            cache.delete_pattern(f"{PERMISSION_CACHE_PREFIX}:*")
            logger.warning("[PermissionCache] ALL permission caches invalidated!")
        except AttributeError:
            # Redis cache backend قد لا يدعم delete_pattern
            logger.warning(
                "[PermissionCache] delete_pattern not supported — "
                "manual invalidation required"
            )
