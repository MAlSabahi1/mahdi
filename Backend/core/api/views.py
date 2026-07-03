"""
Core Views - واجهات API القواميس والهيكل التنظيمي
"""
from rest_framework import permissions
from drf_spectacular.utils import extend_schema, extend_schema_view

from core.models import (
    Rank, ServiceStatus, JobCategory,
    JobTitle, Qualification, Position, ForceType,
    VariableType,
    GeoGovernorate, GeoDistrict, GeoSubDistrict, GeoVillage,
    SecurityAdministration, CentralDepartment, Branch, DistrictPolice,
    Division, Unit,
    StateTransitionRule,
)
from .serializers import (
    RankSerializer, ServiceStatusSerializer,
    JobCategorySerializer, JobTitleSerializer,
    QualificationSerializer, PositionSerializer, ForceTypeSerializer,
    VariableTypeSerializer,
    GeoGovernorateSerializer, GeoDistrictSerializer,
    GeoSubDistrictSerializer, GeoVillageSerializer,
    GeoGovernorateTreeSerializer,
    SecurityAdministrationSerializer, SecurityAdminTreeSerializer,
    CentralDepartmentSerializer, BranchSerializer,
    DistrictPoliceSerializer,
    DivisionSerializer, UnitSerializer,
    StateTransitionRuleSerializer,
)
from infra.security.permissions import ABACPermission, IsAdminPermission
from core.base_views import BaseModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response


class DictionaryViewSetMixin:
    """Mixin مشترك لجميع القواميس"""
    idempotent_actions = ['create', 'update']

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated(), IsAdminPermission()]


# ============================================================================
# Geographic ViewSets (yemen-info.json)
# ============================================================================

@extend_schema_view(
    list=extend_schema(summary='قائمة المحافظات الجغرافية', tags=['geography']),
    retrieve=extend_schema(summary='تفاصيل محافظة جغرافية', tags=['geography']),
)
class GeoGovernorateViewSet(DictionaryViewSetMixin, BaseModelViewSet):
    queryset = GeoGovernorate.objects.all()
    serializer_class = GeoGovernorateSerializer
    search_fields = ['name_ar', 'name_en']
    ordering = ['name_ar']

    @extend_schema(summary='شجرة المحافظات الجغرافية الهرمية', tags=['geography'])
    @action(detail=False, methods=['get'])
    def tree(self, request):
        governorates = GeoGovernorate.objects.filter(is_active=True)
        serializer = GeoGovernorateTreeSerializer(governorates, many=True)
        return Response({'success': True, 'data': serializer.data})


@extend_schema_view(
    list=extend_schema(summary='قائمة المديريات الجغرافية', tags=['geography']),
    retrieve=extend_schema(summary='تفاصيل مديرية جغرافية', tags=['geography']),
)
class GeoDistrictViewSet(DictionaryViewSetMixin, BaseModelViewSet):
    queryset = GeoDistrict.objects.select_related('governorate').all()
    serializer_class = GeoDistrictSerializer
    filterset_fields = ['governorate', 'is_active']
    search_fields = ['name_ar', 'name_en']


@extend_schema_view(
    list=extend_schema(summary='قائمة العزل', tags=['geography']),
)
class GeoSubDistrictViewSet(DictionaryViewSetMixin, BaseModelViewSet):
    queryset = GeoSubDistrict.objects.select_related('district__governorate').all()
    serializer_class = GeoSubDistrictSerializer
    filterset_fields = ['district']
    search_fields = ['name_ar', 'name_en']


@extend_schema_view(
    list=extend_schema(summary='قائمة القرى', tags=['geography']),
)
class GeoVillageViewSet(DictionaryViewSetMixin, BaseModelViewSet):
    queryset = GeoVillage.objects.select_related('sub_district__district').all()
    serializer_class = GeoVillageSerializer
    filterset_fields = ['sub_district']
    search_fields = ['name_ar', 'name_en']


# ============================================================================
# Security Organization ViewSets
# ============================================================================

@extend_schema_view(
    list=extend_schema(summary='قائمة إدارات أمن المحافظات', tags=['security-org']),
    retrieve=extend_schema(summary='تفاصيل إدارة أمن', tags=['security-org']),
)
class SecurityAdministrationViewSet(DictionaryViewSetMixin, BaseModelViewSet):
    queryset = SecurityAdministration.objects.select_related('geo_governorate').all()
    serializer_class = SecurityAdministrationSerializer
    search_fields = ['name', 'code']
    ordering = ['name']

    @extend_schema(summary='شجرة الهيكل الأمني الهرمية', tags=['security-org'])
    @action(detail=False, methods=['get'])
    def tree(self, request):
        qs = SecurityAdministration.objects.filter(is_active=True)
        serializer = SecurityAdminTreeSerializer(qs, many=True)
        return Response({'success': True, 'data': serializer.data})


@extend_schema_view(
    list=extend_schema(summary='قائمة الإدارات المركزية', tags=['security-org']),
    retrieve=extend_schema(summary='تفاصيل إدارة مركزية', tags=['security-org']),
)
class CentralDepartmentViewSet(DictionaryViewSetMixin, BaseModelViewSet):
    queryset = CentralDepartment.objects.select_related('security_admin').all()
    serializer_class = CentralDepartmentSerializer
    filterset_fields = ['security_admin', 'is_active']
    search_fields = ['name', 'code']
    ordering = ['security_admin', 'order', 'name']


@extend_schema_view(
    list=extend_schema(summary='قائمة الفروع', tags=['security-org']),
    retrieve=extend_schema(summary='تفاصيل فرع', tags=['security-org']),
)
class BranchViewSet(DictionaryViewSetMixin, BaseModelViewSet):
    queryset = Branch.objects.select_related('security_admin').all()
    serializer_class = BranchSerializer
    filterset_fields = ['security_admin', 'is_active']
    search_fields = ['name', 'code']
    ordering = ['security_admin', 'order', 'name']


@extend_schema_view(
    list=extend_schema(summary='قائمة أمن المديريات', tags=['security-org']),
    retrieve=extend_schema(summary='تفاصيل أمن مديرية', tags=['security-org']),
)
class DistrictPoliceViewSet(DictionaryViewSetMixin, BaseModelViewSet):
    queryset = DistrictPolice.objects.select_related('security_admin', 'geo_district').all()
    serializer_class = DistrictPoliceSerializer
    filterset_fields = ['security_admin', 'is_active']
    search_fields = ['name', 'code']
    ordering = ['security_admin', 'order', 'name']


@extend_schema_view(
    list=extend_schema(summary='قائمة الأقسام', tags=['security-org']),
    retrieve=extend_schema(summary='تفاصيل قسم', tags=['security-org']),
)
class DivisionViewSet(DictionaryViewSetMixin, BaseModelViewSet):
    queryset = Division.objects.all()
    serializer_class = DivisionSerializer
    filterset_fields = ['central_department', 'branch', 'district_police', 'is_active']
    search_fields = ['name', 'code']
    ordering = ['order', 'name']


@extend_schema_view(
    list=extend_schema(summary='قائمة الوحدات', tags=['security-org']),
    retrieve=extend_schema(summary='تفاصيل وحدة', tags=['security-org']),
)
class UnitViewSet(DictionaryViewSetMixin, BaseModelViewSet):
    queryset = Unit.objects.select_related('division').all()
    serializer_class = UnitSerializer
    filterset_fields = ['division', 'is_active']
    search_fields = ['name', 'code']
    ordering = ['division', 'order', 'name']


# ============================================================================
# Other Dictionaries
# ============================================================================

@extend_schema_view(
    list=extend_schema(summary='قائمة الرتب', tags=['dictionaries']),
    retrieve=extend_schema(summary='تفاصيل رتبة', tags=['dictionaries']),
    create=extend_schema(summary='إنشاء رتبة', tags=['dictionaries']),
    update=extend_schema(summary='تعديل رتبة', tags=['dictionaries']),
    destroy=extend_schema(summary='حذف رتبة', tags=['dictionaries']),
)
class RankViewSet(DictionaryViewSetMixin, BaseModelViewSet):
    queryset = Rank.objects.all()
    serializer_class = RankSerializer
    ordering = ['order']


@extend_schema_view(
    list=extend_schema(summary='قائمة الحالات', tags=['dictionaries']),
    retrieve=extend_schema(summary='تفاصيل حالة', tags=['dictionaries']),
)
class ServiceStatusViewSet(DictionaryViewSetMixin, BaseModelViewSet):
    queryset = ServiceStatus.objects.all()
    serializer_class = ServiceStatusSerializer
    filterset_fields = ['classification']


@extend_schema_view(
    list=extend_schema(summary='قائمة فئات المسميات', tags=['dictionaries']),
)
class JobCategoryViewSet(DictionaryViewSetMixin, BaseModelViewSet):
    queryset = JobCategory.objects.all()
    serializer_class = JobCategorySerializer


@extend_schema_view(
    list=extend_schema(summary='قائمة المسميات', tags=['dictionaries']),
)
class JobTitleViewSet(DictionaryViewSetMixin, BaseModelViewSet):
    queryset = JobTitle.objects.select_related('category').all()
    serializer_class = JobTitleSerializer
    filterset_fields = ['category']


@extend_schema_view(
    list=extend_schema(summary='قائمة المؤهلات', tags=['dictionaries']),
)
class QualificationViewSet(DictionaryViewSetMixin, BaseModelViewSet):
    queryset = Qualification.objects.all()
    serializer_class = QualificationSerializer
    ordering = ['order']


@extend_schema_view(
    list=extend_schema(summary='قائمة المناصب', tags=['dictionaries']),
)
class PositionViewSet(DictionaryViewSetMixin, BaseModelViewSet):
    queryset = Position.objects.select_related('requires_rank').all()
    serializer_class = PositionSerializer
    search_fields = ['name']
    ordering = ['level', 'name']


@extend_schema_view(
    list=extend_schema(summary='قائمة تصنيفات القوة', tags=['dictionaries']),
)
class ForceTypeViewSet(DictionaryViewSetMixin, BaseModelViewSet):
    queryset = ForceType.objects.all()
    serializer_class = ForceTypeSerializer
    filterset_fields = ['category', 'rank_type', 'is_outside_payroll']
    search_fields = ['name', 'code']
    ordering = ['order', 'name']


@extend_schema_view(
    list=extend_schema(summary='قائمة أنواع المتغيرات الشهرية', tags=['other-dictionaries']),
)
class VariableTypeViewSet(DictionaryViewSetMixin, BaseModelViewSet):
    queryset = VariableType.objects.all()
    serializer_class = VariableTypeSerializer
    search_fields = ['name', 'code', 'legacy_aliases']


# ============================================================================
# Workflow & Document Dictionaries
# ============================================================================

@extend_schema_view(
    list=extend_schema(summary='قائمة قواعد انتقال الحالات الخدمية', tags=['workflow']),
    retrieve=extend_schema(summary='تفاصيل قاعدة انتقال حالة', tags=['workflow']),
)
class StateTransitionRuleViewSet(DictionaryViewSetMixin, BaseModelViewSet):
    queryset = StateTransitionRule.objects.select_related('from_state', 'to_state').all()
    serializer_class = StateTransitionRuleSerializer
    filterset_fields = ['from_state', 'to_state', 'is_allowed']

from rest_framework.views import APIView

class DocumentDictionaryViewSet(APIView):
    """
    API لعرض قواميس المرفقات (متطلبات المرفقات لجميع العمليات الإدارية وأنواع المرفقات).
    GET /api/v1/dictionaries/attachment-rules/
    """
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(summary='عرض قواميس المرفقات وقواعدها', tags=['workflow'])
    def get(self, request):
        import os
        import json
        from django.conf import settings
        from infra.storage.models import Document
        
        # 1. جلب قواعد المرفقات للعمليات الإدارية
        rules_path = os.path.join(settings.BASE_DIR, 'core', 'dictionaries', 'action_attachment_rules.json')
        action_rules = {}
        if os.path.exists(rules_path):
            with open(rules_path, 'r', encoding='utf-8') as f:
                action_rules = json.load(f)
                
        # 2. جلب أنواع المرفقات المترجمة من قاعدة البيانات (Source of Truth)
        doc_types = [{'id': k, 'name': str(v)} for k, v in Document.DOCUMENT_TYPE_CHOICES]
        
        return Response({
            'success': True,
            'data': {
                'document_types': doc_types,
                'action_rules': action_rules
            }
        })
