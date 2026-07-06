"""
Serializer for ServiceRequestSync
"""
from rest_framework import serializers
from d_services.models.ServiceRequestSync import ServiceRequestSync


class ServiceRequestSyncSerializer(serializers.ModelSerializer):
    """Serializer for ServiceRequestSync — used in export API"""
    service_code = serializers.ReadOnlyField(
        source='fk_service_request.fk_service.code'
    )
    service_name = serializers.ReadOnlyField(
        source='fk_service_request.fk_service.name_ar'
    )
    organization_ex_id = serializers.SerializerMethodField()
    request_number = serializers.ReadOnlyField(
        source='fk_service_request.request_number'
    )
    
    # بيانات الطلب الأصلية
    target_audience_data = serializers.ReadOnlyField(
        source='fk_service_request.target_audience_data'
    )
    base_component_data = serializers.ReadOnlyField(
        source='fk_service_request.base_component_data'
    )
    requester_name = serializers.ReadOnlyField(
        source='fk_service_request.requester_name'
    )
    requester_id = serializers.ReadOnlyField(
        source='fk_service_request.requester_id'
    )
    requester_description = serializers.ReadOnlyField(
        source='fk_service_request.requester_description'
    )
    version_data = serializers.ReadOnlyField(
        source='fk_service_request.version_data'
    )
    priority = serializers.ReadOnlyField(
        source='fk_service_request.priority'
    )
    
    # Display labels
    school_display = serializers.ReadOnlyField(source='get_school_display')
    university_display = serializers.ReadOnlyField(source='get_university_display')
    institute_display = serializers.ReadOnlyField(source='get_institute_display')
    
    class Meta:
        model = ServiceRequestSync
        fields = [
            'id', 'fk_service_request', 'portal_request_id',
            'service_code', 'service_name', 'organization_ex_id',
            'request_number',
            'target_audience_data', 'base_component_data',
            'requester_name', 'requester_id', 'requester_description',
            'version_data', 'priority',
            'school', 'university', 'institute',
            'school_display', 'university_display', 'institute_display',
            'school_error', 'university_error', 'institute_error',
            'last_sync_attempt',
        ]
    
    def get_organization_ex_id(self, obj):
        org = obj.fk_service_request.fk_organization
        return str(org.ex_id) if hasattr(org, 'ex_id') else None
