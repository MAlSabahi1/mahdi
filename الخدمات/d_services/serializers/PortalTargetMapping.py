"""
Serializer for PortalTargetMapping
"""
from rest_framework import serializers

from d_services.models.PortalTargetMapping import PortalTargetMapping
from config.imports.viewmodel_core import DynamicFieldsModelSerializer


class PortalTargetMappingSerializer(DynamicFieldsModelSerializer):
    """Serializer for PortalTargetMapping"""
    fk_service__name_ar = serializers.ReadOnlyField(
        source='fk_service.name_ar'
    )
    fk_service__code = serializers.ReadOnlyField(
        source='fk_service.code'
    )
    resolve_by__display = serializers.ReadOnlyField(
        source='get_resolve_by_display'
    )

    class Meta:
        model = PortalTargetMapping
        fields = '__all__'
        read_only_fields = ['id']
