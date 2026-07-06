"""
User Permissions API - API صلاحيات المستخدم
للحصول على صلاحيات المستخدم في الخدمات والمراحل مع حالات الإجراءات
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.translation import gettext_lazy as _

from d_services.models.GroupServicePermission import GroupServicePermission
from d_services.models.StagePermission import StagePermission
from d_services.models.Service import Service
from d_services.models.ServiceRequest import ServiceRequest
from d_services.choices.choices import (
    ServicePermissionType,
    ActionPermissionType,
    ServiceStatusChoice,
    StageStatusChoice,
    GrantStatusChoice,
    DiscountStatusChoice
)


class UserPermissionsAPIView(APIView):
    """
    API لجلب صلاحيات المستخدم
    GET /api/d-services/user-permissions/
    """
    permission_classes = [IsAuthenticated]
    
    # ========================================
    # تعريف الحالات المسموحة لكل إجراء
    # ========================================
    
    # إجراءات الطلبات (ServiceRequest)
    REQUEST_ACTION_STATUSES = {
        'CREATE': {
            'allowed_statuses': None,  # لا يتطلب حالة - إنشاء جديد
            'description': 'إنشاء طلب جديد',
            'description_en': 'Create new request'
        },
        'READ': {
            'allowed_statuses': None,  # جميع الحالات
            'description': 'عرض الطلبات',
            'description_en': 'View requests'
        },
        'UPDATE': {
            'allowed_statuses': [ServiceStatusChoice.PENDING],
            'description': 'تعديل الطلب',
            'description_en': 'Update request'
        },
        'DELETE': {
            'allowed_statuses': [ServiceStatusChoice.PENDING],
            'description': 'حذف الطلب',
            'description_en': 'Delete request'
        },
        'PRINT': {
            'allowed_statuses': None,  # جميع الحالات
            'description': 'طباعة الطلب',
            'description_en': 'Print request'
        },
        'START': {
            'allowed_statuses': [ServiceStatusChoice.PENDING],
            'description': 'بدء معالجة الطلب',
            'description_en': 'Start request processing'
        },
        'REJECT': {
            'allowed_statuses': [ServiceStatusChoice.PENDING],
            'description': 'رفض الطلب',
            'description_en': 'Reject request'
        },
        'CANCEL': {
            'allowed_statuses': [ServiceStatusChoice.PENDING, ServiceStatusChoice.IN_PROGRESS],
            'description': 'إلغاء الطلب',
            'description_en': 'Cancel request'
        },
        'COMPLETE': {
            'allowed_statuses': [ServiceStatusChoice.IN_PROGRESS],
            'description': 'إكمال الطلب',
            'description_en': 'Complete request'
        },
        'LOCK': {
            'allowed_statuses': None,  # جميع الحالات (غير المقفول)
            'description': 'قفل الطلب',
            'description_en': 'Lock request',
            'extra_condition': 'is_locked = False'
        },
        'UNLOCK': {
            'allowed_statuses': None,  # جميع الحالات ماعدا REJECTED
            'excluded_statuses': [ServiceStatusChoice.REJECTED],
            'description': 'فتح قفل الطلب',
            'description_en': 'Unlock request',
            'extra_condition': 'is_locked = True'
        },
        'ASSIGN_GRANT': {
            'allowed_statuses': [ServiceStatusChoice.PENDING],
            'description': 'تخصيص منحة',
            'description_en': 'Assign grant'
        },
        'APPROVE_GRANT': {
            'allowed_statuses': [ServiceStatusChoice.PENDING],
            'description': 'الموافقة على المنحة',
            'description_en': 'Approve grant'
        },
        'REJECT_GRANT': {
            'allowed_statuses': [ServiceStatusChoice.PENDING],
            'description': 'رفض المنحة',
            'description_en': 'Reject grant'
        },
        'ADD_DISCOUNT': {
            'allowed_statuses': [ServiceStatusChoice.PENDING],
            'description': 'إضافة خصم',
            'description_en': 'Add discount'
        },
        'APPROVE_DISCOUNT': {
            'allowed_statuses': [ServiceStatusChoice.PENDING],
            'description': 'الموافقة على الخصم',
            'description_en': 'Approve discount'
        },
        'REJECT_DISCOUNT': {
            'allowed_statuses': [ServiceStatusChoice.PENDING],
            'description': 'رفض الخصم',
            'description_en': 'Reject discount'
        },
        'CANCEL_GRANT': {
            'allowed_statuses': [ServiceStatusChoice.PENDING],
            'description': 'إلغاء منحة',
            'description_en': 'Cancel grant'
        },
        'UPDATE_GRANT': {
            'allowed_statuses': [ServiceStatusChoice.PENDING],
            'description': 'تعديل منحة',
            'description_en': 'Update grant'
        },
        'UPDATE_DISCOUNT': {
            'allowed_statuses': [ServiceStatusChoice.PENDING],
            'description': 'تعديل خصم',
            'description_en': 'Update discount'
        },
        'CANCEL_DISCOUNT': {
            'allowed_statuses': [ServiceStatusChoice.PENDING],
            'description': 'إلغاء خصم',
            'description_en': 'Cancel discount'
        },
    }
    
    # إجراءات المراحل (RequestAction/Stage)
    STAGE_ACTION_STATUSES = {
        'START': {
            'allowed_statuses': [StageStatusChoice.PENDING],
            'description': 'بدء المرحلة',
            'description_en': 'Start stage'
        },
        'COMPLETE': {
            'allowed_statuses': [StageStatusChoice.IN_PROGRESS],
            'description': 'إكمال المرحلة',
            'description_en': 'Complete stage'
        },
        'APPROVE': {
            'allowed_statuses': [StageStatusChoice.IN_PROGRESS],
            'description': 'الموافقة على المرحلة',
            'description_en': 'Approve stage'
        },
        'REJECT': {
            'allowed_statuses': [StageStatusChoice.PENDING],
            'description': 'رفض المرحلة',
            'description_en': 'Reject stage'
        },
        'RETURN': {
            'allowed_statuses': [StageStatusChoice.IN_PROGRESS],
            'description': 'إرجاع المرحلة',
            'description_en': 'Return stage'
        },
        'ADVANCE': {
            'allowed_statuses': [StageStatusChoice.COMPLETED],
            'description': 'الانتقال للمرحلة التالية',
            'description_en': 'Advance to next stage'
        },
        'EXECUTE': {
            'allowed_statuses': [StageStatusChoice.IN_PROGRESS],
            'description': 'تنفيذ المرحلة',
            'description_en': 'Execute stage'
        },
        'INPUT': {
            'allowed_statuses': [StageStatusChoice.IN_PROGRESS],
            'description': 'إدارة ملفات المدخل',
            'description_en': 'Manage input files'
        },
        'OUTPUT': {
            'allowed_statuses': [StageStatusChoice.IN_PROGRESS],
            'description': 'إدارة ملفات المخرج',
            'description_en': 'Manage output files'
        },
        'NOTE': {
            'allowed_statuses': None,  # جميع الحالات
            'description': 'إضافة ملاحظة',
            'description_en': 'Add note'
        },
        'CHECKLIST_ADD': {
            'allowed_statuses': [StageStatusChoice.IN_PROGRESS],
            'description': 'إضافة عنصر للقائمة',
            'description_en': 'Add checklist item'
        },
        'CHECKLIST_DELETE': {
            'allowed_statuses': [StageStatusChoice.IN_PROGRESS],
            'description': 'حذف عنصر من القائمة',
            'description_en': 'Delete checklist item'
        },
        'CHECKLIST_CHECK': {
            'allowed_statuses': [StageStatusChoice.IN_PROGRESS],
            'description': 'تحقق من عنصر',
            'description_en': 'Check checklist item'
        },
        'CHECKLIST_UNCHECK': {
            'allowed_statuses': [StageStatusChoice.IN_PROGRESS],
            'description': 'إلغاء تحقق من عنصر',
            'description_en': 'Uncheck checklist item'
        },
    }
    
    def get(self, request):
        """
        جلب صلاحيات المستخدم
        Query params:
            - service_id: معرف الخدمة (اختياري)
            - request_id: معرف الطلب (اختياري) - لجلب صلاحيات المراحل
            - include_statuses: تضمين الحالات المسموحة (true/false)
        """
        user = request.user
        service_id = request.query_params.get('service_id')
        request_id = request.query_params.get('request_id')
        include_statuses = request.query_params.get('include_statuses', 'true').lower() == 'true'
        
        response_data = {
            'user_id': user.id,
            'username': user.username,
            'is_superuser': user.is_superuser,
            'service_permissions': [],
            'stage_permissions': [],
        }
        
        # جلب صلاحيات الخدمات
        if service_id:
            response_data['service_permissions'] = self._get_service_permissions(user, service_id, include_statuses)
        else:
            response_data['service_permissions'] = self._get_all_service_permissions(user, include_statuses)
        
        # جلب صلاحيات المراحل
        if request_id:
            response_data['stage_permissions'] = self._get_stage_permissions(user, request_id, include_statuses)
        
        # إضافة قائمة الإجراءات مع الحالات
        if include_statuses:
            response_data['request_actions'] = self._get_request_actions_with_statuses()
            response_data['stage_actions'] = self._get_stage_actions_with_statuses()
        
        return Response({
            'success': True,
            'message': _('تم جلب صلاحيات المستخدم بنجاح'),
            'data': response_data
        })
    
    def _get_service_permissions(self, user, service_id, include_statuses=True):
        """جلب صلاحيات المستخدم لخدمة معينة"""
        try:
            service = Service.objects.get(pk=service_id)
        except Service.DoesNotExist:
            return []
        
        # جلب الصلاحيات من المجموعات
        user_groups = user.groups.all()
        permissions = GroupServicePermission.objects.filter(
            fk_service=service,
            fk_group__in=user_groups
        ).values_list('permission_type', flat=True).distinct()
        
        permissions_list = list(permissions)
        
        result = {
            'service_id': service.id,
            'service_code': service.code,
            'service_name': service.name_ar,
            'permissions': permissions_list,
        }
        
        if include_statuses:
            result['permissions_with_statuses'] = [
                {
                    'permission': perm,
                    **self.REQUEST_ACTION_STATUSES.get(perm, {})
                }
                for perm in permissions_list
            ]
        
        return [result]
    
    def _get_all_service_permissions(self, user, include_statuses=True):
        """جلب صلاحيات المستخدم لجميع الخدمات"""
        user_groups = user.groups.all()
        
        permissions = GroupServicePermission.objects.filter(
            fk_group__in=user_groups
        ).select_related('fk_service').values(
            'fk_service_id',
            'fk_service__code',
            'fk_service__name_ar',
            'permission_type'
        )
        
        # تجميع حسب الخدمة
        services_dict = {}
        for perm in permissions:
            service_id = perm['fk_service_id']
            if service_id not in services_dict:
                services_dict[service_id] = {
                    'service_id': service_id,
                    'service_code': perm['fk_service__code'],
                    'service_name': perm['fk_service__name_ar'],
                    'permissions': []
                }
            if perm['permission_type'] not in services_dict[service_id]['permissions']:
                services_dict[service_id]['permissions'].append(perm['permission_type'])
        
        result = list(services_dict.values())
        
        if include_statuses:
            for service in result:
                service['permissions_with_statuses'] = [
                    {
                        'permission': perm,
                        **self.REQUEST_ACTION_STATUSES.get(perm, {})
                    }
                    for perm in service['permissions']
                ]
        
        return result
    
    def _get_stage_permissions(self, user, request_id, include_statuses=True):
        """جلب صلاحيات المستخدم على مراحل طلب معين"""
        try:
            service_request = ServiceRequest.objects.get(pk=request_id)
        except ServiceRequest.DoesNotExist:
            return []
        
        # جلب صلاحيات المستخدم على المراحل
        stage_perms = StagePermission.objects.filter(
            fk_user=user,
            fk_workflow_step_permission__fk_workflow_step__fk_service=service_request.fk_service
        ).select_related(
            'fk_workflow_step_permission',
            'fk_workflow_step_permission__fk_workflow_step',
            'fk_workflow_step_permission__fk_workflow_step__fk_stage'
        )
        
        # تجميع حسب الخطوة
        steps_dict = {}
        for sp in stage_perms:
            step = sp.fk_workflow_step_permission.fk_workflow_step
            step_id = step.id
            perm_type = sp.fk_workflow_step_permission.permission_type
            
            if step_id not in steps_dict:
                steps_dict[step_id] = {
                    'workflow_step_id': step_id,
                    'stage_name': step.fk_stage.name_ar if step.fk_stage else None,
                    'order': step.order,
                    'permissions': []
                }
            
            if perm_type not in steps_dict[step_id]['permissions']:
                steps_dict[step_id]['permissions'].append(perm_type)
        
        result = sorted(steps_dict.values(), key=lambda x: x['order'])
        
        if include_statuses:
            for step in result:
                step['permissions_with_statuses'] = [
                    {
                        'permission': perm,
                        **self.STAGE_ACTION_STATUSES.get(perm, {})
                    }
                    for perm in step['permissions']
                ]
        
        return result
    
    def _get_request_actions_with_statuses(self):
        """إرجاع قائمة إجراءات الطلبات مع الحالات المسموحة"""
        result = []
        for action, info in self.REQUEST_ACTION_STATUSES.items():
            result.append({
                'action': action,
                'description': str(info.get('description', '')),
                'description_en': info.get('description_en', ''),
                'allowed_statuses': info.get('allowed_statuses'),
                'excluded_statuses': info.get('excluded_statuses'),
                'extra_condition': info.get('extra_condition'),
            })
        return result
    
    def _get_stage_actions_with_statuses(self):
        """إرجاع قائمة إجراءات المراحل مع الحالات المسموحة"""
        result = []
        for action, info in self.STAGE_ACTION_STATUSES.items():
            result.append({
                'action': action,
                'description': str(info.get('description', '')),
                'description_en': info.get('description_en', ''),
                'allowed_statuses': info.get('allowed_statuses'),
            })
        return result


class RequestActionsStatusAPIView(APIView):
    """
    API لجلب الإجراءات المتاحة لطلب معين حسب حالته
    GET /api/d-services/request-actions-status/{request_id}/
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk=None):
        """جلب الإجراءات المتاحة للطلب حسب حالته الحالية"""
        user = request.user
        
        try:
            service_request = ServiceRequest.objects.select_related('fk_service').get(pk=pk)
        except ServiceRequest.DoesNotExist:
            return Response({
                'success': False,
                'message': _('الطلب غير موجود')
            }, status=404)
        
        current_status = service_request.status
        is_locked = service_request.is_locked
        grant_status = service_request.grant_status
        discount_status = service_request.discount_status
        is_discount_allowed = service_request.is_discount_allowed
        is_donor_invoice_allowed = service_request.is_donor_invoice_allowed
        

        # جلب صلاحيات المستخدم
        user_groups = user.groups.all()
        user_permissions = list(GroupServicePermission.objects.filter(
            fk_permission__fk_service=service_request.fk_service,
            fk_group__in=user_groups
        ).values_list('fk_permission__permission_type', flat=True).distinct())
        # تحديد الإجراءات المتاحة
        available_actions = []
        unavailable_actions = []
        
        action_statuses = UserPermissionsAPIView.REQUEST_ACTION_STATUSES
        
        for action, info in action_statuses.items():
            has_permission = action in user_permissions or user.is_superuser
            allowed_statuses = info.get('allowed_statuses')
            excluded_statuses = info.get('excluded_statuses', [])
            
            # التحقق من الحالة
            status_allowed = True
            if allowed_statuses is not None:
                status_allowed = current_status in allowed_statuses
            if excluded_statuses and current_status in excluded_statuses:
                status_allowed = False
            
            # التحقق من شروط إضافية
            condition_met = True
            extra_condition = info.get('extra_condition')
            if extra_condition:
                if 'is_locked = False' in extra_condition:
                    condition_met = not is_locked
                elif 'is_locked = True' in extra_condition:
                    condition_met = is_locked
            
            if action  == 'ASSIGN_GRANT' and grant_status in  [GrantStatusChoice.PENDING,GrantStatusChoice.APPROVED]:
                condition_met =  False
            if action  == 'ASSIGN_GRANT' and not is_donor_invoice_allowed:
                condition_met =  False
            if action  == 'CANCEL_GRANT' and grant_status not in  [GrantStatusChoice.APPROVED]:
                condition_met =  False
            if action  == 'REJECT_GRANT' and grant_status  not in  [GrantStatusChoice.PENDING]:
                condition_met =  False
            if action  == 'APPROVE_GRANT' and grant_status  not in  [GrantStatusChoice.PENDING]:
                condition_met =  False
            if action  == 'UPDATE_GRANT' and grant_status  not in  [GrantStatusChoice.APPROVED]:
                condition_met =  False
            if action  == 'ADD_DISCOUNT' and discount_status in  [DiscountStatusChoice.PENDING,DiscountStatusChoice.APPROVED]:
                condition_met =  False
            if action  == 'ADD_DISCOUNT' and not is_discount_allowed:
                condition_met =  False
            if action  == 'CANCEL_DISCOUNT' and discount_status not  in  [DiscountStatusChoice.APPROVED]:
                condition_met =  False
            if action  == 'REJECT_DISCOUNT' and discount_status not  in  [DiscountStatusChoice.PENDING]:
                condition_met =  False
            if action  == 'APPROVE_DISCOUNT' and discount_status not  in  [DiscountStatusChoice.PENDING]:
                condition_met =  False
            if action  == 'UPDATE_DISCOUNT' and discount_status not  in  [DiscountStatusChoice.APPROVED]:
                condition_met =  False
            if action  == 'START' and (discount_status in [DiscountStatusChoice.PENDING] or grant_status in  [GrantStatusChoice.PENDING]):
                condition_met =  False

            action_info = {
                'action': action,
                'description': str(info.get('description', '')),
                'description_en': info.get('description_en', ''),
                'has_permission': has_permission,
                'status_allowed': status_allowed,
                'condition_met': condition_met,
                'can_execute': has_permission and status_allowed and condition_met,
            }
            

            if action_info['can_execute']:
                available_actions.append(action_info)
            else:
                action_info['reason'] = []
                if not has_permission:
                    action_info['reason'].append('no_permission')
                if not status_allowed:
                    action_info['reason'].append(f'status_not_allowed (current: {current_status})')
                if not condition_met:
                    action_info['reason'].append(f'condition_not_met ({extra_condition})')
                unavailable_actions.append(action_info)
        
        return Response({
            'success': True,
            'message': _('تم جلب الإجراءات المتاحة بنجاح'),
            'data': {
                'request_id': service_request.id,
                'request_number': service_request.request_number,
                'current_status': current_status,
                'current_status_display': service_request.get_status_display(),
                'is_locked': is_locked,
                'available_actions': available_actions,
                'unavailable_actions': unavailable_actions,
            }
        })


class StageActionsStatusAPIView(APIView):
    """
    API لجلب الإجراءات المتاحة لمرحلة (RequestAction) معينة حسب حالتها
    GET /api/d-services/stage-actions-status/{action_id}/
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk=None):
        """جلب الإجراءات المتاحة للمرحلة حسب حالتها الحالية"""
        from d_services.models.RequestAction import RequestAction
        from d_services.models.StagePermission import StagePermission
        
        user = request.user
        
        try:
            request_action = RequestAction.objects.select_related(
                'fk_request', 'fk_workflow_step', 'fk_workflow_step__fk_stage'
            ).get(pk=pk)
        except RequestAction.DoesNotExist:
            return Response({
                'success': False,
                'message': _('المرحلة غير موجودة')
            }, status=404)
        
        current_status = request_action.stage_status
        is_current = request_action.is_current
        is_request_locked = request_action.fk_request.is_locked
        # Efficient check for first action - use order comparison instead of fetching all actions
        is_first = not RequestAction.objects.filter(
            fk_request_id=request_action.fk_request_id,
            order__lt=request_action.order
        ).exists()
        is_final_step = request_action.is_final_step
        has_approval = request_action.has_approval
        is_approved = request_action.is_approved
        is_executed = request_action.is_executed
        is_execution_step = request_action.is_execution_step
        has_custom_output = request_action.has_custom_output
        has_custom_input = request_action.has_custom_input
        
        if not is_current:
            return Response({
                'success': True,
                'message': _('تم جلب الإجراءات المتاحة للمرحلة بنجاح'),
                'data': {
                    'action_id': request_action.id,
                    'request_id': request_action.fk_request_id,
                    'request_number': request_action.fk_request.request_number,
                    'workflow_step_id': request_action.fk_workflow_step_id,
                    'stage_name': request_action.fk_workflow_step.fk_stage.name_ar if request_action.fk_workflow_step.fk_stage else None,
                    'order': request_action.order,
                    'current_status': current_status,
                    'current_status_display': request_action.get_stage_status_display(),
                    'is_current': is_current,
                    'is_request_locked': is_request_locked,
                    'available_actions': [],
                }
            })

        # جلب صلاحيات المستخدم على هذه المرحلة
        user_stage_permissions = list(StagePermission.objects.filter(
            fk_workflow_step_permission__fk_workflow_step=request_action.fk_workflow_step,
            fk_user=user
        ).values_list('fk_workflow_step_permission__permission_type', flat=True).distinct())
        
        # تحديد الإجراءات المتاحة
        available_actions = []
        unavailable_actions = []
        
        action_statuses = UserPermissionsAPIView.STAGE_ACTION_STATUSES

        for action, info in action_statuses.items():
            has_permission = action in user_stage_permissions or user.is_superuser
            allowed_statuses = info.get('allowed_statuses')
            
            # التحقق من الحالة
            status_allowed = True
            if allowed_statuses is not None:
                status_allowed = current_status in allowed_statuses
            
            # التحقق من شروط إضافية
            condition_met = True
            reasons = []
            
            # التحقق من أن المرحلة هي الحالية (لمعظم الإجراءات)
            if action not in ['NOTE'] and not is_current:
                condition_met = False
                reasons.append('not_current_stage')
            if action in ['RETURN'] and is_first:
                condition_met = False
                reasons.append('first_action')

            if action == 'APPROVE' and not has_approval:
                condition_met = False
                reasons.append('stage_does_not_require_approval')
            if action == 'COMPLETE' and has_approval and not is_approved:
                condition_met = False
                reasons.append('stage_does_not_require_approval')
            
            if action == 'APPROVE' and is_approved:
                condition_met = False
                reasons.append('already_approved')
            if action == 'EXECUTE' and not is_execution_step:
                condition_met = False
                reasons.append('does_not_have_execute')
            if action == 'EXECUTE' and is_executed:
                condition_met = False
                reasons.append('already_execute')
            if action == 'INPUT' and not has_custom_input:
                condition_met = False
                reasons.append('does_not_have_output')
            if action == 'OUTPUT' and not has_custom_output:
                condition_met = False
                reasons.append('does_not_have_input')
            
            # إذا كانت المرحلة الأخيرة لا يظهر إجراء الانتقال للتالية
            if action == 'ADVANCE' and is_final_step:
                condition_met = False
                reasons.append('is_final_step')

            # التحقق من أن الطلب غير مقفول
            if is_request_locked:
                condition_met = False
                reasons.append('request_locked')
            
            action_info = {
                'action': action,
                'description': str(info.get('description', '')),
                'description_en': info.get('description_en', ''),
                'has_permission': has_permission,
                'status_allowed': status_allowed,
                'condition_met': condition_met,
                'can_execute': has_permission and status_allowed and condition_met,
            }
            
            if action_info['can_execute']:
                available_actions.append(action_info)
            else:
                action_info['reason'] = reasons.copy()
                if not has_permission:
                    action_info['reason'].append('no_permission')
                if not status_allowed:
                    action_info['reason'].append(f'status_not_allowed (current: {current_status})')
                unavailable_actions.append(action_info)
        
        return Response({
            'success': True,
            'message': _('تم جلب الإجراءات المتاحة للمرحلة بنجاح'),
            'data': {
                'action_id': request_action.id,
                'request_id': request_action.fk_request_id,
                'request_number': request_action.fk_request.request_number,
                'workflow_step_id': request_action.fk_workflow_step_id,
                'stage_name': request_action.fk_workflow_step.fk_stage.name_ar if request_action.fk_workflow_step.fk_stage else None,
                'order': request_action.order,
                'current_status': current_status,
                'current_status_display': request_action.get_stage_status_display(),
                'is_current': is_current,
                'is_request_locked': is_request_locked,
                'available_actions': available_actions,
                'unavailable_actions': unavailable_actions,
            }
        })
