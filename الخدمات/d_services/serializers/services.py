from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.db import transaction

from d_services.models.Service import Service
from d_services.models.ServiceVersion import ServiceVersion
from d_services.models.ServiceInstallmentPlan import ServiceInstallmentPlan
from d_services.models.OrganizationServiceConfig import OrganizationServiceConfig
from d_services.models.ServicePrerequisite import ServicePrerequisite
from config.imports.viewmodel_core import  DynamicFieldsModelSerializer
from d_services.models.ServiceWorkflowStep import ServiceWorkflowStep
from d_services.models.WorkflowStage import WorkflowStage
from d_services.models.StageChecklistItem import WorkflowStepChecklistTemplate

class ServiceSerializer(DynamicFieldsModelSerializer):    
    category__display = serializers.ReadOnlyField(source='get_category_display')
    output_template_type__display = serializers.ReadOnlyField(source='get_output_template_type_display')
    input_template_type__display = serializers.ReadOnlyField(source='get_input_template_type_display')
    target_audience_component__display = serializers.ReadOnlyField(source='get_target_audience_component_display')
    base_audience_component__display = serializers.ReadOnlyField(source='get_base_audience_component_display')
    versions = serializers.SerializerMethodField()
    workflow_steps = serializers.SerializerMethodField()
    prerequisites = serializers.SerializerMethodField()
    is_locked = serializers.SerializerMethodField()
    locked_reason = serializers.SerializerMethodField()
    locked_at = serializers.SerializerMethodField()
    class Meta:
        model = Service
        fields = '__all__'
        read_only_fields = ['id', 'created_at']
    
    def get_versions(self, obj):
        versions = obj.versions.filter(is_deleted=False)
        return ServiceVersionSerializer(versions, many=True).data
    

    def get_workflow_steps(self, obj):
        steps = obj.workflow_steps.filter(is_deleted=False).order_by('order')
        return ServiceWorkflowStepSerializer(steps, many=True).data
    
    def get_prerequisites(self, obj):
        prereqs = obj.prerequisites.filter(is_deleted=False).order_by('order')
        return ServicePrerequisiteSerializer(prereqs, many=True).data
    
    def _get_org_config(self, obj):
        """Helper method to get organization service config from request context"""
        request = self.context.get('request')
        if not request or not hasattr(request, 'user'):
            return None
        user_org = getattr(request.user, 'fk_organization', None)
        if not user_org:
            return None
        return OrganizationServiceConfig.objects.filter(
            fk_service=obj, 
            fk_organization=user_org
        ).first()
    
    def get_is_locked(self, obj):
        config = self._get_org_config(obj)
        return config.is_locked if config else False
    
    def get_locked_reason(self, obj):
        config = self._get_org_config(obj)
        return config.locked_reason if config else None
    
    def get_locked_at(self, obj):
        config = self._get_org_config(obj)
        return config.locked_at if config else None
    

class ServiceVersionSerializer(DynamicFieldsModelSerializer):
    component_type__display = serializers.ReadOnlyField(source='get_component_type_display')
    fk_service__name_ar = serializers.ReadOnlyField(source='fk_service.name_ar')
    fk_service__code = serializers.ReadOnlyField(source='fk_service.code')
    fk_service__category__display = serializers.ReadOnlyField(source='fk_service.get_category_display')
    class Meta:
        model = ServiceVersion
        fields = '__all__'
        read_only_fields = ['id', 'created_at']
    
    def validate(self, attrs):
        if attrs.get('is_current', False):
            service = attrs.get('fk_service') or (self.instance.fk_service if self.instance else None)
            if service:
                current_version = service.versions.filter(is_current=True, is_deleted=False).first()
                if current_version and current_version != self.instance:
                    if current_version.requests.filter(
                        status__in=['pending', 'in_progress'],
                        is_deleted=False
                    ).exists():
                        raise serializers.ValidationError(
                            _("Current version has active requests")
                        )
        return attrs
    
    def create(self, validated_data):
        with transaction.atomic():
            if validated_data.get('is_current', False):
                service = validated_data.get('fk_service')
                ServiceVersion.objects.filter(
                    fk_service=service, is_current=True
                ).update(is_current=False)
            
            return super().create(validated_data)


class ServiceInstallmentPlanSerializer(DynamicFieldsModelSerializer):
    
    class Meta:
        model = ServiceInstallmentPlan
        fields = '__all__'
        read_only_fields = ['id']


class OrganizationServiceConfigSerializer(DynamicFieldsModelSerializer):
    fk_service__name_ar = serializers.ReadOnlyField(source='fk_service.name_ar')
    fk_organization__name_ar = serializers.ReadOnlyField(source='fk_organization.name_ar')
    fk_service__code = serializers.ReadOnlyField(source='fk_service.code')
    fk_service__category__display = serializers.ReadOnlyField(source='fk_service.get_category_display')
    fk_print_report_setting_for_input__name = serializers.ReadOnlyField(source='fk_print_report_setting_for_input.name')
    fk_print_report_setting_for_output__name = serializers.ReadOnlyField(source='fk_print_report_setting_for_output.name')
    installment_plans = serializers.SerializerMethodField()
    installment_period__display = serializers.ReadOnlyField(source='get_installment_period_display')

    fk_service = ServiceSerializer()

    class Meta:
        model = OrganizationServiceConfig
        fields = '__all__'
        read_only_fields = ['id']
    
    def get_installment_plans(self, obj):
        # Use prefetched data if available
        if hasattr(obj, '_prefetched_objects_cache') and 'installment_plans' in obj._prefetched_objects_cache:
            plans = [p for p in obj.installment_plans.all() if not p.is_deleted]
        else:
            plans = obj.installment_plans.filter(is_deleted=False)
        return ServiceInstallmentPlanSerializer(plans, many=True).data
    
    # def get_service(self, obj):
    #     """Return complete service data"""
    #     service = obj.fk_service
    #     if not service:
    #         return None
    #     return {
    #         'id': service.id,
    #         'code': service.code,
    #         'name_ar': service.name_ar,
    #         'name_en': service.name_en,
    #         'description': service.description,
    #         'icon': service.icon,
    #         'category': service.category,
    #         'category__display': service.get_category_display() if service.category else None,
    #         'is_active': service.is_active,
    #         'target_audience_component': service.target_audience_component,
    #         'target_audience_component__display': service.get_target_audience_component_display() if service.target_audience_component else None,
    #         'base_audience_component': service.base_audience_component,
    #         'base_audience_component__display': service.get_base_audience_component_display() if service.base_audience_component else None,
    #         'output_template_type': service.output_template_type,
    #         'output_template_type__display': service.get_output_template_type_display() if service.output_template_type else None,
    #         'input_template_type': service.input_template_type,
    #         'input_template_type__display': service.get_input_template_type_display() if service.input_template_type else None,
    #     }
    

class ActivateForOrganizationsSerializer(DynamicFieldsModelSerializer):
    organization_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False
    )
    
    def validate_organization_ids(self, value):
        return list(set(value))


class ServicePrerequisiteSerializer(DynamicFieldsModelSerializer):
    fk_service__name_ar = serializers.ReadOnlyField(source='fk_service.name_ar')
    fk_service__code = serializers.ReadOnlyField(source='fk_service.code')
    fk_service__category__display = serializers.ReadOnlyField(source='fk_service.get_category_display')
    class Meta:
        model = ServicePrerequisite
        fields = '__all__'
        read_only_fields = ['id']


class WorkflowStageSerializer(DynamicFieldsModelSerializer):
    stage_type__display = serializers.ReadOnlyField(source='get_stage_type_display')
    class Meta:
        model = WorkflowStage
        fields = '__all__'
        read_only_fields = ['id']



class ServiceWorkflowStepSerializer(DynamicFieldsModelSerializer):
    fk_stage__name_ar = serializers.ReadOnlyField(source='fk_stage.name_ar')
    fk_stage__name_en = serializers.ReadOnlyField(source='fk_stage.name_en')
    fk_stage__stage_type__display = serializers.ReadOnlyField(source='fk_stage.get_stage_type_display')
    fk_stage__stage_type = serializers.ReadOnlyField(source='fk_stage.stage_type')
    fk_service__name_ar = serializers.ReadOnlyField(source='fk_service.name_ar')
    fk_service__code = serializers.ReadOnlyField(source='fk_service.code')
    fk_service__category__display = serializers.ReadOnlyField(source='fk_service.get_category_display')
    custom_input_template__display = serializers.ReadOnlyField(source='get_custom_input_template_display')
    custom_output_template__display = serializers.ReadOnlyField(source='get_custom_output_template_display')
    
    class Meta:
        model = ServiceWorkflowStep
        fields = '__all__'
        read_only_fields = ['id']


class WorkflowStepChecklistTemplateSerializer(DynamicFieldsModelSerializer):
    fk_workflow_step__name_ar = serializers.ReadOnlyField(source='fk_workflow_step.name_ar')
    fk_workflow_step__name_en = serializers.ReadOnlyField(source='fk_workflow_step.name_en')
    fk_workflow_step__stage_type__display = serializers.ReadOnlyField(source='fk_workflow_step.get_stage_type_display')
    fk_workflow_step__stage_type = serializers.ReadOnlyField(source='fk_workflow_step.stage_type')
    fk_service__name_ar = serializers.ReadOnlyField(source='fk_service.name_ar')
    fk_service__code = serializers.ReadOnlyField(source='fk_service.code')
    fk_service__category__display = serializers.ReadOnlyField(source='fk_service.get_category_display')
    class Meta:
        model = WorkflowStepChecklistTemplate
        fields = '__all__'
        read_only_fields = ['id']


from d_services.models.WorkflowStepPrintReportSetting import WorkflowStepPrintReportSetting
class WorkflowStepPrintReportSettingSerializer(DynamicFieldsModelSerializer):
    """Serializer for WorkflowStepPrintReportSetting"""
    fk_workflow_step__order = serializers.ReadOnlyField(source='fk_workflow_step.order')
    fk_workflow_step__fk_stage__name_ar = serializers.ReadOnlyField(source='fk_workflow_step.fk_stage.name_ar')
    fk_workflow_step__fk_stage__name_en = serializers.ReadOnlyField(source='fk_workflow_step.fk_stage.name_en')
    fk_workflow_step__has_custom_output = serializers.ReadOnlyField(source='fk_workflow_step.has_custom_output')
    fk_workflow_step__has_custom_input = serializers.ReadOnlyField(source='fk_workflow_step.has_custom_input')
    fk_print_report_setting_for_output__name = serializers.ReadOnlyField(source='fk_print_report_setting_for_output.name')
    fk_print_report_setting_for_input__name = serializers.ReadOnlyField(source='fk_print_report_setting_for_input.name')
    fk_org_service_config__fk_service__name_ar = serializers.ReadOnlyField(source='fk_org_service_config.fk_service.name_ar')
    fk_org_service_config__fk_organization__name_ar = serializers.ReadOnlyField(source='fk_org_service_config.fk_organization.name_ar')
    
    class Meta:
        model = WorkflowStepPrintReportSetting
        fields = '__all__'
        read_only_fields = ['id']