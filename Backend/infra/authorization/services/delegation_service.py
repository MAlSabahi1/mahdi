"""
Delegation Service — خدمة التفويض
═══════════════════════════════════
إنشاء/إلغاء/جلب التفويضات + Cache Invalidation.

القواعد:
    - المُفوِّض يجب أن يملك الصلاحيات التي يُفوِّضها
    - لا يمكن تفويض صلاحيات لا يملكها
    - التفويض مؤقت (ends_at إلزامي)
    - عند إنشاء/إلغاء تفويض → مسح كاش المُفوَّض إليه

الاستخدام:
    from infra.authorization.services.delegation_service import DelegationService
    DelegationService.create_delegation(delegator, delegate, ...)
"""
import logging
from datetime import timedelta
from typing import List, Optional, Set

from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone

from infra.authorization.cache.permission_cache import PermissionCache
from infra.authorization.models.delegation import Delegation, DelegationStatus

logger = logging.getLogger('authorization.delegation')

User = get_user_model()


class DelegationError(Exception):
    def __init__(self, message: str, code: str = 'delegation_error'):
        self.message = message
        self.code = code
        super().__init__(self.message)


class DelegationService:
    """خدمة التفويض — إنشاء/إلغاء/جلب التفويضات."""

    # ══════════════════════════════════════════════════════════════
    # إنشاء تفويض
    # ══════════════════════════════════════════════════════════════

    @staticmethod
    @transaction.atomic
    def create_delegation(
        delegator,
        delegate_id: str,
        reason: str,
        starts_at=None,
        ends_at=None,
        role_id: int = None,
        permission_codes: List[str] = None,
        notes: str = '',
    ) -> Delegation:
        """
        إنشاء تفويض جديد.

        Args:
            delegator: المُفوِّض (request.user)
            delegate_id: معرف المُفوَّض إليه
            reason: سبب التفويض (إلزامي)
            starts_at: بداية التفويض (افتراضي: الآن)
            ends_at: نهاية التفويض (إلزامي)
            role_id: الدور المُفوَّض (أو None لصلاحيات محددة)
            permission_codes: صلاحيات محددة (إذا لم يُحدد دور)
            notes: ملاحظات
        """
        if not reason.strip():
            raise DelegationError('يجب تحديد سبب التفويض', 'reason_required')

        # جلب المُفوَّض إليه
        try:
            delegate = User.objects.get(pk=delegate_id)
        except User.DoesNotExist:
            raise DelegationError('المستخدم المُفوَّض إليه غير موجود', 'user_not_found')

        # لا يمكن تفويض لنفسك
        if delegator.pk == delegate.pk:
            raise DelegationError('لا يمكنك تفويض صلاحياتك لنفسك', 'self_delegation')

        # ضبط التوقيت
        now = timezone.now()
        starts_at = starts_at or now
        if not ends_at:
            raise DelegationError('يجب تحديد تاريخ انتهاء التفويض', 'ends_at_required')
        if ends_at <= starts_at:
            raise DelegationError('تاريخ الانتهاء يجب أن يكون بعد البداية', 'invalid_dates')

        # فحص عدم وجود تفويض نشط مكرر
        existing = Delegation.objects.filter(
            delegator=delegator,
            delegate=delegate,
            status__in=[DelegationStatus.ACTIVE, DelegationStatus.PENDING],
        ).exists()
        if existing:
            raise DelegationError(
                'يوجد تفويض نشط بالفعل لهذا المستخدم', 'duplicate_delegation',
            )

        # إنشاء التفويض
        delegation = Delegation.objects.create(
            delegator=delegator,
            delegate=delegate,
            role_id=role_id,
            reason=reason,
            starts_at=starts_at,
            ends_at=ends_at,
            status=DelegationStatus.ACTIVE if starts_at <= now else DelegationStatus.PENDING,
            notes=notes,
        )

        # ربط صلاحيات محددة (إذا لم يُحدد دور)
        if permission_codes and not role_id:
            from infra.authorization.models.permission import Permission
            perms = Permission.objects.filter(code__in=permission_codes, is_active=True)
            delegation.permissions.set(perms)

        # مسح كاش المُفوَّض إليه — ليحصل على الصلاحيات الجديدة
        PermissionCache.invalidate_user(str(delegate.pk))

        logger.info(
            f"[DelegationService] Delegation created: "
            f"{delegator} → {delegate} until {ends_at}"
        )
        return delegation

    # ══════════════════════════════════════════════════════════════
    # إلغاء تفويض
    # ══════════════════════════════════════════════════════════════

    @staticmethod
    def revoke_delegation(delegation_id: int, revoked_by) -> Delegation:
        """إلغاء تفويض مبكراً."""
        try:
            delegation = Delegation.objects.get(pk=delegation_id)
        except Delegation.DoesNotExist:
            raise DelegationError('التفويض غير موجود', 'not_found')

        if delegation.status not in (DelegationStatus.ACTIVE, DelegationStatus.PENDING):
            raise DelegationError(
                f'لا يمكن إلغاء تفويض بحالة: {delegation.get_status_display()}',
                'invalid_status',
            )

        delegation.status = DelegationStatus.REVOKED
        delegation.revoked_at = timezone.now()
        delegation.revoked_by = revoked_by
        delegation.save(update_fields=['status', 'revoked_at', 'revoked_by'])

        # مسح كاش المُفوَّض إليه
        PermissionCache.invalidate_user(str(delegation.delegate_id))

        logger.info(f"[DelegationService] Delegation revoked: #{delegation_id} by {revoked_by}")
        return delegation

    # ══════════════════════════════════════════════════════════════
    # جلب التفويضات
    # ══════════════════════════════════════════════════════════════

    @staticmethod
    def get_active_delegations_for_user(user) -> list:
        """التفويضات النشطة التي استلمها المستخدم (المُفوَّض إليه)."""
        now = timezone.now()
        return list(
            Delegation.objects.filter(
                delegate=user,
                status=DelegationStatus.ACTIVE,
                starts_at__lte=now,
                ends_at__gt=now,
            ).select_related('delegator', 'role')
        )

    @staticmethod
    def get_delegations_given(user) -> list:
        """التفويضات التي منحها المستخدم (المُفوِّض)."""
        return list(
            Delegation.objects.filter(delegator=user)
            .select_related('delegate', 'role')
            .order_by('-created_at')
        )

    @staticmethod
    def get_delegated_permissions(user) -> Set[str]:
        """جلب الصلاحيات المكتسبة بالتفويض للمستخدم."""
        delegations = DelegationService.get_active_delegations_for_user(user)
        all_perms: Set[str] = set()
        for d in delegations:
            all_perms.update(d.get_delegated_permission_codes())
        return all_perms

    # ══════════════════════════════════════════════════════════════
    # تنظيف التفويضات المنتهية
    # ══════════════════════════════════════════════════════════════

    @staticmethod
    def cleanup_expired() -> int:
        """تحديث حالة التفويضات المنتهية — يُشغل كمهمة مجدولة."""
        now = timezone.now()
        expired = Delegation.objects.filter(
            status=DelegationStatus.ACTIVE,
            ends_at__lt=now,
        )
        # مسح كاش المتأثرين
        user_ids = list(expired.values_list('delegate_id', flat=True))
        count = expired.update(status=DelegationStatus.EXPIRED)
        for uid in user_ids:
            PermissionCache.invalidate_user(str(uid))
        logger.info(f"[DelegationService] Expired {count} delegations")
        return count

    @staticmethod
    def activate_pending() -> int:
        """تفعيل التفويضات المعلقة التي بدأ وقتها — يُشغل كمهمة مجدولة."""
        now = timezone.now()
        pending = Delegation.objects.filter(
            status=DelegationStatus.PENDING,
            starts_at__lte=now,
            ends_at__gt=now,
        )
        user_ids = list(pending.values_list('delegate_id', flat=True))
        count = pending.update(status=DelegationStatus.ACTIVE)
        for uid in user_ids:
            PermissionCache.invalidate_user(str(uid))
        logger.info(f"[DelegationService] Activated {count} pending delegations")
        return count
