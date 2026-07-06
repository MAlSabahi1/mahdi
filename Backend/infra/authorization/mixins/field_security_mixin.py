"""
Field Security Mixin — حماية الحقول الحساسة في Serializers
═══════════════════════════════════════════════════════════════
يُضاف لأي DRF Serializer ليخفي/يعرض الحقول حسب صلاحية المستخدم.

الاستخدام:
    class PersonnelDetailSerializer(FieldSecurityMixin, serializers.ModelSerializer):
        class Meta:
            model = PersonnelMaster
            field_security_module = 'personnel'   # ← اسم النظام الفرعي
            fields = '__all__'

    # الحقول الحساسة تُخفى تلقائياً إذا لم يملك المستخدم صلاحية رؤيتها.

التدفق:
    1. Serializer.to_representation() يُستدعى
    2. FieldSecurityMixin يقرأ FieldPermission لهذا الـ module
    3. لكل حقل حساس: يفحص هل المستخدم يملك view_permission
    4. إذا لا → يحذف الحقل من الاستجابة
"""
import logging

logger = logging.getLogger('authorization.field_security')


class FieldSecurityMixin:
    """
    Mixin يُطبّق Field-Level Security على DRF Serializers.

    متطلبات:
        - Meta.field_security_module = 'personnel' (اسم النظام الفرعي)
        - request في context (يُمرر تلقائياً من ViewSet)
    """

    def to_representation(self, instance):
        """تجاوز to_representation لإخفاء الحقول الحساسة."""
        data = super().to_representation(instance)

        # جلب المستخدم من السياق
        request = self.context.get('request')
        if not request or not hasattr(request, 'user') or not request.user.is_authenticated:
            return data

        user = request.user

        # Superuser يرى كل شيء
        if user.is_superuser:
            return data

        # جلب اسم النظام الفرعي من Meta
        module = getattr(self.Meta, 'field_security_module', None)
        if not module:
            return data

        # جلب الحقول المحجوبة لهذا المستخدم
        hidden_fields = self._get_hidden_fields(user, module)

        # حذف الحقول المحجوبة
        for field_name in hidden_fields:
            data.pop(field_name, None)

        return data

    def _get_hidden_fields(self, user, module: str) -> list:
        """جلب الحقول التي يجب إخفاؤها عن المستخدم."""
        from infra.authorization.models.field_permission import FieldPermission
        from infra.authorization.services.permission_service import PermissionService

        # جلب كل الحقول الحساسة لهذا الـ module
        field_perms = FieldPermission.objects.filter(
            module=module, is_active=True,
        ).values('field_name', 'view_permission')

        hidden = []
        # جلب صلاحيات المستخدم مرة واحدة
        user_perms = PermissionService.get_user_permissions(user)

        for fp in field_perms:
            if fp['view_permission'] not in user_perms:
                hidden.append(fp['field_name'])

        return hidden

    def get_writable_fields(self, user, module: str) -> list:
        """جلب الحقول التي يمكن للمستخدم تعديلها — للـ Frontend."""
        from infra.authorization.models.field_permission import FieldPermission
        from infra.authorization.services.permission_service import PermissionService

        field_perms = FieldPermission.objects.filter(
            module=module, is_active=True,
        ).exclude(edit_permission='').values('field_name', 'edit_permission')

        user_perms = PermissionService.get_user_permissions(user)
        writable = []

        for fp in field_perms:
            if fp['edit_permission'] in user_perms:
                writable.append(fp['field_name'])

        return writable
