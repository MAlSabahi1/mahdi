from rest_framework import serializers

from d_services.models.ServiceERPSettings import ServiceERPSettings
from config.imports.viewmodel_core import DynamicFieldsModelSerializer


class ServiceERPSettingsSerializer(DynamicFieldsModelSerializer):
    """Serializer for ServiceERPSettings"""
    fk_org_service_config__fk_service__name_ar = serializers.ReadOnlyField(
        source='fk_org_service_config.fk_service.name_ar'
    )
    fk_org_service_config__fk_service__code = serializers.ReadOnlyField(
        source='fk_org_service_config.fk_service.code'
    )
    fk_org_service_config__fk_organization__name_ar = serializers.ReadOnlyField(
        source='fk_org_service_config.fk_organization.name_ar'
    )

    class Meta:
        model = ServiceERPSettings
        fields = '__all__'
        read_only_fields = ['id']
