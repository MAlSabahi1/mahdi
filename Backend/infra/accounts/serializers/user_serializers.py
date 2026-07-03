"""
User Serializers — مسلسلات المستخدمين
═════════════════════════════════════════
مسؤولة فقط عن: التحقق من صحة الإدخال + تنسيق الإخراج.
لا تحتوي على أي business logic — كل شيء في UserService.
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserOutputSerializer(serializers.ModelSerializer):
    """عرض بيانات المستخدم — للقراءة فقط."""
    display_name = serializers.SerializerMethodField()
    security_status = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'full_name', 'display_name',
            'email', 'phone', 'is_active', 'is_staff',
            'last_login', 'created_at', 'updated_at',
            'security_status', 'role',
        ]
        read_only_fields = fields

    def get_display_name(self, obj: User) -> str:
        return obj.get_display_name()

    def get_role(self, obj: User) -> dict | None:
        from infra.authorization.models.user_role import UserRole
        user_role = UserRole.objects.filter(user=obj, is_active=True).select_related('role').first()
        if user_role and user_role.role.is_active:
            return {
                'id': user_role.role.id,
                'name': user_role.role.name,
                'code': user_role.role.code,
            }
        return None

    def get_security_status(self, obj: User) -> dict:
        try:
            sp = obj.security_profile
            return {
                'is_locked': sp.is_locked,
                'failed_attempts': sp.failed_login_attempts,
                'must_change_password': sp.must_change_password,
            }
        except Exception:
            return {
                'is_locked': False,
                'failed_attempts': 0,
                'must_change_password': False,
            }


class UserMeSerializer(serializers.ModelSerializer):
    """بيانات المستخدم الحالي — تُعاد عند /auth/me."""
    display_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'full_name', 'display_name',
            'email', 'phone', 'is_active', 'is_staff',
            'is_superuser', 'last_login',
            'profile_picture', 'bio', 'facebook_link',
            'x_link', 'linkedin_link', 'instagram_link'
        ]
        read_only_fields = fields

    def get_display_name(self, obj: User) -> str:
        return obj.get_display_name()


class UserCreateSerializer(serializers.Serializer):
    """إنشاء مستخدم جديد — للمدير فقط."""
    username = serializers.CharField(
        max_length=150,
        help_text='اسم المستخدم (فريد)',
    )
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        help_text='كلمة المرور (8 حروف على الأقل)',
    )
    full_name = serializers.CharField(
        max_length=300,
        required=False,
        default='',
        help_text='الاسم الكامل',
    )
    email = serializers.EmailField(
        required=False,
        allow_blank=True,
        default='',
        help_text='البريد الإلكتروني',
    )
    phone = serializers.CharField(
        max_length=20,
        required=False,
        default='',
        help_text='رقم الهاتف',
    )
    role_id = serializers.IntegerField(
        required=False,
        help_text='معرف الدور (Role ID)',
    )
    is_staff = serializers.BooleanField(
        default=False,
        help_text='هل يمكنه الوصول للوحة الإدارة',
    )


class UserUpdateSerializer(serializers.Serializer):
    """تحديث بيانات مستخدم — للمدير فقط."""
    full_name = serializers.CharField(max_length=300, required=False)
    email = serializers.EmailField(required=False)
    phone = serializers.CharField(max_length=20, required=False)
    is_active = serializers.BooleanField(required=False)
    is_staff = serializers.BooleanField(required=False)
    role_id = serializers.IntegerField(
        required=False,
        allow_null=True,
        help_text='معرف الدور (Role ID). أرسل null لإزالة الدور',
    )


class UserResetPasswordSerializer(serializers.Serializer):
    """إعادة تعيين كلمة مرور مستخدم — للمدير فقط."""
    new_password = serializers.CharField(
        write_only=True,
        min_length=8,
        help_text='كلمة المرور الجديدة',
    )


class UserDetailOutputSerializer(serializers.Serializer):
    """تفاصيل المستخدم الكاملة — للمدير."""
    user = UserOutputSerializer()
    active_sessions_count = serializers.IntegerField()
    security = serializers.SerializerMethodField()

    def get_security(self, obj: dict) -> dict:
        sp = obj.get('security')
        if not sp:
            return {}
        return {
            'is_locked': sp.is_locked,
            'locked_until': sp.locked_until,
            'failed_login_attempts': sp.failed_login_attempts,
            'must_change_password': sp.must_change_password,
            'password_changed_at': sp.password_changed_at,
            'last_known_ip': sp.last_known_ip,
        }
