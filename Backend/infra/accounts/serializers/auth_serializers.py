"""
Auth Serializers — مسلسلات المصادقة
═════════════════════════════════════
مسؤولة فقط عن: التحقق من صحة الإدخال.
لا تحتوي على أي business logic — كل شيء في AuthService.
"""
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    """تسجيل الدخول — يستقبل username + password فقط."""
    username = serializers.CharField(
        required=True,
        max_length=150,
        help_text='اسم المستخدم',
    )
    password = serializers.CharField(
        required=True,
        write_only=True,
        help_text='كلمة المرور',
    )


class LogoutSerializer(serializers.Serializer):
    """تسجيل الخروج — يستقبل refresh token أو session_id."""
    refresh_token = serializers.CharField(
        required=False,
        allow_blank=True,
        default='',
        help_text='Refresh Token لإلغائه',
    )
    session_id = serializers.CharField(
        required=False,
        allow_blank=True,
        default='',
        help_text='معرف الجلسة لإلغائها',
    )

    def validate(self, attrs: dict) -> dict:
        if not attrs.get('refresh_token') and not attrs.get('session_id'):
            raise serializers.ValidationError(
                'يجب تقديم refresh_token أو session_id'
            )
        return attrs


class RefreshTokenSerializer(serializers.Serializer):
    """تجديد التوكن — يستقبل refresh token فقط."""
    refresh_token = serializers.CharField(
        required=True,
        help_text='Refresh Token الحالي',
    )


class ChangePasswordSerializer(serializers.Serializer):
    """تغيير كلمة المرور — يستقبل القديمة والجديدة."""
    old_password = serializers.CharField(
        required=True,
        write_only=True,
        help_text='كلمة المرور الحالية',
    )
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        min_length=8,
        help_text='كلمة المرور الجديدة (8 حروف على الأقل)',
    )
    confirm_password = serializers.CharField(
        required=True,
        write_only=True,
        help_text='تأكيد كلمة المرور الجديدة',
    )

    def validate(self, attrs: dict) -> dict:
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError(
                {'confirm_password': 'كلمتا المرور غير متطابقتين'}
            )
        if attrs['old_password'] == attrs['new_password']:
            raise serializers.ValidationError(
                {'new_password': 'كلمة المرور الجديدة يجب أن تختلف عن الحالية'}
            )
        return attrs


class AuthResponseSerializer(serializers.Serializer):
    """استجابة تسجيل الدخول الناجح — للتوثيق فقط."""
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()
    session_id = serializers.CharField()
    expires_in = serializers.IntegerField(help_text='مدة صلاحية Access Token بالثواني')
    is_suspicious = serializers.BooleanField(help_text='هل تسجيل الدخول مشبوه')
    user = serializers.DictField(help_text='بيانات المستخدم')
