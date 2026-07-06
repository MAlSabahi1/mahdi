"""
Authorization API Views — واجهات API لكل طبقات الصلاحيات
═══════════════════════════════════════════════════════════
Endpoints كاملة لمطور الـ Frontend:

    Roles:          GET/POST /roles/, GET/PUT/DEL /roles/<id>/
    Permissions:    GET /permissions/, GET /permissions/mine/
    Groups:         GET/POST /permissions/groups/
    Grouped:        GET /permissions/grouped/
    Field Security: GET /permissions/mine/fields/
    Field Perms:    GET/POST /field-permissions/
    Delegations:    GET/POST /delegations/, POST /delegations/<id>/revoke/
    Emergency:      GET/POST /emergency-access/, POST .../revoke/, .../review/
    Record ACL:     GET/POST /record-acl/, DEL /record-acl/<id>/
    Policies:       GET/POST /policies/, GET/PUT/DEL /policies/<id>/
"""
import logging

from django.contrib.contenttypes.models import ContentType
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from drf_spectacular.utils import extend_schema

from infra.authorization.models.permission import Permission
from infra.authorization.services.permission_service import PermissionService
from infra.authorization.services.role_service import RoleService, RoleServiceError
from infra.authorization.serializers.serializers import (
    PermissionSerializer, RoleOutputSerializer, RoleCreateSerializer,
    RoleUpdateSerializer, AssignRoleSerializer, UserPermissionsResponseSerializer,
    PermissionGroupSerializer, PermissionGroupCreateSerializer,
    GroupedPermissionsSerializer, FieldPermissionSerializer,
    FieldPermissionCreateSerializer, RecordACLSerializer,
    RecordACLCreateSerializer, AccessPolicySerializer,
    AccessPolicyCreateSerializer, DelegationSerializer,
    DelegationCreateSerializer, EmergencyAccessSerializer,
    EmergencyGrantSerializer, EmergencyReviewSerializer,
)

logger = logging.getLogger('authorization.views')


# ══════════════════════════════════════════════════════════════
# الأدوار (Roles)
# ══════════════════════════════════════════════════════════════

class RoleViewSet(ViewSet):
    """إدارة الأدوار (مدير النظام فقط)."""
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    @extend_schema(responses={200: RoleOutputSerializer(many=True)}, tags=['roles'])
    def list(self, request) -> Response:
        roles = RoleService.list_roles()
        return Response({'success': True, 'results': RoleOutputSerializer(roles, many=True).data})

    @extend_schema(responses={200: RoleOutputSerializer}, tags=['roles'])
    def retrieve(self, request, pk=None) -> Response:
        try:
            detail = RoleService.get_role_detail(int(pk))
        except RoleServiceError as e:
            return Response({'success': False, 'error': e.message}, status=e.status_code)
        return Response({'success': True, 'data': RoleOutputSerializer(detail['role']).data})

    @extend_schema(request=RoleCreateSerializer, tags=['roles'])
    def create(self, request) -> Response:
        serializer = RoleCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        perm_codes = data.pop('permissions', [])
        try:
            role = RoleService.create_role(**data, created_by=request.user)
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
            return Response({'success': False, 'error': 'user_id و role_id مطلوبان'}, status=400)
        RoleService.revoke_role_from_user(str(user_id), int(role_id))
        return Response({'success': True, 'message': 'تم إلغاء الدور'})


# ══════════════════════════════════════════════════════════════
# الصلاحيات + المجموعات + حماية الحقول
# ══════════════════════════════════════════════════════════════

class PermissionViewSet(ViewSet):
    """الصلاحيات + المجموعات + Field Security."""
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(responses={200: PermissionSerializer(many=True)}, tags=['permissions'])
    def list(self, request) -> Response:
        """قائمة كل الصلاحيات — للمدير."""
        perms = Permission.objects.filter(is_active=True).order_by('module', 'action')
        return Response({'success': True, 'results': PermissionSerializer(perms, many=True).data})

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

    # ── صلاحياتي (للـ Frontend) ──
    @extend_schema(responses={200: UserPermissionsResponseSerializer}, tags=['permissions'])
    @action(detail=False, methods=['get'], url_path='mine')
    def my_permissions(self, request) -> Response:
        """صلاحيات المستخدم + أدواره + تفويضاته — للـ Frontend."""
        user = request.user
        return Response({
            'success': True,
            'data': {
                'permissions': PermissionService.get_user_permissions_list(user),
                'roles': PermissionService.get_user_roles(user),
                'delegations': PermissionService.get_user_delegations(user),
            },
        })

    # ── حماية الحقول لي ──
    @extend_schema(tags=['permissions'])
    @action(detail=False, methods=['get'], url_path='mine/fields')
    def my_field_security(self, request) -> Response:
        """معلومات حماية الحقول للمستخدم — للـ Frontend."""
        module = request.query_params.get('module', 'personnel')
        info = PermissionService.get_field_security_info(request.user, module)
        return Response({'success': True, 'data': info})

    # ── الصلاحيات مُجمَّعة حسب المجموعة ──
    @extend_schema(tags=['permissions'])
    @action(detail=False, methods=['get'], url_path='grouped')
    def grouped(self, request) -> Response:
        """الصلاحيات مُجمَّعة حسب المجموعة — لعرض Admin UI."""
        from infra.authorization.models.permission_group import PermissionGroup
        groups = PermissionGroup.objects.filter(is_active=True).order_by('display_order')
        result = []
        for group in groups:
            perms = Permission.objects.filter(group=group, is_active=True).order_by('action')
            result.append({
                'group': PermissionGroupSerializer(group).data,
                'permissions': PermissionSerializer(perms, many=True).data,
            })
        # صلاحيات بدون مجموعة
        ungrouped = Permission.objects.filter(group__isnull=True, is_active=True).order_by('module')
        if ungrouped.exists():
            result.append({
                'group': {'id': None, 'code': 'ungrouped', 'name': 'بدون مجموعة', 'icon': 'help-circle'},
                'permissions': PermissionSerializer(ungrouped, many=True).data,
            })
        return Response({'success': True, 'results': result})


# ══════════════════════════════════════════════════════════════
# مجموعات الصلاحيات (Permission Groups)
# ══════════════════════════════════════════════════════════════

class PermissionGroupViewSet(ViewSet):
    """إدارة مجموعات الصلاحيات."""
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    @extend_schema(tags=['permission-groups'])
    def list(self, request) -> Response:
        from infra.authorization.models.permission_group import PermissionGroup
        groups = PermissionGroup.objects.filter(is_active=True).order_by('display_order')
        return Response({'success': True, 'results': PermissionGroupSerializer(groups, many=True).data})

    @extend_schema(request=PermissionGroupCreateSerializer, tags=['permission-groups'])
    def create(self, request) -> Response:
        serializer = PermissionGroupCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        group = serializer.save()
        return Response(
            {'success': True, 'data': PermissionGroupSerializer(group).data},
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(tags=['permission-groups'])
    def update(self, request, pk=None) -> Response:
        from infra.authorization.models.permission_group import PermissionGroup
        try:
            group = PermissionGroup.objects.get(pk=pk)
        except PermissionGroup.DoesNotExist:
            return Response({'success': False, 'error': 'المجموعة غير موجودة'}, status=404)
        serializer = PermissionGroupCreateSerializer(group, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'success': True, 'data': PermissionGroupSerializer(group).data})

    def destroy(self, request, pk=None) -> Response:
        from infra.authorization.models.permission_group import PermissionGroup
        PermissionGroup.objects.filter(pk=pk).update(is_active=False)
        return Response({'success': True, 'message': 'تم تعطيل المجموعة'})


# ══════════════════════════════════════════════════════════════
# التفويضات (Delegations)
# ══════════════════════════════════════════════════════════════

class DelegationViewSet(ViewSet):
    """إدارة التفويضات — User → User."""
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(tags=['delegations'])
    def list(self, request) -> Response:
        """تفويضاتي (أعطيتها + استلمتها)."""
        from infra.authorization.services.delegation_service import DelegationService
        given = DelegationService.get_delegations_given(request.user)
        received = DelegationService.get_active_delegations_for_user(request.user)
        return Response({
            'success': True,
            'data': {
                'given': DelegationSerializer(given, many=True).data,
                'received': DelegationSerializer(received, many=True).data,
            },
        })

    @extend_schema(request=DelegationCreateSerializer, tags=['delegations'])
    def create(self, request) -> Response:
        """إنشاء تفويض جديد."""
        from infra.authorization.services.delegation_service import DelegationService, DelegationError
        serializer = DelegationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        d = serializer.validated_data
        try:
            delegation = DelegationService.create_delegation(
                delegator=request.user,
                delegate_id=str(d['delegate_id']),
                reason=d['reason'],
                starts_at=d.get('starts_at'),
                ends_at=d['ends_at'],
                role_id=d.get('role_id'),
                permission_codes=d.get('permission_codes', []),
                notes=d.get('notes', ''),
            )
        except DelegationError as e:
            return Response({'success': False, 'error': e.message}, status=400)
        return Response(
            {'success': True, 'data': DelegationSerializer(delegation).data},
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(tags=['delegations'])
    @action(detail=True, methods=['post'])
    def revoke(self, request, pk=None) -> Response:
        """إلغاء تفويض."""
        from infra.authorization.services.delegation_service import DelegationService, DelegationError
        try:
            delegation = DelegationService.revoke_delegation(int(pk), request.user)
        except DelegationError as e:
            return Response({'success': False, 'error': e.message}, status=400)
        return Response({'success': True, 'data': DelegationSerializer(delegation).data})


# ══════════════════════════════════════════════════════════════
# الوصول الطارئ (Emergency / Break Glass)
# ══════════════════════════════════════════════════════════════

class EmergencyAccessViewSet(ViewSet):
    """إدارة الوصول الطارئ (Break Glass)."""
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    @extend_schema(tags=['emergency-access'])
    def list(self, request) -> Response:
        """قائمة كل الوصول الطارئ."""
        from infra.authorization.services.emergency_service import EmergencyService
        status_filter = request.query_params.get('status')
        qs = EmergencyService.list_all(status_filter)
        return Response({'success': True, 'results': EmergencyAccessSerializer(qs, many=True).data})

    @extend_schema(request=EmergencyGrantSerializer, tags=['emergency-access'])
    @action(detail=False, methods=['post'], url_path='grant')
    def grant(self, request) -> Response:
        """منح وصول طارئ."""
        from infra.authorization.services.emergency_service import EmergencyService, EmergencyError
        serializer = EmergencyGrantSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        d = serializer.validated_data
        try:
            emergency = EmergencyService.grant(
                user_id=str(d['user_id']),
                granted_by=request.user,
                reason=d['reason'],
                permission_codes=d['permission_codes'],
                hours=d.get('hours', 4),
            )
        except EmergencyError as e:
            return Response({'success': False, 'error': e.message}, status=400)
        return Response(
            {'success': True, 'data': EmergencyAccessSerializer(emergency).data},
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(tags=['emergency-access'])
    @action(detail=True, methods=['post'])
    def revoke(self, request, pk=None) -> Response:
        """إلغاء وصول طارئ مبكراً."""
        from infra.authorization.services.emergency_service import EmergencyService, EmergencyError
        try:
            emergency = EmergencyService.revoke(int(pk), request.user)
        except EmergencyError as e:
            return Response({'success': False, 'error': e.message}, status=400)
        return Response({'success': True, 'data': EmergencyAccessSerializer(emergency).data})

    @extend_schema(request=EmergencyReviewSerializer, tags=['emergency-access'])
    @action(detail=True, methods=['post'])
    def review(self, request, pk=None) -> Response:
        """مراجعة وصول طارئ بعد انتهائه."""
        from infra.authorization.services.emergency_service import EmergencyService, EmergencyError
        serializer = EmergencyReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            emergency = EmergencyService.review(
                int(pk), request.user, serializer.validated_data['audit_notes'],
            )
        except EmergencyError as e:
            return Response({'success': False, 'error': e.message}, status=400)
        return Response({'success': True, 'data': EmergencyAccessSerializer(emergency).data})

    @extend_schema(tags=['emergency-access'])
    @action(detail=False, methods=['get'], url_path='pending-reviews')
    def pending_reviews(self, request) -> Response:
        """وصول طارئ يحتاج مراجعة."""
        from infra.authorization.services.emergency_service import EmergencyService
        qs = EmergencyService.get_pending_reviews()
        return Response({'success': True, 'results': EmergencyAccessSerializer(qs, many=True).data})


# ══════════════════════════════════════════════════════════════
# قيود السجلات (Record ACL)
# ══════════════════════════════════════════════════════════════

class RecordACLViewSet(ViewSet):
    """إدارة قيود الوصول على السجلات."""
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    @extend_schema(tags=['record-acl'])
    def list(self, request) -> Response:
        from infra.authorization.services.record_acl_service import RecordACLService
        model_filter = request.query_params.get('model')
        qs = RecordACLService.list_all(model_filter)
        return Response({'success': True, 'results': RecordACLSerializer(qs, many=True).data})

    @extend_schema(request=RecordACLCreateSerializer, tags=['record-acl'])
    def create(self, request) -> Response:
        from infra.authorization.services.record_acl_service import RecordACLService, RecordACLError
        from django.contrib.auth import get_user_model
        User = get_user_model()

        serializer = RecordACLCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        d = serializer.validated_data

        try:
            ct = ContentType.objects.get(model=d['content_type_model'])
        except ContentType.DoesNotExist:
            return Response({'success': False, 'error': 'نوع السجل غير موجود'}, status=400)

        target_user = None
        target_role = None
        if d.get('target_user_id'):
            target_user = User.objects.filter(pk=d['target_user_id']).first()
        if d.get('target_role_id'):
            from infra.authorization.models.role import Role
            target_role = Role.objects.filter(pk=d['target_role_id']).first()

        # نحتاج الكائن — نستخدم ct + object_id بدون جلبه
        class FakeObj:
            def __init__(self, pk_val):
                self.pk = pk_val
            class _meta:
                app_label = ct.app_label
                model_name = ct.model

        try:
            acl = RecordACLService.set_record_acl(
                obj=FakeObj(d['object_id']),
                access_type=d['access_type'],
                reason=d['reason'],
                created_by=request.user,
                target_user=target_user,
                target_role=target_role,
                permission_code=d.get('permission_code', ''),
                expires_at=d.get('expires_at'),
            )
        except RecordACLError as e:
            return Response({'success': False, 'error': e.message}, status=400)
        return Response(
            {'success': True, 'data': RecordACLSerializer(acl).data},
            status=status.HTTP_201_CREATED,
        )

    def destroy(self, request, pk=None) -> Response:
        from infra.authorization.services.record_acl_service import RecordACLService, RecordACLError
        try:
            RecordACLService.remove_record_acl(int(pk))
        except RecordACLError as e:
            return Response({'success': False, 'error': e.message}, status=400)
        return Response({'success': True, 'message': 'تم إزالة القيد'})


# ══════════════════════════════════════════════════════════════
# السياسات الديناميكية (Policies)
# ══════════════════════════════════════════════════════════════

class PolicyViewSet(ViewSet):
    """إدارة السياسات الديناميكية."""
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    @extend_schema(tags=['policies'])
    def list(self, request) -> Response:
        from infra.authorization.services.policy_service import PolicyService
        perm_filter = request.query_params.get('permission_code')
        qs = PolicyService.list_policies(perm_filter)
        return Response({'success': True, 'results': AccessPolicySerializer(qs, many=True).data})

    @extend_schema(tags=['policies'])
    def retrieve(self, request, pk=None) -> Response:
        from infra.authorization.models.policy import AccessPolicy
        try:
            policy = AccessPolicy.objects.get(pk=pk)
        except AccessPolicy.DoesNotExist:
            return Response({'success': False, 'error': 'السياسة غير موجودة'}, status=404)
        return Response({'success': True, 'data': AccessPolicySerializer(policy).data})

    @extend_schema(request=AccessPolicyCreateSerializer, tags=['policies'])
    def create(self, request) -> Response:
        from infra.authorization.services.policy_service import PolicyService, PolicyError
        serializer = AccessPolicyCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        d = serializer.validated_data
        try:
            policy = PolicyService.create_policy(**d, created_by=request.user)
        except PolicyError as e:
            return Response({'success': False, 'error': e.message}, status=400)
        return Response(
            {'success': True, 'data': AccessPolicySerializer(policy).data},
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(tags=['policies'])
    def update(self, request, pk=None) -> Response:
        from infra.authorization.services.policy_service import PolicyService, PolicyError
        try:
            policy = PolicyService.update_policy(int(pk), request.data)
        except PolicyError as e:
            return Response({'success': False, 'error': e.message}, status=400)
        return Response({'success': True, 'data': AccessPolicySerializer(policy).data})

    def partial_update(self, request, pk=None) -> Response:
        return self.update(request, pk)

    def destroy(self, request, pk=None) -> Response:
        from infra.authorization.services.policy_service import PolicyService, PolicyError
        try:
            PolicyService.delete_policy(int(pk))
        except PolicyError as e:
            return Response({'success': False, 'error': e.message}, status=400)
        return Response({'success': True, 'message': 'تم تعطيل السياسة'})


# ══════════════════════════════════════════════════════════════
# صلاحيات الحقول (Field Permissions)
# ══════════════════════════════════════════════════════════════

class FieldPermissionViewSet(ViewSet):
    """إدارة قيود الحقول الحساسة."""
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    @extend_schema(tags=['field-permissions'])
    def list(self, request) -> Response:
        from infra.authorization.models.field_permission import FieldPermission
        module = request.query_params.get('module')
        qs = FieldPermission.objects.filter(is_active=True)
        if module:
            qs = qs.filter(module=module)
        return Response({'success': True, 'results': FieldPermissionSerializer(qs, many=True).data})

    @extend_schema(request=FieldPermissionCreateSerializer, tags=['field-permissions'])
    def create(self, request) -> Response:
        serializer = FieldPermissionCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        fp = serializer.save()
        return Response(
            {'success': True, 'data': FieldPermissionSerializer(fp).data},
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(tags=['field-permissions'])
    def update(self, request, pk=None) -> Response:
        from infra.authorization.models.field_permission import FieldPermission
        try:
            fp = FieldPermission.objects.get(pk=pk)
        except FieldPermission.DoesNotExist:
            return Response({'success': False, 'error': 'غير موجود'}, status=404)
        serializer = FieldPermissionCreateSerializer(fp, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'success': True, 'data': FieldPermissionSerializer(fp).data})

    def destroy(self, request, pk=None) -> Response:
        from infra.authorization.models.field_permission import FieldPermission
        FieldPermission.objects.filter(pk=pk).update(is_active=False)
        return Response({'success': True, 'message': 'تم تعطيل قيد الحقل'})
