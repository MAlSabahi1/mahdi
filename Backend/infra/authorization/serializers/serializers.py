"""
Authorization Serializers — مسلسلات كل طبقات الصلاحيات
═══════════════════════════════════════════════════════════
تغطي: الأدوار، الصلاحيات، المجموعات، التفويضات، الطوارئ،
      قيود السجلات، السياسات، حماية الحقول.

كل Serializer جاهز للـ Frontend مباشرة.
"""
from rest_framework import serializers

from infra.authorization.models.permission import Permission
from infra.authorization.models.permission_group import PermissionGroup
from infra.authorization.models.role import Role
from infra.authorization.models.user_role import UserRole
from infra.authorization.models.field_permission import FieldPermission
from infra.authorization.models.record_acl import RecordACL
from infra.authorization.models.policy import AccessPolicy
from infra.authorization.models.delegation import Delegation
from infra.authorization.models.emergency_access import EmergencyAccess


# ══════════════════════════════════════════════════════════════
# الطبقة 1-2: الصلاحيات والأدوار
# ══════════════════════════════════════════════════════════════

class PermissionSerializer(serializers.ModelSerializer):
    group_name = serializers.CharField(source='group.name', read_only=True, default=None)

    class Meta:
        model = Permission
        fields = [
            'id', 'code', 'module', 'action', 'scope', 'label',
            'category', 'is_active', 'is_system', 'requires_dual_auth',
            'group', 'group_name',
        ]
        read_only_fields = ['code']


class RoleOutputSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()
    users_count = serializers.SerializerMethodField()

    class Meta:
        model = Role
        fields = [
            'id', 'name', 'code', 'description', 'is_active',
            'is_system_role', 'priority', 'permissions', 'users_count',
        ]

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
        fields = [
            'id', 'role', 'role_name', 'role_code', 'is_active',
            'is_effective', 'assigned_at', 'expires_at', 'notes',
        ]


class AssignRoleSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
    role_id = serializers.IntegerField()
    expires_at = serializers.DateTimeField(required=False, allow_null=True)
    notes = serializers.CharField(required=False, default='')


class UserPermissionsResponseSerializer(serializers.Serializer):
    """استجابة صلاحيات المستخدم — تُرسل للـ Frontend."""
    permissions = serializers.ListField(child=serializers.CharField())
    roles = serializers.ListField(child=serializers.DictField())
    delegations = serializers.ListField(child=serializers.DictField(), required=False)
    field_security = serializers.DictField(required=False)


# ══════════════════════════════════════════════════════════════
# الطبقة 3: مجموعات الصلاحيات
# ══════════════════════════════════════════════════════════════

class PermissionGroupSerializer(serializers.ModelSerializer):
    permissions_count = serializers.SerializerMethodField()

    class Meta:
        model = PermissionGroup
        fields = [
            'id', 'code', 'name', 'description', 'icon',
            'display_order', 'is_active', 'permissions_count',
        ]

    def get_permissions_count(self, obj):
        return obj.permissions.filter(is_active=True).count()


class PermissionGroupCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermissionGroup
        fields = ['code', 'name', 'description', 'icon', 'display_order']


class GroupedPermissionsSerializer(serializers.Serializer):
    """الصلاحيات مُجمَّعة حسب المجموعة — للعرض في Admin UI."""
    group = PermissionGroupSerializer()
    permissions = PermissionSerializer(many=True)


# ══════════════════════════════════════════════════════════════
# الطبقة 5: Record-Level Security
# ══════════════════════════════════════════════════════════════

class RecordACLSerializer(serializers.ModelSerializer):
    content_type_name = serializers.CharField(
        source='content_type.model', read_only=True,
    )
    target_user_name = serializers.CharField(
        source='target_user.username', read_only=True, default=None,
    )
    target_role_name = serializers.CharField(
        source='target_role.name', read_only=True, default=None,
    )
    created_by_name = serializers.CharField(
        source='created_by.username', read_only=True, default=None,
    )
    is_effective = serializers.BooleanField(read_only=True)

    class Meta:
        model = RecordACL
        fields = [
            'id', 'content_type', 'content_type_name', 'object_id',
            'target_user', 'target_user_name',
            'target_role', 'target_role_name',
            'access_type', 'permission_code', 'reason',
            'created_by', 'created_by_name',
            'expires_at', 'is_active', 'is_effective',
            'created_at',
        ]
        read_only_fields = ['created_by', 'created_at']


class RecordACLCreateSerializer(serializers.Serializer):
    content_type_model = serializers.CharField(
        help_text='اسم النموذج: personnelmaster, document',
    )
    object_id = serializers.CharField()
    target_user_id = serializers.UUIDField(required=False, allow_null=True)
    target_role_id = serializers.IntegerField(required=False, allow_null=True)
    access_type = serializers.ChoiceField(choices=['allow', 'deny'], default='deny')
    permission_code = serializers.CharField(required=False, default='')
    reason = serializers.CharField()
    expires_at = serializers.DateTimeField(required=False, allow_null=True)


# ══════════════════════════════════════════════════════════════
# الطبقة 6: Field-Level Security
# ══════════════════════════════════════════════════════════════

class FieldPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldPermission
        fields = [
            'id', 'module', 'field_name', 'label',
            'view_permission', 'edit_permission',
            'is_sensitive', 'is_active',
        ]


class FieldPermissionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldPermission
        fields = [
            'module', 'field_name', 'label',
            'view_permission', 'edit_permission',
            'is_sensitive',
        ]


# ══════════════════════════════════════════════════════════════
# الطبقة 8: Dynamic Policies
# ══════════════════════════════════════════════════════════════

class AccessPolicySerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(
        source='created_by.username', read_only=True, default=None,
    )

    class Meta:
        model = AccessPolicy
        fields = [
            'id', 'name', 'code', 'description',
            'permission_code', 'model_name',
            'conditions', 'effect', 'priority',
            'is_active', 'created_by', 'created_by_name',
            'created_at',
        ]
        read_only_fields = ['created_by', 'created_at']


class AccessPolicyCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    code = serializers.CharField(max_length=100)
    description = serializers.CharField(required=False, default='')
    permission_code = serializers.CharField(max_length=100)
    model_name = serializers.CharField(required=False, default='')
    conditions = serializers.ListField(child=serializers.DictField())
    effect = serializers.ChoiceField(choices=['allow', 'deny'], default='allow')
    priority = serializers.IntegerField(required=False, default=0)


# ══════════════════════════════════════════════════════════════
# الطبقة 11: Delegation
# ══════════════════════════════════════════════════════════════

class DelegationSerializer(serializers.ModelSerializer):
    delegator_name = serializers.SerializerMethodField()
    delegate_name = serializers.SerializerMethodField()
    role_name = serializers.CharField(source='role.name', read_only=True, default=None)
    is_effective = serializers.BooleanField(read_only=True)
    permission_codes = serializers.SerializerMethodField()

    class Meta:
        model = Delegation
        fields = [
            'id', 'delegator', 'delegator_name',
            'delegate', 'delegate_name',
            'role', 'role_name', 'permission_codes',
            'reason', 'starts_at', 'ends_at',
            'status', 'approved_by',
            'revoked_at', 'revoked_by', 'notes',
            'is_effective', 'created_at',
        ]
        read_only_fields = [
            'delegator', 'status', 'approved_by',
            'revoked_at', 'revoked_by', 'created_at',
        ]

    def get_delegator_name(self, obj):
        return obj.delegator.get_full_name() or obj.delegator.username

    def get_delegate_name(self, obj):
        return obj.delegate.get_full_name() or obj.delegate.username

    def get_permission_codes(self, obj):
        return obj.get_delegated_permission_codes()


class DelegationCreateSerializer(serializers.Serializer):
    delegate_id = serializers.UUIDField(help_text='معرف المُفوَّض إليه')
    reason = serializers.CharField(help_text='سبب التفويض')
    starts_at = serializers.DateTimeField(required=False, allow_null=True)
    ends_at = serializers.DateTimeField(help_text='تاريخ الانتهاء (إلزامي)')
    role_id = serializers.IntegerField(
        required=False, allow_null=True,
        help_text='الدور المُفوَّض (اتركه فارغاً لصلاحيات محددة)',
    )
    permission_codes = serializers.ListField(
        child=serializers.CharField(),
        required=False, default=[],
        help_text='صلاحيات محددة (إذا لم يُحدد دور)',
    )
    notes = serializers.CharField(required=False, default='')


# ══════════════════════════════════════════════════════════════
# الطبقة 12: Emergency Access
# ══════════════════════════════════════════════════════════════

class EmergencyAccessSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    granted_by_name = serializers.SerializerMethodField()
    revoked_by_name = serializers.CharField(
        source='revoked_by.username', read_only=True, default=None,
    )
    reviewed_by_name = serializers.CharField(
        source='reviewed_by.username', read_only=True, default=None,
    )
    is_effective = serializers.BooleanField(read_only=True)
    needs_review = serializers.BooleanField(read_only=True)
    permission_codes = serializers.SerializerMethodField()

    class Meta:
        model = EmergencyAccess
        fields = [
            'id', 'user', 'user_name',
            'granted_by', 'granted_by_name',
            'reason', 'permission_codes',
            'granted_at', 'expires_at',
            'status', 'is_effective', 'needs_review',
            'revoked_at', 'revoked_by', 'revoked_by_name',
            'reviewed_by', 'reviewed_by_name', 'reviewed_at',
            'audit_notes',
        ]
        read_only_fields = [
            'user', 'granted_by', 'granted_at', 'status',
            'revoked_at', 'revoked_by', 'reviewed_by', 'reviewed_at',
        ]

    def get_user_name(self, obj):
        return obj.user.get_full_name() or obj.user.username

    def get_granted_by_name(self, obj):
        if obj.granted_by:
            return obj.granted_by.get_full_name() or obj.granted_by.username
        return None

    def get_permission_codes(self, obj):
        return obj.get_permission_codes()


class EmergencyGrantSerializer(serializers.Serializer):
    user_id = serializers.UUIDField(help_text='المستخدم الذي سيحصل على الوصول')
    reason = serializers.CharField(help_text='سبب الطوارئ (إلزامي)')
    permission_codes = serializers.ListField(
        child=serializers.CharField(),
        help_text='الصلاحيات الممنوحة',
    )
    hours = serializers.IntegerField(
        min_value=1, max_value=24, default=4,
        help_text='عدد ساعات الوصول (أقصى 24)',
    )


class EmergencyReviewSerializer(serializers.Serializer):
    audit_notes = serializers.CharField(help_text='ملاحظات المراجعة (إلزامي)')
