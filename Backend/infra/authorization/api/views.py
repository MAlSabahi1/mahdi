"""
Authorization API Views
═══════════════════════
Thin Views — كل logic في Services.

Endpoints:
    GET/POST     /roles/                  — قائمة/إنشاء الأدوار
    GET/PUT/DEL  /roles/<id>/             — تفاصيل/تعديل/حذف دور
    POST         /roles/<id>/permissions/ — تعيين صلاحيات الدور
    POST         /roles/assign/           — إسناد دور لمستخدم
    POST         /roles/revoke/           — إلغاء دور من مستخدم
    GET          /permissions/            — قائمة الصلاحيات
    GET          /my-permissions/         — صلاحيات المستخدم الحالي
"""
import logging

from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from drf_spectacular.utils import extend_schema

from infra.authorization.serializers.serializers import (
    PermissionSerializer,
    RoleOutputSerializer,
    RoleCreateSerializer,
    RoleUpdateSerializer,
    AssignRoleSerializer,
    UserPermissionsResponseSerializer,
)
from infra.authorization.services.permission_service import PermissionService
from infra.authorization.services.role_service import RoleService, RoleServiceError
from infra.authorization.models.permission import Permission

logger = logging.getLogger('authorization.views')


class RoleViewSet(ViewSet):
    """إدارة الأدوار (مدير النظام فقط)."""
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    @extend_schema(responses={200: RoleOutputSerializer(many=True)}, tags=['roles'])
    def list(self, request) -> Response:
        roles = RoleService.list_roles()
        serializer = RoleOutputSerializer(roles, many=True)
        return Response({'success': True, 'results': serializer.data})

    @extend_schema(responses={200: RoleOutputSerializer}, tags=['roles'])
    def retrieve(self, request, pk=None) -> Response:
        try:
            detail = RoleService.get_role_detail(int(pk))
        except RoleServiceError as e:
            return Response({'success': False, 'error': e.message}, status=e.status_code)
        return Response({
            'success': True,
            'data': RoleOutputSerializer(detail['role']).data,
        })

    @extend_schema(request=RoleCreateSerializer, tags=['roles'])
    def create(self, request) -> Response:
        serializer = RoleCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        perm_codes = data.pop('permissions', [])

        try:
            role = RoleService.create_role(
                **data, created_by=request.user,
            )
            if perm_codes:
                RoleService.set_role_permissions(role.pk, perm_codes, request.user)
        except RoleServiceError as e:
            return Response({'success': False, 'error': e.message}, status=e.status_code)

        return Response(
            {'success': True, 'data': RoleOutputSerializer(role).data},
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(request=RoleUpdateSerializer, tags=['roles'])
    def update(self, request, pk=None) -> Response:
        serializer = RoleUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        perm_codes = data.pop('permissions', None)

        try:
            role = RoleService.update_role(int(pk), data, request.user)
            if perm_codes is not None:
                RoleService.set_role_permissions(role.pk, perm_codes, request.user)
        except RoleServiceError as e:
            return Response({'success': False, 'error': e.message}, status=e.status_code)

        return Response({'success': True, 'data': RoleOutputSerializer(role).data})

    def partial_update(self, request, pk=None) -> Response:
        return self.update(request, pk)

    def destroy(self, request, pk=None) -> Response:
        try:
            RoleService.delete_role(int(pk))
        except RoleServiceError as e:
            return Response({'success': False, 'error': e.message}, status=e.status_code)
        return Response({'success': True, 'message': 'تم تعطيل الدور'})

    @extend_schema(request=AssignRoleSerializer, tags=['roles'])
    @action(detail=False, methods=['post'])
    def assign(self, request) -> Response:
        serializer = AssignRoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            RoleService.assign_role_to_user(
                user_id=str(serializer.validated_data['user_id']),
                role_id=serializer.validated_data['role_id'],
                assigned_by=request.user,
                expires_at=serializer.validated_data.get('expires_at'),
                notes=serializer.validated_data.get('notes', ''),
            )
        except RoleServiceError as e:
            return Response({'success': False, 'error': e.message}, status=e.status_code)
        return Response({'success': True, 'message': 'تم إسناد الدور'})

    @extend_schema(tags=['roles'])
    @action(detail=False, methods=['post'])
    def revoke(self, request) -> Response:
        user_id = request.data.get('user_id')
        role_id = request.data.get('role_id')
        if not user_id or not role_id:
            return Response(
                {'success': False, 'error': 'user_id و role_id مطلوبان'},
                status=400,
            )
        RoleService.revoke_role_from_user(str(user_id), int(role_id))
        return Response({'success': True, 'message': 'تم إلغاء الدور'})


class PermissionViewSet(ViewSet):
    """قائمة الصلاحيات المتاحة."""
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(responses={200: PermissionSerializer(many=True)}, tags=['permissions'])
    def list(self, request) -> Response:
        """قائمة كل الصلاحيات — للمدير."""
        perms = Permission.objects.filter(is_active=True).order_by('module', 'action')
        serializer = PermissionSerializer(perms, many=True)
        return Response({'success': True, 'results': serializer.data})

    @extend_schema(tags=['permissions'])
    @action(detail=False, methods=['get'], url_path='matrix')
    def matrix(self, request) -> Response:
        """
        مصفوفة الصلاحيات مُهيكلة حسب الشاشة والعملية (CRUD).
        يُستخدم في واجهة إدارة المجموعات والصلاحيات.
        """
        from infra.authorization.registry.permissions import SCREEN_LABELS, classify_permission

        perms = Permission.objects.filter(is_active=True).order_by('module', 'action')

        # تجميع حسب الشاشة (module)
        screens_dict = {}
        for perm in perms:
            mod = perm.module
            if mod not in screens_dict:
                screens_dict[mod] = {
                    'name': mod,
                    'label': SCREEN_LABELS.get(mod, mod),
                    'permissions': {
                        'view': [],
                        'create': [],
                        'edit': [],
                        'delete': [],
                        'approve': [],
                        'export': [],
                        'manage': [],
                        'execute': [],
                        'import': [],
                        'custom': [],
                    }
                }

            category = classify_permission(perm)
            screens_dict[mod]['permissions'][category].append({
                'id': perm.id,
                'code': perm.code,
                'action': perm.action,
                'label': perm.label,
                'scope': perm.scope,
            })

        # ترتيب الشاشات حسب ترتيب SCREEN_LABELS
        ordered_keys = list(SCREEN_LABELS.keys())
        screens = []
        for key in ordered_keys:
            if key in screens_dict:
                screens.append(screens_dict[key])
        # إضافة أي شاشات غير مُعرّفة في SCREEN_LABELS
        for key, val in screens_dict.items():
            if key not in ordered_keys:
                screens.append(val)

        return Response({'success': True, 'screens': screens})

    @extend_schema(
        responses={200: UserPermissionsResponseSerializer},
        tags=['permissions'],
    )
    @action(detail=False, methods=['get'], url_path='mine')
    def my_permissions(self, request) -> Response:
        """صلاحيات المستخدم الحالي — للـ Frontend."""
        permissions_list = PermissionService.get_user_permissions_list(request.user)
        roles = PermissionService.get_user_roles(request.user)
        return Response({
            'success': True,
            'data': {
                'permissions': permissions_list,
                'roles': roles,
            },
        })

