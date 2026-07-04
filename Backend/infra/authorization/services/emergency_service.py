"""
Emergency Access Service — خدمة الوصول الطارئ (Break Glass)
═══════════════════════════════════════════════════════════════
منح/إلغاء/مراجعة الوصول الطارئ مع تدقيق CRITICAL.

القواعد:
    - أقصى مدة: 24 ساعة
    - يُسجّل في Audit بمستوى CRITICAL
    - المراجعة إلزامية بعد الانتهاء
    - عند المنح/الإلغاء → مسح كاش المستخدم

الاستخدام:
    from infra.authorization.services.emergency_service import EmergencyService
    EmergencyService.grant(user, granted_by, reason, permissions, hours=4)
"""
import logging
from datetime import timedelta
from typing import List, Optional, Set

from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone

from infra.authorization.cache.permission_cache import PermissionCache
from infra.authorization.models.emergency_access import EmergencyAccess, EmergencyStatus

logger = logging.getLogger('authorization.emergency')

User = get_user_model()

# أقصى مدة للوصول الطارئ (ساعة)
MAX_EMERGENCY_HOURS = 24


class EmergencyError(Exception):
    def __init__(self, message: str, code: str = 'emergency_error'):
        self.message = message
        self.code = code
        super().__init__(self.message)


class EmergencyService:
    """خدمة Break Glass — منح/إلغاء/مراجعة الوصول الطارئ."""

    # ══════════════════════════════════════════════════════════════
    # منح وصول طارئ
    # ══════════════════════════════════════════════════════════════

    @staticmethod
    @transaction.atomic
    def grant(
        user_id: str,
        granted_by,
        reason: str,
        permission_codes: List[str],
        hours: int = 4,
    ) -> EmergencyAccess:
        """
        منح وصول طارئ.

        Args:
            user_id: المستخدم الذي سيحصل على الوصول
            granted_by: من يمنح الوصول (يجب أن يملك emergency.grant)
            reason: سبب الطوارئ (إلزامي)
            permission_codes: الصلاحيات الممنوحة
            hours: عدد ساعات الوصول (أقصى 24)
        """
        if not reason.strip():
            raise EmergencyError('يجب تحديد سبب الطوارئ', 'reason_required')
        if not permission_codes:
            raise EmergencyError('يجب تحديد صلاحيات للمنح', 'no_permissions')
        if hours < 1 or hours > MAX_EMERGENCY_HOURS:
            raise EmergencyError(
                f'المدة يجب أن تكون بين 1 و {MAX_EMERGENCY_HOURS} ساعة',
                'invalid_duration',
            )

        # جلب المستخدم
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise EmergencyError('المستخدم غير موجود', 'user_not_found')

        # فحص عدم وجود وصول طارئ نشط
        active = EmergencyAccess.objects.filter(
            user=user,
            status=EmergencyStatus.ACTIVE,
            expires_at__gt=timezone.now(),
        ).exists()
        if active:
            raise EmergencyError(
                'يوجد وصول طارئ نشط بالفعل لهذا المستخدم',
                'already_active',
            )

        # إنشاء الوصول الطارئ
        emergency = EmergencyAccess.objects.create(
            user=user,
            granted_by=granted_by,
            reason=reason,
            expires_at=timezone.now() + timedelta(hours=hours),
            status=EmergencyStatus.ACTIVE,
        )

        # ربط الصلاحيات
        from infra.authorization.models.permission import Permission
        perms = Permission.objects.filter(code__in=permission_codes, is_active=True)
        emergency.permissions.set(perms)

        # مسح كاش المستخدم — ليحصل على الصلاحيات الجديدة
        PermissionCache.invalidate_user(str(user.pk))

        # تسجيل في Audit بمستوى CRITICAL
        try:
            from infra.audit.services.audit_service import AuditService
            AuditService.log_action(
                user=granted_by,
                action='EMERGENCY_GRANT',
                model_name='EmergencyAccess',
                object_id=str(emergency.pk),
                new_data={
                    'target_user': str(user.pk),
                    'reason': reason,
                    'permissions': permission_codes,
                    'hours': hours,
                },
                severity='critical',
                module='security',
                change_reason=f'Break Glass: {reason}',
            )
        except Exception as e:
            logger.error(f"[EmergencyService] Audit log failed: {e}")

        logger.warning(
            f"[EmergencyService] 🚨 EMERGENCY ACCESS GRANTED: "
            f"{user} by {granted_by} for {hours}h — {reason}"
        )
        return emergency

    # ══════════════════════════════════════════════════════════════
    # إلغاء مبكر
    # ══════════════════════════════════════════════════════════════

    @staticmethod
    def revoke(emergency_id: int, revoked_by) -> EmergencyAccess:
        """إلغاء وصول طارئ مبكراً."""
        try:
            emergency = EmergencyAccess.objects.get(pk=emergency_id)
        except EmergencyAccess.DoesNotExist:
            raise EmergencyError('الوصول الطارئ غير موجود', 'not_found')

        if emergency.status != EmergencyStatus.ACTIVE:
            raise EmergencyError(
                f'لا يمكن إلغاء وصول بحالة: {emergency.get_status_display()}',
                'invalid_status',
            )

        emergency.status = EmergencyStatus.REVOKED
        emergency.revoked_at = timezone.now()
        emergency.revoked_by = revoked_by
        emergency.save(update_fields=['status', 'revoked_at', 'revoked_by'])

        PermissionCache.invalidate_user(str(emergency.user_id))
        logger.warning(f"[EmergencyService] Emergency revoked: #{emergency_id} by {revoked_by}")
        return emergency

    # ══════════════════════════════════════════════════════════════
    # مراجعة بعد الانتهاء
    # ══════════════════════════════════════════════════════════════

    @staticmethod
    def review(emergency_id: int, reviewed_by, audit_notes: str) -> EmergencyAccess:
        """مراجعة وصول طارئ بعد انتهائه — إلزامي."""
        try:
            emergency = EmergencyAccess.objects.get(pk=emergency_id)
        except EmergencyAccess.DoesNotExist:
            raise EmergencyError('الوصول الطارئ غير موجود', 'not_found')

        if emergency.reviewed_by is not None:
            raise EmergencyError('تمت المراجعة مسبقاً', 'already_reviewed')

        emergency.status = EmergencyStatus.REVIEWED
        emergency.reviewed_by = reviewed_by
        emergency.reviewed_at = timezone.now()
        emergency.audit_notes = audit_notes
        emergency.save(update_fields=[
            'status', 'reviewed_by', 'reviewed_at', 'audit_notes',
        ])

        logger.info(f"[EmergencyService] Emergency reviewed: #{emergency_id} by {reviewed_by}")
        return emergency

    # ══════════════════════════════════════════════════════════════
    # استعلامات
    # ══════════════════════════════════════════════════════════════

    @staticmethod
    def get_active_for_user(user) -> Optional[EmergencyAccess]:
        """جلب الوصول الطارئ النشط للمستخدم (إن وُجد)."""
        return EmergencyAccess.objects.filter(
            user=user,
            status=EmergencyStatus.ACTIVE,
            expires_at__gt=timezone.now(),
        ).first()

    @staticmethod
    def get_emergency_permissions(user) -> Set[str]:
        """جلب الصلاحيات الممنوحة بالطوارئ للمستخدم."""
        emergency = EmergencyService.get_active_for_user(user)
        if not emergency:
            return set()
        return set(emergency.get_permission_codes())

    @staticmethod
    def get_pending_reviews():
        """وصول طارئ منتهي ولم يُراجع بعد — للمراقبة."""
        return EmergencyAccess.objects.filter(
            status__in=[EmergencyStatus.EXPIRED, EmergencyStatus.REVOKED],
            reviewed_by__isnull=True,
        ).select_related('user', 'granted_by').order_by('-granted_at')

    @staticmethod
    def list_all(status_filter: str = None):
        """قائمة كل الوصول الطارئ — للمدقق."""
        qs = EmergencyAccess.objects.select_related(
            'user', 'granted_by', 'revoked_by', 'reviewed_by',
        ).order_by('-granted_at')
        if status_filter:
            qs = qs.filter(status=status_filter)
        return qs

    # ══════════════════════════════════════════════════════════════
    # تنظيف
    # ══════════════════════════════════════════════════════════════

    @staticmethod
    def cleanup_expired() -> int:
        """تحديث حالة الوصول الطارئ المنتهي — يُشغل كمهمة مجدولة."""
        now = timezone.now()
        expired = EmergencyAccess.objects.filter(
            status=EmergencyStatus.ACTIVE,
            expires_at__lt=now,
        )
        user_ids = list(expired.values_list('user_id', flat=True))
        count = expired.update(status=EmergencyStatus.EXPIRED)
        for uid in user_ids:
            PermissionCache.invalidate_user(str(uid))
        if count:
            logger.warning(f"[EmergencyService] Expired {count} emergency accesses")
        return count
