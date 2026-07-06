from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from d_services.models.AudienceConditionVerification import AudienceConditionVerification
from d_services.serializers.base import BaseModelSerializer, OrganizationFilteredSerializer


class AudienceConditionVerificationSerializer(OrganizationFilteredSerializer):
    prerequisite_name = serializers.CharField(source='fk_prerequisite.name', read_only=True)
    prerequisite_status = serializers.CharField(source='fk_prerequisite.status', read_only=True)
    
    class Meta:
        model = AudienceConditionVerification
        fields = [
            'id', 'fk_request', 'fk_prerequisite', 'fk_organization',
            'prerequisite_name', 'prerequisite_status',
            'is_satisfied', 'verification_result',
            'verified_at', 'fk_verified_by', 'notes'
        ]
        read_only_fields = ['id', 'verified_at']


class VerifyPrerequisitesSerializer(serializers.Serializer):
    force_recheck = serializers.BooleanField(default=False)
