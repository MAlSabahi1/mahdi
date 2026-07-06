"""
Service APIs
ViewSets for Service, ServiceVersion, ServiceInstallmentPlan, OrganizationServiceConfig
"""
from time import process_time_ns

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from django.db import transaction

from d_services.models.Service import Service
from d_services.models.ServiceVersion import ServiceVersion
from d_services.models.ServiceInstallmentPlan import ServiceInstallmentPlan
from d_services.models.OrganizationServiceConfig import OrganizationServiceConfig
from d_services.models.WorkflowStage import WorkflowStage
from d_services.models.ServiceWorkflowStep import ServiceWorkflowStep
from d_services.models.ServicePrerequisite import ServicePrerequisite
from d_services.serializers.services import (
    ServiceSerializer,
    ServiceVersionSerializer,
    ServiceInstallmentPlanSerializer,
    OrganizationServiceConfigSerializer,
    ActivateForOrganizationsSerializer,
    ServicePrerequisiteSerializer,
    WorkflowStageSerializer,
    ServiceWorkflowStepSerializer,
)
from config.imports.viewmodel_core import AllMVS
from d_services.utils.exception_handler import handle_exceptions, ValidationException, BusinessRuleException
from d_services.utils.permission_checker import PermissionChecker
from d_services.utils.service_config_handler import ServiceConfigHandler
from d_services.utils.bulk_sync_handler import BulkSyncHandler
from d_services.utils.response_handler import ResponseHandler
from d_services.utils.validation_handler import ValidationHandler
from d_services.models.StageChecklistItem import WorkflowStepChecklistTemplate
from d_services.serializers.services import WorkflowStepChecklistTemplateSerializer

class ServiceMVS(AllMVS):
    """
    """
    queryset = Service.objects.select_related().prefetch_related('versions', 'prerequisites', 'workflow_steps')
    serializer_class = ServiceSerializer
    # enable_actions = ['all','select','list','second_list','filter','filter_paginate',]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, context={'request': request})
        return Response(serializer.data)

    def _has_active_requests(self, service):
        return service.requests.filter(
            status__in=['pending', 'in_progress'],
            is_deleted=False
        ).exists()

    @handle_exceptions
    def partial_update(self, request, pk=None, *args, **kwargs):
        PermissionChecker.require_superuser(request.user)
        
        instance = self.get_object()
        
        if self._has_active_requests(instance):
            return ResponseHandler.bad_request(
                _('لا يمكن تعديل الخدمة لوجود طلبات نشطة'),
                hint=_('يجب إغلاق جميع الطلبات النشطة أولاً')
            )
        
        return super().partial_update(request, *args, **kwargs)

    @handle_exceptions
    @action(detail=True, methods=['patch'], url_name="toggle-active", url_path="toggle-active")
    def toggle_active(self, request, pk=None):
        PermissionChecker.require_superuser(request.user)
        
        instance = self.get_object()
        
        if instance.is_active and self._has_active_requests(instance):
            return ResponseHandler.bad_request(
                _('لا يمكن تعطيل الخدمة عند وجود طلبات نشطة'),
                hint=_('يجب إغلاق جميع الطلبات النشطة أولاً')
            )
        
        instance.is_active = not instance.is_active
        instance.save(update_fields=['is_active'])
        
        return ResponseHandler.success(
            _('تم تفعيل الخدمة') if instance.is_active else _('تم تعطيل الخدمة'),
            extra={'is_active': instance.is_active}
        )


class ServiceVersionMVS(AllMVS):
    queryset = ServiceVersion.objects.select_related('fk_service').prefetch_related('requests')
    serializer_class = ServiceVersionSerializer
    # enable_actions = ['all','select','list','second_list','filter','filter_paginate',]

    
    def _has_active_requests(self, version):
        """Check for active requests on this version"""
        return version.requests.filter(is_deleted=False).exclude(status='rejected').exists()
    
    @handle_exceptions
    def create(self, request, *args, **kwargs):
        """Create new version - superuser only"""
        PermissionChecker.require_superuser(request.user)
        return super().create(request, *args, **kwargs)
    
    @handle_exceptions
    def update(self, request, *args, **kwargs):
        PermissionChecker.require_superuser(request.user)
        
        instance = self.get_object()
        if self._has_active_requests(instance):
            return ResponseHandler.bad_request(
                _('لا يمكن تعديل الإصدار لأنه يحتوي على طلبات نشطة')
            )
        
        return super().update(request, *args, **kwargs)
    
    @handle_exceptions
    def partial_update(self, request, *args, **kwargs):
        PermissionChecker.require_superuser(request.user)
        
        instance = self.get_object()
        if self._has_active_requests(instance):
            return ResponseHandler.bad_request(
                _('لا يمكن تعديل الإصدار لأنه يحتوي على طلبات نشطة')
            )
        
        return super().partial_update(request, *args, **kwargs)
    
    @handle_exceptions
    @action(detail=True, methods=['patch'], url_name="set-current", url_path="set-current")
    def set_current(self, request, pk=None):
        PermissionChecker.require_superuser(request.user)
        
        instance = self.get_object()
        
        current_version = ServiceVersion.objects.filter(
            fk_service_id=instance.fk_service_id,
            is_current=True,
        ).first()
        if current_version and current_version != instance:
            if current_version.requests.filter(status__in=['pending', 'in_progress']).exists():
                return ResponseHandler.bad_request(_('Current version has active requests'))
        
        with transaction.atomic():
            ServiceVersion.objects.filter(
                fk_service_id=instance.fk_service_id
            ).update(is_current=False)
            
            instance.is_current = True
            instance.save(update_fields=['is_current'])
        
        return ResponseHandler.success(
            _('Version set as current'),
            extra={'version': ServiceVersionSerializer(instance).data}
        )


class OrganizationServiceConfigMVS(AllMVS):
    queryset = OrganizationServiceConfig.objects.select_related(
        'fk_service', 'fk_organization', 'fk_currency',
        'fk_print_report_setting_for_input', 'fk_print_report_setting_for_output'
    ).prefetch_related('installment_plans')
    serializer_class = OrganizationServiceConfigSerializer
    enable_actions = ['all','select','list','second_list','filter','filter_paginate',"sync-import" ,  "sync-export",  "sync-push","sync-pull"]

    def get_object(self):
        pk = self.kwargs.get('pk')
        if not pk:
            raise ValidationException(_('معرف الخدمة مطلوب'))
        
        return ServiceConfigHandler.get_config_for_user(pk, self.request.user)

    @handle_exceptions
    def list(self, request, *args, **kwargs):
        """
        قائمة إعدادات الخدمات للمنظمة الخاصة بالمستخدم
        Returns only configs for the user's organization with complete service data
        """
        from d_services.models.GroupServicePermission import GroupServicePermission
        from d_services.choices.choices import ServicePermissionType
        user = request.user
        user_org = getattr(user, 'fk_organization', None)
        queryset = super().get_queryset()
        # if not user.is_superuser:
        queryset = queryset.filter(fk_organization=user_org)
        
        # Optional filter by is_active
        queryset = queryset.filter(fk_service__is_active=True)
        
        # Optional filter by service
        service_id = request.query_params.get('fk_service')
        if service_id:
            queryset = queryset.filter(fk_service_id=service_id)
        
        # Optional filter by service category
        category = request.query_params.get('category')
        if category:
            queryset = queryset.filter(fk_service__category=category)
        
        # Order by service name
        queryset = queryset.order_by('fk_service__name_ar')
        
        user_permissions_by_service= {}
        if user.is_superuser:
            service_ids = queryset.values_list('fk_service_id', flat=True)
            all_permissions = [perm.value for perm in ServicePermissionType]
            for service_id in service_ids:
                user_permissions_by_service[service_id] = all_permissions
        else:
            user_groups = user.groups.all()
            group_permissions = GroupServicePermission.objects.filter(fk_group__in=user_groups).select_related('fk_permission').values("fk_permission__fk_service_id","fk_permission__permission_type")
            for gp in group_permissions:
                service_id = gp["fk_permission__fk_service_id"]
                permission_type = gp["fk_permission__permission_type"]
                if service_id not in user_permissions_by_service:
                    user_permissions_by_service[service_id] = []
                if permission_type not in user_permissions_by_service[service_id]:
                    user_permissions_by_service[service_id].append(permission_type)
        

        # # Pagination
        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)
        


        serializer = self.get_serializer(queryset, many=True)
        data_with_permissions = []
        for item in serializer.data:
            item_data = dict(item)
            service_id = item_data.get('fk_service')
            item_data['user_permissions'] = user_permissions_by_service.get(int(service_id['id']),[])
            data_with_permissions.append(item_data)
        return ResponseHandler.success(
            _('تم جلب قائمة إعدادات الخدمات بنجاح'),
            data= data_with_permissions,
            extra= {'count': queryset.count()}
        )

    @handle_exceptions
    def retrieve(self, request, pk=None, *args, **kwargs):
        config = self.get_object()
        
        return ResponseHandler.success(
            _('تم جلب إعدادات الخدمة بنجاح'),
            data=OrganizationServiceConfigSerializer(config).data
        )

    @handle_exceptions
    def create(self, request, *args, **kwargs):
        PermissionChecker.require_superuser(request.user)
        
        result = ServiceConfigHandler.bulk_create_for_all_orgs()
        
        return ResponseHandler.created(
            _('تم إنشاء التكوينات بنجاح'),
            extra=result
        )

    @handle_exceptions
    def update(self, request, pk=None, *args, **kwargs):
        PermissionChecker.require_manager(request.user)
        
        config = self.get_object()
        
        ServiceConfigHandler.validate_no_active_requests(config, pk)
        
        allowed_fields = [
            'is_paid', 'free_limit_per_year', 'fk_currency', 
            'fee_amount', 'request_prefix', 'is_active',
            'is_installment_allowed', 'installments_count',
            'fk_print_report_setting_for_input',
            'fk_print_report_setting_for_output','installment_period'
        ]
        
        ServiceConfigHandler.update_config_fields(config, request.data, allowed_fields)
        
        return ResponseHandler.success(
            _('تم تحديث التكوين بنجاح'),
            data=OrganizationServiceConfigSerializer(config).data
        )

    @handle_exceptions
    @action(detail=False, methods=['post'], url_path='activate-for-organizations')
    def activate_for_organizations(self, request, service_pk=None):
        PermissionChecker.require_superuser(request.user)
        
        serializer = ActivateForOrganizationsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        created_configs = []
        with transaction.atomic():
            for org_id in serializer.validated_data['organization_ids']:
                config, created = OrganizationServiceConfig.objects.get_or_create(
                    fk_service_id=service_pk,
                    fk_organization_id=org_id,
                    defaults={'is_active': True}
                )
                if not created:
                    config.is_active = True
                    config.save(update_fields=['is_active'])
                created_configs.append(config)
        
        return ResponseHandler.success(
            _('Service activated for organizations'),
            extra={'configs': OrganizationServiceConfigSerializer(created_configs, many=True).data}
        )

    @handle_exceptions
    @action(detail=True, methods=['patch'], url_name="toggle-lock", url_path="toggle-lock")
    def toggle_lock(self, request, pk=None):
        user = request.user
        config = self.get_object()
        
        ValidationHandler.validate_organization(config, user)
        
        if config.is_locked:
            ValidationHandler.validate_permission(user, config.fk_service_id, 'UNLOCK')
            result = ServiceConfigHandler.unlock_service(config)
            
            return ResponseHandler.success(
                _('تم فتح قفل إعدادات الخدمة وجميع طلباتها بنجاح'),
                extra={
                    'is_locked': False,
                    'unlocked_requests_count': result['unlocked_count'],
                    'unlocked_requests_numbers': result['unlocked_numbers']
                }
            )
        else:
            ValidationHandler.validate_permission(user, config.fk_service_id, 'LOCK')
            
            locked_reason = request.data.get('locked_reason')
            result = ServiceConfigHandler.lock_service(config, locked_reason)
            
            return ResponseHandler.success(
                _('تم قفل إعدادات الخدمة وجميع طلباتها النشطة بنجاح'),
                extra={
                    'is_locked': True,
                    'locked_reason': config.locked_reason,
                    'locked_at': config.locked_at,
                    'locked_requests_count': result['locked_count'],
                    'locked_requests_numbers': result['locked_numbers']
                }
            )

    @handle_exceptions
    @action(detail=True, methods=['patch'], url_name="update-erp-invoice-all_settings", url_path="update-erp-invoice-all_settings")
    def update_erp_invoice_settings(self, request, pk=None):
        """
        تحديث إعدادات الفاتورة و ERP للخدمة
        Update ERP invoice all_settings for the service config
        """

        PermissionChecker.require_manager(request.user)

        config = self.get_object()
        
        # Validate organization
        ValidationHandler.validate_organization(config, request.user)
        
        # Define allowed ERP fields
        erp_fields = [
            'is_donor_invoice_allowed',
            'is_discount_allowed',
            'erp_product_id',
            'erp_product_name',
            'erp_product_for_discount_id',
            'erp_product_for_discount_name',
            'erp_product_for_internal_donors_id',
            'erp_product_for_internal_donors_name',
            'erp_project_id',
            'erp_project_name',
            'erp_activity_id',
            'erp_activity_name',
            'erp_cost_center_id',
            'erp_cost_center_name',
        ]
        
        # Update fields
        ServiceConfigHandler.update_config_fields(config, request.data, erp_fields)
        
        return ResponseHandler.success(
            _('تم تحديث إعدادات الفاتورة و ERP بنجاح'),
            data=OrganizationServiceConfigSerializer(config).data
        )


class ServiceInstallmentPlanMVS(AllMVS):
    queryset = ServiceInstallmentPlan.objects.select_related('fk_org_service_config')
    serializer_class = ServiceInstallmentPlanSerializer
    enable_actions = ['all','select','list','second_list','filter','filter_paginate',]
    
    @handle_exceptions
    def list(self, request, *args, **kwargs):
        PermissionChecker.require_manager(request.user)
        
        service_id = request.query_params.get('fk_service')
        if not service_id:
            return ResponseHandler.bad_request(_('معرف الخدمة مطلوب (fk_service)'))
        
        user_org = PermissionChecker.get_user_organization(request.user)
        
        org_config = ServiceConfigHandler.get_active_config(service_id, user_org)
        if not org_config:
            return ResponseHandler.not_found(_('تكوين الخدمة غير موجود لمنظمتك'))
        
        plans = ServiceInstallmentPlan.objects.filter(
            fk_org_service_config=org_config,
            is_deleted=False
        ).order_by('order')
        
        return ResponseHandler.success(
            _('تم جلب خطط التقسيط بنجاح'),
            extra={
                'fk_service': int(service_id),
                'fk_organization': user_org.id,
                'is_installment_allowed': org_config.is_installment_allowed,
                'installments_count': org_config.installments_count,
                'fee_amount': str(org_config.fee_amount) if org_config.fee_amount else None,
                'count': plans.count(),
                'data': ServiceInstallmentPlanSerializer(plans, many=True).data
            }
        )
    
    @handle_exceptions
    def create(self, request, *args, **kwargs):
        PermissionChecker.require_manager(request.user)
        
        plans_data = request.data.get('plans', [])
        service_id = request.data.get('fk_service')
        
        if not service_id:
            return ResponseHandler.bad_request(_('معرف الخدمة مطلوب'))
        
        if not isinstance(plans_data, list):
            return ResponseHandler.bad_request(_('يجب إرسال مصفوفة من خطط التقسيط'))
        
        try:
            service = Service.objects.get(pk=service_id, is_deleted=False)
        except Service.DoesNotExist:
            return ResponseHandler.not_found(_('الخدمة غير موجودة'))
        
        # Get org config
        user_org = PermissionChecker.get_user_organization(request.user)
        org_config = ServiceConfigHandler.get_active_config(service_id, user_org)
        
        if not org_config:
            return ResponseHandler.not_found(_('تكوين الخدمة غير موجود لمنظمتك'))
        
        # Validate installment conditions
        if not org_config.is_installment_allowed:
            return ResponseHandler.bad_request(_('هذه الخدمة لا تسمح بالتقسيط'))
        
        if not org_config.is_paid:
            return ResponseHandler.bad_request(_('هذه الخدمة مجانية'))
        
        if len(plans_data) != org_config.installments_count:
            return ResponseHandler.bad_request(
                _('عدد الأقساط ({}) لا يتطابق مع عدد أقساط الخدمة ({})').format(
                    len(plans_data), org_config.installments_count
                )
            )
        
        if org_config.fee_amount:
            from decimal import Decimal
            # total_percentage = sum(Decimal(str(plan.get('percentage', 0))) for plan in plans_data)
            # if total_percentage != 100:
            #     return ResponseHandler.bad_request(
            #         _('مجموع نسب الأقساط ({}) لا يساوي النسبة من  ({})').format(
            #             total_percentage, 100
            #         )
            #     )
            total_amount = sum(Decimal(str(plan.get('amount', 0))) for plan in plans_data)
            fee_amount = Decimal(str(org_config.fee_amount))
            
            if total_amount != fee_amount:
                return ResponseHandler.bad_request(
                    _('اجمالي الأقساط ({}) لا يساوي رسوم الخدمة ({})').format(
                        total_amount, fee_amount
                    )
                )

        
        result = BulkSyncHandler.sync_by_order(
            model_class=ServiceInstallmentPlan,
            parent_field='fk_org_service_config',
            parent_instance=org_config,
            items_data=plans_data,
            updatable_fields=['installment_period', 'amount', 'due_days_from_request']
        )
        
        all_plans = BulkSyncHandler.get_all_active(
            ServiceInstallmentPlan, 'fk_org_service_config', org_config
        )
        
        return ResponseHandler.success(
            _('تم تحديث خطط التقسيط بنجاح'),
            extra={
                **result.to_dict(),
                'plans': ServiceInstallmentPlanSerializer(all_plans, many=True).data
            }
        )


class ServicePrerequisiteMVS(AllMVS):
    queryset = ServicePrerequisite.objects.select_related('fk_service')
    serializer_class = ServicePrerequisiteSerializer
    enable_actions = ['all','select','list','second_list','filter','filter_paginate',]

    
    def _has_active_requests(self, service):
        return service.requests.filter(
            status__in=['pending', 'in_progress'],
            is_deleted=False
        ).exists()
    
    @handle_exceptions
    def create(self, request, *args, **kwargs):
        PermissionChecker.require_superuser(request.user)
        
        prerequisites_data = request.data.get('prerequisites', [])
        service_id = request.data.get('fk_service')
        
        if not service_id:
            return ResponseHandler.bad_request(_('معرف الخدمة مطلوب'))
        
        if not isinstance(prerequisites_data, list):
            return ResponseHandler.bad_request(_('يجب إرسال مصفوفة من الشروط'))
        
        try:
            service = Service.objects.get(pk=service_id, is_deleted=False)
        except Service.DoesNotExist:
            return ResponseHandler.not_found(_('الخدمة غير موجودة'))
        
        if self._has_active_requests(service):
            return ResponseHandler.bad_request(
                _('لا يمكن تعديل شروط الخدمة لوجود طلبات نشطة')
            )
        
        result = BulkSyncHandler.sync_by_id(
            model_class=ServicePrerequisite,
            parent_field='fk_service',
            parent_instance=service,
            items_data=prerequisites_data,
            updatable_fields=['name_ar', 'name_en', 'description', 'status', 'validation_procedure_name', 'order']
        )
        
        all_prerequisites = BulkSyncHandler.get_all_active(
            ServicePrerequisite, 'fk_service', service
        )
        
        return ResponseHandler.success(
            _('تم تحديث شروط الخدمة بنجاح'),
            extra={
                **result.to_dict(),
                'prerequisites': ServicePrerequisiteSerializer(all_prerequisites, many=True).data
            }
        )


class WorkflowStageMVS(AllMVS):
    queryset = WorkflowStage.objects.all()
    serializer_class = WorkflowStageSerializer


class ServiceWorkflowStepMVS(AllMVS):
    queryset = ServiceWorkflowStep.objects.select_related('fk_service', 'fk_stage')
    serializer_class = ServiceWorkflowStepSerializer
    # enable_actions = ['all','select','list','second_list','filter','filter_paginate',]

    permission_classes=[]
    def _has_active_requests(self, service):
        return service.requests.filter(
            status__in=['pending', 'in_progress'],
            is_deleted=False
        ).exists()
    
    def _sync_step_permissions(self, step):
        from d_services.models.ServiceWorkFlowStepPermission import ServiceWorkFlowStepPermission
        from d_services.choices.choices import ActionPermissionType

        required_permissions = {
            ActionPermissionType.START,
            ActionPermissionType.COMPLETE,
            ActionPermissionType.REJECT,
            ActionPermissionType.CANCEL,
        }
        
        if step.has_approval:
            required_permissions.add(ActionPermissionType.APPROVE)
        if step.is_execution_step:
            required_permissions.add(ActionPermissionType.EXECUTE)
        if step.has_custom_input:
            required_permissions.add(ActionPermissionType.INPUT)
        if step.has_custom_output:
            required_permissions.add(ActionPermissionType.OUTPUT)
        
        existing_permissions = set(
            ServiceWorkFlowStepPermission.objects.filter(
                fk_workflow_step=step
            ).values_list('permission_type', flat=True)
        )
        
        for perm_type in required_permissions - existing_permissions:
            ServiceWorkFlowStepPermission.objects.create(
                fk_workflow_step=step,
                permission_type=perm_type
            )
        
        extra = existing_permissions - required_permissions
        if extra:
            ServiceWorkFlowStepPermission.objects.filter(
                fk_workflow_step=step,
                permission_type__in=extra
            ).delete()
    
    def _validate_workflow_steps(self, steps_data):
        if not steps_data:
            return
        
        sorted_steps = sorted(steps_data, key=lambda x: x.get('order', 0))
        final_count = sum(1 for s in steps_data if s.get('is_final_step', False))
        
        if final_count == 0:
            raise BusinessRuleException(_('يجب تحديد خطوة نهائية واحدة على الأقل'))
        
        if final_count > 1:
            raise BusinessRuleException(_('لا يمكن أن يكون هناك أكثر من خطوة نهائية واحدة'))
        
        if not sorted_steps[-1].get('is_final_step', False):
            raise BusinessRuleException(_('يجب أن تكون الخطوة النهائية هي الأخيرة بالترتيب'))
    
    @handle_exceptions
    def create(self, request, *args, **kwargs):
        PermissionChecker.require_superuser(request.user)
        
        steps_data = request.data.get('steps', [])
        service_id = request.data.get('fk_service')
        
        if not service_id:
            return ResponseHandler.bad_request(_('معرف الخدمة مطلوب'))
        if not isinstance(steps_data, list):
            return ResponseHandler.bad_request(_('يجب إرسال مصفوفة من الخطوات'))
        
        try:
            service = Service.objects.get(pk=service_id, is_deleted=False)
        except Service.DoesNotExist:
            return ResponseHandler.not_found(_('الخدمة غير موجودة'))
        
        if self._has_active_requests(service):
            return ResponseHandler.bad_request(
                _('لا يمكن تعديل خطوات سير العمل لوجود طلبات نشطة')
            )
        
        self._validate_workflow_steps(steps_data)
        
        result = BulkSyncHandler.sync_by_id(
            model_class=ServiceWorkflowStep,
            parent_field='fk_service',
            parent_instance=service,
            items_data=steps_data,
            field_mapping={'fk_stage': 'fk_stage_id'},
            updatable_fields=[
                'fk_stage', 'order', 'is_final_step', 'is_execution_step',
                'has_custom_output', 'has_custom_input', 'has_approval',
                'custom_output_template', 'custom_output_function',
                'custom_input_template', 'custom_input_function',
                'start_offset_days', 'delivery_offset_days', 
                'execution_procedure_name', 'description'
            ],
            post_save_callback=self._sync_step_permissions
        )
        
        all_steps = BulkSyncHandler.get_all_active(
            ServiceWorkflowStep, 'fk_service', service
        )
        
        return ResponseHandler.success(
            _('تم تحديث خطوات سير العمل بنجاح'),
            extra={
                **result.to_dict(),
                'steps': ServiceWorkflowStepSerializer(all_steps, many=True).data
            }
        )

class WorkflowStepChecklistTemplateMVS(AllMVS):
    """
    إدارة قوالب قائمة التحقق لخطوات سير العمل
    - يتم ربط القالب بخطوة سير العمل وإعدادات الخدمة للمنظمة
    - الـ create يعمل كـ bulk sync (إضافة، تحديث، حذف دفعة واحدة)
    """
    queryset = WorkflowStepChecklistTemplate.objects.select_related(
        'fk_workflow_step', 'fk_org_service_config'
    )
    serializer_class = WorkflowStepChecklistTemplateSerializer
    enable_actions = ['all','select','list','second_list','filter','filter_paginate',]
    permission_classes= []
    def list(self, request, *args, **kwargs):
        from d_services.models.OrganizationServiceConfig import OrganizationServiceConfig
        
        user = request.user
        workflow_step_id = request.query_params.get('fk_workflow_step')
        
        if not workflow_step_id:
            return ResponseHandler.bad_request(_('معرف خطوة سير العمل مطلوب'))
        
        queryset = self.queryset.filter(fk_workflow_step_id=workflow_step_id)
        
        org_configs = OrganizationServiceConfig.objects.filter(
            fk_organization=user.fk_organization
        ).values_list('id', flat=True)
        queryset = queryset.filter(fk_org_service_config_id__in=org_configs)
        
        queryset = queryset.order_by('order')
        serializer = self.get_serializer(queryset, many=True)
        
        return ResponseHandler.success(
            message=_('تم جلب قوالب قائمة التحقق بنجاح'),
            data=serializer.data,
            extra={'count': queryset.count()}
        )
    
    def create(self, request, *args, **kwargs):
        from django.db import transaction
        from d_services.models.OrganizationServiceConfig import OrganizationServiceConfig
        from d_services.models.ServiceWorkflowStep import ServiceWorkflowStep
        from d_services.models.StagePermission import StagePermission
        from d_services.choices.choices import ActionPermissionType
        
        user = request.user
        data = request.data
        
        workflow_step_id = data.get('fk_workflow_step')
        if not workflow_step_id:
            return ResponseHandler.bad_request(_('معرف خطوة سير العمل مطلوب'))
        
        try:
            workflow_step = ServiceWorkflowStep.objects.get(pk=workflow_step_id)
        except ServiceWorkflowStep.DoesNotExist:
            return ResponseHandler.not_found(_('خطوة سير العمل غير موجودة'))
        
        # التحقق من صلاحية المستخدم لإضافة عناصر قائمة التحقق
        if not user.is_superuser and not user.is_manager:
            has_permission = StagePermission.objects.filter(
                fk_workflow_step_permission__fk_workflow_step=workflow_step,
                fk_workflow_step_permission__permission_type=ActionPermissionType.CHECKLIST_ADD,
                fk_user=user
            ).exists()
            
            if not has_permission:
                return ResponseHandler.forbidden(
                    _('ليس لديك صلاحية إضافة قوالب قائمة التحقق لهذه المرحلة')
                )

        # استخدام إعدادات منظمة المستخدم
        try:
            org_config = OrganizationServiceConfig.objects.filter(
                fk_organization=user.fk_organization,
                fk_service=workflow_step.fk_service,
                is_active=True
            ).first()
        except OrganizationServiceConfig.DoesNotExist:
            return ResponseHandler.not_found(_('إعدادات الخدمة غير موجودة'))
        

        templates_data = data.get('templates', [])
        
        # التحقق من الترتيب
        try:
            orders = [int(t.get('order', 0)) for t in templates_data]
        except ValueError:
            return ResponseHandler.bad_request(
                _('الترتيب يجب أن يكون رقمًا صحيحًا'),
                hint=_(
                    'تأكد من إدخال أرقام للترتيب بدلاً من نصوص'
                )
            )
        
        if len(orders) != len(set(orders)):
            return ResponseHandler.bad_request(
                _('الترتيب يجب أن يكون فريداً لكل عنصر'),
                hint=_('تأكد من عدم تكرار قيم الترتيب')
            )
        
        # التحقق من تسلسل الترتيب
        sorted_orders = sorted(orders)
        expected_orders = list(range(1, len(orders) + 1))
        if sorted_orders != expected_orders:
            return ResponseHandler.bad_request(
                _('الترتيب يجب أن يكون متسلسلاً من 1'),
                details={'received': sorted_orders, 'expected': expected_orders},
                hint=_('الترتيب يجب أن يبدأ من 1 ويكون متتالياً')
            )
        
        with transaction.atomic():
            # جلب العناصر الموجودة
            existing_templates = WorkflowStepChecklistTemplate.objects.filter(
                fk_workflow_step=workflow_step,
                fk_org_service_config=org_config
            )
            existing_ids = set(existing_templates.values_list('id', flat=True))
            
            # معالجة العناصر
            sent_ids = set()
            created_count = 0
            updated_count = 0
            
            for template_data in templates_data:
                template_id = template_data.get('id')
                title = template_data.get('title', '')
                description = template_data.get('description', '')
                order = template_data.get('order', 0)
                is_required = template_data.get('is_required', True)
                
                if template_id and template_id in existing_ids:
                    # تحديث عنصر موجود
                    sent_ids.add(template_id)
                    template = existing_templates.get(id=template_id)
                    
                    updated = False
                    if title and template.title != title:
                        template.title = title
                        updated = True
                    if description is not None and template.description != description:
                        template.description = description
                        updated = True
                    if template.order != order:
                        template.order = order
                        updated = True
                    if template.is_required != is_required:
                        template.is_required = is_required
                        updated = True
                    
                    if updated:
                        template.save()
                        updated_count += 1
                else:
                    # إنشاء عنصر جديد
                    if not title:
                        return ResponseHandler.bad_request(
                            _('العنوان مطلوب للعناصر الجديدة'),
                            details={'order': order}
                        )
                    
                    WorkflowStepChecklistTemplate.objects.create(
                        fk_workflow_step=workflow_step,
                        fk_org_service_config=org_config,
                        title=title,
                        description=description or '',
                        order=order,
                        is_required=is_required
                    )
                    created_count += 1
            
            # حذف العناصر غير الموجودة في القائمة المرسلة
            ids_to_delete = existing_ids - sent_ids
            deleted_count = 0
            if ids_to_delete:
                deleted_count = WorkflowStepChecklistTemplate.objects.filter(
                    id__in=ids_to_delete
                ).delete()[0]
        
        # جلب العناصر المحدثة
        all_templates = WorkflowStepChecklistTemplate.objects.filter(
            fk_workflow_step=workflow_step,
            fk_org_service_config=org_config
        ).order_by('order')
        
        return ResponseHandler.success(
            message=_('تم تحديث قوالب قائمة التحقق بنجاح'),
            data=WorkflowStepChecklistTemplateSerializer(all_templates, many=True).data,
            extra={
                'created': created_count,
                'updated': updated_count,
                'deleted': deleted_count,
                'total': all_templates.count()
            }
        )


from d_services.serializers.services import WorkflowStepPrintReportSettingSerializer,WorkflowStepPrintReportSetting
from django.db import models
class WorkflowStepPrintReportSettingMVS(AllMVS):
    """
    إدارة إعدادات الطباعة لخطوات سير العمل
    - list: جلب خطوات سير العمل التي لها مدخلات أو مخرجات مخصصة مع get_or_create
    - update: تحديث إعدادات الطباعة مع حذف العناصر التي لم تعد لها مدخلات/مخرجات
    """
    
    queryset = WorkflowStepPrintReportSetting.objects.select_related(
        'fk_org_service_config',
        'fk_org_service_config__fk_service',
        'fk_org_service_config__fk_organization',
        'fk_workflow_step',
        'fk_workflow_step__fk_stage',
        'fk_print_report_setting_for_output',
        'fk_print_report_setting_for_input'
    )
    serializer_class = WorkflowStepPrintReportSettingSerializer
    enable_actions = ['all','select','list','second_list','filter','filter_paginate',]
    
    def _get_org_config(self, user, service_id):
        """Get organization service config for user"""
        org_config = OrganizationServiceConfig.objects.filter(
            fk_organization=user.fk_organization,
            fk_service_id=service_id,
            is_active=True
        ).first()
        return org_config
    
    def _has_active_requests(self, org_config):
        """Check if there are active requests for this org service config"""
        from d_services.models.ServiceRequest import ServiceRequest
        return ServiceRequest.objects.filter(
            fk_organization=org_config.fk_organization,
            fk_service=org_config.fk_service,
            status__in=['pending', 'in_progress']
        ).exists()
    
    @handle_exceptions
    def list(self, request, *args, **kwargs):
        user = request.user
        fk_service = request.query_params.get('fk_service')
        
        if not fk_service:
            return ResponseHandler.bad_request(_('معرف إعدادات الخدمة للمنظمة مطلوب'))
        
        org_config = self._get_org_config(user, fk_service)
        if not org_config:
            return ResponseHandler.not_found(_('إعدادات الخدمة غير موجودة'))
        
        # جلب خطوات سير العمل التي لها مدخلات أو مخرجات مخصصة
        workflow_steps = ServiceWorkflowStep.objects.filter(
            fk_service=org_config.fk_service,
        ).filter(
            models.Q(has_custom_output=True) | models.Q(has_custom_input=True)
        ).select_related('fk_stage').order_by('order')
        
        # إنشاء سجلات جديدة للخطوات التي لا توجد لها إعدادات (get_or_create)
        settings_list = []
        for step in workflow_steps:
            setting, created = WorkflowStepPrintReportSetting.objects.get_or_create(
                fk_org_service_config=org_config,
                fk_workflow_step=step,
                defaults={
                    'fk_print_report_setting_for_output': None,
                    'fk_print_report_setting_for_input': None
                }
            )
            settings_list.append(setting)
        
        # إعادة الاستعلام للحصول على البيانات الكاملة مع العلاقات
        settings = self.queryset.filter(
            fk_org_service_config=org_config
        ).order_by('fk_workflow_step__order')
        
        serializer = WorkflowStepPrintReportSettingSerializer(settings, many=True)
        
        return ResponseHandler.success(
            message=_('تم جلب إعدادات الطباعة لخطوات سير العمل'),
            data=serializer.data,
            extra={
                'count': settings.count(),
                'fk_org_service_config': org_config.id,
                'fk_service': org_config.fk_service_id,
                'fk_organization': org_config.fk_organization_id
            }
        )
    
    @handle_exceptions
    def update(self, request, pk=None, *args, **kwargs):

        user = request.user
        data = request.data
        
        fk_service = data.get('fk_service')
        settings_data = data.get('all_settings', [])
        
        if not fk_service:
            return ResponseHandler.bad_request(_('معرف إعدادات الخدمة للمنظمة مطلوب'))
        
        if not isinstance(settings_data, list):
            return ResponseHandler.bad_request(_('يجب إرسال قائمة من الإعدادات'))
        
        
        org_config = self._get_org_config(user, fk_service)
        if not org_config:
            return ResponseHandler.not_found(_('إعدادات الخدمة غير موجودة'))
        
        has_active_requests = self._has_active_requests(org_config)
        
        with transaction.atomic():
            updated_count = 0
            deleted_count = 0
            
            # جلب الخطوات الحالية التي لها مدخلات/مخرجات
            valid_step_ids = set(
                ServiceWorkflowStep.objects.filter(
                    fk_service=org_config.fk_service,
                    is_deleted=False
                ).filter(
                    models.Q(has_custom_output=True) | models.Q(has_custom_input=True)
                ).values_list('id', flat=True)
            )
            
            # جلب الإعدادات الموجودة
            existing_settings = WorkflowStepPrintReportSetting.objects.filter(
                fk_org_service_config=org_config,
                is_deleted=False
            )
            
            sent_step_ids = set()
            
            for setting_data in settings_data:
                setting_id = setting_data.get('id')
                workflow_step_id = setting_data.get('fk_workflow_step')
                
                if not setting_id and not workflow_step_id:
                    continue
                
                # البحث عن الإعداد
                if setting_id:
                    try:
                        setting = existing_settings.get(id=setting_id)
                        workflow_step_id = setting.fk_workflow_step_id
                    except WorkflowStepPrintReportSetting.DoesNotExist:
                        continue
                else:
                    setting, created = WorkflowStepPrintReportSetting.objects.get_or_create(
                        fk_org_service_config=org_config,
                        fk_workflow_step_id=workflow_step_id
                    )
                
                sent_step_ids.add(workflow_step_id)
                
                # التحقق من صلاحية الخطوة
                if workflow_step_id not in valid_step_ids:
                    if not has_active_requests:
                        setting.delete()
                        deleted_count += 1
                    continue
                
                # تحديث الإعدادات
                updated = False
                if 'fk_print_report_setting_for_output' in setting_data:
                    setting.fk_print_report_setting_for_output_id = setting_data['fk_print_report_setting_for_output']
                    updated = True
                if 'fk_print_report_setting_for_input' in setting_data:
                    setting.fk_print_report_setting_for_input_id = setting_data['fk_print_report_setting_for_input']
                    updated = True
                
                if updated:
                    setting.full_clean()
                    setting.save()
                    updated_count += 1
            
            # حذف الإعدادات للخطوات التي لم تعد لها مدخلات/مخرجات
            if not has_active_requests:
                orphaned = existing_settings.exclude(
                    fk_workflow_step_id__in=valid_step_ids
                )
                deleted_count += orphaned.count()
                orphaned.delete()
        
        # جلب النتائج المحدثة
        settings = self.queryset.filter(
            fk_org_service_config=org_config,
            is_deleted=False
        ).order_by('fk_workflow_step__order')
        
        return ResponseHandler.success(
            message=_('تم تحديث إعدادات الطباعة بنجاح'),
            data=WorkflowStepPrintReportSettingSerializer(settings, many=True).data,
            extra={
                'updated': updated_count,
                'deleted': deleted_count,
                'total': settings.count()
            }
        )
