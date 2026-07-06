"""
Service Config Handler - Operations for OrganizationServiceConfig
"""
from typing import Optional, List, Dict
from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from d_services.models.OrganizationServiceConfig import OrganizationServiceConfig
from d_services.models.Service import Service
from d_services.utils.exception_handler import (
    ResourceNotFoundException,
    ValidationException,
    BusinessRuleException,
)


class ServiceConfigHandler:
    """Handler for OrganizationServiceConfig operations"""
    
    @staticmethod
    def get_config_for_user(service_id: int, user) -> OrganizationServiceConfig:
        """
        Get service config for user's organization.
        Raises exception if not found.
        """
        user_org = getattr(user, 'fk_organization', None)
        if not user_org:
            raise ValidationException(message=_('المستخدم غير مرتبط بمنظمة'))
        
        try:
            return OrganizationServiceConfig.objects.get(
                fk_service_id=service_id,
                fk_organization=user_org
            )
        except OrganizationServiceConfig.DoesNotExist:
            raise ResourceNotFoundException(
                message=_('إعدادات الخدمة غير موجودة لمنظمتك'),
                details={'service_id': service_id}
            )
    
    @staticmethod
    def get_active_config(service_id: int, user_org) -> Optional[OrganizationServiceConfig]:
        """Get active service config for organization"""
        return OrganizationServiceConfig.objects.filter(
            fk_service_id=service_id,
            fk_organization=user_org,
            is_active=True
        ).first()
    
    @staticmethod
    def validate_no_active_requests(config: OrganizationServiceConfig, service_id: int) -> None:
        """Validate no active requests exist for this config"""
        from d_services.models.ServiceRequest import ServiceRequest
        
        has_active = ServiceRequest.objects.filter(
            fk_service_id=service_id,
            fk_organization=config.fk_organization,
            status__in=['pending', 'in_progress'],
            is_deleted=False
        ).exists()
        
        if has_active:
            raise BusinessRuleException(
                message=_('لا يمكن تعديل الإعدادات لوجود طلبات لم تنتهي بعد'),
                hint=_('يجب إغلاق جميع الطلبات النشطة أولاً')
            )
    
    @staticmethod
    def update_config_fields(
        config: OrganizationServiceConfig, 
        data: Dict,
        allowed_fields: List[str]
    ) -> None:
        """Update specific config fields from request data"""
        fk_field_mapping = {
            'fk_currency': 'fk_currency_id',
            'fk_print_report_setting_for_input': 'fk_print_report_setting_for_input_id',
            'fk_print_report_setting_for_output': 'fk_print_report_setting_for_output_id'
        }
        
        for field in allowed_fields:
            if field in data:
                model_field = fk_field_mapping.get(field, field)
                setattr(config, model_field, data[field])
        
        config.save()
    
    @staticmethod
    def lock_service(config: OrganizationServiceConfig, reason: str, now=None) -> Dict:
        """
        Lock service config and all active requests.
        Returns info about locked requests.
        """
        from d_services.models.ServiceRequest import ServiceRequest
        
        if not reason:
            raise ValidationException(message=_('سبب القفل مطلوب'))
        
        now = now or timezone.now()
        
        config.is_locked = True
        config.locked_reason = reason
        config.locked_at = now
        config.save()
        
        # Lock all active requests
        active_requests = ServiceRequest.objects.filter(
            fk_service=config.fk_service,
            fk_organization=config.fk_organization,
            is_locked=False,
            is_locked_from_service=False
        ).exclude(status__in=['rejected', 'completed', 'cancelled'])
        
        locked_numbers = list(active_requests.values_list('request_number', flat=True))
        active_requests.update(
            is_locked=True,
            locked_reason=reason,
            locked_at=now,
            is_locked_from_service=True
        )
        
        return {
            'locked_count': len(locked_numbers),
            'locked_numbers': locked_numbers
        }
    
    @staticmethod
    def unlock_service(config: OrganizationServiceConfig) -> Dict:
        """
        Unlock service config and all requests locked by service.
        Returns info about unlocked requests.
        """
        from d_services.models.ServiceRequest import ServiceRequest
        
        config.is_locked = False
        config.locked_reason = None
        config.locked_at = None
        config.save()
        
        # Unlock all requests that were locked by this service
        locked_requests = ServiceRequest.objects.filter(
            fk_service=config.fk_service,
            fk_organization=config.fk_organization,
            is_locked=True,
            is_locked_from_service=True,
        )
        
        unlocked_numbers = list(locked_requests.values_list('request_number', flat=True))
        locked_requests.update(
            is_locked=False,
            locked_reason=None,
            locked_at=None,
            is_locked_from_service=False
        )
        
        return {
            'unlocked_count': len(unlocked_numbers),
            'unlocked_numbers': unlocked_numbers
        }
    
    @staticmethod
    def bulk_create_for_all_orgs(services_queryset=None) -> Dict:
        """
        Create OrganizationServiceConfig for all organizations for all active services.
        Skips existing configs.
        """
        from OpenSoftCoreV4.common.models.Branch import Organization
        
        all_orgs = list(Organization.objects.values_list('id', flat=True))
        all_services = services_queryset or Service.objects.filter(is_active=True)
        
        if not all_services.exists():
            raise BusinessRuleException(message=_('لا توجد خدمات نشطة'))
        
        created_configs = []
        skipped_count = 0
        
        with transaction.atomic():
            for service in all_services:
                existing_org_ids = set(
                    OrganizationServiceConfig.objects.filter(
                        fk_service=service,
                    ).values_list('fk_organization_id', flat=True)
                )
                
                new_org_ids = [org_id for org_id in all_orgs if org_id not in existing_org_ids]
                
                for org_id in new_org_ids:
                    config = OrganizationServiceConfig.objects.create(
                        fk_service=service,
                        fk_organization_id=org_id,
                        is_active=True
                    )
                    created_configs.append(config)
                
                skipped_count += len(existing_org_ids)
        
        return {
            'created_count': len(created_configs),
            'skipped_count': skipped_count,
            'total_orgs': len(all_orgs),
            'total_services': all_services.count()
        }
