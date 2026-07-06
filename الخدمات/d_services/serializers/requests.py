from OpenSoftCoreV4.utils.classes.serializers import DynamicFieldsModelSerializer
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from d_services.models.GrantSource import GrantSource
from d_services.models.ServiceCallResult import ServiceCallResult
from d_services.models.ServiceRequest import ServiceRequest
from d_services.models.RequestInstallment import RequestInstallment
from d_services.models.RequestAction import RequestAction
from d_services.models.RequestAttachment import RequestAttachment
from d_services.models.RequestNote import RequestNote
from d_services.models.StageChecklistItem import StageChecklistItem
from d_services.serializers.GrantSource import GrantSourceSerializer
from middleware_system.serializers.Invoice import ERPInvoiceSerializer


class ServiceCallResultSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model=ServiceCallResult
        fields = "__all__"
        
class ServiceRequestSerializer(DynamicFieldsModelSerializer):
    attachments = serializers.SerializerMethodField()
    action_steps = serializers.SerializerMethodField()
    installments = serializers.SerializerMethodField()
    notes_count = serializers.SerializerMethodField()
    
    fk_service__code = serializers.ReadOnlyField(source='fk_service.code')
    fk_service__name_ar = serializers.ReadOnlyField(source='fk_service.name_ar')
    fk_service__name_en = serializers.ReadOnlyField(source='fk_service.name_en')
    fk_service__category__display = serializers.ReadOnlyField(source='fk_service.get_category_display')
    fk_service__icon = serializers.ReadOnlyField(source='fk_service.icon')
    
    fk_service_version__version_number = serializers.ReadOnlyField(source='fk_service_version.version_number')
    fk_service_version__is_current = serializers.ReadOnlyField(source='fk_service_version.is_current')
    
    fk_organization__name_ar = serializers.ReadOnlyField(source='fk_organization.name_ar')
    fk_organization__name_en = serializers.ReadOnlyField(source='fk_organization.name_en')
    fk_organization__code = serializers.ReadOnlyField(source='fk_organization.code')
    
    fk_requester__username = serializers.ReadOnlyField(source='fk_requester.username')
    fk_requester__first_name = serializers.ReadOnlyField(source='fk_requester.first_name')
    fk_requester__last_name = serializers.ReadOnlyField(source='fk_requester.last_name')
    fk_requester__email = serializers.ReadOnlyField(source='fk_requester.email')

    status__display = serializers.ReadOnlyField(source='get_status_display')
    payment_status__display = serializers.ReadOnlyField(source='get_payment_status_display')
    request_source__display = serializers.ReadOnlyField(source='get_request_source_display')
    priority__display = serializers.ReadOnlyField(source='get_priority_display')
    
    grant_status__display = serializers.ReadOnlyField(source='get_grant_status_display')
    fk_grant_source__name_ar = serializers.ReadOnlyField(source='fk_grant_source.name_ar')
    fk_grant_source__name_en = serializers.ReadOnlyField(source='fk_grant_source.name_en')
    
    discount_status__display = serializers.ReadOnlyField(source='get_discount_status_display')

    invoices_data = serializers.ReadOnlyField()

    func_call_results_input_data = serializers.SerializerMethodField()
    func_call_results_output_data = serializers.SerializerMethodField()

    def get_func_call_results_input_data(self,obj):
        func = obj.requests.filter(func=obj.input_data_function)
        return getattr(func.first(), 'result') if func else None

    def get_func_call_results_output_data(self,obj):
        func = obj.requests.filter(func=obj.output_data_function)
        return getattr(func.first(), 'result') if func else None


    class Meta:
        model = ServiceRequest
        fields ='__all__'
        read_only_fields = ['id', 'request_number', 'requested_at']


    def get_attachments(self, obj):
        # Use prefetched data - filter in Python instead of DB to avoid N+1
        if hasattr(obj, '_prefetched_objects_cache') and 'attachments' in obj._prefetched_objects_cache:
            attachments = [a for a in obj.attachments.all() if not a.is_deleted]
        else:
            attachments = obj.attachments.filter(is_deleted=False)
        return RequestAttachmentSerializer(attachments, many=True).data

    def get_action_steps(self, obj):
        # Use prefetched actions - already ordered by queryset
        actions = obj.actions.all()
        return RequestActionSerializer(actions, many=True).data
    
    def get_installments(self, obj):
        # Use prefetched data - filter in Python instead of DB to avoid N+1
        if hasattr(obj, '_prefetched_objects_cache') and 'installments' in obj._prefetched_objects_cache:
            installments = [i for i in obj.installments.all() if not i.is_deleted]
        else:
            installments = obj.installments.filter(is_deleted=False)
        return RequestInstallmentSerializer(installments, many=True).data
    
    def get_notes_count(self, obj):
        # Use annotation if available, otherwise query
        if hasattr(obj, 'notes_count_annotation'):
            return obj.notes_count_annotation
        return obj.notes.filter(is_deleted=False).count()


class RequestInstallmentSerializer(DynamicFieldsModelSerializer):
    currency = serializers.ReadOnlyField(source='fk_request.currency')
    grant_amount = serializers.ReadOnlyField()
    discount_amount = serializers.ReadOnlyField()
    due_amount = serializers.ReadOnlyField()

    class Meta:
        model = RequestInstallment
        fields ='__all__'
        read_only_fields = ['id', 'paid_at']

class RequestAttachmentSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = RequestAttachment
        fields ='__all__'
        read_only_fields = ['id', 'uploaded_at', 'fk_uploaded_by']


class StageChecklistItemSerializer(DynamicFieldsModelSerializer):
    """Serializer for stage checklist items"""
    fk_checked_by__username = serializers.ReadOnlyField(source='fk_checked_by.username')
    fk_checked_by__first_name = serializers.ReadOnlyField(source='fk_checked_by.first_name')
    fk_checked_by__last_name = serializers.ReadOnlyField(source='fk_checked_by.last_name')
    fk_checked_by__image_user = serializers.ImageField(source='fk_checked_by.image_user',read_only=True)

    class Meta:
        model = StageChecklistItem
        fields = '__all__'
        read_only_fields = ['id', 'checked_at', 'fk_checked_by']


class RequestActionSerializer(DynamicFieldsModelSerializer):
    fk_request__request_number = serializers.ReadOnlyField(source='fk_request.request_number')
    fk_workflow_step__fk_stage__name_ar = serializers.ReadOnlyField(source='fk_workflow_step.fk_stage.name_ar')
    fk_workflow_step__icon = serializers.ReadOnlyField(source='fk_workflow_step.icon')
    fk_workflow_step__name_ar = serializers.ReadOnlyField(source='fk_workflow_step.name_ar')
    fk_workflow_step__order = serializers.ReadOnlyField(source='fk_workflow_step.order')
    stage_status__display = serializers.ReadOnlyField(source='get_stage_status_display')
    
    fk_started_by__username = serializers.ReadOnlyField(source='fk_started_by.username')
    fk_started_by__image_user = serializers.ImageField(source='fk_started_by.image_user',read_only=True)
    fk_started_by__first_name = serializers.ReadOnlyField(source='fk_started_by.first_name')
    fk_started_by__last_name = serializers.ReadOnlyField(source='fk_started_by.last_name')

    fk_executed_by__username = serializers.ReadOnlyField(source='fk_executed_by.username')
    fk_executed_by__image_user = serializers.ImageField(source='fk_executed_by.image_user',read_only=True)
    fk_executed_by__first_name = serializers.ReadOnlyField(source='fk_executed_by.first_name')
    fk_executed_by__last_name = serializers.ReadOnlyField(source='fk_executed_by.last_name')

    fk_completed_by__username = serializers.ReadOnlyField(source='fk_completed_by.username')
    fk_completed_by__image_user = serializers.ImageField(source='fk_completed_by.image_user',read_only=True)
    fk_completed_by__first_name = serializers.ReadOnlyField(source='fk_completed_by.first_name')
    fk_completed_by__last_name = serializers.ReadOnlyField(source='fk_completed_by.last_name')

    fk_approved_by__username = serializers.ReadOnlyField(source='fk_approved_by.username')
    fk_approved_by__image_user = serializers.ImageField(source='fk_approved_by.image_user',read_only=True)
    fk_approved_by__first_name = serializers.ReadOnlyField(source='fk_approved_by.first_name')
    fk_approved_by__last_name = serializers.ReadOnlyField(source='fk_approved_by.last_name')
    
    fk_returned_by__username = serializers.ReadOnlyField(source='fk_returned_by.username')
    fk_returned_by__image_user = serializers.ImageField(source='fk_returned_by.image_user',read_only=True)
    fk_returned_by__first_name = serializers.ReadOnlyField(source='fk_returned_by.first_name')
    fk_returned_by__last_name = serializers.ReadOnlyField(source='fk_returned_by.last_name')
   
    fk_rejected_by__username = serializers.ReadOnlyField(source='fk_rejected_by.username')
    fk_rejected_by__image_user = serializers.ImageField(source='fk_rejected_by.image_user',read_only=True)
    fk_rejected_by__first_name = serializers.ReadOnlyField(source='fk_rejected_by.first_name')
    fk_rejected_by__last_name = serializers.ReadOnlyField(source='fk_rejected_by.last_name')
    
    fk_moved_to_next_by__username = serializers.ReadOnlyField(source='fk_moved_to_next_by.username')
    fk_moved_to_next_by__image_user = serializers.ImageField(source='fk_moved_to_next_by.image_user',read_only=True)
    fk_moved_to_next_by__first_name = serializers.ReadOnlyField(source='fk_moved_to_next_by.first_name')
    fk_moved_to_next_by__last_name = serializers.ReadOnlyField(source='fk_moved_to_next_by.last_name')

    checklist_items = serializers.SerializerMethodField()
    print_report_settings = serializers.SerializerMethodField()

    class Meta:
        model = RequestAction
        fields = '__all__'
        read_only_fields = ['id', 'start_time', 'delivery_time', 'note_recorded_at', 'executed_at', 'completed_at']
    
    def get_checklist_items(self, obj):
        """Return checklist items for this action - using prefetched data"""
        # Use prefetched items if available, sort in Python to avoid extra query
        if hasattr(obj, '_prefetched_objects_cache') and 'checklist_items' in obj._prefetched_objects_cache:
            items = sorted(obj.checklist_items.all(), key=lambda x: x.order)
        else:
            items = obj.checklist_items.all().order_by('order')
        return StageChecklistItemSerializer(items, many=True).data
    
    def get_print_report_settings(self, obj):
            """Return print report all_settings for this workflow step based on request's organization"""
            from d_services.models.WorkflowStepPrintReportSetting import WorkflowStepPrintReportSetting
            from d_services.models.OrganizationServiceConfig import OrganizationServiceConfig
            
            # إذا لم يكن هناك مدخل أو مخرج مخصص، لا نحتاج لجلب الإعدادات
            if not obj.has_custom_input and not obj.has_custom_output:
                return None
            
            try:
                # جلب المنظمة من الطلب
                organization = obj.fk_request.fk_organization
                service = obj.fk_request.fk_service
                workflow_step = obj.fk_workflow_step
                
                if not organization or not workflow_step:
                    return None
                
                # جلب إعدادات الخدمة للمنظمة
                org_config = OrganizationServiceConfig.objects.filter(
                    fk_organization=organization,
                    fk_service=service
                ).first()
                
                if not org_config:
                    return None
                
                # جلب إعدادات الطباعة للخطوة
                print_setting = WorkflowStepPrintReportSetting.objects.select_related(
                    'fk_print_report_setting_for_output',
                    'fk_print_report_setting_for_input'
                ).filter(
                    fk_org_service_config=org_config,
                    fk_workflow_step=workflow_step
                ).first()
                
                if not print_setting:
                    return None
                
                return {
                    'fk_print_report_setting_for_output': print_setting.fk_print_report_setting_for_output_id,
                    'fk_print_report_setting_for_output__name': print_setting.fk_print_report_setting_for_output.name if print_setting.fk_print_report_setting_for_output else None,
                    'fk_print_report_setting_for_input': print_setting.fk_print_report_setting_for_input_id,
                    'fk_print_report_setting_for_input__name': print_setting.fk_print_report_setting_for_input.name if print_setting.fk_print_report_setting_for_input else None,
                }
            except Exception:
                return None
class RequestNoteSerializer(DynamicFieldsModelSerializer):
    """Serializer for request notes"""
    fk_created_by__username = serializers.ReadOnlyField(source='fk_created_by.username')
    fk_created_by__first_name = serializers.ReadOnlyField(source='fk_created_by.first_name')
    fk_created_by__last_name = serializers.ReadOnlyField(source='fk_created_by.last_name')
    fk_request__request_number = serializers.ReadOnlyField(source='fk_request.request_number')
    
    class Meta:
        model = RequestNote
        fields = '__all__'
        read_only_fields = ['id', 'fk_created_by', 'created_at']





