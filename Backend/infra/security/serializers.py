"""
Security Serializers - مسلسلات الأمان والمصادقة
"""
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import (
    Role, UserProfile, DualAuthorizationRequest,
    MetricsSnapshot, SystemSetting,
    SYSTEM_PERMISSIONS,
)
from infra.audit.models import AuditLog

User = get_user_model()


# ============================================================================
# JWT / Auth Serializers
# ============================================================================

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    JWT Login serializer يُضيف بيانات المستخدم في الاستجابة
    """
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # إضافة claims إضافية
        token['username'] = user.username
        try:
            token['role'] = user.authz_profile.role.code
        except Exception:
            token['role'] = 'unknown'
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        
        # فحص هل الحساب مغلق
        try:
            profile = user.security_profile
            if profile.check_lock_state():
                raise serializers.ValidationError(
                    'حسابك مغلق بسبب محاولات دخول فاشلة متعددة. '
                    'يرجى المحاولة لاحقاً أو التواصل مع المدير.'
                )
        except Exception:
            pass
        
        # إضافة بيانات المستخدم
        data['user'] = UserInfoSerializer(user).data
        
        return data


class UserInfoSerializer(serializers.ModelSerializer):
    """بيانات المستخدم الكاملة (تُعاد عند login و /me)"""
    role = serializers.SerializerMethodField()
    directorate = serializers.SerializerMethodField()
    supervised_directorates = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name', 'email',
            'is_active', 'is_superuser', 'last_login',
            'role', 'directorate', 'supervised_directorates',
            'permissions',
        ]
    
    def get_role(self, obj):
        try:
            return {
                'id': obj.authz_profile.role.id,
                'name': obj.authz_profile.role.name,
                'code': obj.authz_profile.role.code,
                'priority': obj.authz_profile.role.priority,
            }
        except Exception:
            return None
    
    def get_directorate(self, obj):
        try:
            d = obj.authz_profile.directorate
            if d:
                return {'id': d.id, 'name': d.name}
        except Exception:
            pass
        return None
    
    def get_supervised_directorates(self, obj):
        try:
            return list(
                obj.authz_profile.supervised_directorates
                .values_list('id', flat=True)
            )
        except Exception:
            return []
    
    def get_permissions(self, obj):
        if obj.is_superuser:
            return [p[0] for p in SYSTEM_PERMISSIONS]
        try:
            return list(obj.authz_profile.role.permissions.values_list('codename', flat=True))
        except Exception:
            return []


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    
    def validate_new_password(self, value):
        validate_password(value)
        return value
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('كلمة المرور الحالية غير صحيحة')
        return value


# ============================================================================
# User Management Serializers (Admin only)
# ============================================================================

@extend_schema_serializer(component_name='UserProfile')
class UserProfileSerializer(serializers.ModelSerializer):
    """عرض ملف المستخدم"""
    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    is_active = serializers.BooleanField(source='user.is_active', read_only=True)
    role_name = serializers.CharField(source='role.name', read_only=True)
    directorate_name = serializers.CharField(
        source='directorate.name', read_only=True, default=None
    )
    supervised_directorate_ids = serializers.PrimaryKeyRelatedField(
        source='supervised_directorates',
        many=True,
        read_only=True,
    )
    is_account_locked = serializers.SerializerMethodField()
    failed_login_attempts = serializers.SerializerMethodField()
    last_login_ip = serializers.SerializerMethodField()
    
    class Meta:
        model = UserProfile
        fields = [
            'id', 'username', 'first_name', 'last_name', 'email',
            'is_active', 'role', 'role_name', 'directorate',
            'directorate_name', 'supervised_directorate_ids',
            'supervises_all_directorates', 'is_account_locked',
            'failed_login_attempts', 'last_login_ip', 'language',
            'created_at', 'updated_at',
        ]
        read_only_fields = [
            'is_account_locked', 'failed_login_attempts',
            'last_login_ip', 'created_at', 'updated_at',
        ]

    def get_is_account_locked(self, obj):
        try:
            return obj.user.security_profile.check_lock_state()
        except Exception:
            return False

    def get_failed_login_attempts(self, obj):
        try:
            return obj.user.security_profile.failed_login_attempts
        except Exception:
            return 0

    def get_last_login_ip(self, obj):
        try:
            return obj.user.security_profile.last_known_ip or obj.user.security_profile.last_failed_ip
        except Exception:
            return None


class UserCreateSerializer(serializers.Serializer):
    """إنشاء مستخدم جديد"""
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True, min_length=8)
    first_name = serializers.CharField(max_length=150, required=False, default='')
    last_name = serializers.CharField(max_length=150, required=False, default='')
    email = serializers.EmailField(required=False, default='')
    role_id = serializers.IntegerField()
    directorate_id = serializers.IntegerField(required=False, allow_null=True)
    supervised_directorate_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        default=list,
    )
    supervises_all_directorates = serializers.BooleanField(default=False)
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('اسم المستخدم مستخدم بالفعل')
        return value
    
    def validate_role_id(self, value):
        if not Role.objects.filter(pk=value, is_active=True).exists():
            raise serializers.ValidationError('الدور غير موجود أو غير نشط')
        return value
    
    def validate_password(self, value):
        validate_password(value)
        return value
    
    def create(self, validated_data):
        from django.db import transaction
        from core.models import CentralDepartment
        from infra.accounts.models.security import SecurityProfile
        
        with transaction.atomic():
            user = User.objects.create_user(
                username=validated_data['username'],
                password=validated_data['password'],
                first_name=validated_data.get('first_name', ''),
                last_name=validated_data.get('last_name', ''),
                email=validated_data.get('email', ''),
            )
            
            # إنشاء SecurityProfile تلقائياً
            SecurityProfile.objects.create(user=user)
            
            dir_id = validated_data.get('directorate_id')
            directorate = None
            if dir_id:
                directorate = CentralDepartment.objects.get(pk=dir_id)
            
            profile = UserProfile.objects.create(
                user=user,
                role_id=validated_data['role_id'],
                directorate=directorate,
                supervises_all_directorates=validated_data.get(
                    'supervises_all_directorates', False
                ),
            )
            
            sup_ids = validated_data.get('supervised_directorate_ids', [])
            if sup_ids:
                profile.supervised_directorates.set(sup_ids)
        
        return user


class UserUpdateSerializer(serializers.Serializer):
    """تحديث مستخدم"""
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)
    email = serializers.EmailField(required=False)
    is_active = serializers.BooleanField(required=False)
    role_id = serializers.IntegerField(required=False)
    directorate_id = serializers.IntegerField(required=False, allow_null=True)
    supervised_directorate_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
    )
    supervises_all_directorates = serializers.BooleanField(required=False)
    reset_password = serializers.CharField(required=False, write_only=True)
    unlock_account = serializers.BooleanField(required=False)
    
    def update(self, instance, validated_data):
        from django.db import transaction
        
        user = instance
        with transaction.atomic():
            # تحديث User
            for field in ['first_name', 'last_name', 'email']:
                if field in validated_data:
                    setattr(user, field, validated_data[field])
            if 'is_active' in validated_data:
                user.is_active = validated_data['is_active']
            if 'reset_password' in validated_data:
                user.set_password(validated_data['reset_password'])
            user.save()
            
            # تحديث Profile
            profile = user.authz_profile
            if 'role_id' in validated_data:
                profile.role_id = validated_data['role_id']
            if 'directorate_id' in validated_data:
                profile.directorate_id = validated_data['directorate_id']
            if 'supervises_all_directorates' in validated_data:
                profile.supervises_all_directorates = validated_data[
                    'supervises_all_directorates'
                ]
            if 'unlock_account' in validated_data and validated_data['unlock_account']:
                try:
                    user.security_profile.unlock()
                except Exception:
                    pass
            profile.save()
            
            if 'supervised_directorate_ids' in validated_data:
                profile.supervised_directorates.set(
                    validated_data['supervised_directorate_ids']
                )
        
        return user


# ============================================================================
# Role Serializers
# ============================================================================

@extend_schema_serializer(component_name='Role')
class RoleSerializer(serializers.ModelSerializer):
    users_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Role
        fields = [
            'id', 'name', 'code', 'description', 'is_active',
            'is_system_role', 'permissions',
            'priority', 'users_count', 'created_at', 'updated_at',
        ]
        read_only_fields = ['is_system_role', 'created_at', 'updated_at']
    
    def get_users_count(self, obj):
        return obj.users.count()


class RoleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = [
            'name', 'code', 'description', 'permissions',
            'visible_pages', 'priority',
        ]
    
    def validate_code(self, value):
        if Role.objects.filter(code=value).exists():
            raise serializers.ValidationError('رمز الدور مستخدم بالفعل')
        return value
    
    def validate_permissions(self, value):
        valid_codes = [p[0] for p in SYSTEM_PERMISSIONS]
        invalid = [p for p in value if p not in valid_codes]
        if invalid:
            raise serializers.ValidationError(
                f'صلاحيات غير صالحة: {", ".join(invalid)}'
            )
        return value


class AvailablePermissionsSerializer(serializers.Serializer):
    """قائمة الصلاحيات المتاحة في النظام"""
    code = serializers.CharField()
    name = serializers.CharField()


# ============================================================================
# Dual Authorization Serializers
# ============================================================================

@extend_schema_serializer(component_name='DualAuthRequest')
class DualAuthRequestSerializer(serializers.ModelSerializer):
    requester_name = serializers.CharField(
        source='requester.username', read_only=True
    )
    approver_name = serializers.CharField(
        source='approver.username', read_only=True, default=None
    )
    action_display = serializers.CharField(
        source='get_action_type_display', read_only=True
    )
    status_display = serializers.CharField(
        source='get_status_display', read_only=True
    )
    
    class Meta:
        model = DualAuthorizationRequest
        fields = [
            'id', 'requester', 'requester_name', 'approver',
            'approver_name', 'action_type', 'action_display',
            'target_object_type', 'target_object_id',
            'request_data', 'status', 'status_display',
            'requested_at', 'expires_at', 'approved_at',
            'executed_at', 'rejection_reason', 'execution_result',
        ]
        read_only_fields = [
            'requester', 'approver', 'requested_at', 'expires_at',
            'approved_at', 'executed_at', 'execution_result',
        ]


class DualAuthCreateSerializer(serializers.Serializer):
    action_type = serializers.ChoiceField(
        choices=DualAuthorizationRequest.ACTION_TYPE_CHOICES
    )
    target_object_type = serializers.CharField(max_length=100)
    target_object_id = serializers.CharField(max_length=100)
    reason = serializers.CharField(min_length=5)


class DualAuthApproveSerializer(serializers.Serializer):
    pass  # لا يحتاج بيانات


class DualAuthRejectSerializer(serializers.Serializer):
    reason = serializers.CharField(min_length=5)


# ============================================================================
# Audit Log Serializers
# ============================================================================

@extend_schema_serializer(component_name='AuditLog')
class AuditLogSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        source='user.username', read_only=True, default='anonymous'
    )
    signature_valid = serializers.SerializerMethodField()
    
    class Meta:
        model = AuditLog
        fields = [
            'id', 'user', 'username', 'action', 'model_name',
            'object_id', 'old_data', 'new_data', 'ip_address',
            'user_agent', 'session_key', 'timestamp', 'signature', 'signature_valid',
        ]
    
    def get_signature_valid(self, obj):
        if not obj.signature:
            return None
        return obj.verify()


class AuditLogVerifySerializer(serializers.Serializer):
    valid = serializers.BooleanField()
    message = serializers.CharField()


# ============================================================================
# System Setting Serializers
# ============================================================================

@extend_schema_serializer(component_name='SystemSetting')
class SystemSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemSetting
        fields = [
            'id', 'key', 'value', 'description', 'category',
            'is_sensitive', 'updated_by', 'updated_at',
        ]
        read_only_fields = ['updated_by', 'updated_at']


# ============================================================================
# Telemetry Serializers
# ============================================================================

class TelemetryDashboardSerializer(serializers.Serializer):
    login_failures = serializers.DictField()
    active_sessions = serializers.DictField()
    pending_dual_auth = serializers.DictField()
    shadow_table_sizes = serializers.DictField()
    system_health = serializers.DictField()
