
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from d_services.models.ServicePermission import ServicePermission
from d_services.models.GroupServicePermission import GroupServicePermission
from d_services.models.StagePermission import StagePermission
from config.imports.viewmodel_core import  DynamicFieldsModelSerializer


class ServicePermissionSerializer(DynamicFieldsModelSerializer):
    fk_service__code = serializers.ReadOnlyField(source='fk_service.code')
    fk_service__name_ar = serializers.ReadOnlyField(source='fk_service.name_ar')
    fk_service__name_en = serializers.ReadOnlyField(source='fk_service.name_en')
    permission_type__display = serializers.ReadOnlyField(source='get_permission_type_display')
    class Meta:
        model = ServicePermission
        fields = '__all__'
        read_only_fields = ['id']


class GroupServicePermissionSerializer(DynamicFieldsModelSerializer):
    fk_group__name_ar = serializers.ReadOnlyField(source='fk_group.name_ar')
    fk_group__name_en = serializers.ReadOnlyField(source='fk_group.name_en')
    fk_permission__permission_type__display = serializers.ReadOnlyField(source='fk_permission.get_permission_type_display')
    fk_permission__fk_service__code = serializers.ReadOnlyField(source='fk_permission.fk_service.code')
    fk_permission__fk_service__name_ar = serializers.ReadOnlyField(source='fk_permission.fk_service.name_ar')
    fk_permission__fk_service__name_en = serializers.ReadOnlyField(source='fk_permission.fk_service.name_en')
    class Meta:
        model = GroupServicePermission
        fields = '__all__'
        read_only_fields = ['id']


class StagePermissionSerializer(DynamicFieldsModelSerializer):
    fk_workflow_step_permission__fk_workflow_step__fk_stage__name_ar = serializers.ReadOnlyField(source='fk_workflow_step_permission.fk_workflow_step.fk_stage.name_ar')
    fk_workflow_step_permission__fk_workflow_step__fk_stage__name_en = serializers.ReadOnlyField(source='fk_workflow_step_permission.fk_workflow_step.fk_stage.name_en')
    fk_workflow_step_permission__fk_workflow_step__fk_service__code = serializers.ReadOnlyField(source='fk_workflow_step_permission.fk_workflow_step.fk_service.code')
    fk_workflow_step_permission__fk_workflow_step__fk_service__name_ar = serializers.ReadOnlyField(source='fk_workflow_step_permission.fk_workflow_step.fk_service.name_ar')
    fk_workflow_step_permission__fk_workflow_step__fk_service__name_en = serializers.ReadOnlyField(source='fk_workflow_step_permission.fk_workflow_step.fk_service.name_en')
    fk_user__username = serializers.ReadOnlyField(source='fk_user.username')
    fk_user__first_name = serializers.ReadOnlyField(source='fk_user.first_name')
    fk_user__last_name = serializers.ReadOnlyField(source='fk_user.last_name')
    fk_workflow_step_permission__permission_type__display = serializers.ReadOnlyField(source='fk_workflow_step_permission.get_permission_type_display')
    fk_workflow_step_permission__permission_type = serializers.ReadOnlyField(source='fk_workflow_step_permission.permission_type')
    
    class Meta:
        model = StagePermission
        fields = '__all__'
        read_only_fields = ['id']


class ServicePermissionSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = ServicePermission
        fields = '__all__'
