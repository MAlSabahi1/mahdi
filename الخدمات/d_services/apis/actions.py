

from rest_framework.decorators import action
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db import transaction, models
from d_services.models.RequestAttachment import RequestAttachment
from d_services.models.RequestNote import RequestNote

from d_services.utils.exception_handler import (
    handle_exceptions,
    ValidationException,
    PermissionDeniedException,
    ResourceNotFoundException,
    LockedResourceException,
    InvalidStatusException,
    BusinessRuleException,
)
from d_services.models.RequestAction import RequestAction
from d_services.models.StagePermission import StagePermission
from d_services.models.ServiceWorkflowStep import ServiceWorkflowStep
from d_services.models.RequestReturnLog import RequestReturnLog
from d_services.serializers.requests import (
    RequestActionSerializer,
    RequestAttachmentSerializer,
    RequestNoteSerializer
)
from d_services.choices.choices import (
    ServiceStatusChoice,
    StageStatusChoice,
    ReturnReasonChoice,
    LogActionChoice,
)
from config.imports.viewmodel_core import AllMVS
from utils.BranchMixinQuerset import BranchViewSetMixin
from d_services.utils.messages import Messages
from d_services.utils.response_handler import ResponseHandler
from d_services.utils.validation_handler import ValidationHandler
from d_services.utils.logging_manager import LoggingManager
from OpenSoftCoreV4.utils.helpers.utils.requires import require_field,require_instance
from d_services.models.ServiceRequest import ServiceRequest
from d_services.choices.choices import ActionPermissionType
from d_services.choices.choices import WorkflowStageTypeChoice
from d_services.choices.choices import PaymentStatusChoice
from django.db.models import Prefetch
from d_services.models.StageChecklistItem import StageChecklistItem
from d_services.models.Service import Service
# اضافح حقل في ال خطوات 
class RequestActionMVS(BranchViewSetMixin, AllMVS):
    queryset = RequestAction.objects.select_related(
        'fk_request', 'fk_request__fk_service', 'fk_request__fk_organization',
        'fk_workflow_step', 'fk_workflow_step__fk_stage',
        'fk_started_by', 'fk_executed_by', 'fk_completed_by', 
        'fk_approved_by', 'fk_rejected_by', 'fk_moved_to_next_by'
    ).prefetch_related(
        Prefetch('checklist_items', queryset=StageChecklistItem.objects.select_related('fk_checked_by').order_by('order'))
    )
    serializer_class = RequestActionSerializer
    branch_field = 'fk_request__fk_organization'
    # enable_actions = ['all','select','list','second_list','filter','filter_paginate',]
    
    def list(self, request, *args, **kwargs):
        user = request.user
        queryset = super().get_queryset()
        
        request_id = require_field(request.query_params,'fk_request',pop=False)
        request_instance = require_instance(ServiceRequest,{"pk":request_id})
        service_instanse = require_instance(Service,{"pk":request_instance.fk_service_id})
        if not ValidationHandler.check_service_permission(user, service_instanse.id, 'READ'):
                return ResponseHandler.forbidden(_('ليس لديك صلاحية عرض طلبات هذه الخدمة'))
        queryset = queryset.filter(fk_request_id=request_id)
        

        organization = getattr(user, 'fk_organization', None)
        queryset = queryset.filter(fk_request__fk_organization=organization)
        

        stage_status = request.query_params.get('stage_status')
        if stage_status:
            queryset = queryset.filter(stage_status=stage_status)
        

        is_current = request.query_params.get('is_current')
        if is_current and is_current.lower() == 'true':
            queryset = queryset.filter(is_current=True)
        
        serializer = self.get_serializer(queryset, many=True)
        return ResponseHandler.success(
            message=_('تم جلب قائمة المراحل بنجاح'),
            data=serializer.data,
            extra={'count': queryset.count()}
        )
    
    def retrieve(self, request, pk=None, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        request_instance = require_instance(ServiceRequest,{"pk":instance.fk_request_id})
        service_instanse = require_instance(Service,{"pk":request_instance.fk_service_id})
        if not ValidationHandler.check_service_permission(user, service_instanse.id, 'READ'):
                return ResponseHandler.forbidden(_('ليس لديك صلاحية عرض طلبات هذه الخدمة'))
        serializer = self.get_serializer(instance)
        return ResponseHandler.success(
            message=_('تم جلب تفاصيل المرحلة بنجاح'),
            data=serializer.data
        )
    
    def _validate_stage_permission(self, user, action_instance, permission_type=None):
        from d_services.choices.choices import ActionPermissionType
        from django.core.cache import cache
        
        # Check superuser first
        if user.is_superuser:
            return
        
        # Check cache for performance
        cache_key = f'stage_perm_{user.id}_{action_instance.fk_workflow_step_id}_{permission_type}'
        has_permission = cache.get(cache_key)
        
        if has_permission is None:
            # بناء الاستعلام
            query = StagePermission.objects.filter(
                fk_workflow_step_permission__fk_workflow_step=action_instance.fk_workflow_step,
                fk_user=user
            )
            
            # إضافة فلتر نوع الصلاحية إذا تم تحديده
            if permission_type:
                query = query.filter(fk_workflow_step_permission__permission_type=permission_type)
            
            has_permission = query.exists()
            # Cache for 5 minutes
            cache.set(cache_key, has_permission, timeout=300)
        
        if not has_permission:
            raise PermissionDeniedException(
                message=_('ليس لديك صلاحية العمل على هذه المرحلة'),
                hint=_('تواصل مع مدير النظام لإضافتك لقائمة المصرح لهم')
            )
    
    def _validate_action_status(self, action_instance, allowed_statuses, action_name=''):
        if action_instance.stage_status not in allowed_statuses:
            raise InvalidStatusException(
                message=_('لا يمكن تنفيذ هذا الإجراء على المرحلة الحالية'),
                details={
                    'current_status': action_instance.stage_status,
                    'allowed_statuses': allowed_statuses,
                    'action': action_name
                }
            )
    
    def _validate_request_not_locked(self, action_instance):
        if action_instance.fk_request.is_locked:
            raise LockedResourceException(
                message=_('الطلب مقفول ولا يمكن تعديله'),
                details={
                    'locked_at': action_instance.fk_request.locked_at,
                    'locked_reason': action_instance.fk_request.locked_reason
                }
            )
    
    def _validate_is_current(self, action_instance):
        if not action_instance.is_current:
            raise BusinessRuleException(
                message=_('هذه المرحلة غير نشطة حالياً'),
                hint=_('يمكنك فقط العمل على المرحلة الحالية النشطة')
            )
    
    def _validate_checklist_completed(self, action_instance):
        from d_services.models.StageChecklistItem import StageChecklistItem
        
        # جلب العناصر الإلزامية غير المكتملة
        incomplete_required_items = StageChecklistItem.objects.filter(
            fk_request_action=action_instance,
            is_required=True,
            is_checked=False,
        )
        
        if incomplete_required_items.exists():
            incomplete_titles = list(incomplete_required_items.values_list('title', flat=True))
            raise ValidationException(
                message=_('يجب إكمال جميع عناصر قائمة التحقق الإلزامية'),
                details={
                    'incomplete_count': incomplete_required_items.count(),
                    'incomplete_items': incomplete_titles
                },
                hint=_('أكمل العناصر التالية: %s') % ', '.join(incomplete_titles[:3])
            )
    
    @action(detail=True, methods=['post'], url_path='start', url_name='start')
    @handle_exceptions
    def start_stage(self, request, pk=None):
        instance = self.get_object()
        user = request.user
        
        from d_services.choices.choices import ActionPermissionType
        
        # التحققات
        self._validate_stage_permission(user, instance, ActionPermissionType.START)
        self._validate_request_not_locked(instance)
        self._validate_is_current(instance)
        self._validate_action_status(
            instance, 
            [StageStatusChoice.PENDING], 
            'start_stage'
        )
        
        instance.stage_status = StageStatusChoice.IN_PROGRESS
        instance.start_time = timezone.now()
        instance.fk_started_by = user
        instance.save()
        
        # تسجيل بدء المرحلة 📝
        LoggingManager.log_stage_start(
            service_request=instance.fk_request,
            stage=instance.fk_workflow_step,
            user=user,
            request=request,
            request_action=instance,
            notes=f'تم بدء العمل على المرحلة: {instance.fk_workflow_step.fk_stage.name_ar}'
        )
        
        return ResponseHandler.success(
            message=Messages.STAGE_STARTED,
            data=RequestActionSerializer(instance).data,
            extra={
                'stage_name': instance.fk_workflow_step.fk_stage.name_ar,
                'started_at': instance.start_time
            }
        )
    
    @action(detail=True, methods=['post'], url_path='complete', url_name='complete')
    @handle_exceptions
    def complete_stage(self, request, pk=None):
        instance = self.get_object()
        user = request.user
        
        
        # التحققات
        self._validate_stage_permission(user, instance, ActionPermissionType.COMPLETE)
        self._validate_request_not_locked(instance)
        self._validate_is_current(instance)
        self._validate_action_status(
            instance, 
            [StageStatusChoice.IN_PROGRESS], 
            'complete_stage'
        )
        
        if instance.has_custom_input and not instance.input_file:
            raise ValidationException(
                message=_('هذه المرحلة تتطلب رفع ملف المدخل'),
                hint=_('يرجى رفع ملف المدخل قبل إكمال المرحلة')
            )
        if instance.has_approval and not instance.is_approved:
            raise ValidationException(
                message=_('هذه المرحلة تتطلب موافقة'),
                hint=_('يرجى الموافقة على المرحلة قبل إكمالها')
            )
        if instance.is_execution_step and not instance.is_executed:
            raise ValidationException(
                message=_('هذه المرحلة تتطلب التنفيذ'),
                hint=_('يرجى التنفيذ على المرحلة قبل إكمالها')
            )
        if instance.has_custom_output and not instance.output_file:
            raise ValidationException(
                message=_('هذه المرحلة تتطلب رفع ملف المخرج'),
                hint=_('يرجى رفع ملف المخرج قبل إكمال المرحلة')
            )

        
        # التحقق من قائمة التحقق (Checklist)
        self._validate_checklist_completed(instance)
        
        with transaction.atomic():
            instance.stage_status = StageStatusChoice.COMPLETED
            instance.delivery_time = timezone.now()
            instance.fk_completed_by = user

            instance.save()
            
            # تسجيل إكمال المرحلة 📝
            LoggingManager.log_stage_complete(
                service_request=instance.fk_request,
                from_stage=instance.fk_workflow_step,
                user=user,
                request=request,
                request_action=instance,
                notes=f'تم إكمال المرحلة: {instance.fk_workflow_step.fk_stage.name_ar}'
            )
        
        response_data = {
            'stage_name': instance.fk_workflow_step.fk_stage.name_ar,
            'completed_at': instance.delivery_time,
            'is_final_step': instance.is_final_step
        }
        
        return ResponseHandler.success(
            message=Messages.STAGE_COMPLETED,
            data=RequestActionSerializer(instance).data,
            extra=response_data
        )
    
    @action(detail=True, methods=['post'], url_path='approve', url_name='approve')
    @handle_exceptions
    def approve_stage(self, request, pk=None):

        instance = self.get_object()
        user = request.user
        
        # التحققات
        self._validate_stage_permission(user, instance, ActionPermissionType.APPROVE)
        self._validate_request_not_locked(instance)
        self._validate_is_current(instance)
        self._validate_action_status(
            instance, 
            [StageStatusChoice.IN_PROGRESS], 
            'approve_stage'
        )
        if instance.is_approved:
            raise ValidationException(
                message=_("هذه المرحلة مرفوضة بالفعل"),
                hint=_("لا يمكن الموافقة على هذه المرحلة مرة أخرى")
            )
        with transaction.atomic():
            instance.is_approved = True
            instance.approved_at = timezone.now()
            instance.fk_approved_by = user
            instance.save()
            
            # تسجيل الموافقة على المرحلة 📝
            LoggingManager.log_workflow_transition(
                service_request=instance.fk_request,
                action=LogActionChoice.APPROVE,
                request_action=instance,
                user=user,
                request=request,
                notes=f'تمت الموافقة على المرحلة: {instance.fk_workflow_step.fk_stage.name_ar}'
            )
        
        response_data = {
            'stage_name': instance.fk_workflow_step.fk_stage.name_ar,
            'approved_at': instance.approved_at,
            'is_final_step': instance.is_final_step
        }
        
        return ResponseHandler.success(
            message=Messages.STAGE_APPROVED,
            data=RequestActionSerializer(instance).data,
            extra=response_data
        )    
    @action(detail=True, methods=['post'], url_path='reject', url_name='reject')
    @handle_exceptions
    def reject_stage(self, request, pk=None):
        """
        رفض المرحلة
        - التحقق من صلاحية StagePermission
        - تسجيل سبب الرفض
        """
        instance = self.get_object()
        user = request.user
        
    
        # التحققات
        self._validate_stage_permission(user, instance, ActionPermissionType.REJECT)
        self._validate_request_not_locked(instance)
        self._validate_is_current(instance)
        self._validate_action_status(
            instance, 
            [StageStatusChoice.IN_PROGRESS], 
            'reject_stage'
        )
        
        reject_reason = request.data.get('reject_reason')
        if not reject_reason:
            raise ValidationException(message=_('سبب الرفض مطلوب'))
        
        with transaction.atomic():
            instance.stage_status = StageStatusChoice.REJECTED
            instance.reject_reason = reject_reason
            instance.rejected_at = timezone.now()
            instance.fk_rejected_by = user
            instance.save()
            
            # تسجيل رفض المرحلة 📝
            LoggingManager.log_workflow_transition(
                service_request=instance.fk_request,
                action=LogActionChoice.REJECT,
                request_action=instance,
                user=user,
                request=request,
                notes=f'تم رفض المرحلة: {reject_reason}',
                extra_data={'reject_reason': reject_reason}
            )
        
        return ResponseHandler.success(
            message=Messages.STAGE_REJECTED,
            data=RequestActionSerializer(instance).data,
            extra={
                'stage_name': instance.fk_workflow_step.fk_stage.name_ar,
                'reject_reason': reject_reason,
                'rejected_at': instance.delivery_time
            }
        )
    
    @action(detail=True, methods=['post'], url_path='return', url_name='return')
    @handle_exceptions
    def return_stage(self, request, pk=None):
        instance = self.get_object()
        user = request.user
        
        self._validate_stage_permission(user, instance)
        self._validate_request_not_locked(instance)
        self._validate_is_current(instance)
        self._validate_action_status(
            instance, 
            [StageStatusChoice.IN_PROGRESS], 
            'return_stage'
        )
        
        return_reason = request.data.get('return_reason')
        return_reason_details = request.data.get('return_reason_details', '')
        to_stage_id = request.data.get('to_stage_id')
        
        if not return_reason:
            raise ValidationException(message=_('سبب الإرجاع مطلوب'))
        
        previous_action = RequestAction.objects.filter(
            fk_request=instance.fk_request,
            order__lt=instance.order,
        ).order_by('-order').first()
        
        if not previous_action:
            raise BusinessRuleException(
                message=_('لا توجد مرحلة سابقة للإرجاع إليها'),
                hint=_('هذه هي المرحلة الأولى')
            )
        
        with transaction.atomic():
            instance.stage_status = StageStatusChoice.RETURNED
            instance.is_current = False
            instance.returned_reason = f"{return_reason}: {return_reason_details}"
            instance.returned_at = timezone.now()
            instance.fk_returned_by = user
            instance.save()
            
            if previous_action:
                previous_action.stage_status = StageStatusChoice.IN_PROGRESS
                previous_action.is_current = True
                previous_action.start_time = timezone.now()
                previous_action.save()
            
            LoggingManager.log_workflow_transition(
                service_request=instance.fk_request,
                action=LogActionChoice.RETURN,
                from_stage=instance.fk_workflow_step,
                to_stage=previous_action.fk_workflow_step if previous_action else None,
                request_action=instance,
                user=user,
                request=request,
                notes=f'تم إرجاع المرحلة: {return_reason}',
                extra_data={
                    'return_reason': return_reason,
                    'return_reason_details': return_reason_details
                }
            )

        return ResponseHandler.success(
            message=Messages.STAGE_RETURNED,
            data=RequestActionSerializer(instance).data,
            extra={
            }
        )
    
    @action(detail=True, methods=['post'], url_path='advance', url_name='advance')
    @handle_exceptions
    def advance_to_next(self, request, pk=None):
        instance = self.get_object()
        user = request.user
        
        self._validate_stage_permission(user, instance)
        self._validate_request_not_locked(instance)
        self._validate_action_status(
            instance, 
            [StageStatusChoice.COMPLETED], 
            'advance_to_next'
        )
        
        if instance.is_final_step:
            raise BusinessRuleException(
                message=_('هذه هي المرحلة النهائية'),
                hint=_('لا توجد مراحل تالية')
            )
        
        next_step = ServiceWorkflowStep.objects.filter(
            fk_service=instance.fk_request.fk_service,
            order__gt=instance.fk_workflow_step.order,
        ).order_by('order').first()
        
        if not next_step:
            raise BusinessRuleException(
                message=_('لا توجد مرحلة تالية'),
                hint=_('قد تكون هذه آخر مرحلة')
            )
        
        next_action = RequestAction.objects.filter(
            fk_request=instance.fk_request,
            fk_workflow_step=next_step,
            is_deleted=False
        ).first()
        
        with transaction.atomic():
            instance.is_current = False
            instance.fk_moved_to_next_by = user
            instance.moved_to_next_at = timezone.now()
            instance.save()
            
            if next_action:
                next_action.is_current = True
                next_action.stage_status = StageStatusChoice.PENDING
                next_action.save()
            
            LoggingManager.log_workflow_transition(
                service_request=instance.fk_request,
                action=LogActionChoice.MOVE,
                from_stage=instance.fk_workflow_step,
                to_stage=next_step,
                request_action=next_action if next_action else instance,
                user=user,
                request=request,
                notes=f'تم الانتقال من {instance.fk_workflow_step.fk_stage.name_ar} إلى {next_step.fk_stage.name_ar}'
            )
        
        return ResponseHandler.success(
            message=Messages.STAGE_ADVANCED,
            data=RequestActionSerializer(next_action).data if next_action else None,
            extra={
                'from_stage': instance.fk_workflow_step.fk_stage.name_ar,
                'to_stage': next_step.fk_stage.name_ar,
                'next_action_id': next_action.id if next_action else None
            }
        )
    
    @action(detail=True, methods=['post'], url_path='execute', url_name='execute')
    @handle_exceptions
    def execute_stage(self, request, pk=None):

        instance = self.get_object()
        user = request.user
        
        self._validate_stage_permission(user, instance, ActionPermissionType.EXECUTE)
        self._validate_request_not_locked(instance)
        self._validate_is_current(instance)
        self._validate_action_status(
            instance, 
            [StageStatusChoice.IN_PROGRESS], 
            'execute_stage'
        )
        
        if not instance.is_execution_step:
            raise ValidationException(
                message=_('هذه المرحلة ليست مرحلة تنفيذ'),
                hint=_('لا يمكن تنفيذ هذا الإجراء على هذه المرحلة')
            )
        
        procedure_name = instance.fk_workflow_step.execution_procedure_name
        if not procedure_name:
            raise ValidationException(
                message=_('لا يوجد إجراء تنفيذ محدد لهذه المرحلة'),
                hint=_('يرجى تحديد اسم إجراء التنفيذ في إعدادات الخطوة')
            )
        
        from d_services.apis.external_methods import ExternalMethodHandler, FunctionType
        
        if not ExternalMethodHandler.function_exists(procedure_name, FunctionType.EXECUTION):
            raise ValidationException(
                message=_('إجراء التنفيذ غير موجود'),
                hint=_(f'الإجراء {procedure_name} غير معرف في النظام')
            )
        
        with transaction.atomic():
            success, result = ExternalMethodHandler.call_function(
                procedure_name, instance, request, function_type=FunctionType.EXECUTION
            )
            if not success:
                raise BusinessRuleException(message=_(f'فشل تنفيذ الإجراء: {result}'))
            
            if instance.fk_workflow_step.fk_stage.stage_type == WorkflowStageTypeChoice.PAYMENT and instance.fk_request.payment_status in [PaymentStatusChoice.PARTIAL_GRANT, PaymentStatusChoice.PARTIAL_DISCOUNT, PaymentStatusChoice.UNPAID, PaymentStatusChoice.PARTIAL, PaymentStatusChoice.PARTIAL_GRANT_DISCOUNT]:
                raise ValidationException(
                    message=_('لم يتم الدفع بعد'),
                    hint=_('يرجى التحقق من ان الطالب دفع رسوم الخدمه')
                )   
            instance.is_executed = True
            instance.executed_at = timezone.now()
            instance.fk_executed_by = user
            
            instance.save()
        
        return ResponseHandler.success(
            message=_('تم تنفيذ المرحلة بنجاح'),
            data=RequestActionSerializer(instance).data,
            extra={
                'stage_name': instance.fk_workflow_step.fk_stage.name_ar,
                'procedure_name': procedure_name,
                'execution_result': result if isinstance(result, dict) else {'success': True}
            }
        )
    
    @action(detail=True, methods=['get'], url_path='input-data', url_name='input-data')
    @handle_exceptions
    def get_input_template_data(self, request, pk=None):

        instance = self.get_object()
        user = request.user
        
        self._validate_stage_permission(user, instance, ActionPermissionType.INPUT)
        
        if not instance.has_custom_input:
            raise ValidationException(
                message=_('هذه المرحلة لا تحتوي على مدخل خاص'),
                hint=_('لا يوجد قالب مدخل لهذه المرحلة')
            )
        
        response_data = {
            'has_custom_input': instance.has_custom_input,
            'custom_input_template': instance.custom_input_template,
            'input_file': instance.input_file.url if instance.input_file else None,
        }
        
        input_function_name = instance.fk_workflow_step.custom_input_function
        if input_function_name:
            from d_services.apis.external_methods import ExternalMethodHandler, FunctionType
            success, template_data = ExternalMethodHandler.call_function(
                input_function_name, instance, request, function_type=FunctionType.INPUT_DATA
            )
            if success:
                response_data['template_data'] = template_data
        
        return ResponseHandler.success(
            message=_('تم جلب بيانات قالب المدخل بنجاح'),
            data=response_data
        )
    
    @action(detail=True, methods=['get'], url_path='output-data', url_name='output-data')
    @handle_exceptions
    def get_output_template_data(self, request, pk=None):
        """
        جلب بيانات قالب المخرج
        - تنفيذ custom_output_function للحصول على البيانات
        """
        instance = self.get_object()
        user = request.user
        
        self._validate_stage_permission(user, instance, ActionPermissionType.OUTPUT)
        
        # التحقق من وجود مخرج خاص
        if not instance.has_custom_output:
            raise ValidationException(
                message=_('هذه المرحلة لا تحتوي على مخرج خاص'),
                hint=_('لا يوجد قالب مخرج لهذه المرحلة')
            )
        
        response_data = {
            'has_custom_output': instance.has_custom_output,
            'custom_output_template': instance.custom_output_template,
            'output_file': instance.output_file.url if instance.output_file else None,
        }
        
        # تنفيذ دالة المخرج إذا كانت موجودة
        output_function_name = instance.fk_workflow_step.custom_output_function
        if output_function_name:
            from d_services.apis.external_methods import ExternalMethodHandler, FunctionType
            
            success, template_data = ExternalMethodHandler.call_function(
                output_function_name, instance, request, function_type=FunctionType.OUTPUT_DATA
            )
            if success:
                response_data['template_data'] = template_data
        
        return ResponseHandler.success(
            message=_('تم جلب بيانات قالب المخرج بنجاح'),
            data=response_data
        )
    
    @action(detail=True, methods=['post'], url_path='upload-output', url_name='upload-output')
    @handle_exceptions
    def upload_output(self, request, pk=None):
        """
        رفع ملف المخرج
        """
        instance = self.get_object()
        user = request.user
        
        self._validate_stage_permission(user, instance)
        self._validate_request_not_locked(instance)
        
        output_file = request.FILES.get('output_document')
        if not output_file:
            raise ValidationException(message=_('ملف المخرج مطلوب'))
        
        instance.output_file = output_file
        instance.save()
        
        return ResponseHandler.success(
            message=_('تم رفع ملف المخرج بنجاح'),
            data=RequestActionSerializer(instance).data
        )
    
    @action(detail=True, methods=['post'], url_path='upload-input', url_name='upload-input')
    @handle_exceptions
    def upload_input(self, request, pk=None):
        """
        رفع ملف الاستمارة الموقعة
        """
        instance = self.get_object()
        user = request.user
        
        self._validate_stage_permission(user, instance)
        self._validate_request_not_locked(instance)
        
        input_file = request.FILES.get('input_document')
        if not input_file:
            raise ValidationException(message=_('ملف الاستمارة مطلوب'))
        
        instance.input_file = input_file
        instance.save()
        
        return ResponseHandler.success(
            message=_('تم رفع ملف الاستمارة بنجاح'),
            data=RequestActionSerializer(instance).data
        )

    @action(detail=True, methods=['post'], url_path='add-note', url_name='add-note')
    @handle_exceptions
    def add_note(self, request, pk=None):
        """
        إضافة ملاحظة للمرحلة
        """
        instance = self.get_object()
        user = request.user
        
        self._validate_stage_permission(user, instance)
        
        notes = request.data.get('notes')
        if not notes:
            raise ValidationException(message=_('الملاحظة مطلوبة'))
        
        # إضافة للملاحظات الموجودة
        existing_notes = instance.notes or ''
        timestamp = timezone.now().strftime('%Y-%m-%d %H:%M')
        new_note = f"\n&... [{timestamp}] {user.username}: {notes}"
        
        instance.notes = existing_notes + new_note
        instance.note_recorded_at = timezone.now()
        instance.save()
        
        return ResponseHandler.success(
            message=_('تم إضافة الملاحظة بنجاح'),
            data=RequestActionSerializer(instance).data
        )
    
    @action(detail=False, methods=['get'], url_path='my-pending', url_name='my-pending')
    @handle_exceptions
    def my_pending_stages(self, request):
        """
        المراحل المعلقة للمستخدم الحالي
        - يتم جلب المراحل حسب صلاحيات StagePermission للمستخدم
        """
        user = request.user
        
        # جلب خطوات سير العمل التي لديه صلاحية عليها
        permitted_steps = StagePermission.objects.filter(
            fk_user=user
        ).values_list('fk_workflow_step_permission__fk_workflow_step_id', flat=True)
        
        # جلب المراحل المعلقة
        pending_actions = RequestAction.objects.filter(
            fk_workflow_step_id__in=permitted_steps,
            is_current=True,
            stage_status__in=[StageStatusChoice.PENDING, StageStatusChoice.IN_PROGRESS],
        ).select_related(
            'fk_request', 'fk_workflow_step', 'fk_workflow_step__fk_stage'
        )
        
        # تصفية حسب المنظمة
        organization = getattr(user, 'fk_organization', None)
        if organization and not user.is_superuser:
            pending_actions = pending_actions.filter(
                fk_request__fk_organization=organization
            )
        
        serializer = RequestActionSerializer(pending_actions, many=True)
        
        return ResponseHandler.success(
            message=_('تم جلب قائمة المراحل المعلقة بنجاح'),
            data=serializer.data,
            extra={'count': pending_actions.count()}
        )
    
    @action(detail=True, methods=['delete'], url_path='delete-input', url_name='delete-input')
    @handle_exceptions
    def delete_input_file(self, request, pk=None):
        """حذف ملف المدخل للمرحلة"""
        instance = self.get_object()
        user = request.user
        
        self._validate_stage_permission(user, instance, ActionPermissionType.INPUT)
        self._validate_request_not_locked(instance)
        
        if not instance.input_file:
            raise ValidationException(message=_('لا يوجد ملف مدخل للحذف'))
        
        instance.input_file.delete(save=False)
        instance.input_file = None
        instance.save()
        
        return ResponseHandler.success(message=_('تم حذف ملف المدخل بنجاح'))
    
    @action(detail=True, methods=['delete'], url_path='delete-output', url_name='delete-output')
    @handle_exceptions
    def delete_output_file(self, request, pk=None):
        """حذف ملف المخرج للمرحلة"""
        instance = self.get_object()
        user = request.user
        
        self._validate_stage_permission(user, instance, ActionPermissionType.OUTPUT)
        self._validate_request_not_locked(instance)
        
        if not instance.output_file:
            raise ValidationException(message=_('لا يوجد ملف مخرج للحذف'))
        
        instance.output_file.delete(save=False)
        instance.output_file = None
        instance.save()
        
        return ResponseHandler.success(message=_('تم حذف ملف المخرج بنجاح'))

    @action(detail=True, methods=['get'], url_path='checklist', url_name='checklist')
    @handle_exceptions
    def get_checklist(self, request, pk=None):
        """جلب قائمة التحقق للمرحلة"""
        from d_services.models.StageChecklistItem import StageChecklistItem
        
        instance = self.get_object()
        user = request.user
        
        self._validate_stage_permission(user, instance)
        
        checklist_items = StageChecklistItem.objects.filter(
            fk_request_action=instance,
            is_deleted=False
        ).order_by('order').select_related('fk_checked_by')
        
        items_data = []
        for item in checklist_items:
            items_data.append({
                'id': item.id,
                'title': item.title,
                'description': item.description,
                'order': item.order,
                'is_required': item.is_required,
                'is_checked': item.is_checked,
                'checked_at': item.checked_at,
                'checked_by': item.fk_checked_by.username if item.fk_checked_by else None,
            })
        
        # إحصائيات
        total_count = checklist_items.count()
        checked_count = checklist_items.filter(is_checked=True).count()
        required_count = checklist_items.filter(is_required=True).count()
        required_checked = checklist_items.filter(is_required=True, is_checked=True).count()
        
        return ResponseHandler.success(
            message=_('تم جلب قائمة التحقق بنجاح'),
            data={
                'items': items_data,
                'stats': {
                    'total_count': total_count,
                    'checked_count': checked_count,
                    'required_count': required_count,
                    'required_checked': required_checked,
                    'all_required_checked': required_count == required_checked,
                    'completion_percentage': round((checked_count / total_count * 100), 1) if total_count > 0 else 100
                }
            }
        )
    
    @action(detail=True, methods=['post'], url_path='checklist-check/(?P<item_id>[^/.]+)', url_name='checklist-check')
    @handle_exceptions
    def check_item(self, request, pk=None, item_id=None):
        """تعليم عنصر في قائمة التحقق كمكتمل"""
        from d_services.models.StageChecklistItem import StageChecklistItem
        
        instance = self.get_object()
        user = request.user
        
        self._validate_stage_permission(user, instance, ActionPermissionType.CHECKLIST_CHECK)
        self._validate_request_not_locked(instance)
        
        try:
            item = StageChecklistItem.objects.get(
                id=item_id,
                fk_request_action=instance,
                is_deleted=False
            )
        except StageChecklistItem.DoesNotExist:
            raise ResourceNotFoundException(message=_('عنصر قائمة التحقق غير موجود'))
        
        item.check_item(user)
        
        return ResponseHandler.success(
            message=_('تم تعليم العنصر كمكتمل'),
            data={
                'id': item.id,
                'title': item.title,
                'is_checked': item.is_checked,
                'checked_at': item.checked_at,
                'checked_by': user.username
            }
        )
    
    @action(detail=True, methods=['post'], url_path='checklist-uncheck/(?P<item_id>[^/.]+)', url_name='checklist-uncheck')
    @handle_exceptions
    def uncheck_item(self, request, pk=None, item_id=None):
        """إلغاء تعليم عنصر في قائمة التحقق"""
        from d_services.models.StageChecklistItem import StageChecklistItem
        
        instance = self.get_object()
        user = request.user
        
        self._validate_stage_permission(user, instance, ActionPermissionType.CHECKLIST_UNCHECK)
        self._validate_request_not_locked(instance)
        
        try:
            item = StageChecklistItem.objects.get(
                id=item_id,
                fk_request_action=instance,
                is_deleted=False
            )
        except StageChecklistItem.DoesNotExist:
            raise ResourceNotFoundException(message=_('عنصر قائمة التحقق غير موجود'))
        
        item.uncheck_item()
        
        return ResponseHandler.success(
            message=_('تم إلغاء تعليم العنصر'),
            data={
                'id': item.id,
                'title': item.title,
                'is_checked': item.is_checked
            }
        )
    
    @action(detail=True, methods=['post'], url_path='checklist-add', url_name='checklist-add')
    @handle_exceptions
    def add_checklist_item(self, request, pk=None):
        """إضافة عنصر جديد لقائمة التحقق"""
        from d_services.models.StageChecklistItem import StageChecklistItem
        
        instance = self.get_object()
        user = request.user
        
        self._validate_stage_permission(user, instance, ActionPermissionType.CHECKLIST_ADD)
        self._validate_request_not_locked(instance)
        
        title = request.data.get('title')
        if not title:
            raise ValidationException(message=_('عنوان العنصر مطلوب'))
        
        description = request.data.get('description', '')
        is_required = request.data.get('is_required', True)
        
        # حساب الترتيب
        max_order = StageChecklistItem.objects.filter(
            fk_request_action=instance, 
            is_deleted=False
        ).aggregate(max_order=models.Max('order'))['max_order'] or 0
        
        item = StageChecklistItem.objects.create(
            fk_request_action=instance,
            title=title,
            description=description,
            is_required=is_required,
            order=max_order + 1
        )
        
        return ResponseHandler.created(
            message=_('تم إضافة عنصر قائمة التحقق بنجاح'),
            data={
                'id': item.id,
                'title': item.title,
                'description': item.description,
                'is_required': item.is_required,
                'order': item.order,
                'is_checked': item.is_checked
            }
        )
    
    @action(detail=True, methods=['delete'], url_path='checklist-delete/(?P<item_id>[^/.]+)', url_name='checklist-delete')
    @handle_exceptions
    def delete_checklist_item(self, request, pk=None, item_id=None):
        """حذف عنصر من قائمة التحقق"""
        from d_services.models.StageChecklistItem import StageChecklistItem
        
        instance = self.get_object()
        user = request.user
        
        self._validate_stage_permission(user, instance, ActionPermissionType.CHECKLIST_DELETE)
        self._validate_request_not_locked(instance)
        
        try:
            item = StageChecklistItem.objects.get(
                id=item_id,
                fk_request_action=instance,
                is_deleted=False
            )
        except StageChecklistItem.DoesNotExist:
            raise ResourceNotFoundException(message=_('عنصر قائمة التحقق غير موجود'))
        
        item.delete()
        
        return ResponseHandler.success(message=_('تم حذف عنصر قائمة التحقق بنجاح'))
    
    @action(detail=True, methods=['post'], url_path='checklist/init-from-template', url_name='checklist-init-from-template')
    @handle_exceptions
    def init_checklist_from_template(self, request, pk=None):
        """إنشاء قائمة التحقق من القالب المحدد لخطوة سير العمل"""
        from d_services.models.StageChecklistItem import StageChecklistItem, WorkflowStepChecklistTemplate
        
        instance = self.get_object()
        user = request.user
        
        self._validate_stage_permission(user, instance)
        self._validate_request_not_locked(instance)
        
        # التحقق من عدم وجود عناصر مسبقة
        existing_items = StageChecklistItem.objects.filter(
            fk_request_action=instance,
            is_deleted=False
        ).count()
        
        if existing_items > 0:
            raise BusinessRuleException(
                message=_('توجد عناصر في قائمة التحقق بالفعل'),
                hint=_('احذف العناصر الموجودة أولاً أو أضف عناصر جديدة')
            )
        
        # جلب القالب
        templates = WorkflowStepChecklistTemplate.objects.filter(
            fk_workflow_step=instance.fk_workflow_step,
            fk_org_service_config=instance.fk_request.fk_organization
        ).order_by('order')
        
        if not templates.exists():
            return ResponseHandler.success(
                message=_('لا يوجد قالب قائمة تحقق لهذه المرحلة'),
                data={'items_created': 0}
            )
        
        # إنشاء العناصر من القالب
        created_items = []
        for template in templates:
            item = StageChecklistItem.objects.create(
                fk_request_action=instance,
                title=template.title,
                description=template.description,
                order=template.order,
                is_required=template.is_required
            )
            created_items.append({
                'id': item.id,
                'title': item.title,
                'is_required': item.is_required
            })
        
        return ResponseHandler.created(
            message=_('تم إنشاء قائمة التحقق من القالب بنجاح'),
            data={
                'items_created': len(created_items),
                'items': created_items
            }
        )

class RequestNoteMVS(AllMVS):
    queryset = RequestNote.objects.select_related()
    serializer_class = RequestNoteSerializer
    enable_actions = ["sync-import" ,  "sync-export",  "sync-push","sync-pull"]

class RequestAttachmentMVS(AllMVS):
    queryset = RequestAttachment.objects.select_related()
    serializer_class = RequestAttachmentSerializer
    enable_actions = ["sync-import" ,  "sync-export",  "sync-push","sync-pull"]
