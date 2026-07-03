"""
Raw Data Standardized Serializers
مسلسلات البيانات الخام المعاد تنظيمها
"""
from rest_framework import serializers
from systems.personnel.models import PersonnelMaster, SuggestedCorrection, HistoricalMonthlyVariables, RawDataImport
from core.models import Rank, ServiceStatus, CentralDepartment, Branch, DistrictPolice, Division, Unit, JobTitle, Qualification


class RawDataOriginalValuesSerializer(serializers.Serializer):
    """القيم الأصلية من الملف الخام"""
    military_number = serializers.CharField(allow_blank=True, allow_null=True)
    full_name = serializers.CharField(allow_blank=True, allow_null=True)
    national_id = serializers.CharField(allow_blank=True, allow_null=True)
    rank = serializers.CharField(allow_blank=True, allow_null=True)
    directorate = serializers.CharField(allow_blank=True, allow_null=True)
    division = serializers.CharField(allow_blank=True, allow_null=True)
    unit = serializers.CharField(allow_blank=True, allow_null=True)
    job_title = serializers.CharField(allow_blank=True, allow_null=True)
    status = serializers.CharField(allow_blank=True, allow_null=True)


class SuggestedCorrectionMinimalSerializer(serializers.ModelSerializer):
    """اقتراح تصحيح مبسط"""
    correction_type_display = serializers.CharField(source='get_correction_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = SuggestedCorrection
        fields = [
            'id', 'field_name', 'old_value', 'new_value',
            'correction_type', 'correction_type_display',
            'status', 'status_display',
            'requested_at', 'reviewed_at', 'rejection_reason'
        ]


class HistoricalMonthlyVariableSerializer(serializers.ModelSerializer):
    """المتغيرات الشهرية"""
    class Meta:
        model = HistoricalMonthlyVariables
        fields = ['id', 'month', 'variable_value', 'source_column', 'notes', 'created_at']


class RawDataStandardizedSerializer(serializers.ModelSerializer):
    """
    البيانات الخام بعد التنظيم - العرض الكامل
    """
    # البيانات المعتمدة (الحالية)
    current_rank_name = serializers.CharField(source='current_rank.name', read_only=True)
    current_status_name = serializers.CharField(source='current_status.name', read_only=True)
    current_status_classification = serializers.CharField(
        source='current_status.get_classification_display', 
        read_only=True
    )
    
    # الهيكل التنظيمي
    security_admin_name = serializers.CharField(source='security_admin.name', read_only=True)
    central_department_name = serializers.CharField(source='central_department.name', read_only=True)
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    district_police_name = serializers.CharField(source='district_police.name', read_only=True)
    division_name = serializers.CharField(source='division.name', read_only=True)
    unit_name = serializers.CharField(source='unit.name', read_only=True)
    org_path = serializers.SerializerMethodField()
    
    # التوصيف الوظيفي
    category_name = serializers.CharField(source='category.name', read_only=True)
    job_title_name = serializers.CharField(source='job_title.name', read_only=True)
    position_name = serializers.CharField(source='position.name', read_only=True)
    
    # المؤهل
    qualification_name = serializers.CharField(source='qualification.name', read_only=True)
    
    # الرتبة المعلقة
    pending_rank_name = serializers.CharField(source='pending_rank.name', read_only=True, allow_null=True)
    
    # حالة الرقم الوطني (محسوبة من @property)
    national_id_status = serializers.CharField(read_only=True)
    national_id_status_display = serializers.CharField(read_only=True)
    
    # البيانات الأصلية من RawDataImport
    original_values = serializers.SerializerMethodField()
    
    # الاقتراحات المعلقة
    pending_corrections = serializers.SerializerMethodField()
    
    # عدد المتغيرات الشهرية
    monthly_variables_count = serializers.SerializerMethodField()
    
    # الحقول المحسوبة
    age = serializers.IntegerField(read_only=True)
    service_years = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = PersonnelMaster
        fields = [
            # الهوية
            'military_number', 'old_military_number', 'national_id', 'full_name',
            
            # البيانات الشخصية
            'birth_date', 'join_date', 'phone_number', 'age', 'service_years',
            
            # الرتبة والحالة
            'current_rank', 'current_rank_name',
            'pending_rank', 'pending_rank_name',
            'current_status', 'current_status_name', 'current_status_classification',
            
            # الهيكل التنظيمي
            'security_admin', 'security_admin_name',
            'central_department', 'central_department_name',
            'branch', 'branch_name',
            'district_police', 'district_police_name',
            'division', 'division_name',
            'unit', 'unit_name',
            'org_path',
            
            # المؤهل
            'qualification', 'qualification_name',
            
            # التوصيف الوظيفي
            'category', 'category_name',
            'job_title', 'job_title_name',
            'position', 'position_name',
            
            # حالة البيانات
            'national_id_status', 'national_id_status_display',
            'is_data_clean', 'data_quality_score',
            'is_complete', 'notes',
            
            # البيانات الأصلية والاقتراحات
            'original_values',
            'pending_corrections',
            'monthly_variables_count',
            
            # التواريخ
            'created_at', 'updated_at',
        ]
        read_only_fields = ['military_number', 'created_at', 'updated_at']
    
    def get_org_path(self, obj):
        """المسار التنظيمي الكامل"""
        parts = []
        if obj.security_admin:
            parts.append(obj.security_admin.name)
        if obj.central_department:
            parts.append(obj.central_department.name)
        if obj.branch:
            parts.append(obj.branch.name)
        if obj.district_police:
            parts.append(obj.district_police.name)
        if obj.division:
            parts.append(obj.division.name)
        if obj.unit:
            parts.append(obj.unit.name)
        return ' / '.join(parts) if parts else ''
    
    def get_original_values(self, obj):
        """القيم الأصلية من RawDataImport"""
        try:
            raw_import = RawDataImport.objects.filter(
                raw_data__military_number=obj.military_number
            ).first()
            
            if raw_import and raw_import.raw_data:
                return {
                    'military_number': raw_import.raw_data.get('military_number', ''),
                    'full_name': raw_import.raw_data.get('full_name', ''),
                    'national_id': raw_import.raw_data.get('national_id', ''),
                    'rank': raw_import.raw_data.get('rank', ''),
                    'directorate': raw_import.raw_data.get('directorate', ''),
                    'division': raw_import.raw_data.get('division', ''),
                    'unit': raw_import.raw_data.get('unit', ''),
                    'job_title': raw_import.raw_data.get('job_title', ''),
                    'status': raw_import.raw_data.get('status', ''),
                }
        except Exception:
            pass
        return None
    
    def get_pending_corrections(self, obj):
        """الاقتراحات المعلقة"""
        corrections = obj.suggested_corrections.filter(status='pending')
        return SuggestedCorrectionMinimalSerializer(corrections, many=True).data
    
    def get_monthly_variables_count(self, obj):
        """عدد المتغيرات الشهرية"""
        return obj.monthly_variables.count()


class ApplyCorrectionSerializer(serializers.Serializer):
    """تطبيق تصحيح"""
    correction_id = serializers.IntegerField(required=True)
    notes = serializers.CharField(required=False, allow_blank=True)


class RejectCorrectionSerializer(serializers.Serializer):
    """رفض تصحيح"""
    correction_id = serializers.IntegerField(required=True)
    rejection_reason = serializers.CharField(required=True)


class BulkApplyCorrectionSerializer(serializers.Serializer):
    """تطبيق تصحيحات متعددة"""
    correction_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=True
    )
    notes = serializers.CharField(required=False, allow_blank=True)


class BulkRejectCorrectionSerializer(serializers.Serializer):
    """رفض تصحيحات متعددة"""
    correction_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=True
    )
    rejection_reason = serializers.CharField(required=True)

class DirectUpdatePersonnelSerializer(serializers.ModelSerializer):
    """تعديل مباشر لبيانات الفرد من محرك المعالجة"""
    class Meta:
        model = PersonnelMaster
        fields = [
            'military_number', 'national_id', 'full_name',
            'birth_date', 'join_date', 'phone_number',
            'expense_status', 'notes'
        ]


class RawDataStatisticsSerializer(serializers.Serializer):
    """إحصائيات المعالجة"""
    total_records = serializers.IntegerField()
    clean_records = serializers.IntegerField()
    clean_percentage = serializers.FloatField()
    error_records = serializers.IntegerField()
    warning_records = serializers.IntegerField()
