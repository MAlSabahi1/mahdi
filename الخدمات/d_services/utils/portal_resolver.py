"""
Portal Target Resolver - محرك تحويل حقول البوابة إلى حقول QAS
"""
import logging
from django.apps import apps
from django.utils.translation import gettext_lazy as _

from d_services.models.PortalTargetMapping import PortalTargetMapping
from d_services.choices.choices import ResolveByChoice

logger = logging.getLogger(__name__)


# ========================================
# Custom Resolvers Registry
# ========================================
# أضف دوال تحويل مخصصة هنا
CUSTOM_RESOLVERS = {}


def register_resolver(name):
    """Decorator لتسجيل دالة تحويل مخصصة"""
    def decorator(func):
        CUSTOM_RESOLVERS[name] = func
        return func
    return decorator


def get_custom_resolver(name):
    """جلب دالة تحويل مخصصة بالاسم"""
    resolver = CUSTOM_RESOLVERS.get(name)
    if not resolver:
        raise ValueError(f'Custom resolver "{name}" not found. Available: {list(CUSTOM_RESOLVERS.keys())}')
    return resolver


# ========================================
# App Label Registry for Models
# ========================================
# ربط أسماء الموديلات بـ app_label
MODEL_APP_LABELS = {
    'College': 'system_management',
    'Section': 'system_management',
    'Specialization': 'system_management',
    'Batch': 'student_affairs',
    'Level': 'student_affairs',
    'StudentBatch': 'student_affairs',
    'StudentLevel': 'student_affairs',
}


def _get_model(model_name):
    """جلب Model class من الاسم"""
    app_label = MODEL_APP_LABELS.get(model_name)
    if app_label:
        return apps.get_model(app_label, model_name)
    
    # البحث في جميع التطبيقات
    for app_config in apps.get_app_configs():
        try:
            return apps.get_model(app_config.label, model_name)
        except LookupError:
            continue
    raise LookupError(f'Model "{model_name}" not found in any app')


class PortalTargetResolver:
    """
    محرك تحويل بيانات Target من البوابة إلى QAS
    يقرأ خريطة الربط من PortalTargetMapping ويحول البيانات
    """
    
    @staticmethod
    def resolve(service, portal_data):
        """
        يحول portal_data → qas_target_data
        الربط مشترك لكل المنظمات (على مستوى الخدمة)
        
        Args:
            service: Service instance
            portal_data: dict من بيانات البوابة {portal_field_name: value, ...}
        
        Returns:
            dict: بيانات QAS المحولة {qas_field_name: qas_id, ...}
        """
        mappings = PortalTargetMapping.objects.filter(
            fk_service=service, is_deleted=False
        ).order_by('field_order')
        
        if not mappings.exists():
            logger.warning(f'No portal target mappings found for service: {service.code}')
            return {}
        
        qas_data = {}
        errors = []
        
        for mapping in mappings:
            portal_value = portal_data.get(mapping.portal_field_name)
            if portal_value is None:
                logger.debug(f'Portal field "{mapping.portal_field_name}" not found in data')
                continue
            
            try:
                resolved_value = PortalTargetResolver._resolve_field(mapping, portal_value)
                qas_data[mapping.qas_field_name] = resolved_value
            except Exception as e:
                error_msg = (
                    f'Failed to resolve {mapping.portal_field_name} → '
                    f'{mapping.qas_field_name}: {str(e)}'
                )
                logger.error(error_msg)
                errors.append(error_msg)
        
        if errors:
            logger.warning(f'Portal resolve completed with {len(errors)} errors for service {service.code}')
        
        return qas_data
    
    @staticmethod
    def _resolve_field(mapping, portal_value):
        """تحويل قيمة حقل واحد"""
        
        if mapping.resolve_by == ResolveByChoice.DIRECT:
            return portal_value
        
        elif mapping.resolve_by == ResolveByChoice.EX_ID:
            Model = _get_model(mapping.qas_model_name)
            obj = Model.objects.filter(
                **{mapping.resolve_field: portal_value}
            ).first()
            if obj is None:
                raise ValueError(
                    f'{mapping.qas_model_name} with {mapping.resolve_field}='
                    f'"{portal_value}" not found'
                )
            return obj.id
        
        elif mapping.resolve_by == ResolveByChoice.CODE:
            Model = _get_model(mapping.qas_model_name)
            obj = Model.objects.filter(code=portal_value).first()
            if obj is None:
                raise ValueError(
                    f'{mapping.qas_model_name} with code="{portal_value}" not found'
                )
            return obj.id
        
        elif mapping.resolve_by == ResolveByChoice.CUSTOM:
            if not mapping.custom_resolver:
                raise ValueError('custom_resolver name is required for CUSTOM resolve_by')
            resolver_fn = get_custom_resolver(mapping.custom_resolver)
            return resolver_fn(portal_value, mapping)
        
        else:
            raise ValueError(f'Unknown resolve_by: {mapping.resolve_by}')
