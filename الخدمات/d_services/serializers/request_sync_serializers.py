"""
Serializers لمزامنة الطلبات — تصدير الطلب بكامل علاقاته
تُرسل FKs كـ ex_id. User FKs تُرسل كـ username.
"""
from rest_framework import serializers

from d_services.models.ServiceRequest import ServiceRequest
from d_services.models.RequestAction import RequestAction
from d_services.models.StageChecklistItem import StageChecklistItem
from d_services.models.RequestInstallment import RequestInstallment
from d_services.models.RequestAttachment import RequestAttachment
from d_services.models.RequestNote import RequestNote
from d_services.models.RequestReturnLog import RequestReturnLog


# ── helpers ─────────────────────────────────────────────────────

class _UserField(serializers.CharField):
    """حقل يحول FK user إلى username"""
    def __init__(self, source_field, **kw):
        kw.setdefault('read_only', True)
        kw.setdefault('allow_null', True)
        super().__init__(source=f'{source_field}.username', **kw)


# ── Leaf serializers ────────────────────────────────────────────


class SyncChecklistItemSerializer(serializers.ModelSerializer):
    checked_by_username = _UserField('fk_checked_by')

    class Meta:
        model = StageChecklistItem
        fields = [
            'ex_id', 'title', 'description', 'order',
            'is_checked', 'is_required', 'checked_at',
            'checked_by_username',
        ]


class SyncActionSerializer(serializers.ModelSerializer):
    workflow_step_ex_id = serializers.UUIDField(source='fk_workflow_step.ex_id', read_only=True)
    started_by_username = _UserField('fk_started_by')
    executed_by_username = _UserField('fk_executed_by')
    completed_by_username = _UserField('fk_completed_by')
    approved_by_username = _UserField('fk_approved_by')
    rejected_by_username = _UserField('fk_rejected_by')
    cancelled_by_username = _UserField('fk_cancelled_by')
    returned_by_username = _UserField('fk_returned_by')
    moved_to_next_by_username = _UserField('fk_moved_to_next_by')
    checklist_items = SyncChecklistItemSerializer(many=True, read_only=True)

    class Meta:
        model = RequestAction
        fields = [
            'ex_id', 'workflow_step_ex_id', 'order',
            'is_final_step', 'is_execution_step',
            'has_custom_output', 'has_custom_input', 'has_approval',
            'is_approved', 'is_executed',
            'custom_output_template', 'custom_input_template',
            'notes', 'note_recorded_at',
            'stage_status', 'stage_metadata', 'is_current',
            # timestamps & users
            'start_time', 'started_by_username',
            'executed_at', 'executed_by_username',
            'delivery_time', 'completed_by_username',
            'approved_at', 'approved_by_username',
            'rejected_at', 'rejected_by_username',
            'reject_reason',
            'cancelled_at', 'cancelled_by_username',
            'returned_at', 'returned_by_username',
            'returned_reason',
            'moved_to_next_at', 'moved_to_next_by_username',
            # children
            'checklist_items',
        ]


class SyncInstallmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestInstallment
        fields = [
            'ex_id', 'period', 'order', 'due_date',
            'payment_status', 'paid_at', 'amount',
        ]


class SyncAttachmentSerializer(serializers.ModelSerializer):
    uploaded_by_username = _UserField('fk_uploaded_by')

    class Meta:
        model = RequestAttachment
        fields = [
            'ex_id', 'name', 'description',
            'attachment_type', 'attachment_size', 'attachment_extension',
            'uploaded_at', 'uploaded_by_username',
        ]


class SyncNoteSerializer(serializers.ModelSerializer):
    created_by_username = _UserField('fk_created_by')

    class Meta:
        model = RequestNote
        fields = [
            'ex_id', 'content', 'created_by_username', 'created_at',
        ]


class SyncReturnLogSerializer(serializers.ModelSerializer):
    from_step_ex_id = serializers.UUIDField(source='fk_from_stage.ex_id', read_only=True)
    to_step_ex_id = serializers.UUIDField(source='fk_to_stage.ex_id', read_only=True, allow_null=True)
    returned_by_username = _UserField('fk_returned_by')

    class Meta:
        model = RequestReturnLog
        fields = [
            'ex_id', 'from_step_ex_id', 'to_step_ex_id',
            'return_reason', 'return_reason_details',
            'returned_at', 'returned_by_username',
            'is_resolved', 'resolution_notes', 'resolved_at',
        ]


# ── Top-level Request serializer ────────────────────────────────


class SyncRequestExportSerializer(serializers.ModelSerializer):
    """Serializer شامل لتصدير طلب خدمة بكامل علاقاته"""
    organization_ex_id = serializers.UUIDField(source='fk_organization.ex_id', read_only=True)
    service_ex_id = serializers.UUIDField(source='fk_service.ex_id', read_only=True)
    service_version_ex_id = serializers.UUIDField(
        source='fk_service_version.ex_id', read_only=True, allow_null=True
    )
    requester_username = _UserField('fk_requester')
    grant_source_ex_id = serializers.SerializerMethodField()
    grant_assigned_by_username = _UserField('grant_assigned_by')
    grant_cancel_by_username = _UserField('grant_cancel_by')
    grant_rejected_by_username = _UserField('grant_rejected_by')
    discount_by_username = _UserField('discount_by')
    discount_rejected_by_username = _UserField('discount_rejected_by')
    discount_canceled_by_username = _UserField('discount_canceled_by')

    actions = serializers.SerializerMethodField()
    installments = SyncInstallmentSerializer(many=True, read_only=True)
    attachments = serializers.SerializerMethodField()
    notes = serializers.SerializerMethodField()
    return_logs = serializers.SerializerMethodField()

    class Meta:
        model = ServiceRequest
        fields = [
            'ex_id', 'request_number',
            'organization_ex_id', 'service_ex_id', 'service_version_ex_id',
            'version_data',
            'target_audience_component', 'target_audience_data',
            'base_audience_component', 'base_component_data',
            'requested_at', 'start_request_at', 'final_delivery_date',
            'status', 'has_approvals',
            'output_template_type', 'input_template_type',
            'output_data_function', 'input_data_function',
            'request_source', 'requester_username',
            'requester_name', 'requester_description', 'requester_id',
            'priority',
            # Financial
            'total_fee', 'amount_paid', 'remaining_amount', 'payment_status',
            # ERP
            'is_donor_invoice_allowed', 'is_discount_allowed', 'is_internal_donors',
            'erp_product_id', 'erp_product_name',
            'erp_product_for_discount_id', 'erp_product_for_discount_name',
            'erp_product_for_internal_donors_id', 'erp_product_for_internal_donors_name',
            'erp_project_id', 'erp_project_name',
            'erp_activity_id', 'erp_activity_name',
            'erp_cost_center_id', 'erp_cost_center_name',
            # Grant
            'grant_status', 'grant_source_ex_id',
            'grant_amount', 'grant_percentage',
            'grant_assigned_at', 'grant_assigned_by_username',
            'grant_cancel_reason', 'grant_cancel_at', 'grant_cancel_by_username',
            'grant_rejected_reason', 'grant_rejected_at', 'grant_rejected_by_username',
            # Discount
            'discount_status', 'discounted_fee', 'discounted_fee_reason',
            'discount_amount', 'discount_reason', 'discount_at', 'discount_by_username',
            'discount_rejected_reason', 'discount_rejected_at', 'discount_rejected_by_username',
            'discount_canceled_reason', 'discount_canceled_at', 'discount_canceled_by_username',
            # Snapshots
            'workflow_stages_snapshot', 'prerequisites_snapshot',
            # Control
            'is_locked', 'locked_reason', 'locked_at',
            'is_locked_from_service',
            'reject_reason', 'reject_at',
            'cancel_reason', 'cancelled_at',
            # Children
            'actions', 'installments', 'attachments', 'notes', 'return_logs',
        ]

    def get_grant_source_ex_id(self, obj):
        gs = obj.fk_grant_source
        return str(gs.ex_id) if gs and hasattr(gs, 'ex_id') else None

    def get_actions(self, obj):
        qs = obj.actions.filter(is_deleted=False).select_related(
            'fk_workflow_step',
            'fk_started_by', 'fk_executed_by', 'fk_completed_by',
            'fk_approved_by', 'fk_rejected_by', 'fk_cancelled_by',
            'fk_returned_by', 'fk_moved_to_next_by',
        ).prefetch_related('checklist_items')
        return SyncActionSerializer(qs, many=True).data

    def get_attachments(self, obj):
        qs = obj.attachments.filter(is_deleted=False).select_related('fk_uploaded_by')
        return SyncAttachmentSerializer(qs, many=True).data

    def get_notes(self, obj):
        qs = obj.notes.filter(is_deleted=False).select_related('fk_created_by')
        return SyncNoteSerializer(qs, many=True).data

    def get_return_logs(self, obj):
        qs = obj.return_logs.filter(is_deleted=False).select_related(
            'fk_from_stage', 'fk_to_stage', 'fk_returned_by'
        )
        return SyncReturnLogSerializer(qs, many=True).data
