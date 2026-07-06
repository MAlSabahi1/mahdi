from typing import List, Optional
from django.utils.translation import gettext_lazy as _
from django.core.cache import cache

from d_services.utils.exception_handler import (
    ValidationException,
    PermissionDeniedException,
    LockedResourceException,
    InvalidStatusException,
    BusinessRuleException,
)
from d_services.models.GroupServicePermission import GroupServicePermission

ALLOWED_UPDATE_FIELDS = [
    'target_audience_data', 'base_component_data', 'version_data', 'priority'
]

class ValidationHandler:
    
    @staticmethod
    def validate_organization(instance, user) -> None:

        if instance.fk_organization != user.fk_organization:
            raise PermissionDeniedException(
                message=_('ليس لديك صلاحية على هذا الطلب'),
                hint=_('يجب أن تكون من نفس المنظمة التي تقدم الطلب')
            )
    
    @staticmethod
    def validate_not_locked(instance) -> None:

        if instance.is_locked:
            raise LockedResourceException(
                message=_('الطلب مقفول ولا يمكن تعديله'),
                details={
                    'locked_reason': instance.locked_reason or _('غير محدد'),
                    'locked_at': instance.locked_at.strftime('%Y-%m-%d %H:%M') if instance.locked_at else None
                },
                hint=_('تواصل مع مدير النظام لفتح قفل الطلب')
            )
    
    @staticmethod
    def validate_request_status(instance, allowed_statuses: List, action_name: str = '') -> None:

        if instance.status not in allowed_statuses:
            status_names = [s.label for s in allowed_statuses]
            raise InvalidStatusException(
                message=_('لا يمكن تنفيذ هذا الإجراء على الطلب الحالي'),
                details={
                    'current_status': instance.get_status_display(),
                    'allowed_statuses': status_names,
                    'action': action_name
                },
                hint=_('تحقق من حالة الطلب قبل تنفيذ هذا الإجراء')
            )
    
    @staticmethod
    def validate_grant_status(instance, allowed_statuses: List) -> None:

        if instance.grant_status not in allowed_statuses:
            raise InvalidStatusException(
                message=_('حالة المنحة الحالية لا تسمح بهذا الإجراء'),
                details={'current_status': instance.grant_status}
            )
    
    @staticmethod
    def validate_discount_status(instance, allowed_statuses: List) -> None:

        if instance.discount_status not in allowed_statuses:
            raise InvalidStatusException(
                message=_('حالة الخصم الحالية لا تسمح بهذا الإجراء'),
                details={'current_status': instance.discount_status}
            )
    
    @staticmethod
    def check_service_permission(user, service_id: int, permission_type: str = 'CREATE') -> bool:
        """Check if user has permission on service - with caching for performance"""
        if user.is_superuser:
            return True
        
        # Check cache first for performance
        cache_key = f'svc_perm_{user.id}_{service_id}_{permission_type}'
        result = cache.get(cache_key)
        if result is not None:
            return result
        
        # Query with optimized group IDs instead of queryset
        user_group_ids = list(user.groups.values_list('id', flat=True))
        result = GroupServicePermission.objects.filter(
            fk_group_id__in=user_group_ids,
            fk_permission__fk_service_id=service_id,
            fk_permission__permission_type=permission_type
        ).exists()
        
        # Cache for 5 minutes
        cache.set(cache_key, result, timeout=300)
        return result
    
    @staticmethod
    def validate_permission(user, service_id: int, permission_type: str) -> None:

        if not ValidationHandler.check_service_permission(user, service_id, permission_type):
            raise PermissionDeniedException(
                message=_('ليس لديك صلاحية تنفيذ هذا الإجراء'),
                details={'required_permission': permission_type}
            )
    
    @staticmethod
    def validate_for_action(
        instance,
        user,
        permission_type: str,
        allowed_statuses: Optional[List] = None,
        check_lock: bool = True,
        action_name: str = ''
    ) -> None:

        ValidationHandler.validate_organization(instance, user)
        ValidationHandler.validate_permission(user, instance.fk_service_id, permission_type)
        
        if check_lock:
            ValidationHandler.validate_not_locked(instance)
        
        if allowed_statuses:
            ValidationHandler.validate_request_status(instance, allowed_statuses, action_name)
    
    @staticmethod
    def validate_required(value, field_name: str) -> None:

        if not value:
            raise ValidationException(message=_('%s مطلوب') % field_name)
    
    @staticmethod
    def validate_positive_decimal(value, field_name: str):

        from decimal import Decimal
        value = Decimal(str(value))
        if value <= 0:
            raise ValidationException(message=_('%s يجب أن يكون أكبر من صفر') % field_name)
        return value
    
    @staticmethod
    def validate_max_value(value, max_value, field_name: str, max_field_name: str):

        if value > max_value:
            raise ValidationException(
                message=_('%s لا يمكن أن يتجاوز %s') % (field_name, max_field_name),
                details={max_field_name: float(max_value), field_name: float(value)}
            )
    
    @staticmethod
    def validate_update_fields(data):
        invalid_fields = []
        for field in data.keys():
            if field not in ALLOWED_UPDATE_FIELDS:
                invalid_fields.append(field)
        return invalid_fields