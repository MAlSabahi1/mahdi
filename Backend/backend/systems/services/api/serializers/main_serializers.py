"""
Serializers لخدمات دورة الكشوفات
المهمة 5.4: API Serializers للاستيراد
"""
from rest_framework import serializers
from systems.services.models import StagingRecord, ExportLog, RejectionLog, DirectorateCompliance


class ImportUploadSerializer(serializers.Serializer):
    """Serializer لرفع ملف الاستيراد"""
    file = serializers.FileField(
        required=True,
        help_text="ملف Excel (.xlsx أو .xls)"
    )
    export_id = serializers.UUIDField(
        required=True,
        help_text="معرف التصدير (UUID)"
    )
    service_month = serializers.CharField(
        required=False,
        allow_null=True,
        help_text="شهر الخدمة (YYYY-MM)"
    )
    
    def validate_file(self, value):
        """التحقق من نوع الملف"""
        if not value.name.endswith(('.xlsx', '.xls')):
            raise serializers.ValidationError(
                "يجب أن يكون الملف من نوع Excel (.xlsx أو .xls)"
            )
        
        # التحقق من الحجم (20 ميجابايت)
        if value.size > 20 * 1024 * 1024:
            raise serializers.ValidationError(
                "حجم الملف يجب أن لا يتجاوز 20 ميجابايت"
            )
        
        return value


class ImportTaskStatusSerializer(serializers.Serializer):
    """Serializer لحالة مهمة الاستيراد"""
    task_id = serializers.CharField(read_only=True)
    status = serializers.ChoiceField(
        choices=['pending', 'processing', 'completed', 'failed'],
        read_only=True
    )
    progress = serializers.IntegerField(
        min_value=0,
        max_value=100,
        read_only=True
    )
    message = serializers.CharField(read_only=True, required=False)
    result = serializers.JSONField(read_only=True, required=False)
    error = serializers.CharField(read_only=True, required=False)


class ConflictFieldSerializer(serializers.Serializer):
    """Serializer لحقل مختلف"""
    field_name = serializers.CharField()
    field_label = serializers.CharField()
    system_value = serializers.CharField(allow_null=True)
    file_value = serializers.CharField(allow_null=True)
    severity = serializers.ChoiceField(choices=['low', 'medium', 'high'])


class ConflictRecordSerializer(serializers.Serializer):
    """Serializer لسجل يحتوي على اختلافات"""
    id = serializers.IntegerField()
    military_number = serializers.CharField()
    full_name = serializers.CharField()
    conflicts = ConflictFieldSerializer(many=True)


class MatchedRecordSerializer(serializers.Serializer):
    """Serializer لسجل متطابق"""
    id = serializers.IntegerField()
    military_number = serializers.CharField()
    full_name = serializers.CharField()
    rank = serializers.CharField()
    department = serializers.CharField()
    match_score = serializers.IntegerField()


class NewRecordSerializer(serializers.Serializer):
    """Serializer لسجل جديد"""
    military_number = serializers.CharField()
    full_name = serializers.CharField()
    rank = serializers.CharField(allow_null=True)
    department = serializers.CharField(allow_null=True)
    national_id = serializers.CharField(allow_null=True)


class MissingRecordSerializer(serializers.Serializer):
    """Serializer لسجل مفقود"""
    id = serializers.IntegerField()
    military_number = serializers.CharField()
    full_name = serializers.CharField()
    rank = serializers.CharField()
    department = serializers.CharField()


class ImportStatsSerializer(serializers.Serializer):
    """Serializer لإحصائيات الاستيراد"""
    total_count = serializers.IntegerField()
    matched_count = serializers.IntegerField()
    conflict_count = serializers.IntegerField()
    new_count = serializers.IntegerField()
    missing_count = serializers.IntegerField()


class ImportResultsSerializer(serializers.Serializer):
    """Serializer لنتائج الاستيراد"""
    task_id = serializers.CharField()
    status = serializers.ChoiceField(
        choices=['pending', 'processing', 'completed', 'failed']
    )
    progress = serializers.IntegerField(min_value=0, max_value=100)
    stats = ImportStatsSerializer()
    matched = MatchedRecordSerializer(many=True)
    conflicts = ConflictRecordSerializer(many=True)
    new_records = NewRecordSerializer(many=True)
    missing = MissingRecordSerializer(many=True)


class ConflictResolutionSerializer(serializers.Serializer):
    """Serializer لحل اختلاف واحد"""
    record_id = serializers.IntegerField()
    selected_values = serializers.DictField(
        child=serializers.ChoiceField(choices=['system', 'file']),
        help_text="قاموس: {field_name: 'system' أو 'file'}"
    )


class ResolveConflictsSerializer(serializers.Serializer):
    """Serializer لحل الاختلافات"""
    task_id = serializers.CharField()
    resolutions = ConflictResolutionSerializer(many=True)


class ApproveMatchedSerializer(serializers.Serializer):
    """Serializer لقبول السجلات المتطابقة"""
    task_id = serializers.CharField()
    record_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        help_text="قائمة معرفات السجلات (فارغة = قبول الكل)"
    )


class CreateNewRecordsSerializer(serializers.Serializer):
    """Serializer لإضافة سجلات جديدة"""
    task_id = serializers.CharField()
    records = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False,
        help_text="قائمة indexes السجلات الجديدة"
    )


class NotifyMissingSerializer(serializers.Serializer):
    """Serializer لإرسال تنبيهات للسجلات المفقودة"""
    task_id = serializers.CharField()
    record_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False,
        help_text="قائمة معرفات السجلات المفقودة"
    )


class StagingRecordSerializer(serializers.ModelSerializer):
    """Serializer لسجل Staging لتطابق الفرونت إند"""
    personnel = serializers.SerializerMethodField()
    field_name = serializers.SerializerMethodField()
    old_value = serializers.SerializerMethodField()
    new_value = serializers.SerializerMethodField()
    
    class Meta:
        model = StagingRecord
        fields = [
            'id',
            'personnel',
            'field_name',
            'old_value',
            'new_value',
            'status',
            'severity',
            'created_at',
            'upload_batch_id',
        ]
        read_only_fields = ['id', 'created_at', 'upload_batch_id']

    def get_personnel(self, obj):
        return {
            'military_number': obj.personnel.military_number if obj.personnel else '',
            'full_name': obj.personnel.full_name if obj.personnel else ''
        }
        
    def get_field_name(self, obj):
        return obj.proposed_change.get('field_name', '') if obj.proposed_change else ''
        
    def get_old_value(self, obj):
        return obj.proposed_change.get('old_value', '') if obj.proposed_change else ''
        
    def get_new_value(self, obj):
        return obj.proposed_change.get('new_value', '') if obj.proposed_change else ''


class ExportLogSerializer(serializers.ModelSerializer):
    """Serializer لسجل التصدير"""
    central_department_name = serializers.CharField(source='central_department.name', read_only=True)
    exported_by_name = serializers.CharField(source='exported_by.get_full_name', read_only=True)
    
    class Meta:
        model = ExportLog
        fields = [
            'export_id',
            'central_department',
            'security_admin',
            'central_department_name',
            'service_month',
            'exported_by',
            'exported_by_name',
            'exported_at',
            'file_hash',
            'row_count',
            'row_uuids',
            'status',
            'expires_at',
        ]
        read_only_fields = [
            'export_id',
            'exported_at',
            'file_hash',
            'row_count',
            'row_uuids',
        ]


class DirectorateComplianceSerializer(serializers.ModelSerializer):
    """Serializer لالتزام المديرية/الإدارة"""
    central_department_name = serializers.CharField(source='central_department.name', read_only=True)
    
    class Meta:
        model = DirectorateCompliance
        fields = [
            'id',
            'central_department',
            'security_admin',
            'central_department_name',
            'service_month',
            'submitted_at',
            'error_count',
            'quality_score',
        ]
        read_only_fields = ['id', 'submitted_at']


# ============================================================================
# Legacy Serializers (للتوافق مع views.py القديم)
# ============================================================================

class ApproveSerializer(serializers.Serializer):
    """Serializer للموافقة على تغيير"""
    document_uuid = serializers.UUIDField(
        required=False,
        allow_null=True,
        help_text="معرف المستند المرفق (للتغييرات التي تحتاج مستند)"
    )


class RejectSerializer(serializers.Serializer):
    """Serializer لرفض تغيير"""
    rejection_reason = serializers.CharField(
        required=True,
        min_length=10,
        help_text="سبب الرفض (10 أحرف على الأقل)"
    )


class BulkApproveSerializer(serializers.Serializer):
    """Serializer للموافقة الجماعية"""
    staging_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False,
        help_text="قائمة معرفات السجلات للموافقة عليها"
    )


class ExportRequestSerializer(serializers.Serializer):
    """Serializer لطلب تصدير"""
    directorate_id = serializers.IntegerField()
    service_month = serializers.CharField(help_text="YYYY-MM")


class ImportResponseSerializer(serializers.Serializer):
    """Serializer لاستجابة الاستيراد"""
    success = serializers.BooleanField()
    batch_id = serializers.UUIDField(required=False)
    message = serializers.CharField()
    stats = serializers.DictField(required=False)


class TaskStatusSerializer(serializers.Serializer):
    """Serializer لحالة المهمة"""
    task_id = serializers.CharField()
    status = serializers.CharField()
    progress = serializers.IntegerField(required=False)
    result = serializers.JSONField(required=False)
    error = serializers.CharField(required=False)


class MonthlySnapshotSerializer(serializers.Serializer):
    """Serializer للقطة الشهرية"""
    service_month = serializers.CharField()
    locked = serializers.BooleanField()
    snapshot_data = serializers.JSONField()


class ReconciliationTaskSerializer(serializers.Serializer):
    """Serializer لمهمة المطابقة"""
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    task_type = serializers.CharField()
    status = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)
    results = serializers.JSONField(read_only=True, required=False)


class ReconciliationCreateSerializer(serializers.Serializer):
    """Serializer لإنشاء مهمة مطابقة"""
    name = serializers.CharField()
    task_type = serializers.ChoiceField(choices=['strength', 'salary', 'courses'])
    key_field = serializers.CharField(default='military_number')


class ReconciliationResolveSerializer(serializers.Serializer):
    """Serializer لحل اختلافات المطابقة"""
    resolutions = serializers.ListField(
        child=serializers.DictField()
    )


class RejectionLogSerializer(serializers.ModelSerializer):
    """Serializer لسجل الرفض ليتطابق مع الفرونت إند"""
    personnel = serializers.SerializerMethodField()
    rejected_by = serializers.SerializerMethodField()
    
    class Meta:
        from systems.services.models import RejectionLog
        model = RejectionLog
        fields = [
            'id',
            'personnel',
            'service_month',
            'rejection_reason',
            'rejected_by',
            'rejected_at',
        ]
        
    def get_personnel(self, obj):
        return {
            'military_number': obj.personnel.military_number if obj.personnel else '',
            'full_name': obj.personnel.full_name if obj.personnel else ''
        }
        
    def get_rejected_by(self, obj):
        return {
            'username': obj.rejected_by.username if obj.rejected_by else 'النظام'
        }


class WebhookConfigSerializer(serializers.ModelSerializer):
    """Serializer لإعدادات Webhook"""
    class Meta:
        from systems.services.models import WebhookConfig
        model = WebhookConfig
        fields = ["id", "url", "secret", "events", "is_active", "central_department", "created_at"]
        read_only_fields = ["id", "created_at"]


class ReportTemplateSerializer(serializers.Serializer):
    """Serializer لقالب التقرير"""
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    slug = serializers.SlugField()
    description = serializers.CharField()


class ReportGenerateSerializer(serializers.Serializer):
    """Serializer لتوليد تقرير"""
    template_slug = serializers.SlugField()
    filters = serializers.DictField(required=False)
    format = serializers.ChoiceField(
        choices=['excel', 'pdf', 'html'],
        default='excel'
    )
