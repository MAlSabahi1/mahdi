"""
Core Serializers - مسلسلات القواميس والهيكل التنظيمي
"""
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_serializer
from core.models import (
    Rank, ServiceStatus, JobCategory,
    JobTitle, Qualification, Position, ForceType,
    VariableType,
    # Geographic
    GeoGovernorate, GeoDistrict, GeoSubDistrict, GeoVillage,
    # Security Organization
    SecurityAdministration, CentralDepartment, Branch, DistrictPolice,
    Division, Unit,
    # Workflow
    StateTransitionRule,
)


# ============================================================================
# Geographic Serializers (yemen-info.json)
# ============================================================================

@extend_schema_serializer(component_name='GeoGovernorate')
class GeoGovernorateSerializer(serializers.ModelSerializer):
    districts_count = serializers.SerializerMethodField()

    class Meta:
        model = GeoGovernorate
        fields = [
            'id', 'name_ar', 'name_en', 'name_ar_normalized',
            'phone_numbering_plan', 'capital_name_ar', 'is_active',
            'districts_count',
        ]

    def get_districts_count(self, obj):
        return obj.districts.count()


@extend_schema_serializer(component_name='GeoDistrict')
class GeoDistrictSerializer(serializers.ModelSerializer):
    governorate_name = serializers.CharField(source='governorate.name_ar', read_only=True)

    class Meta:
        model = GeoDistrict
        fields = [
            'id', 'name_ar', 'name_en', 'name_ar_normalized',
            'governorate', 'governorate_name', 'is_active',
        ]


@extend_schema_serializer(component_name='GeoSubDistrict')
class GeoSubDistrictSerializer(serializers.ModelSerializer):
    district_name = serializers.CharField(source='district.name_ar', read_only=True)

    class Meta:
        model = GeoSubDistrict
        fields = ['id', 'name_ar', 'name_en', 'district', 'district_name']


@extend_schema_serializer(component_name='GeoVillage')
class GeoVillageSerializer(serializers.ModelSerializer):
    sub_district_name = serializers.CharField(source='sub_district.name_ar', read_only=True)

    class Meta:
        model = GeoVillage
        fields = ['id', 'name_ar', 'name_en', 'sub_district', 'sub_district_name']


# ============================================================================
# Security Organization Serializers
# ============================================================================

@extend_schema_serializer(component_name='SecurityAdministration')
class SecurityAdministrationSerializer(serializers.ModelSerializer):
    geo_governorate_name = serializers.CharField(source='geo_governorate.name_ar', read_only=True)
    departments_count = serializers.SerializerMethodField()
    branches_count = serializers.SerializerMethodField()
    district_police_count = serializers.SerializerMethodField()

    class Meta:
        model = SecurityAdministration
        fields = [
            'id', 'name', 'code', 'geo_governorate', 'geo_governorate_name',
            'head', 'is_active', 'description',
            'departments_count', 'branches_count', 'district_police_count',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_departments_count(self, obj):
        return obj.central_departments.filter(is_active=True).count()

    def get_branches_count(self, obj):
        return obj.branches.filter(is_active=True).count()

    def get_district_police_count(self, obj):
        return obj.district_police_units.filter(is_active=True).count()


@extend_schema_serializer(component_name='CentralDepartment')
class CentralDepartmentSerializer(serializers.ModelSerializer):
    security_admin_name = serializers.CharField(source='security_admin.name', read_only=True)

    class Meta:
        model = CentralDepartment
        fields = [
            'id', 'name', 'code', 'security_admin', 'security_admin_name',
            'head', 'head_position', 'is_active', 'order',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']


@extend_schema_serializer(component_name='Branch')
class BranchSerializer(serializers.ModelSerializer):
    security_admin_name = serializers.CharField(source='security_admin.name', read_only=True)

    class Meta:
        model = Branch
        fields = [
            'id', 'name', 'code', 'security_admin', 'security_admin_name',
            'head', 'head_position', 'is_active', 'order',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']


@extend_schema_serializer(component_name='DistrictPolice')
class DistrictPoliceSerializer(serializers.ModelSerializer):
    security_admin_name = serializers.CharField(source='security_admin.name', read_only=True)
    geo_district_name = serializers.CharField(source='geo_district.name_ar', read_only=True)

    class Meta:
        model = DistrictPolice
        fields = [
            'id', 'name', 'code', 'security_admin', 'security_admin_name',
            'geo_district', 'geo_district_name',
            'head', 'head_position', 'is_active', 'order',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']


@extend_schema_serializer(component_name='Division')
class DivisionSerializer(serializers.ModelSerializer):
    parent_name = serializers.SerializerMethodField()
    parent_type = serializers.SerializerMethodField()
    units_count = serializers.SerializerMethodField()

    class Meta:
        model = Division
        fields = [
            'id', 'name', 'code',
            'central_department', 'branch', 'district_police',
            'parent_name', 'parent_type',
            'head', 'head_position', 'is_active', 'order',
            'units_count', 'created_at', 'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_parent_name(self, obj):
        parent = obj.parent
        return parent.name if parent else None

    def get_parent_type(self, obj):
        return obj.parent_type

    def get_units_count(self, obj):
        return obj.units.filter(is_active=True).count()


@extend_schema_serializer(component_name='Unit')
class UnitSerializer(serializers.ModelSerializer):
    division_name = serializers.CharField(source='division.name', read_only=True)

    class Meta:
        model = Unit
        fields = [
            'id', 'name', 'code', 'division', 'division_name',
            'head', 'head_position', 'is_active', 'order',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']


# ============================================================================
# Tree Serializers (Hierarchical Display)
# ============================================================================

class UnitTreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ['id', 'name', 'code', 'is_active', 'order']

class DivisionTreeSerializer(serializers.ModelSerializer):
    units = serializers.SerializerMethodField()
    class Meta:
        model = Division
        fields = ['id', 'name', 'code', 'is_active', 'order', 'units']
    def get_units(self, obj):
        return UnitTreeSerializer(obj.units.filter(is_active=True), many=True).data

class CentralDepartmentTreeSerializer(serializers.ModelSerializer):
    divisions = serializers.SerializerMethodField()
    class Meta:
        model = CentralDepartment
        fields = ['id', 'name', 'code', 'is_active', 'order', 'divisions']
    def get_divisions(self, obj):
        return DivisionTreeSerializer(obj.divisions.filter(is_active=True), many=True).data

class BranchTreeSerializer(serializers.ModelSerializer):
    divisions = serializers.SerializerMethodField()
    class Meta:
        model = Branch
        fields = ['id', 'name', 'code', 'is_active', 'order', 'divisions']
    def get_divisions(self, obj):
        return DivisionTreeSerializer(obj.divisions.filter(is_active=True), many=True).data

class DistrictPoliceTreeSerializer(serializers.ModelSerializer):
    divisions = serializers.SerializerMethodField()
    class Meta:
        model = DistrictPolice
        fields = ['id', 'name', 'code', 'is_active', 'order', 'divisions']
    def get_divisions(self, obj):
        return DivisionTreeSerializer(obj.divisions.filter(is_active=True), many=True).data

class SecurityAdminTreeSerializer(serializers.ModelSerializer):
    """شجرة إدارة الأمن: إدارات + فروع + أمن مديريات"""
    central_departments = serializers.SerializerMethodField()
    branches = serializers.SerializerMethodField()
    district_police_units = serializers.SerializerMethodField()

    class Meta:
        model = SecurityAdministration
        fields = ['id', 'name', 'code', 'central_departments', 'branches', 'district_police_units']

    def get_central_departments(self, obj):
        qs = obj.central_departments.filter(is_active=True)
        return CentralDepartmentTreeSerializer(qs, many=True).data

    def get_branches(self, obj):
        qs = obj.branches.filter(is_active=True)
        return BranchTreeSerializer(qs, many=True).data

    def get_district_police_units(self, obj):
        qs = obj.district_police_units.filter(is_active=True)
        return DistrictPoliceTreeSerializer(qs, many=True).data


class GeoGovernorateTreeSerializer(serializers.ModelSerializer):
    """شجرة المحافظة الجغرافية: مديريات → عزل → قرى"""
    districts = serializers.SerializerMethodField()

    class Meta:
        model = GeoGovernorate
        fields = ['id', 'name_ar', 'name_en', 'districts']

    def get_districts(self, obj):
        qs = obj.districts.filter(is_active=True)
        return GeoDistrictTreeSerializer(qs, many=True).data


class GeoDistrictTreeSerializer(serializers.ModelSerializer):
    sub_districts = serializers.SerializerMethodField()

    class Meta:
        model = GeoDistrict
        fields = ['id', 'name_ar', 'name_en', 'sub_districts']

    def get_sub_districts(self, obj):
        return GeoSubDistrictTreeSerializer(obj.sub_districts.all(), many=True).data


class GeoSubDistrictTreeSerializer(serializers.ModelSerializer):
    villages = serializers.SerializerMethodField()

    class Meta:
        model = GeoSubDistrict
        fields = ['id', 'name_ar', 'name_en', 'villages']

    def get_villages(self, obj):
        return GeoVillageSerializer(obj.villages.all(), many=True).data


# ============================================================================
# Other Dictionaries
# ============================================================================

@extend_schema_serializer(component_name='Position')
class PositionSerializer(serializers.ModelSerializer):
    requires_rank_name = serializers.CharField(source='requires_rank.name', read_only=True)

    class Meta:
        model = Position
        fields = [
            'id', 'name', 'level', 'requires_rank', 'requires_rank_name',
            'allowed_categories', 'created_at', 'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']


@extend_schema_serializer(component_name='ForceType')
class ForceTypeSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    rank_type_display = serializers.CharField(source='get_rank_type_display', read_only=True)

    class Meta:
        model = ForceType
        fields = [
            'id', 'name', 'code', 'category', 'category_display',
            'rank_type', 'rank_type_display', 'is_outside_payroll',
            'description', 'order', 'created_at', 'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']


@extend_schema_serializer(component_name='Rank')
class RankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rank
        fields = ['id', 'name', 'order', 'is_officer', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


@extend_schema_serializer(component_name='ServiceStatus')
class ServiceStatusSerializer(serializers.ModelSerializer):
    classification_display = serializers.CharField(source='get_classification_display', read_only=True)

    class Meta:
        model = ServiceStatus
        fields = [
            'id', 'name', 'classification', 'classification_display',
            'requires_document', 'receives_salary', 'is_permanent_deactivation',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']


@extend_schema_serializer(component_name='JobCategory')
class JobCategorySerializer(serializers.ModelSerializer):
    job_titles_count = serializers.SerializerMethodField()

    class Meta:
        model = JobCategory
        fields = ['id', 'name', 'job_titles_count', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def get_job_titles_count(self, obj):
        return obj.job_titles.count()


@extend_schema_serializer(component_name='JobTitle')
class JobTitleSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = JobTitle
        fields = [
            'id', 'name', 'category', 'category_name', 'description',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']


@extend_schema_serializer(component_name='Qualification')
class QualificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qualification
        fields = ['id', 'name', 'order', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


@extend_schema_serializer(component_name='VariableType')
class VariableTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariableType
        fields = [
            'id', 'code', 'name',
            'description', 'legacy_aliases', 'is_active', 'order',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']

@extend_schema_serializer(component_name='StateTransitionRule')
class StateTransitionRuleSerializer(serializers.ModelSerializer):
    from_state_name = serializers.CharField(source='from_state.name', read_only=True)
    to_state_name = serializers.CharField(source='to_state.name', read_only=True)

    class Meta:
        model = StateTransitionRule
        fields = [
            'id', 'from_state', 'from_state_name', 'to_state', 'to_state_name',
            'is_allowed', 'requires_approval', 'required_documents',
            'conditions', 'created_at', 'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']

