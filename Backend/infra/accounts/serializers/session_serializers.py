"""
Session Serializers — مسلسلات الجلسات
═════════════════════════════════════════
عرض الأجهزة النشطة وإدارتها.
"""
from rest_framework import serializers
from infra.accounts.models.session import UserSession


class SessionOutputSerializer(serializers.ModelSerializer):
    """عرض جلسة نشطة — للمستخدم أو المدير."""
    is_current = serializers.SerializerMethodField()
    is_expired = serializers.BooleanField(read_only=True)
    inactivity_seconds = serializers.IntegerField(read_only=True)

    class Meta:
        model = UserSession
        fields = [
            'session_id', 'device_name', 'browser', 'os',
            'ip_address', 'last_activity', 'created_at',
            'is_active', 'is_current', 'is_expired',
            'inactivity_seconds',
        ]
        read_only_fields = fields

    def get_is_current(self, obj: UserSession) -> bool:
        """هل هذه هي الجلسة الحالية للطلب."""
        request = self.context.get('request')
        if not request:
            return False
        current_session_id = getattr(request, '_session_id', None)
        return str(obj.session_id) == str(current_session_id)


class TerminateSessionSerializer(serializers.Serializer):
    """إلغاء جلسة معينة."""
    session_id = serializers.UUIDField(
        required=True,
        help_text='معرف الجلسة المراد إلغاؤها',
    )
