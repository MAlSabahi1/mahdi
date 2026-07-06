"""
Serializers لمزامنة الخدمات — تصدير واستيراد الخدمة بكامل علاقاتها
تُستخدم في Server API (تصدير) و Client API (استيراد)
"""
from rest_framework import serializers

from d_services.models.Service import Service
from d_services.models.OrganizationServiceConfig import OrganizationServiceConfig
from d_services.models.ServiceERPSettings import ServiceERPSettings
from d_services.models.ServiceInstallmentPlan import ServiceInstallmentPlan
from d_services.models.ServicePrerequisite import ServicePrerequisite
from d_services.models.ServiceVersion import ServiceVersion
from d_services.models.ServiceWorkflowStep import ServiceWorkflowStep
from d_services.models.ServiceWorkFlowStepPermission import ServiceWorkFlowStepPermission
from d_services.models.StageChecklistItem import WorkflowStepChecklistTemplate
from d_services.models.WorkflowStage import WorkflowStage
from d_services.models.WorkflowStepPrintReportSetting import WorkflowStepPrintReportSetting


# ── Leaf serializers (no nested children) ──────────────────────


class SyncWorkflowStageSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkflowStage
        fields = [
            'ex_id', 'name_ar', 'name_en', 'stage_type',
            'is_final_stage', 'is_execution_stage', 'expected_duration_days',
        ]


class SyncServicePrerequisiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicePrerequisite
        fields = [
            'ex_id', 'name_ar', 'name_en', 'description',
            'status', 'validation_procedure_name', 'order',
        ]


class SyncServiceVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceVersion
        fields = [
            'ex_id', 'version_name', 'component_type',
            'is_current', 'fields_schema', 'is_locked',
        ]


class SyncStepPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceWorkFlowStepPermission
        fields = ['ex_id', 'permission_type']


class SyncWorkflowStepSerializer(serializers.ModelSerializer):
    permissions = SyncStepPermissionSerializer(many=True, read_only=True)
    stage_ex_id = serializers.UUIDField(source='fk_stage.ex_id', read_only=True)

    class Meta:
        model = ServiceWorkflowStep
        fields = [
            'ex_id', 'stage_ex_id', 'order', 'description',
            'is_final_step', 'is_execution_step',
            'has_custom_output', 'has_approval',
            'custom_output_template', 'custom_output_function',
            'has_custom_input', 'custom_input_template', 'custom_input_function',
            'start_offset_days', 'delivery_offset_days',
            'execution_procedure_name', 'icon',
            'permissions',
        ]


# ── OrganizationServiceConfig children ─────────────────────────


class SyncInstallmentPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceInstallmentPlan
        fields = ['ex_id', 'amount', 'order', 'due_days_from_request']


class SyncERPSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceERPSettings
        fields = [
            'ex_id', 'specialization_id', 'study_system_id',
            'service_fee',
            'is_donor_invoice_allowed', 'is_discount_allowed',
            'erp_product_id', 'erp_product_name',
            'erp_product_for_discount_id', 'erp_product_for_discount_name',
            'erp_product_for_internal_donors_id', 'erp_product_for_internal_donors_name',
            'erp_project_id', 'erp_project_name',
            'erp_activity_id', 'erp_activity_name',
            'erp_cost_center_id', 'erp_cost_center_name',
        ]


class SyncChecklistTemplateSerializer(serializers.ModelSerializer):
    workflow_step_ex_id = serializers.UUIDField(
        source='fk_workflow_step.ex_id', read_only=True
    )

    class Meta:
        model = WorkflowStepChecklistTemplate
        fields = [
            # 'ex_id', 
            'workflow_step_ex_id',
            'title', 'description', 'order', 'is_required',
        ]


class SyncPrintReportSettingSerializer(serializers.ModelSerializer):
    workflow_step_ex_id = serializers.UUIDField(
        source='fk_workflow_step.ex_id', read_only=True
    )

    class Meta:
        model = WorkflowStepPrintReportSetting
        fields = [
            'ex_id', 'workflow_step_ex_id',
        ]


class SyncOrgConfigSerializer(serializers.ModelSerializer):
    organization_ex_id = serializers.UUIDField(
        source='fk_organization.ex_id', read_only=True
    )
    currency_id = serializers.IntegerField(
        source='fk_currency_id', read_only=True, allow_null=True
    )
    installment_plans = SyncInstallmentPlanSerializer(many=True, read_only=True)
    erp_settings = SyncERPSettingsSerializer(
        source='service_specialization_settings', many=True, read_only=True
    )
    checklist_templates = SyncChecklistTemplateSerializer(many=True, read_only=True)
    print_report_settings = serializers.SerializerMethodField()

    class Meta:
        model = OrganizationServiceConfig
        fields = [
            'ex_id', 'organization_ex_id', 'currency_id',
            'is_installment_allowed', 'installments_count',
            'is_paid', 'free_limit_per_year', 'fee_amount',
            'installment_period', 'request_prefix',
            'is_active', 'is_locked', 'locked_reason',
            # ERP fields
            'is_donor_invoice_allowed', 'is_discount_allowed',
            'erp_product_id', 'erp_product_name',
            'erp_product_for_discount_id', 'erp_product_for_discount_name',
            'erp_product_for_internal_donors_id', 'erp_product_for_internal_donors_name',
            'erp_project_id', 'erp_project_name',
            'erp_activity_id', 'erp_activity_name',
            'erp_cost_center_id', 'erp_cost_center_name',
            # Nested
            'installment_plans', 'erp_settings',
            'checklist_templates', 'print_report_settings',
        ]

    def get_print_report_settings(self, obj):
        qs = obj.workflow_step_print_settings.filter(is_deleted=False)
        return SyncPrintReportSettingSerializer(qs, many=True).data


# ── Top-level Service serializer ────────────────────────────────


class SyncServiceExportSerializer(serializers.ModelSerializer):
    """Serializer شامل لتصدير خدمة بكامل علاقاتها"""
    workflow_stages = serializers.SerializerMethodField()
    prerequisites = SyncServicePrerequisiteSerializer(many=True, read_only=True)
    versions = SyncServiceVersionSerializer(many=True, read_only=True)
    workflow_steps = serializers.SerializerMethodField()
    org_configs = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = [
            'ex_id', 'code', 'name_ar', 'name_en', 'description',
            'category', 'icon',
            'requires_approval', 'is_repeatable', 'is_active',
            'start_date',
            'output_template_type', 'input_template_type',
            'output_data_function', 'input_data_function',
            'erp_data_function',
            'erp_specialization_data_autolist', 'erp_study_system_data_autolist',
            'target_audience_component', 'base_audience_component',
            'requester_image_function', 'requester_info_function',
            'target_system_type',
            # Nested
            'workflow_stages', 'prerequisites', 'versions',
            'workflow_steps', 'org_configs',
        ]

    def get_workflow_stages(self, service):
        """جلب كل WorkflowStage المستخدمة في خطوات هذه الخدمة"""
        stage_ids = service.workflow_steps.filter(
            is_deleted=False
        ).values_list('fk_stage_id', flat=True).distinct()
        stages = WorkflowStage.objects.filter(id__in=stage_ids)
        return SyncWorkflowStageSerializer(stages, many=True).data

    def get_workflow_steps(self, service):
        qs = service.workflow_steps.filter(is_deleted=False).select_related(
            'fk_stage'
        ).prefetch_related('permissions')
        return SyncWorkflowStepSerializer(qs, many=True).data

    def get_org_configs(self, service):
        qs = service.org_configs.filter(is_deleted=False).select_related(
            'fk_organization', 'fk_currency'
        ).prefetch_related(
            'installment_plans',
            'service_specialization_settings',
            'checklist_templates',
            'workflow_step_print_settings',
        )
        return SyncOrgConfigSerializer(qs, many=True).data
