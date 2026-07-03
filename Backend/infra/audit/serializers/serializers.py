"""
Audit Serializers — مسلسلات التدقيق
"""
from rest_framework import serializers
from infra.audit.models.audit_log import AuditLog, AuditSeverity
from infra.audit.models.login_audit import LoginAuditLog


class AuditLogSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    is_verified = serializers.SerializerMethodField()

    class Meta:
        model = AuditLog
        fields = [
            'id', 'user', 'username', 'action', 'model_name', 'object_id',
            'old_data', 'new_data', 'change_reason', 'ip_address',
            'user_agent', 'severity', 'module', 'timestamp',
            'is_verified', 'is_archived',
        ]
        read_only_fields = fields

    def get_is_verified(self, obj) -> bool:
        return obj.verify()


class AuditLogListSerializer(serializers.ModelSerializer):
    """نسخة خفيفة للقوائم."""
    username = serializers.CharField(read_only=True)

    class Meta:
        model = AuditLog
        fields = [
            'id', 'username', 'action', 'model_name', 'object_id',
            'severity', 'module', 'timestamp', 'change_reason',
        ]
        read_only_fields = fields


class LoginAuditLogSerializer(serializers.ModelSerializer):
    action_display = serializers.CharField(
        source='get_action_display', read_only=True
    )

    class Meta:
        model = LoginAuditLog
        fields = [
            'id', 'user', 'username_attempted', 'action', 'action_display',
            'ip_address', 'user_agent', 'failure_reason',
            'extra_data', 'geo_location', 'timestamp',
        ]
        read_only_fields = fields


class AuditStatsSerializer(serializers.Serializer):
    """إحصائيات التدقيق."""
    total_records = serializers.IntegerField()
    today_count = serializers.IntegerField()
    by_action = serializers.DictField()
    by_severity = serializers.DictField()
    by_module = serializers.DictField()
