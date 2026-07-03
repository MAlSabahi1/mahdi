"""
Security URLs — مسارات API الأمان
═══════════════════════════════════
ملاحظة: Auth + Users + Sessions انتقلت إلى accounts app.
هنا يبقى: Dual Auth, Telemetry, Roles, Audit, Settings.
"""
from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'roles', views.RoleViewSet, basename='role')
router.register(r'audit-logs', views.AuditLogViewSet, basename='audit-log')
router.register(r'settings', views.SystemSettingViewSet, basename='system-setting')

urlpatterns = [
    # Dual Auth (Four-Eyes Principle)
    path('dual-auth/', views.DualAuthViewSet.as_view({'get': 'list', 'post': 'create'}), name='dual-auth-list'),
    path('dual-auth/<uuid:pk>/', views.DualAuthViewSet.as_view({'get': 'retrieve'}), name='dual-auth-detail'),
    path('dual-auth/<uuid:pk>/approve/', views.DualAuthViewSet.as_view({'post': 'approve'}), name='dual-auth-approve'),
    path('dual-auth/<uuid:pk>/reject/', views.DualAuthViewSet.as_view({'post': 'reject'}), name='dual-auth-reject'),
    
    # Telemetry
    path('telemetry/dashboard/', views.TelemetryViewSet.as_view({'get': 'dashboard'}), name='telemetry-dashboard'),
    path('telemetry/collect/', views.TelemetryViewSet.as_view({'post': 'collect'}), name='telemetry-collect'),
    path('telemetry/login-failures/', views.TelemetryViewSet.as_view({'get': 'login_failures'}), name='telemetry-login-failures'),
    path('telemetry/active-sessions/', views.TelemetryViewSet.as_view({'get': 'active_sessions'}), name='telemetry-active-sessions'),
    path('telemetry/slow-queries/', views.TelemetryViewSet.as_view({'get': 'slow_queries'}), name='telemetry-slow-queries'),
    path('telemetry/celery-queue-length/', views.TelemetryViewSet.as_view({'get': 'celery_queue_length'}), name='telemetry-celery-queue'),
    path('telemetry/database-connections/', views.TelemetryViewSet.as_view({'get': 'database_connections'}), name='telemetry-db-connections'),
]

urlpatterns += router.urls

