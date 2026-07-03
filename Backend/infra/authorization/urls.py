"""
Authorization URLs
═══════════════════
"""
from django.urls import path
from rest_framework.routers import DefaultRouter

from infra.authorization.api.views import RoleViewSet, PermissionViewSet

router = DefaultRouter()
router.register(r'roles', RoleViewSet, basename='auth-role')
router.register(r'permissions', PermissionViewSet, basename='auth-permission')

urlpatterns = router.urls
