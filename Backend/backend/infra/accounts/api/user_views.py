"""
User Views — واجهات API إدارة المستخدمين
═════════════════════════════════════════════
Views نحيفة — كل business logic في UserService.
للمدير فقط (IsAdminUser).

Endpoints:
    GET    /users/              — قائمة المستخدمين
    POST   /users/              — إنشاء مستخدم
    GET    /users/<id>/         — تفاصيل مستخدم
    PUT    /users/<id>/         — تحديث مستخدم
    DELETE /users/<id>/         — تعطيل مستخدم
    POST   /users/<id>/activate/      — تفعيل مستخدم
    POST   /users/<id>/reset-password/ — إعادة تعيين كلمة المرور
    POST   /users/<id>/unlock/        — فك قفل الحساب
"""
import logging

from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from drf_spectacular.utils import extend_schema, extend_schema_view

from infra.accounts.serializers.user_serializers import (
    UserOutputSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
    UserResetPasswordSerializer,
    UserDetailOutputSerializer,
)
from infra.accounts.services.user_service import UserService, UserServiceError

logger = logging.getLogger('accounts.views.user')


@extend_schema_view(
    list=extend_schema(summary='قائمة المستخدمين', tags=['users']),
    retrieve=extend_schema(summary='تفاصيل مستخدم', tags=['users']),
    create=extend_schema(summary='إنشاء مستخدم', tags=['users']),
    update=extend_schema(summary='تحديث مستخدم', tags=['users']),
    destroy=extend_schema(summary='تعطيل مستخدم', tags=['users']),
)
class UserManagementViewSet(ViewSet):
    """
    إدارة المستخدمين (مدير النظام فقط).
    Views نحيفة — كل الـ logic في UserService.
    """
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    # ── List ──

    def list(self, request) -> Response:
        """GET /users/"""
        search = request.query_params.get('search')
        is_active = request.query_params.get('is_active')

        if is_active is not None:
            is_active = is_active.lower() in ('true', '1', 'yes')

        users = UserService.list_users(
            search=search,
            is_active=is_active,
        )
        serializer = UserOutputSerializer(users, many=True)

        return Response({
            'success': True,
            'count': users.count(),
            'results': serializer.data,
        })

    # ── Retrieve ──

    def retrieve(self, request, pk=None) -> Response:
        """GET /users/<id>/"""
        try:
            detail = UserService.get_user_detail(pk)
        except UserServiceError as e:
            return Response(
                {'success': False, 'error': e.message, 'code': e.code},
                status=e.status_code,
            )

        return Response({
            'success': True,
            'data': {
                'user': UserOutputSerializer(detail['user']).data,
                'security': UserDetailOutputSerializer(detail).data.get('security', {}),
                'active_sessions_count': detail['active_sessions_count'],
            },
        })

    # ── Create ──

    @extend_schema(request=UserCreateSerializer, tags=['users'])
    def create(self, request) -> Response:
        """POST /users/"""
        serializer = UserCreateSerializer(data=request.data)
        if not serializer.is_valid():
            print(f">>>> UserCreateSerializer Errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            role_id = serializer.validated_data.pop('role_id', None)
            
            user = UserService.create_user(
                **serializer.validated_data,
                created_by=request.user,
            )
            
            if role_id:
                from infra.authorization.services.role_service import RoleService
                RoleService.assign_role_to_user(
                    user_id=str(user.id),
                    role_id=role_id,
                    assigned_by=request.user
                )
        except Exception as e:
            # Handling UserServiceError or RoleServiceError generically for now
            msg = getattr(e, 'message', str(e))
            code = getattr(e, 'code', 'error')
            status_code = getattr(e, 'status_code', 400)
            return Response(
                {'success': False, 'error': msg, 'code': code},
                status=status_code,
            )

        return Response(
            {
                'success': True,
                'data': UserOutputSerializer(user).data,
                'message': 'تم إنشاء المستخدم بنجاح',
            },
            status=status.HTTP_201_CREATED,
        )

    # ── Update ──

    @extend_schema(request=UserUpdateSerializer, tags=['users'])
    def update(self, request, pk=None) -> Response:
        """PUT /users/<id>/"""
        serializer = UserUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            # Handle role update separately
            has_role_update = 'role_id' in serializer.validated_data
            role_id = serializer.validated_data.pop('role_id', None)

            user = UserService.update_user(
                user_id=pk,
                data=serializer.validated_data,
                updated_by=request.user,
            )

            # Assign or remove role if it was included in the request
            if has_role_update:
                from infra.authorization.services.role_service import RoleService
                if role_id is not None:
                    RoleService.assign_role_to_user(
                        user_id=str(user.id),
                        role_id=role_id,
                        assigned_by=request.user
                    )
                else:
                    # Remove all roles if role_id is null
                    from infra.authorization.models.user_role import UserRole
                    UserRole.objects.filter(user=user).update(is_active=False)

        except Exception as e:
            msg = getattr(e, 'message', str(e))
            code = getattr(e, 'code', 'error')
            status_code = getattr(e, 'status_code', 400)
            return Response(
                {'success': False, 'error': msg, 'code': code},
                status=status_code,
            )

        return Response({
            'success': True,
            'data': UserOutputSerializer(user).data,
            'message': 'تم تحديث المستخدم بنجاح',
        })

    def partial_update(self, request, pk=None) -> Response:
        """PATCH /users/<id>/"""
        return self.update(request, pk)

    # ── Destroy (Deactivate) ──

    def destroy(self, request, pk=None) -> Response:
        """DELETE /users/<id>/ — يعطّل الحساب ولا يحذفه."""
        try:
            UserService.deactivate_user(
                user_id=pk,
                deactivated_by=request.user,
            )
        except UserServiceError as e:
            return Response(
                {'success': False, 'error': e.message, 'code': e.code},
                status=e.status_code,
            )

        return Response({
            'success': True,
            'message': 'تم تعطيل الحساب بنجاح',
        })

    # ── Custom Actions ──

    @extend_schema(summary='تفعيل حساب مستخدم', tags=['users'])
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None) -> Response:
        """POST /users/<id>/activate/"""
        try:
            UserService.activate_user(
                user_id=pk,
                activated_by=request.user,
            )
        except UserServiceError as e:
            return Response(
                {'success': False, 'error': e.message, 'code': e.code},
                status=e.status_code,
            )

        return Response({
            'success': True,
            'message': 'تم تفعيل الحساب بنجاح',
        })

    @extend_schema(
        request=UserResetPasswordSerializer,
        summary='إعادة تعيين كلمة المرور',
        tags=['users'],
    )
    @action(detail=True, methods=['post'], url_path='reset-password')
    def reset_password(self, request, pk=None) -> Response:
        """POST /users/<id>/reset-password/"""
        serializer = UserResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            UserService.reset_password(
                user_id=pk,
                new_password=serializer.validated_data['new_password'],
                reset_by=request.user,
            )
        except UserServiceError as e:
            return Response(
                {'success': False, 'error': e.message, 'code': e.code},
                status=e.status_code,
            )

        return Response({
            'success': True,
            'message': 'تم إعادة تعيين كلمة المرور. المستخدم سيُطلب منه تغييرها عند الدخول.',
        })

    @extend_schema(summary='فك قفل حساب', tags=['users'])
    @action(detail=True, methods=['post'])
    def unlock(self, request, pk=None) -> Response:
        """POST /users/<id>/unlock/"""
        try:
            UserService.unlock_account(
                user_id=pk,
                unlocked_by=request.user,
            )
        except (UserServiceError, ValueError) as e:
            msg = e.message if hasattr(e, 'message') else str(e)
            return Response(
                {'success': False, 'error': msg},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response({
            'success': True,
            'message': 'تم فك قفل الحساب بنجاح',
        })

    @extend_schema(summary='إنهاء جميع جلسات المستخدم', tags=['users'])
    @action(detail=True, methods=['post'], url_path='terminate-sessions')
    def terminate_sessions(self, request, pk=None) -> Response:
        """POST /users/<id>/terminate-sessions/"""
        from infra.accounts.services.session_service import SessionService
        from django.contrib.auth import get_user_model
        User = get_user_model()
        try:
            target_user = User.objects.get(pk=pk)
            count = SessionService.revoke_all_user_sessions(
                user=target_user,
                reason='admin_terminated'
            )
            return Response({
                'success': True,
                'message': f'تم إنهاء {count} جلسة للمستخدم بنجاح',
            })
        except User.DoesNotExist:
            return Response(
                {'success': False, 'error': 'المستخدم غير موجود'},
                status=status.HTTP_404_NOT_FOUND,
            )

    @extend_schema(summary='تصدير قائمة المستخدمين', tags=['users'])
    @action(detail=False, methods=['get'])
    def export(self, request) -> Response:
        """GET /users/export/"""
        import csv
        from django.http import HttpResponse

        search = request.query_params.get('search')
        is_active = request.query_params.get('is_active')

        if is_active is not None:
            is_active = is_active.lower() in ('true', '1', 'yes')

        users = UserService.list_users(
            search=search,
            is_active=is_active,
        )

        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="users_export.csv"'
        response.write('\ufeff')  # BOM for Excel

        writer = csv.writer(response)
        writer.writerow([
            'ID', 'الاسم الكامل', 'اسم المستخدم', 'البريد الإلكتروني',
            'رقم الهاتف', 'نشط', 'تاريخ الإنشاء', 'آخر دخول',
        ])

        for user in users.iterator(chunk_size=1000):
            writer.writerow([
                user.id,
                user.full_name,
                user.username,
                user.email,
                user.phone,
                'نعم' if user.is_active else 'لا',
                user.created_at.strftime('%Y-%m-%d %H:%M:%S') if user.created_at else '',
                user.last_login.strftime('%Y-%m-%d %H:%M:%S') if user.last_login else '',
            ])

        return response

