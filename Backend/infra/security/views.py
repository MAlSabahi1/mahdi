"""
Security Views - واجهات API الأمان والمصادقة والإدارة
المرحلة 4: Auth (JWT), Users, Roles, DualAuth, Audit, Telemetry
"""
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth import get_user_model
from django.db import connection
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter

from .serializers import (
    CustomTokenObtainPairSerializer, UserInfoSerializer,
    ChangePasswordSerializer, UserProfileSerializer,
    UserCreateSerializer, UserUpdateSerializer,
    RoleSerializer, RoleCreateSerializer,
    AvailablePermissionsSerializer,
    DualAuthRequestSerializer, DualAuthCreateSerializer,
    DualAuthApproveSerializer, DualAuthRejectSerializer,
    AuditLogSerializer, AuditLogVerifySerializer,
    SystemSettingSerializer, TelemetryDashboardSerializer,
)
from .models import (
    Role, UserProfile, DualAuthorizationRequest,
    SystemSetting, SYSTEM_PERMISSIONS,
)
from .permissions import (
    ABACPermission, IsAdminPermission,
    has_permission as check_perm,
)
from .dual_auth_service import DualAuthorizationService, DualAuthError
from .telemetry_service import TelemetryService
from .idempotency import IdempotencyMixin
from .audit_signing import verify_all_signatures
from infra.audit.models import AuditLog
from core.base_views import BaseModelViewSet, BaseReadOnlyViewSet, BaseViewSet

User = get_user_model()


# ============================================================================
# Authentication ViewSet (المهمة 4.1.1)
# ============================================================================

class AuthViewSet(BaseViewSet):
    """
    المصادقة وإدارة الجلسات
    
    - POST /auth/login/ - تسجيل الدخول (JWT)
    - POST /auth/logout/ - تسجيل الخروج
    - POST /auth/refresh/ - تجديد التوكن
    - GET /auth/me/ - بيانات المستخدم الحالي
    - POST /auth/change-password/ - تغيير كلمة المرور
    """
    permission_classes = [permissions.AllowAny]
    throttle_scope = 'auth'
    
    @extend_schema(
        request=CustomTokenObtainPairSerializer,
        responses={200: {'type': 'object'}},
        tags=['auth'],
        summary='تسجيل الدخول',
    )
    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = CustomTokenObtainPairSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response(
                {'success': False, 'error': str(e)},
                status=status.HTTP_401_UNAUTHORIZED
            )
        return Response({
            'success': True,
            **serializer.validated_data,
        })
    
    @extend_schema(
        request={'type': 'object', 'properties': {'refresh': {'type': 'string'}}},
        tags=['auth'],
        summary='تسجيل الخروج',
    )
    @action(detail=False, methods=['post'],
            permission_classes=[permissions.IsAuthenticated])
    def logout(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
        except TokenError:
            pass
        
        # تسجيل في AuditLog
        AuditLog.objects.create(
            user=request.user,
            action='LOGOUT',
            model_name='accounts.User',
            object_id=str(request.user.pk),
            ip_address=self._get_ip(request),
        )
        
        return Response({'success': True, 'detail': 'تم تسجيل الخروج'})
    
    @extend_schema(
        tags=['auth'],
        summary='بيانات المستخدم الحالي',
        responses={200: UserInfoSerializer},
    )
    @action(detail=False, methods=['get'],
            permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        serializer = UserInfoSerializer(request.user)
        return Response({'success': True, 'data': serializer.data})
    
    @extend_schema(
        request=ChangePasswordSerializer,
        tags=['auth'],
        summary='تغيير كلمة المرور',
    )
    @action(detail=False, methods=['post'], url_path='change-password',
            permission_classes=[permissions.IsAuthenticated])
    def change_password(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        
        AuditLog.objects.create(
            user=request.user,
            action='UPDATE',
            model_name='accounts.User',
            object_id=str(request.user.pk),
            new_data={'action': 'password_changed'},
            ip_address=self._get_ip(request),
        )
        
        return Response({'success': True, 'detail': 'تم تغيير كلمة المرور'})
    
    def _get_ip(self, request):
        xff = request.META.get('HTTP_X_FORWARDED_FOR')
        if xff:
            return xff.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')


# ============================================================================
# User Management ViewSet (المهمة 4.1.2)
# ============================================================================

@extend_schema_view(
    list=extend_schema(summary='قائمة المستخدمين', tags=['users']),
    retrieve=extend_schema(summary='تفاصيل مستخدم', tags=['users']),
    create=extend_schema(summary='إنشاء مستخدم', tags=['users']),
    update=extend_schema(summary='تحديث مستخدم', tags=['users']),
    destroy=extend_schema(summary='تعطيل مستخدم', tags=['users']),
)
class UserManagementViewSet(IdempotencyMixin, BaseViewSet):
    """إدارة المستخدمين (مدير النظام فقط)"""
    permission_classes = [permissions.IsAuthenticated, IsAdminPermission]
    idempotent_actions = ['create', 'update']
    
    def list(self, request):
        profiles = UserProfile.objects.select_related(
            'user', 'role', 'directorate'
        ).all()
        
        # فلترة حسب الدور
        role_id = request.query_params.get('role_id')
        if role_id:
            profiles = profiles.filter(role_id=role_id)
        
        # فلترة حسب الإدارة
        dir_id = request.query_params.get('directorate_id')
        if dir_id:
            profiles = profiles.filter(directorate_id=dir_id)
        
        # بحث
        search = request.query_params.get('search')
        if search:
            profiles = profiles.filter(
                user__username__icontains=search
            ) | profiles.filter(
                user__first_name__icontains=search
            )
        
        serializer = UserProfileSerializer(profiles, many=True)
        return Response({
            'success': True,
            'count': profiles.count(),
            'data': serializer.data,
        })
    
    def retrieve(self, request, pk=None):
        try:
            profile = UserProfile.objects.select_related(
                'user', 'role', 'directorate'
            ).get(user__pk=pk)
        except UserProfile.DoesNotExist:
            return Response(
                {'success': False, 'error': 'المستخدم غير موجود'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = UserProfileSerializer(profile)
        return Response({'success': True, 'data': serializer.data})
    
    def create(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        AuditLog.objects.create(
            user=request.user,
            action='CREATE',
            model_name='accounts.User',
            object_id=str(user.pk),
            new_data={'username': user.username},
            ip_address=self._get_ip(request),
        )
        
        profile_serializer = UserProfileSerializer(user.profile)
        return Response(
            {'success': True, 'data': profile_serializer.data},
            status=status.HTTP_201_CREATED
        )
    
    def update(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(
                {'success': False, 'error': 'المستخدم غير موجود'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = UserUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(user, serializer.validated_data)
        
        AuditLog.objects.create(
            user=request.user,
            action='UPDATE',
            model_name='accounts.User',
            object_id=str(user.pk),
            new_data=serializer.validated_data,
            ip_address=self._get_ip(request),
        )
        
        profile_serializer = UserProfileSerializer(user.profile)
        return Response({'success': True, 'data': profile_serializer.data})
    
    def destroy(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(
                {'success': False, 'error': 'المستخدم غير موجود'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Four-Eyes لمدير النظام
        try:
            if user.profile.role.code == 'super_admin':
                service = DualAuthorizationService(request.user)
                req = service.create_request(
                    action_type='MODIFY_SUPER_ADMIN',
                    target_object_type='User',
                    target_object_id=str(user.pk),
                    reason=request.data.get('reason', 'تعطيل حساب مدير'),
                )
                return Response({
                    'success': True,
                    'requires_dual_auth': True,
                    'dual_auth_request_id': str(req.pk),
                    'message': 'تم إنشاء طلب تفويض مزدوج - بانتظار الموافقة',
                })
        except Exception:
            pass
        
        # تعطيل الحساب
        user.is_active = False
        user.save()
        
        AuditLog.objects.create(
            user=request.user,
            action='DELETE',
            model_name='accounts.User',
            object_id=str(user.pk),
            new_data={'action': 'deactivated'},
            ip_address=self._get_ip(request),
        )
        
        return Response({'success': True, 'detail': 'تم تعطيل الحساب'})
    
    def _get_ip(self, request):
        xff = request.META.get('HTTP_X_FORWARDED_FOR')
        return xff.split(',')[0].strip() if xff else request.META.get('REMOTE_ADDR')


# ============================================================================
# Role ViewSet
# ============================================================================

@extend_schema_view(
    list=extend_schema(summary='قائمة الأدوار', tags=['roles']),
    retrieve=extend_schema(summary='تفاصيل دور', tags=['roles']),
    create=extend_schema(summary='إنشاء دور', tags=['roles']),
    update=extend_schema(summary='تعديل دور', tags=['roles']),
    destroy=extend_schema(summary='حذف دور', tags=['roles']),
)
class RoleViewSet(BaseModelViewSet):
    """إدارة الأدوار (مدير النظام فقط)"""
    permission_classes = [permissions.IsAuthenticated, IsAdminPermission]
    serializer_class = RoleSerializer
    queryset = Role.objects.all()
    idempotent_actions = ['create', 'update']
    
    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return RoleCreateSerializer
        return RoleSerializer
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        role = self.get_object()
        if role.is_system_role:
            return Response(
                {'success': False, 'error': 'لا يمكن حذف دور نظامي'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if role.users.exists():
            return Response(
                {'success': False, 'error': 'لا يمكن حذف دور مستخدم من قبل مستخدمين'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)
    
    @extend_schema(summary='قائمة الصلاحيات المتاحة', tags=['roles'])
    @action(detail=False, methods=['get'], url_path='available-permissions')
    def available_permissions(self, request):
        data = [
            {'code': p[0], 'name': p[1]} for p in SYSTEM_PERMISSIONS
        ]
        return Response({'success': True, 'data': data})


# ============================================================================
# Dual Authorization ViewSet (المهمة 4.8)
# ============================================================================

@extend_schema_view(
    list=extend_schema(summary='طلبات التفويض المعلقة', tags=['dual-auth']),
    retrieve=extend_schema(summary='تفاصيل طلب تفويض', tags=['dual-auth']),
)
class DualAuthViewSet(IdempotencyMixin, BaseViewSet):
    """إدارة التفويض المزدوج"""
    permission_classes = [permissions.IsAuthenticated]
    idempotent_actions = ['approve', 'reject']
    
    def list(self, request):
        requests = DualAuthorizationService.get_pending_requests(request.user)
        serializer = DualAuthRequestSerializer(requests, many=True)
        return Response({
            'success': True,
            'count': requests.count(),
            'data': serializer.data,
        })
    
    def retrieve(self, request, pk=None):
        try:
            req = DualAuthorizationRequest.objects.get(pk=pk)
        except DualAuthorizationRequest.DoesNotExist:
            return Response(
                {'success': False, 'error': 'الطلب غير موجود'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = DualAuthRequestSerializer(req)
        return Response({'success': True, 'data': serializer.data})
    
    @extend_schema(
        request=DualAuthCreateSerializer,
        summary='إنشاء طلب تفويض مزدوج',
        tags=['dual-auth'],
    )
    def create(self, request):
        serializer = DualAuthCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            service = DualAuthorizationService(request.user)
            req = service.create_request(**serializer.validated_data)
            return Response(
                {
                    'success': True,
                    'data': DualAuthRequestSerializer(req).data,
                },
                status=status.HTTP_201_CREATED
            )
        except DualAuthError as e:
            return Response(
                {'success': False, 'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @extend_schema(summary='الموافقة على طلب تفويض', tags=['dual-auth'])
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        try:
            service = DualAuthorizationService(request.user)
            result = service.approve_request(pk)
            return Response({'success': True, 'data': result})
        except DualAuthError as e:
            return Response(
                {'success': False, 'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @extend_schema(
        request=DualAuthRejectSerializer,
        summary='رفض طلب تفويض',
        tags=['dual-auth'],
    )
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        serializer = DualAuthRejectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            service = DualAuthorizationService(request.user)
            result = service.reject_request(
                pk, reason=serializer.validated_data['reason']
            )
            return Response({'success': True, 'data': result})
        except DualAuthError as e:
            return Response(
                {'success': False, 'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


# ============================================================================
# Audit Log ViewSet (المهمة 4.7)
# ============================================================================

@extend_schema_view(
    list=extend_schema(summary='سجلات التدقيق', tags=['audit']),
    retrieve=extend_schema(summary='تفاصيل سجل تدقيق', tags=['audit']),
)
class AuditLogViewSet(BaseReadOnlyViewSet):
    """عرض سجلات التدقيق (عرض فقط)"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AuditLogSerializer
    queryset = AuditLog.objects.select_related('user').all()
    filterset_fields = ['action', 'model_name', 'user']
    search_fields = ['object_id', 'user__username']
    ordering_fields = ['timestamp', 'action']
    
    def get_queryset(self):
        qs = super().get_queryset()
        
        # فلترة بالتاريخ
        from_date = self.request.query_params.get('from_date')
        to_date = self.request.query_params.get('to_date')
        if from_date:
            qs = qs.filter(timestamp__date__gte=from_date)
        if to_date:
            qs = qs.filter(timestamp__date__lte=to_date)
        
        return qs
    
    @extend_schema(summary='التحقق من توقيع سجل', tags=['audit'])
    @action(detail=True, methods=['get'])
    def verify(self, request, pk=None):
        log = self.get_object()
        is_valid = log.verify()
        return Response({
            'success': True,
            'data': {
                'valid': is_valid,
                'message': 'التوقيع صحيح' if is_valid else 'تحذير: التوقيع غير صحيح!',
            }
        })
    
    @extend_schema(summary='فحص جميع التوقيعات', tags=['audit'])
    @action(detail=False, methods=['get'], url_path='verify-all')
    def verify_all(self, request):
        if not check_perm(request.user, 'verify_audit_signatures'):
            return Response(
                {'success': False, 'error': 'ليس لديك صلاحية'},
                status=status.HTTP_403_FORBIDDEN
            )
        result = verify_all_signatures()
        return Response({'success': True, 'data': result})
    
    @extend_schema(summary='تصدير سجلات التدقيق (CSV)', tags=['audit'])
    @action(detail=False, methods=['get'])
    def export(self, request):
        """تصدير سجلات التدقيق كملف CSV"""
        if not check_perm(request.user, 'view_audit_log'):
            return Response(
                {'success': False, 'error': 'ليس لديك صلاحية'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        import csv
        from django.http import HttpResponse
        
        qs = self.get_queryset()
        
        from_date = request.query_params.get('from_date')
        to_date = request.query_params.get('to_date')
        if from_date:
            qs = qs.filter(timestamp__date__gte=from_date)
        if to_date:
            qs = qs.filter(timestamp__date__lte=to_date)
        
        response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
        response['Content-Disposition'] = 'attachment; filename="audit_logs.csv"'
        
        # BOM for Excel UTF-8
        response.write('\ufeff')
        
        writer = csv.writer(response)
        writer.writerow([
            'ID', 'المستخدم', 'الإجراء', 'النموذج',
            'معرف الكائن', 'IP', 'التوقيت', 'صحة التوقيع'
        ])
        
        for log in qs[:5000]:
            writer.writerow([
                log.pk,
                log.user.username if log.user else '',
                log.get_action_display(),
                log.model_name,
                log.object_id,
                log.ip_address or '',
                log.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'صحيح' if log.verify() else 'غير صحيح',
            ])
        
        return response


# ============================================================================
# System Settings ViewSet
# ============================================================================

class SystemSettingViewSet(BaseModelViewSet):
    """إدارة إعدادات النظام"""
    permission_classes = [permissions.IsAuthenticated, IsAdminPermission]
    serializer_class = SystemSettingSerializer
    queryset = SystemSetting.objects.all()
    filterset_fields = ['category']
    
    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


# ============================================================================
# Telemetry ViewSet (المهمة 4.9)
# ============================================================================

class TelemetryViewSet(BaseViewSet):
    """لوحة المراقبة الأمنية (مدير فقط)"""
    permission_classes = [permissions.IsAuthenticated, IsAdminPermission]
    
    @extend_schema(summary='لوحة المراقبة الكاملة', tags=['telemetry'])
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        service = TelemetryService()
        data = service.get_dashboard_data()
        return Response({'success': True, 'data': data})
    
    @extend_schema(summary='تجميع إحصائيات جديدة', tags=['telemetry'])
    @action(detail=False, methods=['post'])
    def collect(self, request):
        service = TelemetryService()
        metrics = service.collect_all_metrics()
        return Response({'success': True, 'data': metrics})
    
    @extend_schema(summary='خريطة محاولات الدخول الفاشلة', tags=['telemetry'])
    @action(detail=False, methods=['get'], url_path='login-failures')
    def login_failures(self, request):
        service = TelemetryService()
        data = service._collect_login_failures()
        return Response({'success': True, 'data': data})
    
    @extend_schema(summary='الجلسات النشطة', tags=['telemetry'])
    @action(detail=False, methods=['get'], url_path='active-sessions')
    def active_sessions(self, request):
        service = TelemetryService()
        data = service._collect_active_sessions()
        return Response({'success': True, 'data': data})
    
    @extend_schema(summary='أبطأ الاستعلامات', tags=['telemetry'])
    @action(detail=False, methods=['get'], url_path='slow-queries')
    def slow_queries(self, request):
        """عرض أبطأ الاستعلامات في قاعدة البيانات"""
        from django.db import connection
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT query, calls, mean_exec_time, total_exec_time
                    FROM pg_stat_statements
                    ORDER BY mean_exec_time DESC
                    LIMIT 10
                """)
                columns = [col[0] for col in cursor.description]
                rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
        except Exception:
            rows = [{'message': 'pg_stat_statements غير مفعّل'}]
        
        return Response({'success': True, 'data': rows})
    
    @extend_schema(summary='طول طابور Celery', tags=['telemetry'])
    @action(detail=False, methods=['get'], url_path='celery-queue-length')
    def celery_queue_length(self, request):
        """عرض طول طابور مهام Celery"""
        try:
            from django.core.cache import cache
            import redis
            r = cache.client.get_client()
            queue_length = r.llen('celery')
        except Exception:
            queue_length = -1  # Redis غير متوفر
        
        return Response({
            'success': True,
            'data': {'queue_length': queue_length}
        })
    
    @extend_schema(summary='اتصالات قاعدة البيانات', tags=['telemetry'])
    @action(detail=False, methods=['get'], url_path='database-connections')
    def database_connections(self, request):
        """عرض إحصائيات اتصالات قاعدة البيانات"""
        from django.db import connection
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT
                        count(*) as total,
                        count(*) FILTER (WHERE state = 'active') as active,
                        count(*) FILTER (WHERE state = 'idle') as idle,
                        count(*) FILTER (WHERE state = 'idle in transaction') as idle_in_tx
                    FROM pg_stat_activity
                    WHERE datname = current_database()
                """)
                row = cursor.fetchone()
                data = {
                    'total': row[0],
                    'active': row[1],
                    'idle': row[2],
                    'idle_in_transaction': row[3],
                }
        except Exception as e:
            data = {'error': str(e)}
        
        return Response({'success': True, 'data': data})
