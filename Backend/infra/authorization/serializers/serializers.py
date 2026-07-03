"""
Authorization Serializers — مسلسلات الصلاحيات والأدوار
"""
from rest_framework import serializers
from infra.authorization.models.permission import Permission
from infra.authorization.models.role import Role
from infra.authorization.models.user_role import UserRole
from infra.authorization.models.user_profile import UserProfile


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'code', 'module', 'action', 'scope', 'label',
                  'category', 'is_active', 'is_system', 'requires_dual_auth']
        read_only_fields = ['code']


class RoleOutputSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()
    users_count = serializers.SerializerMethodField()

    class Meta:
        model = Role
        fields = ['id', 'name', 'code', 'description', 'is_active',
                  'is_system_role', 'priority', 'permissions', 'users_count']

    def get_permissions(self, obj):
        return obj.get_all_permission_codes()

    def get_users_count(self, obj):
        return UserRole.objects.filter(role=obj, is_active=True).count()


class RoleCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    code = serializers.CharField(max_length=50)
    description = serializers.CharField(required=False, default='')
    priority = serializers.IntegerField(required=False, default=0)
    permissions = serializers.ListField(
        child=serializers.CharField(),
        required=False, default=[],
        help_text='قائمة أكواد الصلاحيات',
    )


class RoleUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, required=False)
    description = serializers.CharField(required=False)
    is_active = serializers.BooleanField(required=False)
    priority = serializers.IntegerField(required=False)
    permissions = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        help_text='قائمة أكواد الصلاحيات (يستبدل القائمة الحالية)',
    )


class UserRoleSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source='role.name', read_only=True)
    role_code = serializers.CharField(source='role.code', read_only=True)
    is_effective = serializers.BooleanField(read_only=True)

    class Meta:
        model = UserRole
        fields = ['id', 'role', 'role_name', 'role_code', 'is_active',
                  'is_effective', 'assigned_at', 'expires_at', 'notes']


class AssignRoleSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
    role_id = serializers.IntegerField()
    expires_at = serializers.DateTimeField(required=False, allow_null=True)
    notes = serializers.CharField(required=False, default='')


class UserPermissionsResponseSerializer(serializers.Serializer):
    """استجابة صلاحيات المستخدم — تُرسل للـ Frontend."""
    permissions = serializers.ListField(child=serializers.CharField())
    roles = serializers.ListField(child=serializers.DictField())
