"""
Reconciliation Serializers — مسلسلات المطابقة
═════════════════════════════════════════════
تحقق من صحة المدخلات وتنسيق المخرجات لواجهة API المطابقة.
"""
from rest_framework import serializers


class CreateReconciliationSerializer(serializers.Serializer):
    """
    مسلسل إنشاء مهمة مطابقة جديدة.
    ─── الحقول ───
    • name:              اسم المهمة (وصف مختصر)
    • task_type:         نوع المطابقة (attendance | payroll | qualification)
    • security_admin_id: معرف إدارة الأمن
    • key_field:         حقل الربط (military_number | national_id)
    • source_file:       ملف Excel المصدر
    """
    name = serializers.CharField(
        max_length=255,
        help_text='اسم وصفي للمهمة (مثال: مطابقة حضور شهر يونيو 2026)'
    )
    task_type = serializers.ChoiceField(
        choices=['attendance', 'payroll', 'qualification'],
        help_text='نوع المطابقة: حضور، رواتب، أو مؤهلات'
    )
    security_admin_id = serializers.IntegerField(
        help_text='معرف إدارة الأمن المستهدفة'
    )
    key_field = serializers.ChoiceField(
        choices=['military_number', 'national_id'],
        default='military_number',
        help_text='الحقل المستخدم للربط بين الملف وقاعدة البيانات'
    )
    source_file = serializers.FileField(
        help_text='ملف Excel (.xlsx) المصدر للمطابقة'
    )

    def validate_source_file(self, value):
        """التحقق من أن الملف المرفوع هو Excel صالح."""
        allowed_extensions = ['.xlsx', '.xls']
        name = value.name.lower()
        if not any(name.endswith(ext) for ext in allowed_extensions):
            raise serializers.ValidationError(
                'يجب أن يكون الملف بصيغة Excel (.xlsx أو .xls)'
            )

        # حد أقصى 10 ميجابايت
        max_size = 10 * 1024 * 1024
        if value.size > max_size:
            raise serializers.ValidationError(
                f'حجم الملف ({value.size // 1024 // 1024}MB) يتجاوز الحد الأقصى (10MB)'
            )

        return value


class ReconciliationTaskOutputSerializer(serializers.Serializer):
    """
    مسلسل عرض نتائج مهمة المطابقة.
    يُستخدم للقراءة فقط (GET responses).
    """
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(read_only=True)
    task_type = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)
    security_admin_id = serializers.IntegerField(read_only=True)
    key_field = serializers.CharField(read_only=True)
    summary = serializers.CharField(
        read_only=True,
        source='get_result_summary',
        help_text='ملخص النتائج (عدد المتطابقين، المختلفين، الخ)'
    )
    result = serializers.DictField(
        read_only=True,
        allow_null=True,
        help_text='تفاصيل النتائج الكاملة'
    )
    created_at = serializers.DateTimeField(read_only=True, required=False)
