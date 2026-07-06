"""
Policy Service — محرك السياسات الديناميكية
═══════════════════════════════════════════════
تقييم شروط مركّبة للتحكم بالوصول.

أمثلة الشروط:
    {"field": "user.branch_id", "op": "eq", "value_ref": "obj.branch_id"}
    {"field": "obj.status",     "op": "ne", "value": "archived"}
    {"field": "user.is_staff",  "op": "eq", "value": true}

العمليات المدعومة:
    eq, ne, gt, lt, gte, lte, in, not_in, contains, is_null

الاستخدام:
    from infra.authorization.services.policy_service import PolicyService
    allowed = PolicyService.evaluate(user, 'personnel.edit.all', obj)
"""
import logging
import operator
from typing import Any, Optional

from django.db import transaction

from infra.authorization.models.policy import AccessPolicy, PolicyEffect

logger = logging.getLogger('authorization.policy')

# خريطة العمليات المدعومة
OPERATORS = {
    'eq': operator.eq,
    'ne': operator.ne,
    'gt': operator.gt,
    'lt': operator.lt,
    'gte': operator.ge,
    'lte': operator.le,
    'in': lambda a, b: a in b,
    'not_in': lambda a, b: a not in b,
    'contains': lambda a, b: b in a if a else False,
    'is_null': lambda a, b: (a is None) == b,
}


class PolicyError(Exception):
    def __init__(self, message: str, code: str = 'policy_error'):
        self.message = message
        self.code = code
        super().__init__(self.message)


class PolicyService:
    """محرك السياسات الديناميكية — تقييم/إنشاء/تحديث."""

    # ══════════════════════════════════════════════════════════════
    # تقييم السياسات — الأهم
    # ══════════════════════════════════════════════════════════════

    @staticmethod
    def evaluate(user, permission_code: str, obj=None) -> Optional[bool]:
        """
        تقييم السياسات الديناميكية.

        Returns:
            True — سياسة allow تطابقت
            False — سياسة deny تطابقت
            None — لا سياسات مُطابقة (اترك القرار لنظام الصلاحيات العادي)
        """
        policies = AccessPolicy.objects.filter(
            permission_code=permission_code,
            is_active=True,
        ).order_by('-priority')

        if not policies.exists():
            return None  # لا سياسات → القرار للنظام العادي

        for policy in policies:
            if _evaluate_conditions(policy.conditions, user, obj):
                if policy.effect == PolicyEffect.DENY:
                    return False  # deny يتغلب فوراً
                return True  # allow

        return None  # لا شرط تطابق

    # ══════════════════════════════════════════════════════════════
    # إدارة السياسات
    # ══════════════════════════════════════════════════════════════

    @staticmethod
    @transaction.atomic
    def create_policy(
        name: str,
        code: str,
        permission_code: str,
        conditions: list,
        effect: str = 'allow',
        priority: int = 0,
        model_name: str = '',
        description: str = '',
        created_by=None,
    ) -> AccessPolicy:
        """إنشاء سياسة ديناميكية جديدة."""
        if not name.strip():
            raise PolicyError('يجب تحديد اسم السياسة', 'name_required')
        if not conditions:
            raise PolicyError('يجب تحديد شرط واحد على الأقل', 'no_conditions')

        # التحقق من صحة الشروط
        for cond in conditions:
            _validate_condition(cond)

        policy = AccessPolicy.objects.create(
            name=name,
            code=code,
            permission_code=permission_code,
            conditions=conditions,
            effect=effect,
            priority=priority,
            model_name=model_name,
            description=description,
            created_by=created_by,
        )
        logger.info(f"[PolicyService] Policy created: {code} ({effect})")
        return policy

    @staticmethod
    def update_policy(policy_id: int, data: dict, updated_by=None) -> AccessPolicy:
        """تحديث سياسة."""
        try:
            policy = AccessPolicy.objects.get(pk=policy_id)
        except AccessPolicy.DoesNotExist:
            raise PolicyError('السياسة غير موجودة', 'not_found')

        if 'conditions' in data:
            for cond in data['conditions']:
                _validate_condition(cond)

        for field, value in data.items():
            if hasattr(policy, field):
                setattr(policy, field, value)
        policy.save()

        logger.info(f"[PolicyService] Policy updated: #{policy_id}")
        return policy

    @staticmethod
    def delete_policy(policy_id: int) -> None:
        """تعطيل سياسة (Soft)."""
        updated = AccessPolicy.objects.filter(pk=policy_id).update(is_active=False)
        if not updated:
            raise PolicyError('السياسة غير موجودة', 'not_found')

    @staticmethod
    def list_policies(permission_code: str = None):
        """قائمة السياسات النشطة."""
        qs = AccessPolicy.objects.filter(is_active=True).order_by('-priority')
        if permission_code:
            qs = qs.filter(permission_code=permission_code)
        return qs


# ══════════════════════════════════════════════════════════════
# دوال مساعدة داخلية
# ══════════════════════════════════════════════════════════════

def _evaluate_conditions(conditions: list, user, obj) -> bool:
    """تقييم كل الشروط (AND). كلها يجب أن تتحقق."""
    if not conditions:
        return True

    for cond in conditions:
        if not _evaluate_single_condition(cond, user, obj):
            return False
    return True


def _evaluate_single_condition(cond: dict, user, obj) -> bool:
    """تقييم شرط واحد."""
    try:
        field = cond.get('field', '')
        op_name = cond.get('op', 'eq')

        # جلب القيمة الفعلية من user/obj
        actual_value = _resolve_value(field, user, obj)

        # جلب القيمة المتوقعة
        if 'value_ref' in cond:
            expected_value = _resolve_value(cond['value_ref'], user, obj)
        else:
            expected_value = cond.get('value')

        op_func = OPERATORS.get(op_name)
        if not op_func:
            logger.warning(f"[PolicyService] Unknown operator: {op_name}")
            return False

        return op_func(actual_value, expected_value)

    except Exception as e:
        logger.debug(f"[PolicyService] Condition evaluation failed: {e}")
        return False


def _resolve_value(path: str, user, obj) -> Any:
    """
    حل مسار القيمة.

    أمثلة:
        'user.branch_id' → user.branch_id
        'obj.status' → obj.status
        'user.is_staff' → user.is_staff
    """
    parts = path.split('.')
    if len(parts) < 2:
        return None

    root = parts[0]
    if root == 'user':
        target = user
    elif root == 'obj':
        target = obj
    else:
        return None

    if target is None:
        return None

    # تتبع المسار: user.profile.branch_id
    for part in parts[1:]:
        if target is None:
            return None
        target = getattr(target, part, None)

    return target


def _validate_condition(cond: dict) -> None:
    """التحقق من صحة بنية الشرط."""
    if not isinstance(cond, dict):
        raise PolicyError('كل شرط يجب أن يكون dict', 'invalid_condition')
    if 'field' not in cond:
        raise PolicyError('الشرط يجب أن يحتوي على field', 'missing_field')
    if 'op' not in cond:
        raise PolicyError('الشرط يجب أن يحتوي على op', 'missing_op')
    if cond['op'] not in OPERATORS:
        raise PolicyError(
            f"العملية غير مدعومة: {cond['op']}. المتاح: {list(OPERATORS.keys())}",
            'invalid_op',
        )
    if 'value' not in cond and 'value_ref' not in cond:
        raise PolicyError(
            'الشرط يجب أن يحتوي على value أو value_ref', 'missing_value',
        )
