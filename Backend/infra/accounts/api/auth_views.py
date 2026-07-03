"""
Auth Views — واجهات API المصادقة
═════════════════════════════════
Views نحيفة — كل business logic في AuthService.

Endpoints:
    POST /auth/login/           — تسجيل الدخول
    POST /auth/logout/          — تسجيل الخروج
    POST /auth/refresh/         — تجديد التوكن
    GET  /auth/me/              — بيانات المستخدم الحالي
    POST /auth/change-password/ — تغيير كلمة المرور
    POST /auth/logout-all/      — الخروج من جميع الأجهزة
"""
import logging
from typing import Optional

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from drf_spectacular.utils import extend_schema

from infra.accounts.serializers.auth_serializers import (
    LoginSerializer,
    LogoutSerializer,
    RefreshTokenSerializer,
    ChangePasswordSerializer,
    AuthResponseSerializer,
)
from infra.accounts.serializers.user_serializers import UserMeSerializer
from infra.accounts.services.auth_service import AuthService, AuthError

logger = logging.getLogger('accounts.views.auth')


class AuthViewSet(ViewSet):
    """
    المصادقة وإدارة الجلسات.
    Views نحيفة — كل الـ logic في AuthService.
    """
    permission_classes = [permissions.AllowAny]
    throttle_scope = 'auth'

    # ── Login ──

    @extend_schema(
        request=LoginSerializer,
        responses={200: AuthResponseSerializer},
        tags=['auth'],
        summary='تسجيل الدخول',
        description='تسجيل الدخول والحصول على Access Token + Refresh Token',
    )
    def login(self, request) -> Response:
        """POST /auth/login/"""
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        ip_address = self._get_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        try:
            result = AuthService.login(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password'],
                ip_address=ip_address,
                user_agent=user_agent,
            )
        except AuthError as e:
            return Response(
                {
                    'success': False,
                    'error': e.message,
                    'code': e.code,
                },
                status=e.status_code,
            )

        return Response({
            'success': True,
            'data': {
                'access_token': result.access_token,
                'refresh_token': result.refresh_token,
                'session_id': result.session_id,
                'expires_in': result.expires_in,
                'is_suspicious': result.is_suspicious,
                'user': UserMeSerializer(result.user, context={'request': request}).data,
            },
        })

    # ── Logout ──

    @extend_schema(
        request=LogoutSerializer,
        tags=['auth'],
        summary='تسجيل الخروج',
        description='إلغاء الجلسة الحالية',
    )
    def logout(self, request) -> Response:
        """POST /auth/logout/"""
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        AuthService.logout(
            user=request.user,
            refresh_token=serializer.validated_data.get('refresh_token', ''),
            session_id=serializer.validated_data.get('session_id', ''),
        )

        return Response({
            'success': True,
            'message': 'تم تسجيل الخروج بنجاح',
        })

    # ── Logout All Devices ──

    @extend_schema(
        tags=['auth'],
        summary='الخروج من جميع الأجهزة',
        description='إلغاء جميع الجلسات النشطة',
    )
    def logout_all(self, request) -> Response:
        """POST /auth/logout-all/"""
        count = AuthService.logout_all_devices(request.user)
        return Response({
            'success': True,
            'message': f'تم تسجيل الخروج من {count} جهاز',
            'data': {'revoked_sessions': count},
        })

    # ── Refresh Token ──

    @extend_schema(
        request=RefreshTokenSerializer,
        responses={200: AuthResponseSerializer},
        tags=['auth'],
        summary='تجديد التوكن',
        description='تجديد Access Token باستخدام Refresh Token (مع Token Rotation)',
    )
    def refresh(self, request) -> Response:
        """POST /auth/refresh/"""
        serializer = RefreshTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        ip_address = self._get_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        try:
            result = AuthService.refresh_token(
                raw_refresh_token=serializer.validated_data['refresh_token'],
                ip_address=ip_address,
                user_agent=user_agent,
            )
        except AuthError as e:
            return Response(
                {
                    'success': False,
                    'error': e.message,
                    'code': e.code,
                },
                status=e.status_code,
            )

        return Response({
            'success': True,
            'data': {
                'access_token': result.access_token,
                'refresh_token': result.refresh_token,
                'session_id': result.session_id,
                'expires_in': result.expires_in,
            },
        })

    # ── Me ──

    @extend_schema(
        responses={200: UserMeSerializer},
        tags=['auth'],
        summary='بيانات المستخدم الحالي',
    )
    def me(self, request) -> Response:
        """GET /auth/me/"""
        serializer = UserMeSerializer(request.user, context={'request': request})
        return Response({
            'success': True,
            'data': serializer.data,
        })

    # ── Update Me ──

    @extend_schema(
        tags=['auth'],
        summary='تحديث بيانات المستخدم الحالي',
    )
    def update_me(self, request) -> Response:
        """PUT/PATCH /auth/me/"""
        from infra.accounts.services.user_service import UserService, UserServiceError
        from infra.accounts.serializers.user_serializers import UserMeSerializer
        
        # We manually extract only supported fields to avoid serializer errors
        # for fields sent by frontend that are not in the User model yet.
        data = {
            'full_name': request.data.get('full_name'),
            'email': request.data.get('email'),
            'phone': request.data.get('phone'),
            'bio': request.data.get('bio'),
            'facebook_link': request.data.get('facebook_link'),
            'x_link': request.data.get('x_link'),
            'linkedin_link': request.data.get('linkedin_link'),
            'instagram_link': request.data.get('instagram_link'),
        }
        
        # Include file if it was uploaded
        if 'profile_picture' in request.FILES:
            data['profile_picture'] = request.FILES['profile_picture']
            
        # Remove None values
        data = {k: v for k, v in data.items() if v is not None}

        try:
            user = UserService.update_user(
                user_id=request.user.id,
                data=data,
                updated_by=request.user,
            )
        except UserServiceError as e:
            return Response(
                {'success': False, 'error': e.message, 'code': e.code},
                status=e.status_code,
            )

        return Response({
            'success': True,
            'data': UserMeSerializer(user, context={'request': request}).data,
            'message': 'تم تحديث البيانات بنجاح',
        })

    # ── Change Password ──

    @extend_schema(
        request=ChangePasswordSerializer,
        tags=['auth'],
        summary='تغيير كلمة المرور',
    )
    def change_password(self, request) -> Response:
        """POST /auth/change-password/"""
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            AuthService.change_password(
                user=request.user,
                old_password=serializer.validated_data['old_password'],
                new_password=serializer.validated_data['new_password'],
            )
        except AuthError as e:
            return Response(
                {
                    'success': False,
                    'error': e.message,
                    'code': e.code,
                },
                status=e.status_code,
            )

        return Response({
            'success': True,
            'message': 'تم تغيير كلمة المرور بنجاح. يرجى تسجيل الدخول مجدداً.',
        })

    # ── Helpers ──

    @staticmethod
    def _get_ip(request) -> str:
        """استخراج IP Address من الطلب."""
        xff = request.META.get('HTTP_X_FORWARDED_FOR')
        if xff:
            return xff.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', '127.0.0.1')

    def get_permissions(self):
        """Login و Refresh لا يحتاجان مصادقة — الباقي يحتاج."""
        if self.action in ('login', 'refresh'):
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
