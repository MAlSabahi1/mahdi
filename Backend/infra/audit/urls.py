"""Audit URLs."""
from rest_framework.routers import DefaultRouter
from infra.audit.api.views import AuditLogViewSet, LoginAuditViewSet

router = DefaultRouter()
router.register(r'audit/logs', AuditLogViewSet, basename='audit-log')
router.register(r'audit/logins', LoginAuditViewSet, basename='audit-login')

urlpatterns = router.urls
