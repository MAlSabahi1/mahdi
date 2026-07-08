from rest_framework import serializers
from ..models import ExportRequest
from django.contrib.auth import get_user_model

User = get_user_model()

class ExportRequestSerializer(serializers.ModelSerializer):
    requested_by_name = serializers.CharField(source='requested_by.get_full_name', read_only=True)
    approved_by_name = serializers.CharField(source='approved_by.get_full_name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = ExportRequest
        fields = [
            'id', 'report_id', 'report_name', 'requested_by', 'requested_by_name',
            'reason', 'status', 'status_display', 'approved_by', 'approved_by_name',
            'approval_notes', 'created_at', 'updated_at', 'expires_at'
        ]
        read_only_fields = ['requested_by', 'status', 'approved_by', 'approval_notes', 'expires_at']
