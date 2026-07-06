"""
Log Serializers - Enhanced
Serializers for ServiceLog, RequestLog, WorkflowLog with advanced fields
"""
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

from d_services.models.ServiceLog import ServiceLog
from d_services.models.RequestLog import RequestLog
from d_services.models.WorkflowLog import WorkflowLog
from d_services.models.RequestReturnLog import RequestReturnLog
from config.imports.viewmodel_core import DynamicFieldsModelSerializer

class EnhancedServiceLogSerializer(DynamicFieldsModelSerializer):
    service_code = serializers.CharField(source='fk_service.code', read_only=True)
    service_name = serializers.CharField(source='fk_service.name_ar', read_only=True)
    user_name = serializers.CharField(source='fk_user.username', read_only=True, allow_null=True)
    user_full_name = serializers.SerializerMethodField()
    action_display = serializers.CharField(read_only=True)
    severity_display = serializers.CharField(read_only=True)
    reviewed_by_name = serializers.CharField(source='reviewed_by.username', read_only=True, allow_null=True)
    changes_count = serializers.IntegerField(read_only=True)
    is_critical = serializers.BooleanField(read_only=True)
    needs_review = serializers.BooleanField(read_only=True)
    duration_formatted = serializers.SerializerMethodField()
    
    class Meta:
        model = ServiceLog
        fields = [
            'id', 'fk_service', 'service_code', 'service_name',
            'action', 'action_display',
            'fk_user', 'user_name', 'user_full_name',
            'changes', 'old_values', 'new_values', 'affected_fields', 'changes_count',
            'timestamp', 'duration_ms', 'duration_formatted',
            'ip_address', 'request_path', 'request_method',
            'notes', 'severity', 'severity_display', 'is_critical',
            'is_flagged', 'flag_reason', 'needs_review',
            'reviewed_by', 'reviewed_by_name', 'reviewed_at', 'review_notes',
        ]
        read_only_fields = fields
    
    @extend_schema_field(str)
    def get_user_full_name(self, obj) -> str:
        if obj.fk_user:
            return f"{obj.fk_user.first_name} {obj.fk_user.last_name}".strip() or obj.fk_user.username
        return None
    
    @extend_schema_field(str)
    def get_duration_formatted(self, obj) -> str:
        if obj.duration_ms:
            if obj.duration_ms < 1000:
                return f"{obj.duration_ms}ms"
            return f"{obj.duration_ms / 1000:.2f}s"
        return None


class ServiceLogDetailSerializer(EnhancedServiceLogSerializer):
    related_version_code = serializers.CharField(source='related_version.version_code', read_only=True, allow_null=True)
    
    class Meta(EnhancedServiceLogSerializer.Meta):
        fields = EnhancedServiceLogSerializer.Meta.fields + [
            'session_id', 'request_id', 'user_agent',
            'related_version', 'related_version_code',
            'extra_data',
        ]


class ServiceLogStatisticsSerializer(DynamicFieldsModelSerializer):
    """Serializer لإحصائيات السجلات"""
    total_count = serializers.IntegerField()
    flagged_count = serializers.IntegerField()
    pending_review_count = serializers.IntegerField()
    by_action = serializers.DictField()
    by_severity = serializers.DictField()
    by_day = serializers.ListField()


class EnhancedRequestLogSerializer(DynamicFieldsModelSerializer):
    """Serializer محسن لسجلات الطلبات"""
    request_number = serializers.CharField(source='fk_request.request_number', read_only=True)
    service_code = serializers.CharField(source='fk_request.fk_service.code', read_only=True)
    service_name = serializers.CharField(source='fk_request.fk_service.name_ar', read_only=True)
    user_name = serializers.CharField(source='fk_user.username', read_only=True, allow_null=True)
    user_full_name = serializers.SerializerMethodField()
    action_display = serializers.CharField(read_only=True)
    severity_display = serializers.CharField(read_only=True)
    is_status_change = serializers.BooleanField(read_only=True)
    is_critical = serializers.BooleanField(read_only=True)
    needs_review = serializers.BooleanField(read_only=True)
    changes_count = serializers.IntegerField(read_only=True)
    related_stage_name = serializers.SerializerMethodField()
    duration_formatted = serializers.SerializerMethodField()
    
    class Meta:
        model = RequestLog
        fields = [
            'id', 'fk_request', 'request_number', 'service_code', 'service_name',
            'action', 'action_display',
            'fk_user', 'user_name', 'user_full_name',
            'changes', 'old_values', 'new_values', 'affected_fields', 'changes_count',
            'old_status', 'new_status', 'is_status_change',
            'old_payment_status', 'new_payment_status',
            'timestamp', 'duration_ms', 'duration_formatted',
            'ip_address',
            'notes', 'severity', 'severity_display', 'is_critical',
            'is_flagged', 'flag_reason', 'needs_review',
            'related_stage', 'related_stage_name',
        ]
        read_only_fields = fields
    
    @extend_schema_field(str)
    def get_user_full_name(self, obj) -> str:
        if obj.fk_user:
            return f"{obj.fk_user.first_name} {obj.fk_user.last_name}".strip() or obj.fk_user.username
        return None
    
    @extend_schema_field(str)
    def get_related_stage_name(self, obj) -> str:
        if obj.related_stage and hasattr(obj.related_stage, 'fk_workflow_step'):
            step = obj.related_stage.fk_workflow_step
            if hasattr(step, 'fk_stage'):
                return step.fk_stage.name_ar
        return None
    
    @extend_schema_field(str)
    def get_duration_formatted(self, obj) -> str:
        if obj.duration_ms:
            if obj.duration_ms < 1000:
                return f"{obj.duration_ms}ms"
            return f"{obj.duration_ms / 1000:.2f}s"
        return None


class RequestLogDetailSerializer(EnhancedRequestLogSerializer):
    """Serializer تفصيلي لسجل طلب واحد"""
    reviewed_by_name = serializers.CharField(source='reviewed_by.username', read_only=True, allow_null=True)
    
    class Meta(EnhancedRequestLogSerializer.Meta):
        fields = EnhancedRequestLogSerializer.Meta.fields + [
            'session_id', 'request_id', 'user_agent', 'request_path', 'request_method',
            'reviewed_by', 'reviewed_by_name', 'reviewed_at', 'review_notes',
            'rollback_data', 'extra_data',
        ]



class EnhancedWorkflowLogSerializer(DynamicFieldsModelSerializer):
    """Serializer محسن لسجلات سير العمل"""
    request_number = serializers.CharField(source='fk_request.request_number', read_only=True)
    service_code = serializers.CharField(source='fk_request.fk_service.code', read_only=True)
    user_name = serializers.CharField(source='fk_user.username', read_only=True, allow_null=True)
    user_full_name = serializers.SerializerMethodField()
    action_display = serializers.CharField(read_only=True)
    sla_status_display = serializers.CharField(read_only=True)
    from_stage_name = serializers.CharField(read_only=True)
    to_stage_name = serializers.CharField(read_only=True)
    stage_duration = serializers.FloatField(read_only=True)
    is_transition = serializers.BooleanField(read_only=True)
    duration_formatted = serializers.SerializerMethodField()
    
    class Meta:
        model = WorkflowLog
        fields = [
            'id', 'fk_request', 'request_number', 'service_code',
            'action', 'action_display', 'action_taken',
            'fk_from_stage', 'from_stage_name',
            'fk_to_stage', 'to_stage_name',
            'is_transition',
            'fk_user', 'user_name', 'user_full_name',
            'timestamp', 'started_at', 'completed_at',
            'duration_ms', 'duration_formatted', 'stage_duration',
            'sla_status', 'sla_status_display',
            'expected_duration_hours', 'actual_duration_hours',
            'is_overdue', 'overdue_hours',
            'notes', 'decision_notes',
            'severity', 'is_flagged', 'flag_reason',
        ]
        read_only_fields = fields
    
    @extend_schema_field(str)
    def get_user_full_name(self, obj) -> str:
        if obj.fk_user:
            return f"{obj.fk_user.first_name} {obj.fk_user.last_name}".strip() or obj.fk_user.username
        return None
    
    @extend_schema_field(str)
    def get_duration_formatted(self, obj) -> str:
        if obj.duration_ms:
            if obj.duration_ms < 1000:
                return f"{obj.duration_ms}ms"
            return f"{obj.duration_ms / 1000:.2f}s"
        return None


class WorkflowLogDetailSerializer(EnhancedWorkflowLogSerializer):
    """Serializer تفصيلي لسجل سير عمل واحد"""
    request_action_status = serializers.CharField(source='fk_request_action.status', read_only=True, allow_null=True)
    
    class Meta(EnhancedWorkflowLogSerializer.Meta):
        fields = EnhancedWorkflowLogSerializer.Meta.fields + [
            'session_id', 'fk_request_action', 'request_action_status',
            'input_data', 'output_data', 'extra_data',
        ]


class RequestReturnLogSerializer(DynamicFieldsModelSerializer):
    """Serializer لسجلات إرجاع الطلبات"""
    request_number = serializers.CharField(source='fk_request.request_number', read_only=True)
    returned_by_name = serializers.CharField(source='fk_returned_by.username', read_only=True, allow_null=True)
    from_stage_name = serializers.SerializerMethodField()
    to_stage_name = serializers.SerializerMethodField()
    
    class Meta:
        model = RequestReturnLog
        fields = [
            'id', 'fk_request', 'request_number',
            'fk_from_stage', 'from_stage_name',
            'fk_to_stage', 'to_stage_name',
            'return_reason', 'return_reason_details',
            'returned_at', 'fk_returned_by', 'returned_by_name',
            'is_resolved', 'resolution_notes', 'resolved_at'
        ]
        read_only_fields = fields
    
    @extend_schema_field(str)
    def get_from_stage_name(self, obj) -> str:
        if obj.fk_from_stage and hasattr(obj.fk_from_stage, 'fk_stage'):
            return obj.fk_from_stage.fk_stage.name_ar
        return None
    
    @extend_schema_field(str)
    def get_to_stage_name(self, obj) -> str:
        if obj.fk_to_stage and hasattr(obj.fk_to_stage, 'fk_stage'):
            return obj.fk_to_stage.fk_stage.name_ar
        return None


class ServiceLogSerializer(EnhancedServiceLogSerializer):
    """Alias للتوافق مع الكود القديم"""
    pass


class RequestLogSerializer(EnhancedRequestLogSerializer):
    """Alias للتوافق مع الكود القديم"""
    pass


class WorkflowLogSerializer(EnhancedWorkflowLogSerializer):
    """Alias للتوافق مع الكود القديم"""
    pass
