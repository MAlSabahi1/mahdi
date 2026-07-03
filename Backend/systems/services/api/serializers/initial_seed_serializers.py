"""
Initial Seed Serializers - مسلسلات التأسيس الأولي
"""
from rest_framework import serializers

class InitialSeedPreviewSerializer(serializers.Serializer):
    """مسلسل رفع ملف التأسيس للمعاينة"""
    file = serializers.FileField(
        required=True,
        help_text='ملف Excel يحتوي على البيانات الخام للتأسيس'
    )

class InitialSeedValidateSerializer(serializers.Serializer):
    """مسلسل رفع ملف التأسيس للفحص"""
    file = serializers.FileField(
        required=True,
        help_text='ملف Excel يحتوي على البيانات الخام للتأسيس'
    )
    mapping = serializers.JSONField(
        required=False,
        help_text='قاموس لربط أسماء أعمدة المستخدم مع أعمدة النظام'
    )

class InitialSeedCommitSerializer(serializers.Serializer):
    """مسلسل اعتماد ملف التأسيس بعد نجاح الفحص"""
    file = serializers.FileField(
        required=True,
        help_text='ملف Excel السليم تماماً للاعتماد النهائي'
    )
    batch_id = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text='معرف دفعة اختياري (UUID أو أي نص)'
    )
    mapping = serializers.JSONField(
        required=False,
        help_text='قاموس لربط أسماء أعمدة المستخدم مع أعمدة النظام'
    )

class InitialSeedValidateJsonSerializer(serializers.Serializer):
    """مسلسل فحص البيانات مباشرة عبر JSON"""
    data = serializers.ListField(
        child=serializers.DictField(),
        required=True,
        help_text='قائمة من القواميس تمثل صفوف الإكسل'
    )

class InitialSeedCommitJsonSerializer(serializers.Serializer):
    """مسلسل اعتماد البيانات مباشرة عبر JSON"""
    data = serializers.ListField(
        child=serializers.DictField(),
        required=True,
        help_text='قائمة من القواميس تمثل صفوف الإكسل السليمة'
    )
    batch_id = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text='معرف دفعة اختياري (UUID أو أي نص)'
    )
