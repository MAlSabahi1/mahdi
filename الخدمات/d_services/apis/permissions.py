
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.db import transaction

from d_services.models.GroupServicePermission import GroupServicePermission
from d_services.models.ServicePermission import ServicePermission
from d_services.models.StagePermission import StagePermission
from d_services.serializers.permissions import (
    GroupServicePermissionSerializer,
    ServicePermissionSerializer,
    StagePermissionSerializer,
)
from config.imports.viewmodel_core import AllMVS
from OpenSoftCoreV4.usermanager.models.Group import CustomGroup
from utils.BranchMixinQuerset import BranchViewSetMixin

User = get_user_model()


class GroupServicePermissionMVS(AllMVS):
    queryset = GroupServicePermission.objects.prefetch_related()
    serializer_class = GroupServicePermissionSerializer
    enable_actions = ['all','select','list','second_list','filter','filter_paginate',"sync-import" ,  "sync-export",  "sync-push","sync-pull"]
    def create(self, request, *args, **kwargs):
        """
        {
            "fk_service": 1,
            "groups": [
                {
                    "fk_group": 1,
                    "permissions": ["CREATE", "READ", "UPDATE"]  # قائمة بـ permission_type
                },
                {
                    "fk_group": 2,
                    "permissions": ["CREATE", "DELETE", "PRINT"]
                }
            ]
        }
        """
        from d_services.models.ServicePermission import ServicePermission
        from d_services.models.Service import Service
        
        groups_data = request.data.get('groups', [])
        service_id = request.data.get('fk_service')
        
        user = request.user
        if not service_id:
            return Response(
                {'error': _('معرف الخدمة مطلوب')},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not isinstance(groups_data, list):
            return Response(
                {'error': _('يجب إرسال مصفوفة من المجموعات')},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # جلب الخدمة
        try:
            service = Service.objects.get(pk=service_id, is_deleted=False)
        except Service.DoesNotExist:
            return Response(
                {'error': _('الخدمة غير موجودة')},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # جلب صلاحيات الخدمة مع أنواعها
        service_permissions = ServicePermission.objects.filter(fk_service=service)
        service_permission_ids = set(service_permissions.values_list('id', flat=True))
        # إنشاء قاموس لربط permission_type بـ permission_id
        permission_type_to_id = {
            sp.permission_type: sp.id for sp in service_permissions
        }
        
        user_org = getattr(request.user, 'fk_organization', None)
        
        with transaction.atomic():
            # جلب المجموعات الموجودة حالياً التي لها صلاحيات على هذه الخدمة
            existing_group_ids = set(
                GroupServicePermission.objects.filter(
                    fk_permission_id__in=service_permission_ids,
                    fk_group__fk_organization = user.fk_organization
                ).values_list('fk_group_id', flat=True).distinct()
            )
            
            # المجموعات المرسلة
            sent_group_ids = set(
                group.get('fk_group') for group in groups_data if group.get('fk_group')
            )
            
            created_count = 0
            updated_count = 0
            deleted_permissions_count = 0
            
            for group_data in groups_data:
                group_id = group_data.get('fk_group')
                permission_types = group_data.get('permissions', [])
                if not group_id:
                    return Response(
                        {'error': _('معرف المجموعة مطلوب')},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # جلب المجموعة
                try:
                    group = CustomGroup.objects.get(pk=group_id)
                except CustomGroup.DoesNotExist:
                    return Response(
                        {'error': _('المجموعة غير موجودة'), 'group_id': group_id},
                        status=status.HTTP_404_NOT_FOUND
                    )
                
                # التحقق من أن المجموعة تابعة لنفس منظمة المستخدم
                group_org = getattr(group, 'fk_organization', None)
                if user_org != group_org:
                    return Response(
                        {'error': _('المجموعة غير موجودة أو لا تابع لنظرك'), 'group_id': group_id},
                        status=status.HTTP_403_FORBIDDEN
                    )
                
                # تحويل permission_types إلى permission_ids والتأكد من أنها تابعة للخدمة
                valid_permission_ids = set(
                    permission_type_to_id[pt] for pt in permission_types 
                    if pt in permission_type_to_id
                )
                
                # جلب الصلاحيات الموجودة لهذه المجموعة على هذه الخدمة
                existing_permissions = set(
                    GroupServicePermission.objects.filter(
                        fk_group=group,
                        fk_permission_id__in=service_permission_ids
                    ).values_list('fk_permission_id', flat=True)
                )
                
                # إضافة الصلاحيات الجديدة
                for permission_id in valid_permission_ids:
                    if permission_id not in existing_permissions:
                        GroupServicePermission.objects.create(
                            fk_group=group,
                            fk_permission_id=permission_id
                        )
                        created_count += 1
                
                # حذف الصلاحيات القديمة
                for permission_id in existing_permissions:
                    if permission_id not in valid_permission_ids:
                        GroupServicePermission.objects.filter(
                            fk_group=group,
                            fk_permission_id=permission_id
                        ).delete()
                        deleted_permissions_count += 1
                
                updated_count += 1
            
            # حذف المجموعات غير المرسلة (حذف جميع صلاحياتها على هذه الخدمة)
            deleted_groups_count = 0
            for group_id in existing_group_ids:
                if group_id not in sent_group_ids:
                    GroupServicePermission.objects.filter(
                        fk_group_id=group_id,
                        fk_permission_id__in=service_permission_ids
                    ).delete()
                    deleted_groups_count += 1
        
        # جلب النتيجة النهائية
        result = self._get_service_groups_permissions(service,user ,service_permission_ids)
        
        return Response({
            'message': _('تم تحديث صلاحيات المجموعات بنجاح'),
            'created_permissions_count': created_count,
            'deleted_permissions_count': deleted_permissions_count,
            'updated_groups_count': updated_count,
            'deleted_groups_count': deleted_groups_count,
            'groups': result
        }, status=status.HTTP_200_OK)
    
    def _get_service_groups_permissions(self, service, user, service_permission_ids=None):
        """جلب المجموعات مع صلاحياتها للخدمة"""
        from d_services.models.ServicePermission import ServicePermission
        
        if service_permission_ids is None:
            service_permission_ids = set(
                ServicePermission.objects.filter(
                    fk_service=service
                ).values_list('id', flat=True)
            )
        
        # جلب جميع الصلاحيات المربوطة بالمجموعات لهذه الخدمة
        group_permissions = GroupServicePermission.objects.filter(
            fk_permission_id__in=service_permission_ids,
            fk_group__fk_organization=user.fk_organization
        ).select_related('fk_group', 'fk_permission')
        
        # تجميع الصلاحيات حسب المجموعة
        groups_dict = {}
        for gp in group_permissions:
            group_id = gp.fk_group_id
            permission_type = gp.fk_permission.permission_type
            if group_id not in groups_dict:
                groups_dict[group_id] = {
                    'fk_group': group_id,
                    'fk_group__name_ar': getattr(gp.fk_group, 'name_ar', ''),
                    'fk_group__name_en': getattr(gp.fk_group, 'name_en', ''),
                    'permissions': []
                }
            groups_dict[group_id]['permissions'].append(permission_type)
        
        return list(groups_dict.values())
    
    def list(self, request):
        """
        جلب جميع المجموعات مع صلاحياتها لخدمة معينة
        """

        from d_services.models.Service import Service
        fk_service = request.query_params.get('fk_service')
        try:
            service = Service.objects.get(pk=fk_service)
        except Service.DoesNotExist:
            return Response(
                {'error': _('الخدمة غير موجودة')},
                status=status.HTTP_404_NOT_FOUND
            )
        user =request.user

        result = self._get_service_groups_permissions(service,user)
        
        return Response({
            'fk_service': service.id,
            'fk_service__code': service.code,
            'fk_service__name_ar': service.name_ar,
            'groups': result
        })



class StagePermissionMVS(BranchViewSetMixin, AllMVS):
    queryset = StagePermission.objects.prefetch_related()
    serializer_class = StagePermissionSerializer
    branch_field = 'fk_user__fk_organization'
    enable_actions = ['all','select','list','second_list','filter','filter_paginate',]
    
    def list(self, request, *args, **kwargs):

        from d_services.models.ServiceWorkflowStep import ServiceWorkflowStep
        from d_services.models.ServiceWorkFlowStepPermission import ServiceWorkFlowStepPermission
        
        workflow_step_id = request.query_params.get('fk_workflow_step')
        
        # التحقق من صلاحيات المستخدم
        if not getattr(request.user, 'is_manager', False):
            return Response(
                {'error': _('ليس لديك صلاحيات')},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if not workflow_step_id:
            return Response(
                {'error': _('معرف خطوة سير العمل مطلوب (fk_workflow_step)')},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # جلب منظمة المستخدم
        user_org = getattr(request.user, 'fk_organization', None)
        if not user_org:
            return Response(
                {'error': _('المستخدم غير مرتبط بمنظمة')},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # التحقق من وجود خطوة سير العمل
        try:
            workflow_step = ServiceWorkflowStep.objects.get(pk=workflow_step_id, is_deleted=False)
        except ServiceWorkflowStep.DoesNotExist:
            return Response(
                {'error': _('خطوة سير العمل غير موجودة')},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # جلب صلاحيات المرحلة للمستخدمين
        result = self._get_users_permissions(workflow_step, user_org)
        
        return Response({
            'message': _('تم جلب صلاحيات المرحلة بنجاح'),
            'fk_workflow_step': int(workflow_step_id),
            'fk_organization': user_org.id,
            'workflow_step_name': str(workflow_step),
            'users': result
        }, status=status.HTTP_200_OK)
    
    def _get_users_permissions(self, workflow_step, user_org):
        """جلب المستخدمين مع صلاحياتهم"""
        # جلب جميع صلاحيات المرحلة
        stage_perms = StagePermission.objects.filter(
            fk_workflow_step_permission__fk_workflow_step=workflow_step,
            fk_user__fk_organization=user_org
        ).select_related('fk_user', 'fk_workflow_step_permission')
        
        # تجميع الصلاحيات حسب المستخدم
        users_dict = {}
        for sp in stage_perms:
            user_id = sp.fk_user_id
            permission_type = sp.fk_workflow_step_permission.permission_type
            
            if user_id not in users_dict:
                user = sp.fk_user
                users_dict[user_id] = {
                    'fk_user': user_id,
                    'username': user.username,
                    'full_name': getattr(user, 'get_full_name', lambda: '')() or user.username,
                    'permissions': []
                }
            users_dict[user_id]['permissions'].append(permission_type)
        
        return list(users_dict.values())
    
    def create(self, request, *args, **kwargs):
        """
        Request:
        {
            "fk_workflow_step": 1,
            "users": [
                {"fk_user": 1, "permissions": ["START", "APPROVE"]},
                {"fk_user": 2, "permissions": ["EXECUTE"]}
            ]
        }
        """
        from d_services.models.ServiceWorkflowStep import ServiceWorkflowStep
        from d_services.models.ServiceWorkFlowStepPermission import ServiceWorkFlowStepPermission
        
        workflow_step_id = request.data.get('fk_workflow_step')
        users_data = request.data.get('users', [])
        
        if not getattr(request.user, 'is_manager', False):
            return Response(
                {'error': _('ليس لديك صلاحيات')},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if not workflow_step_id:
            return Response(
                {'error': _('معرف خطوة سير العمل مطلوب')},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not isinstance(users_data, list):
            return Response(
                {'error': _('يجب إرسال مصفوفة من المستخدمين')},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            workflow_step = ServiceWorkflowStep.objects.get(pk=workflow_step_id, is_deleted=False)
        except ServiceWorkflowStep.DoesNotExist:
            return Response(
                {'error': _('خطوة سير العمل غير موجودة')},
                status=status.HTTP_404_NOT_FOUND
            )
        
        user_org = getattr(request.user, 'fk_organization', None)
        if not user_org:
            return Response(
                {'error': _('المستخدم غير مرتبط بمنظمة')},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # جلب أنواع الصلاحيات لهذه الخطوة
        step_permissions = ServiceWorkFlowStepPermission.objects.filter(
            fk_workflow_step=workflow_step
        )
        permission_type_to_obj = {sp.permission_type: sp for sp in step_permissions}
        
        with transaction.atomic():
            created_count = 0
            deleted_count = 0
            sent_user_ids = set()
            
            for user_data in users_data:
                user_id = user_data.get('fk_user')
                permission_types = user_data.get('permissions', [])
                
                if not user_id:
                    return Response(
                        {'error': _('معرف المستخدم مطلوب')},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # التحقق من أن المستخدم ينتمي للمنظمة
                try:
                    user = User.objects.get(pk=user_id, fk_organization=user_org)
                except User.DoesNotExist:
                    return Response(
                        {'error': _('المستخدم غير موجود أو لا ينتمي لمنظمتك'), 'user_id': user_id},
                        status=status.HTTP_403_FORBIDDEN
                    )
                
                sent_user_ids.add(user_id)
                
                # جلب الصلاحيات الموجودة لهذا المستخدم
                existing_perm_types = set(
                    StagePermission.objects.filter(
                        fk_workflow_step_permission__fk_workflow_step=workflow_step,
                        fk_user=user
                    ).values_list('fk_workflow_step_permission__permission_type', flat=True)
                )
                
                sent_perm_types = set(permission_types)
                
                # إضافة صلاحيات جديدة
                for perm_type in sent_perm_types:
                    if perm_type not in existing_perm_types:
                        if perm_type in permission_type_to_obj:
                            step_perm = permission_type_to_obj[perm_type]
                        else:
                            step_perm = ServiceWorkFlowStepPermission.objects.create(
                                fk_workflow_step=workflow_step,
                                permission_type=perm_type
                            )
                            permission_type_to_obj[perm_type] = step_perm
                        
                        StagePermission.objects.create(
                            fk_workflow_step_permission=step_perm,
                            fk_user=user
                        )
                        created_count += 1
                
                # حذف الصلاحيات غير المرسلة
                for perm_type in existing_perm_types:
                    if perm_type not in sent_perm_types:
                        StagePermission.objects.filter(
                            fk_workflow_step_permission__fk_workflow_step=workflow_step,
                            fk_workflow_step_permission__permission_type=perm_type,
                            fk_user=user
                        ).delete()
                        deleted_count += 1
            
            # حذف المستخدمين غير المرسلين
            existing_user_ids = set(
                StagePermission.objects.filter(
                    fk_workflow_step_permission__fk_workflow_step=workflow_step,
                    fk_user__fk_organization=user_org
                ).values_list('fk_user_id', flat=True).distinct()
            )
            
            for uid in existing_user_ids:
                if uid not in sent_user_ids:
                    StagePermission.objects.filter(
                        fk_workflow_step_permission__fk_workflow_step=workflow_step,
                        fk_user_id=uid
                    ).delete()
                    deleted_count += 1
        
        # جلب النتيجة النهائية
        result = self._get_users_permissions(workflow_step, user_org)
        
        return Response({
            'message': _('تم تحديث صلاحيات المرحلة بنجاح'),
            'fk_workflow_step': workflow_step_id,
            'created_count': created_count,
            'deleted_count': deleted_count,
            'users': result
        }, status=status.HTTP_200_OK)

class ServicePermissionMVS(AllMVS):
    queryset = ServicePermission.objects.prefetch_related()
    serializer_class = ServicePermissionSerializer
    # enable_actions = ["sync-import" ,  "sync-export",  "sync-push","sync-pull"]