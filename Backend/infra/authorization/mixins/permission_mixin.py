"""
Permission Mixin — ViewSet Mixin لفحص الصلاحيات
═══════════════════════════════════════════════════
يُضاف لأي ViewSet ليفحص الصلاحيات تلقائياً.

الاستخدام:
    class PersonnelViewSet(PermissionRequiredMixin, ModelViewSet):
        permission_map = {
            'list': Perms.PERSONNEL_VIEW,
            'create': Perms.PERSONNEL_CREATE,
            'update': Perms.PERSONNEL_EDIT,
            'destroy': Perms.PERSONNEL_DELETE,
        }
"""
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

from infra.authorization.services.permission_service import PermissionService


class ServicePermission(permissions.BasePermission):
    """
    DRF Permission Class — يستخدم PermissionService.
    يُوضع في permission_classes لأي View.
    """

    def has_permission(self, request, view) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False

        # جلب الصلاحية المطلوبة من View
        required = getattr(view, 'required_permission', None)
        if required is None:
            # فحص permission_map
            permission_map = getattr(view, 'permission_map', {})
            action = getattr(view, 'action', None)
            required = permission_map.get(action)

        if required is None:
            return True  # لا صلاحية مطلوبة

        return PermissionService.has_permission(request.user, required)

    def has_object_permission(self, request, view, obj) -> bool:
        """فحص نطاق البيانات (ABAC) على مستوى الكائن."""
        required = getattr(view, 'required_permission', None)
        if required is None:
            permission_map = getattr(view, 'permission_map', {})
            action = getattr(view, 'action', None)
            required = permission_map.get(action)

        if required is None:
            return True

        return PermissionService.check_data_scope(request.user, required, obj)


class PermissionRequiredMixin:
    """
    ViewSet Mixin — يفحص الصلاحيات حسب الـ action.

    الاستخدام:
        class MyViewSet(PermissionRequiredMixin, ModelViewSet):
            permission_map = {
                'list': 'personnel.view.all',
                'create': 'personnel.create.all',
            }
    """
    permission_map: dict = {}
    permission_classes = [permissions.IsAuthenticated, ServicePermission]

    def get_queryset(self):
        """فلترة تلقائية حسب Data Scope."""
        qs = super().get_queryset()
        action = getattr(self, 'action', None)
        perm_code = self.permission_map.get(action)

        if perm_code and hasattr(self, 'request'):
            qs = PermissionService.get_scoped_queryset(
                self.request.user, qs, perm_code
            )
        return qs
