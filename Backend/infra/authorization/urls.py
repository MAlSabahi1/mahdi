"""
Authorization URLs — كل مسارات API الصلاحيات
═══════════════════════════════════════════════
مسارات جاهزة لمطور الـ Frontend:

    /api/v1/authorization/roles/                — إدارة الأدوار
    /api/v1/authorization/permissions/          — الصلاحيات + المجموعة
    /api/v1/authorization/permission-groups/    — مجموعات الصلاحيات
    /api/v1/authorization/delegations/          — التفويضات
    /api/v1/authorization/emergency-access/     — الوصول الطارئ
    /api/v1/authorization/record-acl/           — قيود السجلات
    /api/v1/authorization/policies/             — السياسات الديناميكية
    /api/v1/authorization/field-permissions/    — صلاحيات الحقول
"""
from rest_framework.routers import DefaultRouter

from infra.authorization.api.views import (
    RoleViewSet, PermissionViewSet, PermissionGroupViewSet,
    DelegationViewSet, EmergencyAccessViewSet,
    RecordACLViewSet, PolicyViewSet, FieldPermissionViewSet,
)

router = DefaultRouter()
router.register(r'roles', RoleViewSet, basename='auth-role')
router.register(r'permissions', PermissionViewSet, basename='auth-permission')
router.register(r'permission-groups', PermissionGroupViewSet, basename='auth-perm-group')
router.register(r'delegations', DelegationViewSet, basename='auth-delegation')
router.register(r'emergency-access', EmergencyAccessViewSet, basename='auth-emergency')
router.register(r'record-acl', RecordACLViewSet, basename='auth-record-acl')
router.register(r'policies', PolicyViewSet, basename='auth-policy')
router.register(r'field-permissions', FieldPermissionViewSet, basename='auth-field-perm')

urlpatterns = router.urls

