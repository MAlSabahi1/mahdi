"""
Field Permission Mixin — إخفاء الحقول ديناميكياً
══════════════════════════════════════════════════════
المستوى 5 من الصلاحيات — يُخفي حقول حسب صلاحيات المستخدم.

الاستخدام:
    class PersonnelSerializer(FieldPermissionMixin, ModelSerializer):
        class Meta:
            model = Personnel
            fields = '__all__'
            field_permissions = {
                'salary': 'personnel.view_salary.all',
                'military_number': 'personnel.view_military_number.all',
            }
"""
from infra.authorization.services.permission_service import PermissionService


class FieldPermissionMixin:
    """
    Serializer Mixin — يُخفي الحقول ديناميكياً.

    كيف يعمل:
        1. الـ Serializer يعرّف field_permissions في Meta
        2. عند to_representation — يفحص كل حقل
        3. إذا المستخدم لا يملك الصلاحية → الحقل لا يظهر

    مثال:
        يمكنه رؤية الاسم ← لكن لا يرى الراتب
    """

    def get_fields(self):
        """تصفية الحقول حسب الصلاحيات."""
        fields = super().get_fields()

        request = self.context.get('request')
        if not request or not hasattr(request, 'user'):
            return fields

        user = request.user
        if not user or not user.is_authenticated or user.is_superuser:
            return fields

        field_permissions = getattr(self.Meta, 'field_permissions', {})
        if not field_permissions:
            return fields

        # حذف الحقول غير المسموحة
        for field_name, perm_code in field_permissions.items():
            if field_name in fields:
                if not PermissionService.has_permission(user, perm_code):
                    del fields[field_name]

        return fields

    def to_representation(self, instance):
        """
        طبقة حماية إضافية — حتى لو get_fields لم تعمل.
        يحذف الحقول من الـ output النهائي.
        """
        data = super().to_representation(instance)

        request = self.context.get('request')
        if not request or not hasattr(request, 'user'):
            return data

        user = request.user
        if not user or not user.is_authenticated or user.is_superuser:
            return data

        field_permissions = getattr(self.Meta, 'field_permissions', {})
        for field_name, perm_code in field_permissions.items():
            if field_name in data:
                if not PermissionService.has_permission(user, perm_code):
                    del data[field_name]

        return data
