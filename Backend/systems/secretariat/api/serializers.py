from rest_framework import serializers
from ..models import Correspondence, Task, Circular
from systems.personnel.models import PersonnelMaster
from core.models import SecurityAdministration

class CorrespondenceSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    security_admin_name = serializers.CharField(source='security_admin.name', read_only=True)
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Correspondence
        fields = '__all__'
        read_only_fields = ('created_by', 'security_admin')

class TaskSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.full_name', read_only=True)
    security_admin_name = serializers.CharField(source='security_admin.name', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('created_by', 'security_admin')

class CircularSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    security_admin_name = serializers.CharField(source='security_admin.name', read_only=True)

    class Meta:
        model = Circular
        fields = '__all__'
        read_only_fields = ('created_by', 'security_admin')
