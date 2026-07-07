from rest_framework import serializers
from systems.services.models import (
    ServiceCatalog, 
    ServicePrerequisite, 
    ChecklistTemplate,
    FormNote,
    FormEventLog,
    FormReturnLog,
    FormChecklist,
    StatusChangeForm,
    WorkflowStage,
    ServiceWorkflowStep
)
from django.contrib.auth import get_user_model

User = get_user_model()


class ServicePrerequisiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicePrerequisite
        fields = ['id', 'service', 'name_ar', 'description', 'validation_type', 'validation_value', 'is_mandatory', 'order']


class ChecklistTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChecklistTemplate
        fields = ['id', 'stage', 'title', 'description', 'is_required', 'order']


class WorkflowStageSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkflowStage
        fields = ['id', 'code', 'name_ar', 'description', 'icon', 'is_active']


class ServiceWorkflowStepSerializer(serializers.ModelSerializer):
    stage_details = WorkflowStageSerializer(source='stage', read_only=True)
    
    class Meta:
        model = ServiceWorkflowStep
        fields = [
            'id', 'service', 'stage', 'stage_details', 'order', 'description', 
            'is_final_step', 'is_execution_step', 'requires_approval'
        ]


class ServiceCatalogSerializer(serializers.ModelSerializer):
    prerequisites = ServicePrerequisiteSerializer(many=True, read_only=True)
    checklist_templates = ChecklistTemplateSerializer(many=True, read_only=True)
    workflow_steps = ServiceWorkflowStepSerializer(many=True, read_only=True)
    approval_type_display = serializers.CharField(source='get_approval_type_display', read_only=True)
    service_type_display = serializers.CharField(source='get_service_type_display', read_only=True)

    class Meta:
        model = ServiceCatalog
        fields = [
            'id', 'code', 'name_ar', 'description', 'category', 'icon', 'form_type',
            'approval_type', 'approval_type_display', 'service_type', 'service_type_display',
            'is_active', 'requires_approval', 'is_repeatable', 'is_locked', 'lock_reason',
            'expected_duration_hours',
            'attachments_count', 'target_audience', 'fields_schema', 'sort_order',
            'prerequisites', 'checklist_templates', 'workflow_steps'
        ]


class FormNoteSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)

    class Meta:
        model = FormNote
        fields = ['id', 'content', 'created_by', 'created_by_name', 'created_at']
        read_only_fields = ['created_by', 'created_at']


class FormEventLogSerializer(serializers.ModelSerializer):
    performed_by_name = serializers.CharField(source='performed_by.get_full_name', read_only=True)
    action_display = serializers.CharField(source='get_action_display', read_only=True)
    sla_status_display = serializers.CharField(source='get_sla_status_display', read_only=True)

    class Meta:
        model = FormEventLog
        fields = [
            'id', 'action', 'action_display', 'from_status', 'to_status', 
            'performed_by', 'performed_by_name', 'notes', 
            'expected_duration_hours', 'actual_duration_hours', 'sla_status', 
            'sla_status_display', 'is_overdue', 'created_at'
        ]


class FormReturnLogSerializer(serializers.ModelSerializer):
    returned_by_name = serializers.CharField(source='returned_by.get_full_name', read_only=True)
    return_reason_display = serializers.CharField(source='get_return_reason_display', read_only=True)

    class Meta:
        model = FormReturnLog
        fields = [
            'id', 'return_reason', 'return_reason_display', 'return_details',
            'from_status', 'to_status', 'returned_by', 'returned_by_name',
            'is_resolved', 'resolution_notes', 'resolved_at', 'created_at'
        ]


class FormChecklistSerializer(serializers.ModelSerializer):
    checked_by_name = serializers.CharField(source='checked_by.get_full_name', read_only=True)

    class Meta:
        model = FormChecklist
        fields = [
            'id', 'title', 'description', 'stage', 'is_required', 
            'is_checked', 'checked_by', 'checked_by_name', 'checked_at', 'order'
        ]
        read_only_fields = ['checked_by', 'checked_at']
