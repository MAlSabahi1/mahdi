"""
Record ACL Service — خدمة قيود الوصول على السجلات
═══════════════════════════════════════════════════════
إدارة قيود Record-Level Security.

القواعد:
    - deny يتغلب على allow (Deny-First)
    - القيود المنتهية لا تُحسب
    - يدعم قيود على مستخدم أو دور أو الجميع

الاستخدام:
    from infra.authorization.services.record_acl_service import RecordACLService
    RecordACLService.check_access(user, obj)  # True/False
"""
import logging
from typing import List, Optional

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.utils import timezone

from infra.authorization.models.record_acl import RecordACL, AccessType

logger = logging.getLogger('authorization.record_acl')

User = get_user_model()


class RecordACLError(Exception):
    def __init__(self, message: str, code: str = 'acl_error'):
        self.message = message
        self.code = code
        super().__init__(self.message)


class RecordACLService:
    """خدمة Record-Level Security — وضع/إزالة/فحص قيود السجلات."""

    # ══════════════════════════════════════════════════════════════
    # فحص الوصول — الأهم
    # ══════════════════════════════════════════════════════════════

    @staticmethod
    def check_access(user, obj, permission_code: str = '') -> bool:
        """
        هل المستخدم يملك حق الوصول لهذا السجل؟

        القاعدة: deny يتغلب على allow.
        إذا لا توجد قيود → مسموح (افتراضي).
        """
        if user.is_superuser:
            return True

        ct = ContentType.objects.get_for_model(obj)
        obj_id = str(obj.pk)
        now = timezone.now()

        # جلب القيود النشطة لهذا السجل
        acls = RecordACL.objects.filter(
            content_type=ct,
            object_id=obj_id,
            is_active=True,
        ).filter(
            # غير منتهية
            models_Q_not_expired(now),
        )

        if permission_code:
            # قيود على صلاحية محددة أو كل الصلاحيات
            from django.db.models import Q
            acls = acls.filter(
                Q(permission_code=permission_code) | Q(permission_code='')
            )

        # جلب أدوار المستخدم
        user_role_ids = _get_user_role_ids(user)

        for acl in acls:
            if _acl_applies_to_user(acl, user, user_role_ids):
                if acl.access_type == AccessType.DENY:
                    return False  # deny يتغلب فوراً

        return True  # لا قيد deny → مسموح

    @staticmethod
    def get_restricted_records(user, model_class, permission_code: str = '') -> list:
        """قائمة معرفات السجلات المقيّدة على المستخدم."""
        ct = ContentType.objects.get_for_model(model_class)
        now = timezone.now()
        user_role_ids = _get_user_role_ids(user)

        deny_acls = RecordACL.objects.filter(
            content_type=ct,
            access_type=AccessType.DENY,
            is_active=True,
        ).filter(models_Q_not_expired(now))

        if permission_code:
            from django.db.models import Q
            deny_acls = deny_acls.filter(
                Q(permission_code=permission_code) | Q(permission_code='')
            )

        restricted = []
        for acl in deny_acls:
            if _acl_applies_to_user(acl, user, user_role_ids):
                restricted.append(acl.object_id)

        return restricted

    # ══════════════════════════════════════════════════════════════
    # إدارة القيود
    # ══════════════════════════════════════════════════════════════

    @staticmethod
    @transaction.atomic
    def set_record_acl(
        obj,
        access_type: str,
        reason: str,
        created_by,
        target_user=None,
        target_role=None,
        permission_code: str = '',
        expires_at=None,
    ) -> RecordACL:
        """وضع قيد وصول على سجل."""
        if not reason.strip():
            raise RecordACLError('يجب تحديد سبب القيد', 'reason_required')

        ct = ContentType.objects.get_for_model(obj)
        obj_id = str(obj.pk)

        acl = RecordACL.objects.create(
            content_type=ct,
            object_id=obj_id,
            target_user=target_user,
            target_role=target_role,
            access_type=access_type,
            permission_code=permission_code,
            reason=reason,
            created_by=created_by,
            expires_at=expires_at,
            is_active=True,
        )

        logger.info(
            f"[RecordACL] {access_type} set on {ct.model}#{obj_id} "
            f"for {target_user or target_role or 'ALL'} by {created_by}"
        )
        return acl

    @staticmethod
    def remove_record_acl(acl_id: int) -> None:
        """إزالة قيد (تعطيل)."""
        updated = RecordACL.objects.filter(pk=acl_id).update(is_active=False)
        if not updated:
            raise RecordACLError('القيد غير موجود', 'not_found')
        logger.info(f"[RecordACL] ACL #{acl_id} deactivated")

    @staticmethod
    def list_acls_for_object(obj):
        """قائمة القيود على سجل معين."""
        ct = ContentType.objects.get_for_model(obj)
        return RecordACL.objects.filter(
            content_type=ct,
            object_id=str(obj.pk),
            is_active=True,
        ).select_related('target_user', 'target_role', 'created_by')

    @staticmethod
    def list_all(content_type_model: str = None):
        """كل القيود النشطة — للمدير."""
        qs = RecordACL.objects.filter(is_active=True).select_related(
            'content_type', 'target_user', 'target_role', 'created_by',
        ).order_by('-created_at')
        if content_type_model:
            qs = qs.filter(content_type__model=content_type_model)
        return qs


# ══════════════════════════════════════════════════════════════
# دوال مساعدة داخلية
# ══════════════════════════════════════════════════════════════

def models_Q_not_expired(now):
    """شرط: القيد غير منتهي الصلاحية."""
    from django.db.models import Q
    return Q(expires_at__isnull=True) | Q(expires_at__gt=now)


def _get_user_role_ids(user) -> list:
    """جلب معرفات أدوار المستخدم."""
    role_ids = []
    try:
        profile = user.authz_profile
        if profile.role_id:
            role_ids.append(profile.role_id)
    except Exception:
        pass

    from infra.authorization.models.user_role import UserRole
    additional = UserRole.objects.filter(
        user=user, is_active=True,
    ).values_list('role_id', flat=True)
    role_ids.extend(additional)
    return role_ids


def _acl_applies_to_user(acl: RecordACL, user, user_role_ids: list) -> bool:
    """هل هذا القيد ينطبق على المستخدم."""
    # قيد على الجميع (لا مستخدم ولا دور محدد)
    if acl.target_user_id is None and acl.target_role_id is None:
        return True
    # قيد على مستخدم محدد
    if acl.target_user_id and acl.target_user_id == user.pk:
        return True
    # قيد على دور محدد
    if acl.target_role_id and acl.target_role_id in user_role_ids:
        return True
    return False
