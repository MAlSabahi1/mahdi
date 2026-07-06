
from decimal import Decimal

from rest_framework.decorators import action
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db import transaction
from d_services.models.ServiceCallResult import ServiceCallResult

from d_services.utils.exception_handler import (
    handle_exceptions,
    ValidationException,
    ResourceNotFoundException,
    InvalidStatusException,
    BusinessRuleException,
)
from d_services.models.ServiceRequest import ServiceRequest
from d_services.models.RequestInstallment import RequestInstallment
from d_services.models.RequestAction import RequestAction
from d_services.models.RequestAttachment import RequestAttachment
from d_services.models.Service import Service
from d_services.models.OrganizationServiceConfig import OrganizationServiceConfig
from d_services.models.GrantSource import GrantSource
from d_services.serializers.requests import (
    ServiceCallResultSerializer,
    ServiceRequestSerializer,
)
from d_services.choices.choices import (
    ServiceStatusChoice,
    PaymentStatusChoice,
    StageStatusChoice,
    GrantStatusChoice,
    DiscountStatusChoice,
    LogActionChoice,
)
from config.imports.viewmodel_core import AllMVS
from d_services.models.GroupServicePermission import GroupServicePermission
from middleware_system.models.Invoice import PartnerType
from middleware_system.serializers.Invoice import ERPInvoiceSerializer, ERPInvoice
from utils.BranchMixinQuerset import BranchViewSetMixin

from d_services.utils.messages import Messages
from d_services.utils.response_handler import ResponseHandler
from d_services.utils.validation_handler import ValidationHandler
from d_services.utils.calculation_handler import CalculationHandler
from d_services.utils.workflow_handler import WorkflowHandler
from d_services.utils.logging_manager import LoggingManager

from OpenSoftCoreV4.utils.helpers.utils.requires import require_field,require_instance
import json
from OpenSoftCoreV4.utils.helpers.utils.dict import reconstruct_nested_dict
from d_services.choices.choices import ServiceStatusChoice

from django.db.models import Prefetch, Count, Q
from d_services.models.StageChecklistItem import StageChecklistItem
from utils.core.base_api_view import BaseAPIViewWithUserOrg

class ServiceCallResultMVS(AllMVS):
    queryset = ServiceCallResult.objects.prefetch_related()
    serializer_class = ServiceCallResultSerializer
    

class ServiceRequestMVS(BaseAPIViewWithUserOrg, AllMVS):
    # Optimized queryset with deep prefetch for N+1 prevention
    queryset = ServiceRequest.objects.select_related(
        'fk_service', 'fk_organization', 'fk_requester', 'fk_grant_source', 'fk_service_version'
    ).prefetch_related(
        Prefetch('installments', queryset=RequestInstallment.objects.filter(is_deleted=False)),
        Prefetch('attachments', queryset=RequestAttachment.objects.filter(is_deleted=False).select_related('fk_uploaded_by')),
        Prefetch('actions', queryset=RequestAction.objects.select_related(
            'fk_workflow_step', 'fk_workflow_step__fk_stage',
            'fk_started_by', 'fk_executed_by', 'fk_completed_by', 'fk_approved_by'
        ).prefetch_related(
            Prefetch('checklist_items', queryset=StageChecklistItem.objects.select_related('fk_checked_by').order_by('order'))
        ).order_by('order'))
    )
    serializer_class = ServiceRequestSerializer
    branch_field = 'fk_organization'
    # enable_actions = ['all','select','list','second_list','filter','filter_paginate',]

                        
    def list(self, request, *args, **kwargs):
        user = request.user
        queryset = super().get_queryset()
        # Add notes count annotation to avoid N+1 for notes_count field
        queryset = queryset.annotate(
            notes_count_annotation=Count('notes', filter=Q(notes__is_deleted=False))
        )
        
        service_id = request.query_params.get('fk_service')
        if service_id:
            if not ValidationHandler.check_service_permission(user, service_id, 'READ'):
                return ResponseHandler.forbidden(_('ليس لديك صلاحية عرض طلبات هذه الخدمة'))
            queryset = queryset.filter(fk_service_id=service_id)
        else:
            return ResponseHandler.bad_request(_('يجب تحديد رقم الخدمة'))
        organization = getattr(user, 'fk_organization', None)
        if organization and not user.is_superuser:
            queryset = queryset.filter(fk_organization=organization)
        
        status_filter = request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        priority = request.query_params.get('priority')
        if priority:
            queryset = queryset.filter(priority=priority)
        
        payment_status_filter = request.query_params.get('payment_status')
        if payment_status_filter:
            queryset = queryset.filter(payment_status=payment_status_filter)
        
        grant_status_filter = request.query_params.get('grant_status')
        if grant_status_filter:
            queryset = queryset.filter(grant_status=grant_status_filter)
        
        discount_status_filter = request.query_params.get('discount_status')
        if discount_status_filter:
            queryset = queryset.filter(discount_status=discount_status_filter)
        
        is_locked = request.query_params.get('is_locked')
        if is_locked is not None:
            queryset = queryset.filter(is_locked=is_locked.lower() == 'true')
        
        requester_id = request.query_params.get('fk_requester')
        if requester_id:
            queryset = queryset.filter(fk_requester_id=requester_id)
        
        request_number = request.query_params.get('request_number')
        if request_number:
            queryset = queryset.filter(request_number__icontains=request_number)
        
        date_from = request.query_params.get('date_from')
        if date_from:
            queryset = queryset.filter(requested_at__date__gte=date_from)
        
        date_to = request.query_params.get('date_to')
        if date_to:
            queryset = queryset.filter(requested_at__date__lte=date_to)
        
        ordering = request.query_params.get('sort_by', '-requested_at')
        queryset = queryset.order_by(ordering)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return self.get_paginated_response(serializer.data)
    
    def retrieve(self, request, pk=None, *args, **kwargs):
        import os
        import json
        
        instance = self.get_object()
        user = request.user
        
        if not ValidationHandler.check_service_permission(user, instance.fk_service_id, 'READ'):
            return ResponseHandler.forbidden(_('ليس لديك صلاحية عرض تفاصيل هذا الطلب'))
        if instance.fk_organization != user.fk_organization:
            return ResponseHandler.forbidden(_('ليس لديك صلاحية عرض تفاصيل هذا الطلب'))
        
        service = instance.fk_service
        serializer = ServiceRequestSerializer(instance)
        
        # جلب مخططات المكونات من الملفات
        component_base_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'apis', 'component'
        )
        
        def load_schema_file(folder_name, component_name):
            if not component_name:
                return None
            json_file_path = os.path.join(component_base_path, folder_name, f'{component_name}.json')
            if os.path.exists(json_file_path):
                try:
                    with open(json_file_path, 'r', encoding='utf-8') as f:
                        return json.load(f)
                except (json.JSONDecodeError, IOError):
                    return None
            return None
        
        base_component_schema = load_schema_file('base', service.base_audience_component)
        target_component_schema = load_schema_file('target', service.target_audience_component)
        
        # جلب بيانات الإصدار
        current_version = service.versions.filter(is_current=True).first()
        
        # جلب إعدادات تقرير الطباعة من تكوين المنظمة
        org_config = OrganizationServiceConfig.objects.filter(
            fk_service=service, 
            fk_organization=instance.fk_organization
        ).first()

        return ResponseHandler.success(
            message=Messages.DETAIL_SUCCESS,
            data={
                **serializer.data,
                # بيانات الخدمة
                'fk_service__name': service.name_ar,
                'fk_service__code': service.code,
                'input_template_type': service.input_template_type,
                'output_template_type': service.output_template_type,
                # مكون الجمهور المستهدف
                'target_audience_component': service.target_audience_component,
                'target_audience_schema': target_component_schema,
                # المكون الأساسي
                'base_audience_component': service.base_audience_component,
                'base_audience_schema': base_component_schema,
                # بيانات الإصدار
                'version_name': current_version.version_name if current_version else None,
                'version_schema': current_version.fields_schema if current_version else {},
                'component_type': current_version.component_type if current_version else None,
                # إعدادات تقرير الطباعة
                'fk_print_report_setting_for_input': org_config.fk_print_report_setting_for_input_id if org_config else None,
                'fk_print_report_setting_for_output': org_config.fk_print_report_setting_for_output_id if org_config else None,
                'fk_print_report_setting_for_input__name': org_config.fk_print_report_setting_for_input.name if org_config and org_config.fk_print_report_setting_for_input else None,
                'fk_print_report_setting_for_output__name': org_config.fk_print_report_setting_for_output.name if org_config and org_config.fk_print_report_setting_for_output else None,
                'fk_currency__name_ar': org_config.fk_currency.name_ar if org_config and org_config.fk_currency else None,
                'fk_currency': org_config.fk_currency.id if org_config and org_config.fk_currency else None,
            }
        )
    
    def update(self, request, pk=None, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        
        row_data = request.data.copy() if hasattr(request.data, 'copy') else dict(request.data)
        data_json = row_data.get('data')
        if data_json:
            if isinstance(data_json, list):
                data_json = data_json[0]
            try:
                data = json.loads(data_json)
            except (json.JSONDecodeError, TypeError):
                return ResponseHandler.bad_request(_('صيغة البيانات غير صحيحة'))
        else:
            data = dict(row_data)
        
        row_data = reconstruct_nested_dict(row_data)
        
        if instance.fk_organization != user.fk_organization:
            return ResponseHandler.forbidden(_('ليس لديك صلاحية تعديل هذا الطلب'))
        if not ValidationHandler.check_service_permission(user, instance.fk_service_id, 'UPDATE'):
            return ResponseHandler.forbidden(_('ليس لديك صلاحية تعديل هذا الطلب'))
        
        if instance.status != ServiceStatusChoice.PENDING:
            return ResponseHandler.bad_request(
                _('لا يمكن تعديل الطلب لأنه ليس في حالة انتظار'),
                details={'current_status': instance.get_status_display()},
                hint=_('يمكن تعديل الطلبات فقط عندما تكون في حالة "انتظار"')
            )
        
        if instance.is_locked:
            return ResponseHandler.bad_request(
                _('الطلب مقفول ولا يمكن تعديله'),
                details={
                    'locked_reason': instance.locked_reason or _('غير محدد'),
                    'locked_at': instance.locked_at.strftime('%Y-%m-%d %H:%M') if instance.locked_at else None
                },
                hint=_('تواصل مع مدير النظام لفتح قفل الطلب إذا كنت بحاجة لتعديله')
            )
        
        with transaction.atomic():
            allowed_fields = ['version_data', 'priority']
            for field in allowed_fields:
                if field in data:
                    setattr(instance, field, data[field])
            
            instance.save()
            
            attachments_dict = row_data.get('attachments', {})
            sent_attachment_ids = set()
            
            for key, attachment_data in attachments_dict.items():
                attachment_id = attachment_data.get('id')
                
                if attachment_id:
                    sent_attachment_ids.add(int(attachment_id))
                    try:
                        existing_attachment = RequestAttachment.objects.get(
                            id=attachment_id, 
                            fk_request=instance
                        )
                        if attachment_data.get('name'):
                            existing_attachment.name = attachment_data.get('name')
                        if attachment_data.get('description'):
                            existing_attachment.description = attachment_data.get('description')
                        if attachment_data.get('file'):
                            existing_attachment.file = attachment_data.get('file')
                        existing_attachment.save()
                    except RequestAttachment.DoesNotExist:
                        pass
                else:
                    if attachment_data.get('file'):
                        RequestAttachment.objects.create(
                            fk_request=instance,
                            name=attachment_data.get('name', ''),
                            file=attachment_data.get('file'),
                            fk_uploaded_by=user,
                            description=attachment_data.get('description', '')
                        )
            
            if attachments_dict:
                instance.attachments.exclude(id__in=sent_attachment_ids).delete()
        
        return ResponseHandler.success(
            message=Messages.UPDATE_SUCCESS,
            data=ServiceRequestSerializer(instance).data
        )
    
    def partial_update(self, request, pk=None, *args, **kwargs):
        return self.update(request, pk, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        user = request.user
        row_data = request.data.copy() if hasattr(request.data, 'copy') else dict(request.data)
        data = require_field(row_data, 'data', pop=True)
        data = json.loads(data)
        row_data = reconstruct_nested_dict(row_data)
        service_id = data.get('fk_service')
        if not service_id:
            return ResponseHandler.bad_request(_('معرف الخدمة مطلوب'))
        
        try:
            service = Service.objects.get(pk=service_id)
        except Service.DoesNotExist:
            return ResponseHandler.not_found(
                _('الخدمة غير موجودة'),
                hint=_('تأكد من صحة معرف الخدمة المرسل')
            )
        
        if not ValidationHandler.check_service_permission(user, service_id, 'CREATE'):
            return ResponseHandler.forbidden(_('ليس لديك صلاحية إنشاء طلب لهذه الخدمة'))
        
        if not service.is_active:
            return ResponseHandler.bad_request(
                _('الخدمة غير مفعلة حالياً'),
                details={'service_name': service.name_ar},
                hint=_('تواصل مع مدير النظام لتفعيل الخدمة')
            )
        
        # التحقق من وجود خطوات سير عمل للخدمة
        if not service.workflow_steps.all().exists():
            return ResponseHandler.bad_request(
                _('الخدمة لا تحتوي على خطوات سير عمل'),
                details={'service_name': service.name_ar},
                hint=_('تواصل مع مدير النظام لإعداد خطوات سير العمل لهذه الخدمة')
            )
        
        if service.start_date and service.start_date > timezone.now().date():
            return ResponseHandler.bad_request(
                _('الخدمة لم تبدأ بعد'),
                details={'service_name': service.name_ar, 'start_date': service.start_date.strftime('%Y-%m-%d')},
                hint=_('ستكون الخدمة متاحة ابتداءً من التاريخ المحدد')
            )
    
        organization = getattr(user, 'fk_organization', None)
        if not organization:
            return ResponseHandler.bad_request(_('المستخدم غير مرتبط بمنظمة'))
        
        org_config = OrganizationServiceConfig.objects.filter(
            fk_service=service, fk_organization=organization, is_active=True
        ).first()
        
        if not org_config:
            return ResponseHandler.bad_request(
                _('الخدمة غير متاحة لمنظمتك'),
                details={'service_name': service.name_ar},
                hint=_('تواصل مع مدير النظام لتفعيل الخدمة لمنظمتك')
            )
        
        installment_plans = None
        if org_config.is_installment_allowed:
            installment_plans = org_config.installment_plans.order_by('order')
            if not installment_plans.exists():
                return ResponseHandler.bad_request(
                    _('الخدمة تتطلب تقسيط ولكن لم يتم تحديد خطط الأقساط'),
                    hint=_('تواصل مع مدير النظام لإعداد خطط التقسيط لهذه الخدمة')
                )
        
        prerequisites_validation = WorkflowHandler.validate_prerequisites(service, user, data)
        if prerequisites_validation and prerequisites_validation.get('has_errors'):
            return ResponseHandler.bad_request(
                _('لم يتم استيفاء شروط الخدمة'),
                details={
                    'prerequisites_errors': prerequisites_validation.get('errors'),
                    'all_validations': prerequisites_validation.get('all_results')
                }
            )
        
        with transaction.atomic():

            # جلب صورة مقدم الطلب باستخدام الدالة المحددة في الخدمة
            from d_services.utils.image_handler import ImageHandler, ERPHandler
            requester_image = ImageHandler.get_image_for_service(service, user, data)
            # اذا كانت الصورة عبارة عن مسار يتم حذف /media لكي لا يتكرر عند تخزين الصورة
            if requester_image and isinstance(requester_image,str) and requester_image.startswith('/media'):
                requester_image = requester_image.split('/media')[1]
            # جلب بيانات مقدم الطلب (الاسم والوصف)
            requester_info = ImageHandler.get_info_for_service(service, user, data)
            requester_name = requester_info.get('name', '') if requester_info else ''
            requester_description = requester_info.get('description', '') if requester_info else ''
            requester_id = requester_info.get('id', '') if requester_info else None
            

            existing_request = ServiceRequest.objects.filter(fk_service=service,fk_organization=organization,requester_id=requester_id,status__in=[ServiceStatusChoice.APPROVED,ServiceStatusChoice.IN_PROGRESS]).first()
            if existing_request:
                return ResponseHandler.bad_request(
                    _('يوجد طلب سابق لنفس مقدم الطلب قيد المراجعة'),
                    hint=_('يجب الانتظار حتى يتم الانتهاء من الطلب السابق او إلغائة')
                )


            request_number = CalculationHandler.generate_request_number(organization, org_config)
            fees = CalculationHandler.calculate_fees(service, org_config, organization,requester_id=requester_id)
            
            # --- ERP defaults: try erp_data_function, fallback to org_config ---
            erp_data = ERPHandler.get_erp_data(service, user, data, org_config)
            # جلب معرفات الجهات المانحة المتاحة للطالب (مقدم الطلب) من البيانات الراجعة من erp_data function
            available_grant_sources_ids = erp_data.get('available_grant_sources_ids', [])
            partner_data = erp_data.get('partner_data', {})


            # fee & currency: prefer erp_data result, then CalculationHandler
            fee_amount = erp_data.get('service_fee') or fees.get('total_fee', 0)
            currency_code = erp_data.get('fk_currency')

            # التحقق من وجود الاسم والصورة (إذا كانت مطلوبة)
            
            if not requester_name:
                return ResponseHandler.bad_request(
                    _('لم يتم العثور على اسم مقدم الطلب'),
                    hint=_('تأكد من اكتمال بيانات المستخدم')
                )
   
            current_version = service.versions.filter(is_current=True).first()
            version_id = current_version.id if current_version else None
            
            service_request = ServiceRequest.objects.create(
                fk_organization=organization,
                fk_service=service,
                fk_service_version_id=version_id,
                fk_requester=user,
                requester_image=requester_image,
                requester_name=requester_name,
                requester_description=requester_description,
                requester_id=requester_id,
                request_number=request_number,
                target_audience_component= service.target_audience_component,
                target_audience_data=data.get('target_audience_data', {}),
                base_audience_component=service.base_audience_component,
                base_component_data=data.get('base_component_data', {}),
                version_data=data.get('version_data'),
                output_template_type=service.output_template_type,
                input_template_type=service.input_template_type,
                output_data_function=service.output_data_function,
                input_data_function=service.input_data_function,
                status=ServiceStatusChoice.PENDING,
                priority=data.get('priority', 'normal'),
                has_approvals=service.requires_approval,
                total_fee=fee_amount,
                discounted_fee=fees['discounted_fee'],
                discounted_fee_reason=fees.get('discounted_fee_reason'),
                amount_paid=fees['amount_paid'],
                remaining_amount=fees['remaining_amount'],
                payment_status=fees['payment_status'],
                partner_data=partner_data,
                currency=currency_code,
                workflow_stages_snapshot=WorkflowHandler.get_workflow_snapshot(service),
                prerequisites_snapshot=WorkflowHandler.get_prerequisites_snapshot(service),
                # ERP integration fields — from erp_data_function or org_config
                is_donor_invoice_allowed=ERPHandler.get_field(erp_data, 'is_donor_invoice_allowed', org_config.is_donor_invoice_allowed),
                available_grant_sources_ids=available_grant_sources_ids,
                is_discount_allowed=ERPHandler.get_field(erp_data, 'is_discount_allowed', org_config.is_discount_allowed),
                erp_product_id=ERPHandler.get_field(erp_data, 'erp_product_id', org_config.erp_product_id),
                erp_product_name=ERPHandler.get_field(erp_data, 'erp_product_name', org_config.erp_product_name),
                erp_product_for_discount_id=ERPHandler.get_field(erp_data, 'erp_product_for_discount_id', org_config.erp_product_for_discount_id),
                erp_product_for_discount_name=ERPHandler.get_field(erp_data, 'erp_product_for_discount_name', org_config.erp_product_for_discount_name),
                erp_product_for_internal_donors_id=ERPHandler.get_field(erp_data, 'erp_product_for_internal_donors_id', org_config.erp_product_for_internal_donors_id),
                erp_product_for_internal_donors_name=ERPHandler.get_field(erp_data, 'erp_product_for_internal_donors_name', org_config.erp_product_for_internal_donors_name),
                erp_project_id=ERPHandler.get_field(erp_data, 'erp_project_id', org_config.erp_project_id),
                erp_project_name=ERPHandler.get_field(erp_data, 'erp_project_name', org_config.erp_project_name),
                erp_activity_id=ERPHandler.get_field(erp_data, 'erp_activity_id', org_config.erp_activity_id),
                erp_activity_name=ERPHandler.get_field(erp_data, 'erp_activity_name', org_config.erp_activity_name),
                erp_cost_center_id=ERPHandler.get_field(erp_data, 'erp_cost_center_id', org_config.erp_cost_center_id),
                erp_cost_center_name=ERPHandler.get_field(erp_data, 'erp_cost_center_name', org_config.erp_cost_center_name),
            )
            
            WorkflowHandler.save_prerequisites_verification(
                service=service,
                user=user,
                data=data,
                service_request=service_request
            )
            
            attachments_dict = row_data.get('attachments', {})
            for key, attachment in attachments_dict.items():
                if attachment.get('file'):
                    RequestAttachment.objects.create(
                        fk_request=service_request,
                        name=attachment.get('name', ''),
                        file=attachment.get('file'),
                        fk_uploaded_by=user,
                        description=attachment.get('description', '')
                    )
            
            if installment_plans and fees['remaining_amount'] > 0:
                for plan in installment_plans:
                    # نسبة القسط من خطة الاقساط مقابل رسوم الخدمة الاساسية
                    plan_percentage = plan.percentage
                    # plan_amount = plan.amount
                    plan_amount = round(Decimal(service_request.total_fee) * plan_percentage,2)
                    org_service_config = service_request.org_service_config
                    due_date = timezone.now().date() + timezone.timedelta(days=plan.due_days_from_request or 0)
                    RequestInstallment.objects.create(
                        fk_request=service_request,
                        amount=plan_amount,
                        period=org_service_config.installment_period,
                        order=plan.order,
                        due_date=due_date,
                        payment_status=PaymentStatusChoice.UNPAID
                    )

            LoggingManager.log_request_create(
                service_request=service_request,
                user=user,
                request=request,
                new_status=ServiceStatusChoice.PENDING,
                notes=f'تم إنشاء طلب جديد برقم {request_number}',
                extra_data={
                    'service_id': service_id,
                    'service_name': service.name_ar,
                    'total_fee': str(fees['total_fee']),
                    'payment_status': fees['payment_status'],
                }
            )
        
        return ResponseHandler.created(
            message=Messages.REQUEST_CREATED,
            data=ServiceRequestSerializer(service_request).data,
            extra={'request_number': request_number}
        )
    
    @action(detail=True, methods=['post'], url_path='start', url_name='start')
    @handle_exceptions
    def start_request(self, request, pk=None):
        instance = self.get_object()
        user = request.user
        
        ValidationHandler.validate_for_action(
            instance=instance,
            user=user,
            permission_type='START',
            allowed_statuses=[ServiceStatusChoice.PENDING],
            check_lock=True,
            action_name='start_request'
        )
        
        with transaction.atomic():
            instance.status = ServiceStatusChoice.IN_PROGRESS
            instance.start_request_at = timezone.now()
            instance.save()
            
            installments = instance.installments.filter(is_deleted=False)
            updated_installments_count = 0
            
            if installments.exists():
                org_config = OrganizationServiceConfig.objects.filter(
                    fk_service=instance.fk_service,
                    fk_organization=instance.fk_organization,
                    is_active=True
                ).first()
                
                if org_config:
                    installment_plans = {
                        plan.order: plan.due_days_from_request or 0
                        for plan in org_config.installment_plans.all()
                    }
                    
                    for installment in installments:
                        due_days = installment_plans.get(installment.order, 0)
                        new_due_date = timezone.now().date() + timezone.timedelta(days=due_days)
                        installment.due_date = new_due_date
                        installment.save()
                        updated_installments_count += 1
            
            workflow_steps = list(instance.fk_service.workflow_steps.filter(
            ).order_by('order'))
            
            # Import here to avoid circular import
            from d_services.models.StageChecklistItem import StageChecklistItem, WorkflowStepChecklistTemplate
            
            # Prepare all actions first for bulk creation
            now = timezone.now()
            actions_to_create = []
            workflow_step_ids = [step.id for step in workflow_steps]
            
            for index, step in enumerate(workflow_steps):
                is_first = (index == 0)
                actions_to_create.append(RequestAction(
                    fk_request=instance,
                    fk_workflow_step=step,
                    is_final_step=step.is_final_step,
                    is_execution_step=step.is_execution_step,
                    has_custom_output=step.has_custom_output,
                    has_custom_input=step.has_custom_input,
                    has_approval=step.has_approval,
                    custom_output_template=step.custom_output_template,
                    custom_input_template=step.custom_input_template,
                    start_time=now if is_first else None,
                    stage_status=StageStatusChoice.PENDING,
                    is_current=is_first,
                    order=step.order,
                    stage_metadata={
                        'workflow_step_order': step.order,
                        'start_offset_days': step.start_offset_days,
                        'delivery_offset_days': step.delivery_offset_days,
                        'execution_procedure_name': step.execution_procedure_name,
                    }
                ))
            
            # Bulk create all actions at once
            created_actions = RequestAction.objects.bulk_create(actions_to_create)
            created_actions_count = len(created_actions)
            
            # Map workflow step ID to created action for checklist creation
            step_to_action = {action.fk_workflow_step_id: action for action in created_actions}
            first_action = created_actions[0] if created_actions else None
            
            # Fetch all checklist templates for all workflow steps at once
            all_templates = WorkflowStepChecklistTemplate.objects.filter(
                fk_workflow_step_id__in=workflow_step_ids,
                fk_org_service_config__fk_organization=instance.fk_organization
            ).order_by('fk_workflow_step_id', 'order')
            
            # Prepare checklist items for bulk creation
            checklist_items_to_create = []
            for template in all_templates:
                action = step_to_action.get(template.fk_workflow_step_id)
                if action:
                    checklist_items_to_create.append(StageChecklistItem(
                        fk_request_action=action,
                        title=template.title,
                        description=template.description,
                        order=template.order,
                        is_required=template.is_required
                    ))
            
            # Bulk create all checklist items at once
            if checklist_items_to_create:
                StageChecklistItem.objects.bulk_create(checklist_items_to_create)
        
        response_extra = {
            'actions_created': created_actions_count,
        }
        
        if first_action:
            response_extra['current_action'] = {
                'id': first_action.id,
                'workflow_step': first_action.fk_workflow_step_id,
                'stage_status': first_action.stage_status,
                'is_current': first_action.is_current
            }
        
        if updated_installments_count > 0:
            response_extra['installments_message'] = _('تم تحديث تواريخ استحقاق %d قسط/أقساط بناءً على تاريخ البدء') % updated_installments_count
        
        LoggingManager.log_request_action(
            service_request=instance,
            action=LogActionChoice.START,
            user=user,
            request=request,
            old_status=ServiceStatusChoice.PENDING,
            new_status=ServiceStatusChoice.IN_PROGRESS,
            notes=f'تم بدء تنفيذ الطلب - تم إنشاء {created_actions_count} مرحلة',
            extra_data={'actions_created': created_actions_count}
        )
        
        return ResponseHandler.success(
            message=Messages.REQUEST_STARTED,
            data=ServiceRequestSerializer(instance).data,
            extra=response_extra
        )
    
    @action(detail=True, methods=['post'], url_path='lock', url_name='lock')
    @handle_exceptions
    def lock_request(self, request, pk=None):
        instance = self.get_object()
        user = request.user
        
        ValidationHandler.validate_organization(instance, user)
        ValidationHandler.validate_permission(user, instance.fk_service_id, 'LOCK')
        
        if instance.is_locked:
            raise BusinessRuleException(
                message=_('الطلب مقفول بالفعل'),
                details={
                    'locked_at': instance.locked_at.strftime('%Y-%m-%d %H:%M') if instance.locked_at else None,
                    'locked_reason': instance.locked_reason
                }
            )
        
        locked_reason = request.data.get('locked_reason')
        if not locked_reason:
            raise ValidationException(message=_('سبب القفل مطلوب'))
        
        instance.is_locked = True
        instance.locked_reason = locked_reason
        instance.locked_at = timezone.now()
        instance.save()
        
        LoggingManager.log_request_action(
            service_request=instance,
            action=LogActionChoice.LOCK,
            user=user,
            request=request,
            notes=f'تم قفل الطلب: {locked_reason}',
            extra_data={'locked_reason': locked_reason}
        )
        
        return ResponseHandler.success(
            message=Messages.REQUEST_LOCKED,
            data=ServiceRequestSerializer(instance).data,
            extra={
                'locked_at': instance.locked_at,
                'locked_reason': instance.locked_reason
            }
        )
    
    @action(detail=True, methods=['post'], url_path='unlock', url_name='unlock')
    @handle_exceptions
    def unlock_request(self, request, pk=None):
        instance = self.get_object()
        user = request.user
        
        ValidationHandler.validate_organization(instance, user)
        ValidationHandler.validate_permission(user, instance.fk_service_id, 'UNLOCK')
        
        if not instance.is_locked:
            raise BusinessRuleException(
                message=_('الطلب غير مقفول'),
                hint=_('لا يمكن فتح قفل طلب غير مقفول')
            )
        
        if instance.status == ServiceStatusChoice.REJECTED:
            raise InvalidStatusException(
                message=_('لا يمكن فتح قفل طلب مرفوض'),
                details={'status': instance.get_status_display()}
            )
        lock_days = 0
        if instance.locked_at:
            lock_duration = timezone.now() - instance.locked_at
            lock_days = lock_duration.days
        
        with transaction.atomic():
            unpaid_installments = instance.installments.filter(
                is_deleted=False,
                payment_status=PaymentStatusChoice.UNPAID
            )
            
            updated_installments_count = 0
            installments_info = []
            
            if unpaid_installments.exists() and lock_days > 0:
                for installment in unpaid_installments:
                    old_due_date = installment.due_date
                    new_due_date = old_due_date + timezone.timedelta(days=lock_days)
                    installment.due_date = new_due_date
                    installment.save()
                    updated_installments_count += 1
                    installments_info.append({
                        'order': installment.order,
                        'old_due_date': old_due_date.strftime('%Y-%m-%d'),
                        'new_due_date': new_due_date.strftime('%Y-%m-%d'),
                        'added_days': lock_days
                    })
            
            previous_locked_at = instance.locked_at
            previous_locked_reason = instance.locked_reason
            
            instance.is_locked = False
            instance.locked_reason = None
            instance.locked_at = None
            instance.save()
            
            LoggingManager.log_request_action(
                service_request=instance,
                action=LogActionChoice.UNLOCK,
                user=user,
                request=request,
                notes=f'تم فتح قفل الطلب بعد {lock_days} أيام',
                extra_data={
                    'lock_days': lock_days,
                    'previous_reason': previous_locked_reason,
                    'installments_updated': updated_installments_count
                }
            )
        
        response_extra = {
            'lock_duration_days': lock_days,
            'previous_locked_at': previous_locked_at.strftime('%Y-%m-%d %H:%M') if previous_locked_at else None,
            'previous_locked_reason': previous_locked_reason,
        }
        
        if updated_installments_count > 0:
            response_extra['installments_updated'] = {
                'message': _('تم إضافة %d يوم/أيام إلى تواريخ استحقاق %d قسط/أقساط غير مدفوعة') % (lock_days, updated_installments_count),
                'details': installments_info
            }
        elif unpaid_installments.exists() and lock_days == 0:
            response_extra['installments_note'] = _('لم تتم إضافة أيام للأقساط لأن مدة القفل أقل من يوم واحد')
        
        return ResponseHandler.success(
            message=Messages.REQUEST_UNLOCKED,
            data=ServiceRequestSerializer(instance).data,
            extra=response_extra
        )

    @action(detail=True, methods=['post'], url_path='reject', url_name='reject')
    @handle_exceptions
    def reject_request(self, request, pk=None):
        instance = self.get_object()
        user = request.user
        
        ValidationHandler.validate_for_action(
            instance=instance,
            user=user,
            permission_type='REJECT',
            allowed_statuses=[ServiceStatusChoice.PENDING],
            check_lock=True,
            action_name='reject_request'
        )
        
        reject_reason = request.data.get('reject_reason')
        if not reject_reason:
            raise ValidationException(message=_('سبب الرفض مطلوب'))
        
        old_status = instance.status
        instance.status = ServiceStatusChoice.REJECTED
        instance.reject_reason = reject_reason
        instance.reject_at = timezone.now()
        instance.is_locked = True
        instance.locked_reason = _('تم رفض الطلب')
        instance.locked_at = timezone.now()
        instance.save()
        
        LoggingManager.log_request_status_change(
            service_request=instance,
            user=user,
            request=request,
            old_status=old_status,
            new_status=ServiceStatusChoice.REJECTED,
            notes=f'تم رفض الطلب: {reject_reason}',
            extra_data={'reject_reason': reject_reason}
        )
        
        return ResponseHandler.success(
            message=Messages.REQUEST_REJECTED,
            data=ServiceRequestSerializer(instance).data,
            extra={
                'reject_at': instance.reject_at,
                'reject_reason': instance.reject_reason
            }
        )

    @action(detail=True, methods=['post'], url_path='complete', url_name='complete')
    @handle_exceptions
    def complete_request(self, request, pk=None):
        instance = self.get_object()
        user = request.user
        
        ValidationHandler.validate_for_action(
            instance=instance,
            user=user,
            permission_type='COMPLETE',
            allowed_statuses=[ServiceStatusChoice.IN_PROGRESS],
            check_lock=True,
            action_name='complete_request'
        )
        
        if instance.status == ServiceStatusChoice.REJECTED:
            raise InvalidStatusException(
                message=_('لا يمكن إكمال طلب مرفوض'),
                details={
                    'reject_reason': instance.reject_reason,
                    'rejected_at': instance.reject_at.strftime('%Y-%m-%d %H:%M') if instance.reject_at else None
                }
            )
        
        all_actions = instance.actions.filter(is_deleted=False)
        
        if not all_actions.exists():
            raise BusinessRuleException(
                message=_('لا توجد مراحل لهذا الطلب'),
                hint=_('يجب بدء الطلب أولاً لإنشاء المراحل')
            )
        
        incomplete_actions = all_actions.exclude(stage_status=StageStatusChoice.COMPLETED)
        
        if incomplete_actions.exists():
            incomplete_steps = [
                {
                    'action_id': action.id,
                    'workflow_step_id': action.fk_workflow_step_id,
                    'step_order': action.fk_workflow_step.order if action.fk_workflow_step else None,
                    'stage_status': action.stage_status,
                    'stage_status_display': action.get_stage_status_display()
                }
                for action in incomplete_actions
            ]
            raise BusinessRuleException(
                message=_('لا يمكن إكمال الطلب لأن بعض المراحل غير مكتملة'),
                details={
                    'incomplete_steps_count': incomplete_actions.count(),
                    'incomplete_steps': incomplete_steps
                },
                hint=_('يجب إكمال جميع المراحل قبل إكمال الطلب')
            )
        
        with transaction.atomic():
            old_status = instance.status
            instance.status = ServiceStatusChoice.COMPLETED
            instance.final_delivery_date = timezone.now().date()
            instance.save()
            
            LoggingManager.log_request_status_change(
                service_request=instance,
                user=user,
                request=request,
                old_status=old_status,
                new_status=ServiceStatusChoice.COMPLETED,
                notes='تم إكمال الطلب بنجاح',
                extra_data={'final_delivery_date': str(instance.final_delivery_date)}
            )
        
        return ResponseHandler.success(
            message=Messages.REQUEST_COMPLETED,
            data=ServiceRequestSerializer(instance).data,
            extra={'completed_at': instance.final_delivery_date}
        )

    @action(detail=True, methods=['post'], url_path='cancel', url_name='cancel')
    @handle_exceptions
    def cancel_request(self, request, pk=None):

        instance = self.get_object()
        user = request.user
        
        allowed_statuses = [
            ServiceStatusChoice.PENDING,
            ServiceStatusChoice.APPROVED,
            ServiceStatusChoice.IN_PROGRESS
        ]
        
        ValidationHandler.validate_for_action(
            instance=instance,
            user=user,
            permission_type='CANCEL',
            allowed_statuses=allowed_statuses,
            check_lock=True,
            action_name='cancel_request'
        )
        
        cancel_reason = request.data.get('cancel_reason')
        if not cancel_reason:
            raise ValidationException(message=_('سبب الإلغاء مطلوب'))
        
        with transaction.atomic():
            old_status = instance.status
            instance.status = ServiceStatusChoice.CANCELLED
            instance.cancel_reason = cancel_reason
            instance.cancelled_at = timezone.now()
            instance.is_locked = True
            instance.locked_reason = _('تم إلغاء الطلب')
            instance.locked_at = timezone.now()
            instance.save()
            
            cancelled_actions_count = instance.actions.exclude(
                stage_status=StageStatusChoice.COMPLETED
            ).update(
                stage_status=StageStatusChoice.CANCELLED,
                notes=_('تم إلغاء المرحلة بسبب إلغاء الطلب')
            )
            
            LoggingManager.log_request_status_change(
                service_request=instance,
                user=user,
                request=request,
                old_status=old_status,
                new_status=ServiceStatusChoice.CANCELLED,
                notes=f'تم إلغاء الطلب: {cancel_reason}',
                extra_data={
                    'cancel_reason': cancel_reason,
                    'cancelled_actions_count': cancelled_actions_count
                }
            )
        
        return ResponseHandler.success(
            message=Messages.REQUEST_CANCELLED,
            data=ServiceRequestSerializer(instance).data,
            extra={
                'cancelled_at': instance.cancelled_at,
                'cancel_reason': instance.cancel_reason
            }
        )

    @action(detail=True, methods=['post'], url_path='assign-grant', url_name='assign-grant')
    @handle_exceptions
    def assign_grant(self, request, pk=None):
        instance = self.get_object()
        user = request.user

        ValidationHandler.validate_for_action(
            instance=instance,
            user=user,
            permission_type='ASSIGN_GRANT',
            allowed_statuses=[ServiceStatusChoice.PENDING, ServiceStatusChoice.APPROVED],
            check_lock=True,
            action_name='assign_grant'
        )

        # Check if grants are allowed for this service request
        if not instance.is_donor_invoice_allowed:
            raise BusinessRuleException(
                message=_('هذا الطلب لا يتيح خيار المنحة'),
                hint=_('تم تعطيل خيار المنحة لهذه الخدمة')
            )

        allowed_grant_statuses = [GrantStatusChoice.NO_GRANT, GrantStatusChoice.REJECTED, GrantStatusChoice.CANCELLED]
        if instance.grant_status not in allowed_grant_statuses:
            raise BusinessRuleException(
                message=_('الطلب لديه منحة قيد الانتظار أو مقبولة'),
                details={'current_status': instance.grant_status},
                hint=_('يجب إلغاء أو رفض المنحة الحالية أولاً')
            )

        is_internal_donors = request.data.get('is_internal_donors', False)
        grant_source_id = request.data.get('fk_grant_source')
        grant_percentage = request.data.get('grant_percentage')

        # grant_percentage is required
        if grant_percentage is None:
            raise ValidationException(message=_('نسبة المنحة مطلوبة'))

        grant_percentage = Decimal(str(grant_percentage))
        if grant_percentage < 0 or grant_percentage > 100:
            raise ValidationException(
                message=_('نسبة المنحة يجب أن تكون بين 0 و 100'),
                details={'provided_value': float(grant_percentage)}
            )

        # تحديد الخصم المسموح به بعد احتساب الخصم اذا وجد
        available_grant_percent = 100 - instance.discount_percentage

        if grant_percentage > available_grant_percent:
            raise ValidationException(
                message=_(f"نسبة المنحة اكبر من نسبة المنحة المسموح به ({available_grant_percent})"))

        grant_source = None
        erp_product_for_internal_donors_id = None
        erp_product_for_internal_donors_name = None

        if is_internal_donors:
            # For internal donors, require ERP fields from request data
            erp_product_for_internal_donors_id = request.data.get('erp_product_for_internal_donors_id')
            erp_product_for_internal_donors_name = request.data.get('erp_product_for_internal_donors_name')
            
            if not erp_product_for_internal_donors_id or not erp_product_for_internal_donors_name:
                raise ValidationException(
                    message=_('معرف واسم المنتج للمنح الداخلية مطلوبان'),
                    hint=_('يجب إرسال erp_product_for_internal_donors_id و erp_product_for_internal_donors_name')
                )
        else:
            # For external donors, grant_source is required
            if not grant_source_id:
                raise ValidationException(message=_('معرف مصدر المنحة مطلوب'))

            try:
                grant_source = GrantSource.objects.get(pk=grant_source_id, is_active=True)
            except GrantSource.DoesNotExist:
                raise ResourceNotFoundException(message=_('مصدر المنحة غير موجود أو غير نشط'))

        with transaction.atomic():
            instance.is_internal_donors = is_internal_donors
            instance.fk_grant_source = grant_source
            instance.grant_percentage = grant_percentage
            instance.grant_status = GrantStatusChoice.PENDING
            instance.grant_assigned_at = timezone.now()
            instance.grant_assigned_by = user

            # Update internal donors ERP fields if provided and different
            if is_internal_donors:
                if instance.erp_product_for_internal_donors_id != erp_product_for_internal_donors_id:
                    instance.erp_product_for_internal_donors_id = erp_product_for_internal_donors_id
                if instance.erp_product_for_internal_donors_name != erp_product_for_internal_donors_name:
                    instance.erp_product_for_internal_donors_name = erp_product_for_internal_donors_name

            instance.save()

        response_extra = {
            'is_internal_donors': is_internal_donors,
            'grant_percentage': float(grant_percentage),
            'grant_status': instance.grant_status,
            'hint': _('تحتاج موافقة لتفعيل المنحة')
        }

        if grant_source:
            response_extra['grant_source'] = grant_source.name_ar

        return ResponseHandler.success(
            message=_('تم تعيين المنحة (قيد الانتظار)'),
            extra=response_extra
        )

    @action(detail=True, methods=['post'], url_path='approve-grant', url_name='approve-grant')
    @handle_exceptions
    def approve_grant(self, request, pk=None):
        instance = self.get_object()
        user = request.user

        ValidationHandler.validate_for_action(
            instance=instance,
            user=user,
            permission_type='APPROVE_GRANT',
            allowed_statuses=[ServiceStatusChoice.PENDING, ServiceStatusChoice.APPROVED],
            check_lock=True,
            action_name='approve_grant'
        )

        if instance.grant_status != GrantStatusChoice.PENDING:
            raise InvalidStatusException(
                message=_('لا توجد منحة قيد الانتظار للموافقة عليها'),
                details={'current_status': instance.grant_status}
            )

        with transaction.atomic():
            grant_amount = (instance.total_fee * instance.grant_percentage) / 100

            instance.grant_amount = grant_amount
            instance.grant_status = GrantStatusChoice.APPROVED

            CalculationHandler.update_payment_status(instance)
            instance.save()

        return ResponseHandler.success(
            message=Messages.GRANT_APPROVED,
            extra={
                'grant_source': instance.fk_grant_source.name_ar,
                'grant_percentage': float(instance.grant_percentage),
                'grant_amount': float(instance.grant_amount),
                'grant_status': instance.grant_status,
                'remaining_amount': float(instance.remaining_amount),
                'payment_status': instance.payment_status
            }
        )

    @action(detail=True, methods=['post'], url_path='update-grant', url_name='update-grant')
    @handle_exceptions
    def update_grant(self, request, pk=None):
        instance = self.get_object()
        user = request.user

        ValidationHandler.validate_for_action(
            instance=instance, user=user,
            permission_type='UPDATE_GRANT',
            allowed_statuses=[ServiceStatusChoice.PENDING, ServiceStatusChoice.APPROVED],
            action_name='update_grant'
        )

        if instance.grant_status != GrantStatusChoice.APPROVED:
            raise InvalidStatusException(
                message=_('لا توجد منحة مقبولة للتعديل'),
                details={'current_status': instance.grant_status}
            )

        is_internal_donors = request.data.get('is_internal_donors')
        grant_source_id = request.data.get('fk_grant_source')
        grant_percentage = request.data.get('grant_percentage')
        erp_product_for_internal_donors_id = request.data.get('erp_product_for_internal_donors_id')
        erp_product_for_internal_donors_name = request.data.get('erp_product_for_internal_donors_name')

        if is_internal_donors is None and grant_source_id is None and grant_percentage is None:
            raise ValidationException(message=_('يجب تحديد على الأقل حقل واحد للتعديل'))

        old_is_internal = instance.is_internal_donors
        old_grant_source = instance.fk_grant_source.name_ar if instance.fk_grant_source else None
        old_grant_percentage = instance.grant_percentage
        old_grant_amount = instance.grant_amount

        with transaction.atomic():
            # Handle is_internal_donors change
            if is_internal_donors is not None:
                if is_internal_donors:
                    # Switching to internal donors, require ERP fields from request data
                    if not erp_product_for_internal_donors_id or not erp_product_for_internal_donors_name:
                        raise ValidationException(
                            message=_('معرف واسم المنتج للمنح الداخلية مطلوبان'),
                            hint=_('يجب إرسال erp_product_for_internal_donors_id و erp_product_for_internal_donors_name')
                        )
                    instance.is_internal_donors = True
                    instance.fk_grant_source = None  # Clear external grant source

                    # Update ERP fields if different
                    if instance.erp_product_for_internal_donors_id != erp_product_for_internal_donors_id:
                        instance.erp_product_for_internal_donors_id = erp_product_for_internal_donors_id
                    if instance.erp_product_for_internal_donors_name != erp_product_for_internal_donors_name:
                        instance.erp_product_for_internal_donors_name = erp_product_for_internal_donors_name
                else:
                    instance.is_internal_donors = False

            # Handle grant_source update (only for non-internal donors)
            if grant_source_id is not None:
                if instance.is_internal_donors:
                    raise ValidationException(message=_('لا يمكن تحديد مصدر منحة للمنح الداخلية'))
                try:
                    grant_source = GrantSource.objects.get(pk=grant_source_id, is_active=True)
                    instance.fk_grant_source = grant_source
                except GrantSource.DoesNotExist:
                    raise ResourceNotFoundException(message=_('مصدر المنحة غير موجود أو غير نشط'))

            if grant_percentage is not None:
                grant_percentage = Decimal(str(grant_percentage))
                if grant_percentage < 0 or grant_percentage > 100:
                    raise ValidationException(
                        message=_('نسبة المنحة يجب أن تكون بين 0 و 100'),
                        details={'provided_value': float(grant_percentage)}
                    )
                # تحديد الخصم المسموح به بعد احتساب الخصم اذا وجد
                available_grant_percent = 100 - instance.discount_percentage

                if grant_percentage > available_grant_percent:
                    raise ValidationException(
                        message=_(f"نسبة المنحة اكبر من نسبة المنحة المسموح به ({available_grant_percent})"))
                instance.grant_percentage = grant_percentage

            instance.grant_amount = (instance.total_fee * instance.grant_percentage) / 100

            CalculationHandler.update_payment_status(instance)
            instance.save()

        return ResponseHandler.success(
            message=Messages.GRANT_UPDATED,
            extra={
                'old_is_internal': old_is_internal,
                'new_is_internal': instance.is_internal_donors,
                'old_grant_source': old_grant_source,
                'new_grant_source': instance.fk_grant_source.name_ar if instance.fk_grant_source else None,
                'old_percentage': float(old_grant_percentage),
                'new_percentage': float(instance.grant_percentage),
                'old_amount': float(old_grant_amount),
                'new_amount': float(instance.grant_amount),
                'remaining_amount': float(instance.remaining_amount),
                'payment_status': instance.payment_status
            }
        )

    @action(detail=True, methods=['post'], url_path='cancel-grant', url_name='cancel-grant')
    @handle_exceptions
    def cancel_grant(self, request, pk=None):
        instance = self.get_object()
        user = request.user

        ValidationHandler.validate_for_action(
            instance=instance, user=user,
            permission_type='CANCEL_GRANT',
            allowed_statuses=[ServiceStatusChoice.PENDING, ServiceStatusChoice.APPROVED],
            action_name='cancel_grant'
        )

        if instance.grant_status not in [GrantStatusChoice.PENDING, GrantStatusChoice.APPROVED]:
            raise BusinessRuleException(
                message=_('لا توجد منحة لإلغائها'),
                details={'current_status': instance.grant_status}
            )

        cancel_reason = request.data.get('cancel_reason')
        if not cancel_reason:
            raise ValidationException(message=_('سبب الإلغاء مطلوب'))

        old_grant_source = instance.fk_grant_source.name_ar if instance.fk_grant_source else None
        old_grant_amount = instance.grant_amount

        with transaction.atomic():
            instance.grant_status = GrantStatusChoice.CANCELLED
            instance.grant_cancel_reason = cancel_reason
            instance.grant_cancel_at = timezone.now()
            instance.grant_cancel_by = user

            instance.grant_amount = 0
            instance.grant_percentage = 0

            CalculationHandler.update_payment_status(instance)
            instance.save()

        return ResponseHandler.success(
            message=Messages.GRANT_CANCELLED,
            extra={
                'cancelled_grant': old_grant_source,
                'cancelled_amount': float(old_grant_amount),
                'cancel_reason': cancel_reason,
                'grant_status': instance.grant_status,
                'remaining_amount': float(instance.remaining_amount),
                'payment_status': instance.payment_status
            }
        )

    @action(detail=True, methods=['post'], url_path='reject-grant', url_name='reject-grant')
    @handle_exceptions
    def reject_grant(self, request, pk=None):
        try:

            instance = self.get_object()
            user = request.user

            ValidationHandler.validate_for_action(
                instance=instance, user=user,
                permission_type='REJECT_GRANT',
                allowed_statuses=[ServiceStatusChoice.PENDING, ServiceStatusChoice.APPROVED],
                action_name='reject_grant'
            )

            if not instance.fk_grant_source or instance.grant_status != GrantStatusChoice.PENDING:
                raise BusinessRuleException(
                    message=_('لا توجد منحة  تحت الانتظار لرفضها'),
                    details={'current_status': instance.grant_status}
                )

            reject_reason = request.data.get('reject_reason')
            if not reject_reason:
                raise ValidationException(message=_('سبب الرفض مطلوب'))

            old_grant_source = instance.fk_grant_source.name_ar
            old_grant_amount = instance.grant_amount

            with transaction.atomic():
                instance.grant_status = GrantStatusChoice.REJECTED
                instance.grant_rejected_reason = reject_reason
                instance.grant_rejected_at = timezone.now()
                instance.grant_rejected_by = user
                instance.grant_amount = 0
                instance.grant_percentage = 0
                CalculationHandler.update_payment_status(instance)
                instance.save()

            return ResponseHandler.success(
                message=Messages.GRANT_REJECTED,
                extra={
                    'rejected_grant': old_grant_source,
                    'rejected_amount': float(old_grant_amount),
                    'reject_reason': reject_reason,
                    'grant_status': instance.grant_status,
                    'remaining_amount': float(instance.remaining_amount),
                    'payment_status': instance.payment_status
                }
            )
        except Exception as e:
            print(e)
            return  ResponseHandler.bad_request(
                message="فشل رفض المنحة"
            )


    @action(detail=True, methods=['post'], url_path='add-discount', url_name='add-discount')
    @handle_exceptions
    def add_discount(self, request, pk=None):
        instance = self.get_object()
        user = request.user

        ValidationHandler.validate_for_action(
            instance=instance, user=user,
            permission_type='ADD_DISCOUNT',
            allowed_statuses=[ServiceStatusChoice.PENDING, ServiceStatusChoice.APPROVED],
            action_name='add_discount'
        )

        # Check if discounts are allowed for this service request
        if not instance.is_discount_allowed:
            raise BusinessRuleException(
                message=_('هذا الطلب لا يتيح خيار الخصم'),
                hint=_('تم تعطيل خيار الخصم لهذه الخدمة')
            )

        if instance.discount_status in [DiscountStatusChoice.PENDING, DiscountStatusChoice.APPROVED]:
            raise BusinessRuleException(
                message=_('يوجد خصم قيد الانتظار أو مقبول على هذا الطلب'),
                details={'current_status': instance.discount_status},
                hint=_('يجب إلغاء أو رفض الخصم الحالي أولاً')
            )

        discount_percentage = request.data.get('discount_percentage')
        discount_reason = request.data.get('discount_reason')
        erp_product_for_discount_id = request.data.get('erp_product_for_discount_id')
        erp_product_for_discount_name = request.data.get('erp_product_for_discount_name')

        if not discount_percentage:
            raise ValidationException(message=_('نسبة الخصم مطلوب'))
        if not discount_reason:
            raise ValidationException(message=_('سبب الخصم مطلوب'))

        # Require discount ERP product fields from request data
        if not erp_product_for_discount_id or not erp_product_for_discount_name:
            raise ValidationException(
                message=_('معرف واسم المنتج للخصم مطلوبان'),
                hint=_('يجب إرسال erp_product_for_discount_id و erp_product_for_discount_name')
            )

        discount_percentage = Decimal(str(discount_percentage))

        # if discount_percentage <= 0:
        #     raise ValidationException(message=_('نسبة الخصم يجب أن تكون أكبر من صفر'))
        #
        if discount_percentage > 100 or discount_percentage < 0:
            raise ValidationException(
                message=_('نسبة الخصم يجب ان تكون بين 0 - 100 '),
                details={'total_fee': float(instance.total_fee), 'requested': float(discount_percentage)}
            )
        # تحديد الخصم المسموح به بعد احتساب المنحة اذا وجدت
        available_discount_percent = 100 - instance.grant_percentage

        if discount_percentage > available_discount_percent:
            raise ValidationException(
                message=_(f"نسبة الخصم اكبر من نسبة الخصم المسموح به ({available_discount_percent})"))

        with transaction.atomic():
            instance.discount_percentage = discount_percentage
            instance.discount_reason = discount_reason
            instance.discount_status = DiscountStatusChoice.PENDING
            instance.discount_at = timezone.now()
            instance.discount_by = user

            # Update discount ERP fields if different
            if instance.erp_product_for_discount_id != erp_product_for_discount_id:
                instance.erp_product_for_discount_id = erp_product_for_discount_id
            if instance.erp_product_for_discount_name != erp_product_for_discount_name:
                instance.erp_product_for_discount_name = erp_product_for_discount_name

            instance.save()
        discount_ratio = round(Decimal(discount_percentage) / 100, 2) if discount_percentage else 0
        discount_amount = round(instance.total_fee * discount_ratio, 2) if discount_ratio else 0
        return ResponseHandler.success(
            message=Messages.DISCOUNT_ADDED,
            extra={
                'discount_amount':float(discount_amount),
                'discount_percentage': float(discount_percentage),
                'discount_reason': discount_reason,
                'discount_status': instance.discount_status,
                'erp_product_for_discount_id': erp_product_for_discount_id,
                'erp_product_for_discount_name': erp_product_for_discount_name,
                'hint': Messages.HINT_DISCOUNT_PENDING
            }
        )

    @action(detail=True, methods=['post'], url_path='approve-discount', url_name='approve-discount')
    @handle_exceptions
    def approve_discount(self, request, pk=None):
        instance = self.get_object()
        user = request.user

        ValidationHandler.validate_for_action(
            instance=instance, user=user,
            permission_type='APPROVE_DISCOUNT',
            allowed_statuses=[ServiceStatusChoice.PENDING, ServiceStatusChoice.APPROVED],
            action_name='approve_discount'
        )

        if instance.discount_status != DiscountStatusChoice.PENDING:
            raise InvalidStatusException(
                message=_('لا يوجد خصم قيد الانتظار للموافقة عليه'),
                details={'current_status': instance.discount_status}
            )

        with transaction.atomic():
            discount_ratio = round(Decimal(instance.discount_percentage) / 100, 2) if instance.discount_percentage else None
            discount_amount = round(instance.total_fee * discount_ratio, 2) if discount_ratio else None
            instance.discount_status = DiscountStatusChoice.APPROVED
            instance.discount_amount = discount_amount
            CalculationHandler.update_payment_status(instance)
            instance.save()

        return ResponseHandler.success(
            message=Messages.DISCOUNT_APPROVED,
            extra={
                'discount_amount': float(instance.discount_amount),
                'discount_reason': instance.discount_reason,
                'discount_status': instance.discount_status,
                'remaining_amount': float(instance.remaining_amount),
                'payment_status': instance.payment_status
            }
        )

    @action(detail=True, methods=['post'], url_path='update-discount', url_name='update-discount')
    @handle_exceptions
    def update_discount(self, request, pk=None):
        instance = self.get_object()
        user = request.user

        ValidationHandler.validate_for_action(
            instance=instance, user=user,
            permission_type='UPDATE_DISCOUNT',
            allowed_statuses=[ServiceStatusChoice.PENDING, ServiceStatusChoice.APPROVED],
            action_name='update_discount'
        )
        
        if instance.discount_status != DiscountStatusChoice.APPROVED:
            raise InvalidStatusException(
                message=_('لا يوجد خصم مقبول للتعديل'),
                details={'current_status': instance.discount_status}
            )

        # discount_amount = request.data.get('discount_amount')
        discount_percentage = request.data.get('discount_percentage')
        discount_reason = request.data.get('discount_reason')
        erp_product_for_discount_id = request.data.get('erp_product_for_discount_id')
        erp_product_for_discount_name = request.data.get('erp_product_for_discount_name')

        if discount_percentage is None and discount_reason is None and erp_product_for_discount_id is None and erp_product_for_discount_name is None:
            raise ValidationException(message=_('يجب تحديد على الأقل حقل واحد للتعديل'))

        old_discount = instance.discount_amount
        old_reason = instance.discount_reason

        with transaction.atomic():
            if discount_percentage is not None:
                discount_percentage = Decimal(str(discount_percentage))

                if discount_percentage > 100 or discount_percentage < 0:
                    raise ValidationException(
                        message=_('نسبة الخصم يجب ان تكون بين 0 - 100 '),
                        details={'total_fee': float(instance.total_fee), 'requested': float(discount_percentage)}
                    )
                # تحديد الخصم المسموح به بعد احتساب المنحة اذا وجدت
                available_discount_percent = 100 - instance.grant_percentage

                if discount_percentage > available_discount_percent:
                    raise ValidationException(
                        message=_(f"نسبة الخصم اكبر من نسبة الخصم المسموح به ({available_discount_percent})"))

                instance.discount_percentage = discount_percentage
                discount_ratio = round(Decimal(instance.discount_percentage) / 100,2) if instance.discount_percentage else 0
                discount_amount = round(instance.total_fee * discount_ratio, 2) if discount_ratio else 0
                instance.discount_amount = discount_amount

            if discount_reason is not None:
                instance.discount_reason = discount_reason

            # Update discount ERP fields if provided and different
            if erp_product_for_discount_id is not None:
                if instance.erp_product_for_discount_id != erp_product_for_discount_id:
                    instance.erp_product_for_discount_id = erp_product_for_discount_id
            if erp_product_for_discount_name is not None:
                if instance.erp_product_for_discount_name != erp_product_for_discount_name:
                    instance.erp_product_for_discount_name = erp_product_for_discount_name

            CalculationHandler.update_payment_status(instance)
            instance.save()

        return ResponseHandler.success(
            message=Messages.DISCOUNT_UPDATED,
            extra={
                'old_discount': float(old_discount),
                'new_discount': float(instance.discount_amount),
                'old_reason': old_reason,
                'new_reason': instance.discount_reason,
                'erp_product_for_discount_id': instance.erp_product_for_discount_id,
                'erp_product_for_discount_name': instance.erp_product_for_discount_name,
                'remaining_amount': float(instance.remaining_amount),
                'payment_status': instance.payment_status
            }
        )

    @action(detail=True, methods=['post'], url_path='cancel-discount', url_name='cancel-discount')
    @handle_exceptions
    def cancel_discount(self, request, pk=None):
        instance = self.get_object()
        user = request.user

        ValidationHandler.validate_for_action(
            instance=instance, user=user,
            permission_type='CANCEL_DISCOUNT',
            allowed_statuses=[ServiceStatusChoice.PENDING, ServiceStatusChoice.APPROVED],
            action_name='cancel_discount'
        )

        if instance.discount_status != DiscountStatusChoice.APPROVED:
            raise InvalidStatusException(
                message=_('لا يوجد خصم مقبول لإلغائه'),
                details={'current_status': instance.discount_status}
            )

        cancel_reason = request.data.get('cancel_reason')
        if not cancel_reason:
            raise ValidationException(message=_('سبب الإلغاء مطلوب'))

        old_discount_amount = instance.discount_amount
        old_discount_reason = instance.discount_reason

        with transaction.atomic():
            instance.discount_status = DiscountStatusChoice.CANCELLED
            instance.discount_canceled_reason = cancel_reason
            instance.discount_canceled_at = timezone.now()
            instance.discount_canceled_by = user
            instance.discount_amount = 0
            instance.discount_percentage = 0
            CalculationHandler.update_payment_status(instance)
            instance.save()

        return ResponseHandler.success(
            message=Messages.DISCOUNT_CANCELLED,
            extra={
                'cancelled_discount_amount': float(old_discount_amount),
                'cancelled_discount_reason': old_discount_reason,
                'cancel_reason': cancel_reason,
                'discount_status': instance.discount_status,
                'remaining_amount': float(instance.remaining_amount),
                'payment_status': instance.payment_status
            }
        )

    @action(detail=True, methods=['post'], url_path='reject-discount', url_name='reject-discount')
    @handle_exceptions
    def reject_discount(self, request, pk=None):
        instance = self.get_object()
        user = request.user

        ValidationHandler.validate_for_action(
            instance=instance, user=user,
            permission_type='REJECT_DISCOUNT',
            allowed_statuses=[ServiceStatusChoice.PENDING, ServiceStatusChoice.APPROVED],
            action_name='reject_discount'
        )

        if instance.discount_status != DiscountStatusChoice.PENDING:
            raise InvalidStatusException(
                message=_('لا يوجد خصم تحت الانتظار لرفضه'),
                details={'current_status': instance.discount_status}
            )

        reject_reason = request.data.get('reject_reason')
        if not reject_reason:
            raise ValidationException(message=_('سبب الرفض مطلوب'))

        old_discount_amount = instance.discount_amount

        with transaction.atomic():
            instance.discount_status = DiscountStatusChoice.REJECTED
            instance.discount_rejected_reason = reject_reason
            instance.discount_rejected_at = timezone.now()
            instance.discount_rejected_by = user
            instance.discount_amount = 0
            instance.discount_percentage = 0
            CalculationHandler.update_payment_status(instance)
            instance.save()

        return ResponseHandler.success(
            message=Messages.DISCOUNT_REJECTED,
            extra={
                'rejected_discount_amount': float(old_discount_amount),
                'reject_reason': reject_reason,
                'discount_status': instance.discount_status,
                'remaining_amount': float(instance.remaining_amount),
                'payment_status': instance.payment_status
            }
        )

    # ========================================
    # إعدادات ERP للطلب - Request ERP Settings
    # ========================================
    @action(detail=True, methods=['patch'], url_path='update-erp-all_settings', url_name='update-erp-all_settings')
    @handle_exceptions
    def update_erp_settings(self, request, pk=None):
        """
        تحديث إعدادات ERP للطلب
        Update ERP all_settings for the service request
        """
        instance = self.get_object()
        user = request.user

        ValidationHandler.validate_for_action(
            instance=instance, user=user,
            permission_type='UPDATE',
            allowed_statuses=[ServiceStatusChoice.PENDING, ServiceStatusChoice.APPROVED, ServiceStatusChoice.IN_PROGRESS],
            action_name='update_erp_settings'
        )

        # Define allowed ERP fields for update
        erp_fields = [
            'erp_product_id',
            'erp_product_name',
            'erp_project_id',
            'erp_project_name',
            'erp_activity_id',
            'erp_activity_name',
            'erp_cost_center_id',
            'erp_cost_center_name',
        ]

        updated_fields = {}
        with transaction.atomic():
            for field in erp_fields:
                if field in request.data:
                    old_value = getattr(instance, field)
                    new_value = request.data.get(field)
                    if old_value != new_value:
                        setattr(instance, field, new_value)
                        updated_fields[field] = {
                            'old': old_value,
                            'new': new_value
                        }

            if not updated_fields:
                raise ValidationException(message=_('لم يتم تحديد أي حقول للتعديل'))

            instance.save()

        return ResponseHandler.success(
            message=_('تم تحديث إعدادات ERP للطلب بنجاح'),
            data=ServiceRequestSerializer(instance).data,
            extra={
                'updated_fields': updated_fields
            }
        )

    # ========================================
    # ملاحظات الطلب - Request Notes
    # ========================================
    @action(detail=True, methods=['get'], url_path='list-notes', url_name='list-notes')
    @handle_exceptions
    def list_notes(self, request, pk=None):
        """عرض ملاحظات الطلب - يتطلب صلاحية READ"""
        from d_services.models.RequestNote import RequestNote
        from d_services.serializers.requests import RequestNoteSerializer

        instance = self.get_object()
        user = request.user

        if not ValidationHandler.check_service_permission(user, instance.fk_service_id, 'READ'):
            return ResponseHandler.forbidden(_('ليس لديك صلاحية عرض ملاحظات هذا الطلب'))

        if instance.fk_organization != user.fk_organization and not user.is_superuser:
            return ResponseHandler.forbidden(_('ليس لديك صلاحية عرض ملاحظات هذا الطلب'))

        notes = instance.notes.filter(is_deleted=False).order_by('-created_at')
        serializer = RequestNoteSerializer(notes, many=True)

        return ResponseHandler.success(
            message=_('تم جلب الملاحظات بنجاح'),
            data=serializer.data,
            extra={'count': notes.count()}
        )

    @action(detail=True, methods=['post'], url_path='add-note', url_name='add-note')
    @handle_exceptions
    def add_note(self, request, pk=None):
        """إضافة ملاحظة على الطلب - يتطلب صلاحية READ"""
        from d_services.models.RequestNote import RequestNote
        from d_services.serializers.requests import RequestNoteSerializer

        instance = self.get_object()
        user = request.user

        if not ValidationHandler.check_service_permission(user, instance.fk_service_id, 'READ'):
            return ResponseHandler.forbidden(_('ليس لديك صلاحية إضافة ملاحظة على هذا الطلب'))

        if instance.fk_organization != user.fk_organization and not user.is_superuser:
            return ResponseHandler.forbidden(_('ليس لديك صلاحية إضافة ملاحظة على هذا الطلب'))

        content = request.data.get('content')
        if not content:
            raise ValidationException(message=_('محتوى الملاحظة مطلوب'))

        note = RequestNote.objects.create(
            fk_request=instance,
            content=content,
            fk_created_by=user
        )

        return ResponseHandler.created(
            message=_('تمت إضافة الملاحظة بنجاح'),
            data=RequestNoteSerializer(note).data
        )

    @action(detail=True, methods=['delete'], url_path='delete-note/(?P<note_id>[^/.]+)', url_name='delete-note')
    @handle_exceptions
    def delete_note(self, request, pk=None, note_id=None):
        """حذف ملاحظة - فقط صاحب الملاحظة أو المسؤول"""
        from d_services.models.RequestNote import RequestNote

        instance = self.get_object()
        user = request.user
        if not ValidationHandler.check_service_permission(user, instance.fk_service_id, 'DELETE'):
            return ResponseHandler.forbidden(_('ليس لديك صلاحية حذف ملاحظة على هذا الطلب'))
        try:
            note = RequestNote.objects.get(pk=note_id, fk_request=instance, is_deleted=False)
        except RequestNote.DoesNotExist:
            raise ResourceNotFoundException(message=_('الملاحظة غير موجودة'))

        if note.fk_created_by != user and not user.is_superuser:
            return ResponseHandler.forbidden(_('لا يمكنك حذف ملاحظة شخص آخر'))

        note.is_deleted = True
        note.save()

        return ResponseHandler.success(message=_('تم حذف الملاحظة بنجاح'))

    # ============================================================
    # إدارة المستندات - Document Management
    # ============================================================

    @action(detail=True, methods=['get'], url_path='input-data', url_name='input-data')
    @handle_exceptions
    def get_input_data(self, request, pk=None):
        """جلب بيانات المدخل للطلب"""
        instance = self.get_object()
        user = request.user

        if not ValidationHandler.check_service_permission(user, instance.fk_service_id, 'GET_INPUT_DATA'):
            return ResponseHandler.forbidden(_('ليس لديك صلاحية جلب بيانات المدخل'))

        if instance.fk_organization != user.fk_organization:
            return ResponseHandler.forbidden(_('ليس لديك صلاحية الوصول لهذا الطلب'))

        service = instance.fk_service

        func = instance.requests.filter(func=instance.input_data_function)

        response_data = {
            'input_template_type': service.input_template_type,
            'input_document': instance.input_document.url if instance.input_document else None,
            'input_data': getattr(func.first(), 'result') if func else None
        }

        # استدعاء دالة بيانات المدخل إذا وجدت
        # if service.input_data_function:
        #     from d_services.apis.external_methods import ExternalMethodHandler, FunctionType
        #     success, data = ExternalMethodHandler.call_function(
        #         service.input_data_function, instance, request,
        #         function_type=FunctionType.INPUT_DATA
        #     )
        #     if success:
        #         response_data['input_data'] = data

        return ResponseHandler.success(
            message=_('تم جلب بيانات المدخل بنجاح'),
            data=response_data
        )

    @action(detail=True, methods=['get'], url_path='output-data', url_name='output-data')
    @handle_exceptions
    def get_output_data(self, request, pk=None):
        """جلب بيانات المخرج للطلب"""
        instance = self.get_object()
        user = request.user

        if not ValidationHandler.check_service_permission(user, instance.fk_service_id, 'GET_OUTPUT_DATA'):
            return ResponseHandler.forbidden(_('ليس لديك صلاحية جلب بيانات المخرج'))

        if instance.fk_organization != user.fk_organization:
            return ResponseHandler.forbidden(_('ليس لديك صلاحية الوصول لهذا الطلب'))

        service = instance.fk_service

        func = instance.requests.filter(func=instance.output_data_function)

        response_data = {
            'output_template_type': service.output_template_type,
            'output_document': instance.output_document.url if instance.output_document else None,
            'output_data': getattr(func.first(), 'result') if func else None
        }

        # استدعاء دالة بيانات المخرج إذا وجدت
        # if service.output_data_function:
        #     from d_services.apis.external_methods import ExternalMethodHandler, FunctionType
        #     success, data = ExternalMethodHandler.call_function(
        #         service.output_data_function, instance, request,
        #         function_type=FunctionType.OUTPUT_DATA
        #     )
        #     if success:
        #         response_data['output_data'] = data

        return ResponseHandler.success(
            message=_('تم جلب بيانات المخرج بنجاح'),
            data=response_data
        )

    @action(detail=True, methods=['post'], url_path='upload-input', url_name='upload-input')
    @handle_exceptions
    def upload_input(self, request, pk=None):
        """رفع ملف المدخل"""
        instance = self.get_object()
        user = request.user

        if not ValidationHandler.check_service_permission(user, instance.fk_service_id, 'UPLOAD_INPUT'):
            return ResponseHandler.forbidden(_('ليس لديك صلاحية رفع ملف المدخل'))

        if instance.fk_organization != user.fk_organization:
            return ResponseHandler.forbidden(_('ليس لديك صلاحية الوصول لهذا الطلب'))

        if instance.is_locked:
            return ResponseHandler.forbidden(_('الطلب مقفول ولا يمكن تعديله'))

        input_file = request.FILES.get('input_document')
        if not input_file:
            raise ValidationException(message=_('ملف المدخل مطلوب'))

        instance.input_document = input_file
        instance.save()

        LoggingManager.log_request_action(
            service_request=instance,
            action=LogActionChoice.UPLOAD,
            user=user,
            request=request,
            notes=_('تم رفع ملف المدخل')
        )

        return ResponseHandler.success(
            message=_('تم رفع ملف المدخل بنجاح'),
            data={'input_document': instance.input_document.url}
        )

    @action(detail=True, methods=['post'], url_path='upload-output', url_name='upload-output')
    @handle_exceptions
    def upload_output(self, request, pk=None):
        """رفع ملف المخرج"""
        instance = self.get_object()
        user = request.user

        if not ValidationHandler.check_service_permission(user, instance.fk_service_id, 'UPLOAD_OUTPUT'):
            return ResponseHandler.forbidden(_('ليس لديك صلاحية رفع ملف المخرج'))

        if instance.fk_organization != user.fk_organization:
            return ResponseHandler.forbidden(_('ليس لديك صلاحية الوصول لهذا الطلب'))

        if instance.is_locked:
            return ResponseHandler.forbidden(_('الطلب مقفول ولا يمكن تعديله'))

        output_file = request.FILES.get('output_document')
        if not output_file:
            raise ValidationException(message=_('ملف المخرج مطلوب'))

        instance.output_document = output_file
        instance.save()

        LoggingManager.log_request_action(
            service_request=instance,
            action=LogActionChoice.UPLOAD,
            user=user,
            request=request,
            notes=_('تم رفع ملف المخرج')
        )

        return ResponseHandler.success(
            message=_('تم رفع ملف المخرج بنجاح'),
            data={'output_document': instance.output_document.url}
        )

    @action(detail=True, methods=['delete'], url_path='delete-input', url_name='delete-input')
    @handle_exceptions
    def delete_input(self, request, pk=None):
        """حذف ملف المدخل"""
        instance = self.get_object()
        user = request.user

        if not ValidationHandler.check_service_permission(user, instance.fk_service_id, 'DELETE_INPUT'):
            return ResponseHandler.forbidden(_('ليس لديك صلاحية حذف ملف المدخل'))

        if instance.fk_organization != user.fk_organization:
            return ResponseHandler.forbidden(_('ليس لديك صلاحية الوصول لهذا الطلب'))

        if instance.is_locked:
            return ResponseHandler.forbidden(_('الطلب مقفول ولا يمكن تعديله'))

        if not instance.input_document:
            raise ValidationException(message=_('لا يوجد ملف مدخل للحذف'))

        instance.input_document.delete(save=False)
        instance.input_document = None
        instance.save()

        return ResponseHandler.success(message=_('تم حذف ملف المدخل بنجاح'))

    @action(detail=True, methods=['delete'], url_path='delete-output', url_name='delete-output')
    @handle_exceptions
    def delete_output(self, request, pk=None):
        """حذف ملف المخرج"""
        instance = self.get_object()
        user = request.user
        
        if not ValidationHandler.check_service_permission(user, instance.fk_service_id, 'DELETE_OUTPUT'):
            return ResponseHandler.forbidden(_('ليس لديك صلاحية حذف ملف المخرج'))
        
        if instance.fk_organization != user.fk_organization:
            return ResponseHandler.forbidden(_('ليس لديك صلاحية الوصول لهذا الطلب'))
        # check status of request
        if instance.status not in [ServiceStatusChoice.PENDING,ServiceStatusChoice.IN_PROGRESS]:
            return ResponseHandler.forbidden(_('الطلب مقفول ولا يمكن تعديله'))

        if instance.is_locked:
            return ResponseHandler.forbidden(_('الطلب مقفول ولا يمكن تعديله'))
        
        if not instance.output_document:
            raise ValidationException(message=_('لا يوجد ملف مخرج للحذف'))

        instance.output_document.delete(save=False)
        instance.output_document = None
        instance.save()

        return ResponseHandler.success(message=_('تم حذف ملف المخرج بنجاح'))

    @action(detail=True,methods=['post'], url_path='create-invoices', url_name='create_invoices')
    @handle_exceptions
    def create_invoices(self, request, pk=None):
        request_obj = self.get_object()
        allowed_status = [ServiceStatusChoice.PENDING, ServiceStatusChoice.IN_PROGRESS]
        if request_obj.status not in allowed_status:
            return ResponseHandler.bad_request(
                message=_(f'لا يمكن اتمام عملية امر السداد'),
                details={
                    'current_status': request_obj.get_status_display(),
                    'allowed_status': [status.label for status in allowed_status],
                }
            )
        invoices_data = request_obj.get_invoices_data()
        for invoice_data in invoices_data:
            serializer = ERPInvoiceSerializer(data=invoice_data)
            if serializer.is_valid():
                invoice_obj = serializer.save()
                if invoice_obj.partner_type == PartnerType.STUDENT:
                    request_obj.student_invoice_number = invoice_obj.invoice_number
                if invoice_obj.partner_type == PartnerType.DONOR:
                    request_obj.grant_invoice_number = invoice_obj.invoice_number
                request_obj.save()
            print('creating invoice waiting for 5sec...')
        return ResponseHandler.success(
            message=_('تم انشاء فواتير السداد لهذا الطلب'),
        )

    @action(detail=True, methods=['post'], url_path='create-installment-invoices/(?P<installment_pk>[^/.]+)', url_name='create_installment_invoices')
    @handle_exceptions
    def create_installment_invoices(self, request, pk=None,installment_pk=None):
        request_obj = self.get_object()
        allowed_status = [ServiceStatusChoice.APPROVED, ServiceStatusChoice.IN_PROGRESS]
        if request_obj.status not in allowed_status:
            return ResponseHandler.bad_request(
                message=_(f' لا يمكن اتمام عملية امر السداد على الطلب.'),
                details={
                    'الحالة الحالية': request_obj.get_status_display(),
                    'الحالات المسموحة': [status.label for status in allowed_status],
                }
            )
        installments = request_obj.installments.all()
        if installments.filter(id=installment_pk).exists():
            installment = installments.get(id=installment_pk)
            for invoice in installment.get_invoices_data():
                serializer = ERPInvoiceSerializer(data=invoice)
                if serializer.is_valid():
                    invoice_obj = serializer.save()
                    if invoice_obj.partner_type == PartnerType.STUDENT:
                        installment.student_invoice_number = invoice_obj.invoice_number
                    if invoice_obj.partner_type == PartnerType.DONOR:
                        installment.grant_invoice_number = invoice_obj.invoice_number
                    installment.save()

            return ResponseHandler.success(
                message=_('تم انشاء فواتير السداد لهذا القسط'),
            )
        return ResponseHandler.bad_request(
            message=_('هذا القسط غير موجود او خاص بطلب اخر.'),
        )
