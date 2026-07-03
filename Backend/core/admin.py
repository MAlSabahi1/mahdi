"""
Core Admin - واجهة الإدارة للقواميس والهيكل التنظيمي
"""
from django.contrib import admin
from django import forms
from django.utils.translation import gettext_lazy as _
from infra.storage.models import Document
from .models import (
    Rank, ServiceStatus, JobCategory,
    JobTitle, Qualification, Position,
    GeoGovernorate, GeoDistrict, GeoSubDistrict, GeoVillage,
    SecurityAdministration, CentralDepartment, Branch, DistrictPolice,
    Division, Unit, ForceType, VariableType, StateTransitionRule
)


# ============================================================================
# Geographic Admin
# ============================================================================

@admin.register(GeoGovernorate)
class GeoGovernorateAdmin(admin.ModelAdmin):
    list_display = ['name_ar', 'name_en', 'capital_name_ar', 'is_active']
    search_fields = ['name_ar', 'name_en']
    list_filter = ['is_active']


@admin.register(GeoDistrict)
class GeoDistrictAdmin(admin.ModelAdmin):
    list_display = ['name_ar', 'name_en', 'governorate', 'is_active']
    search_fields = ['name_ar', 'name_en']
    list_filter = ['governorate', 'is_active']
    autocomplete_fields = ['governorate']


@admin.register(GeoSubDistrict)
class GeoSubDistrictAdmin(admin.ModelAdmin):
    list_display = ['name_ar', 'name_en', 'district']
    search_fields = ['name_ar', 'name_en']
    list_filter = ['district__governorate']
    autocomplete_fields = ['district']


@admin.register(GeoVillage)
class GeoVillageAdmin(admin.ModelAdmin):
    list_display = ['name_ar', 'name_en', 'sub_district']
    search_fields = ['name_ar', 'name_en']
    autocomplete_fields = ['sub_district']


# ============================================================================
# Security Organization Admin
# ============================================================================

@admin.register(SecurityAdministration)
class SecurityAdministrationAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'geo_governorate', 'is_active']
    search_fields = ['name', 'code']
    list_filter = ['is_active']
    autocomplete_fields = ['geo_governorate']


@admin.register(CentralDepartment)
class CentralDepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'security_admin', 'order', 'is_active']
    search_fields = ['name', 'code']
    list_filter = ['security_admin', 'is_active']
    autocomplete_fields = ['security_admin']


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'security_admin', 'order', 'is_active']
    search_fields = ['name', 'code']
    list_filter = ['security_admin', 'is_active']
    autocomplete_fields = ['security_admin']


@admin.register(DistrictPolice)
class DistrictPoliceAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'security_admin', 'geo_district', 'is_active']
    search_fields = ['name', 'code']
    list_filter = ['security_admin', 'is_active']
    autocomplete_fields = ['security_admin', 'geo_district']


@admin.register(Division)
class DivisionAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'central_department', 'branch', 'district_police', 'is_active']
    search_fields = ['name', 'code']
    list_filter = ['is_active']


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'division', 'is_active']
    search_fields = ['name', 'code']
    list_filter = ['is_active']
    autocomplete_fields = ['division']


# ============================================================================
# Other Dictionaries
# ============================================================================

@admin.register(Rank)
class RankAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'is_officer', 'created_at']
    search_fields = ['name']
    list_filter = ['is_officer']
    ordering = ['order']


@admin.register(ServiceStatus)
class ServiceStatusAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'classification', 'receives_salary',
        'requires_document', 'is_permanent_deactivation'
    ]
    search_fields = ['name']
    list_filter = ['classification', 'receives_salary', 'requires_document']


@admin.register(JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']


@admin.register(JobTitle)
class JobTitleAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'created_at']
    search_fields = ['name']
    list_filter = ['category']
    autocomplete_fields = ['category']


@admin.register(Qualification)
class QualificationAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'created_at']
    search_fields = ['name']
    ordering = ['order']


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ['name', 'level', 'requires_rank', 'created_at']
    search_fields = ['name']
    list_filter = ['level', 'requires_rank']
    autocomplete_fields = ['requires_rank']
    ordering = ['level', 'name']


@admin.register(ForceType)
class ForceTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'category', 'rank_type', 'is_outside_payroll']
    search_fields = ['name', 'code']
    list_filter = ['category', 'rank_type', 'is_outside_payroll']


@admin.register(VariableType)
class VariableTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'is_active']
    search_fields = ['name', 'code']
    list_filter = ['is_active']


class StateTransitionRuleForm(forms.ModelForm):
    required_document_types = forms.MultipleChoiceField(
        choices=Document.DOCUMENT_TYPE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label=_('أنواع المرفقات المطلوبة'),
        help_text=_('اختر المرفقات المطلوبة لإتمام هذه الحالة')
    )

    class Meta:
        model = StateTransitionRule
        fields = '__all__'

    def clean_required_document_types(self):
        # The form returns a list of selected strings, which is perfect for JSONField!
        return self.cleaned_data.get('required_document_types', [])

@admin.register(StateTransitionRule)
class StateTransitionRuleAdmin(admin.ModelAdmin):
    form = StateTransitionRuleForm
    list_display = ['from_status', 'to_status', 'requires_document', 'requires_dual_auth', 'is_active']
    search_fields = ['from_status__name', 'to_status__name']
    list_filter = ['requires_document', 'requires_dual_auth', 'is_active']
    autocomplete_fields = ['from_status', 'to_status']
