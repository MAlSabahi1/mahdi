from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django.db.models import Count
from systems.personnel.models import PersonnelMaster

class CategoricalWorkforceReportView(APIView):
    """
    نموذج (2): خلاصة عددية للقوة العاملة بحسب الفئة
    يعرض الفئات (ضباط، أفراد، مدنيين) كأعمدة، والجهات كصفوف.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        level = request.query_params.get('level', 'central')
        
        level_field_map = {
            'central': 'central_department__name',
            'branch': 'branch__name',
            'district': 'district_police__name',
            'security_admin': 'security_admin__name',
        }
        
        if level not in level_field_map and level != 'all':
            raise ValidationError({"error": "Invalid level specified."})
            
        from django.db.models.functions import Coalesce
        from core.models.organization import CentralDepartment, Branch, DistrictPolice, SecurityAdministration
        from core.models.personnel_refs import JobCategory
        
        data_map = {}
        if level == 'all':
            units_central = list(CentralDepartment.objects.filter(is_active=True).values_list('name', flat=True))
            units_branch = list(Branch.objects.filter(is_active=True).values_list('name', flat=True))
            units_district = list(DistrictPolice.objects.filter(is_active=True).values_list('name', flat=True))
            units = units_central + units_branch + units_district
        elif level == 'central':
            units = CentralDepartment.objects.filter(is_active=True).values_list('name', flat=True)
        elif level == 'branch':
            units = Branch.objects.filter(is_active=True).values_list('name', flat=True)
        elif level == 'district':
            units = DistrictPolice.objects.filter(is_active=True).values_list('name', flat=True)
        else:
            units = SecurityAdministration.objects.filter(is_active=True).values_list('name', flat=True)
            
        for u in units:
            data_map[u] = {
                "unit_name": u,
                "categories": {},
                "total": 0
            }
        
        # تجميع البيانات: فقط لمن هم "بالخدمة" حسب الفئة
        qs = PersonnelMaster.objects.filter(
            current_status__classification__startswith='active'
        )
        
        if level == 'all':
            qs = qs.annotate(
                unit_name=Coalesce('central_department__name', 'branch__name', 'district_police__name')
            ).values(
                'unit_name', 
                'category__name'
            ).annotate(
                count=Count('military_number')
            )
            group_field = 'unit_name'
        else:
            group_field = level_field_map[level]
            qs = qs.filter(**{f"{group_field.split('__')[0]}__isnull": False}).values(
                group_field, 
                'category__name'
            ).annotate(
                count=Count('military_number')
            )
        
        grand_totals = {}
        
        for row in qs:
            unit = row[group_field] or 'غير محدد'
            category = row['category__name'] or 'غير محدد'
            count = row['count']
            
            if unit not in data_map:
                data_map[unit] = {
                    "unit_name": unit,
                    "categories": {},
                    "total": 0
                }
                
            data_map[unit]["categories"][category] = data_map[unit]["categories"].get(category, 0) + count
            data_map[unit]["total"] += count
            
            grand_totals[category] = grand_totals.get(category, 0) + count
            
        data_list = list(data_map.values())
        data_list.sort(key=lambda x: x['unit_name'])
        
        # Get active job categories sorted by sort_order
        ordered_categories = list(JobCategory.objects.filter(is_active=True).order_by('sort_order', 'name').values_list('name', flat=True))
        
        return Response({
            "level": level,
            "data": data_list,
            "totals": grand_totals,
            "categories": ordered_categories
        })


class NonWorkforceReportView(APIView):
    """
    نموذج (3): خلاصة عددية للقوة غير العاملة بحسب الرتبة
    يعرض الرتب كأعمدة، ومحل الخدمة (حالة الفرد: سجين، دراسة، مريض) كصفوف.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        level = request.query_params.get('level', 'central')
        
        level_field_map = {
            'central': 'central_department__name',
            'branch': 'branch__name',
            'district': 'district_police__name',
            'security_admin': 'security_admin__name',
        }
        
        # جلب الحالات ديناميكياً من قاعدة البيانات بدلاً من كتابتها يدوياً
        from core.models.personnel_refs import ServiceStatus
        # بناءً على طلبك: الحالات يتم سحبها من جدول ServiceStatus
        # نجلب الحالات التي تتبع قوة غير عاملة نهائياً كما طلبت
        db_statuses = ServiceStatus.objects.filter(
            classification='inactive_perm'
        ).values_list('name', flat=True)
        
        dynamic_statuses = list(db_statuses)
        
        # القوة غير العاملة فقط بحسب الحالات المسحوبة من قاعدة البيانات
        qs = PersonnelMaster.objects.filter(
            current_status__name__in=dynamic_statuses
        )
        
        # فلترة بناءً على المستوى المطلوب (إذا لم يكن 'all')
        if level != 'all':
            filter_kwargs = {}
            if level == 'central':
                filter_kwargs['central_department__isnull'] = False
            elif level == 'branch':
                filter_kwargs['branch__isnull'] = False
            elif level == 'district':
                filter_kwargs['district_police__isnull'] = False
            elif level == 'security_admin':
                filter_kwargs['security_admin__isnull'] = False
                
            if filter_kwargs:
                qs = qs.filter(**filter_kwargs)
                
        qs = qs.values(
            'current_status__name', 
            'current_rank__name'
        ).annotate(
            count=Count('military_number')
        )
        
        data_map = {}
        # تهيئة جميع الحالات بصفر لضمان ظهورها حتى لو لم يكن هناك أفراد
        for s in dynamic_statuses:
            data_map[s] = {
                "unit_name": s,
                "ranks": {},
                "total": 0
            }
            
        grand_totals = {}
        
        for row in qs:
            status = row['current_status__name']
            rank = row['current_rank__name'] or 'بدون رتبة'
            count = row['count']
            
            if status in data_map:
                data_map[status]["ranks"][rank] = data_map[status]["ranks"].get(rank, 0) + count
                data_map[status]["total"] += count
                
                grand_totals[rank] = grand_totals.get(rank, 0) + count
            
        # إرجاع القائمة ديناميكياً
        data_list = [data_map[s] for s in dynamic_statuses]
        
        return Response({
            "level": level,
            "data": data_list,
            "totals": grand_totals
        })

from rest_framework import viewsets, status
from rest_framework.decorators import action
from django.utils import timezone
from datetime import timedelta
from ..models import ExportRequest
from .serializers import ExportRequestSerializer

class ExportRequestViewSet(viewsets.ModelViewSet):
    """
    إدارة طلبات تصدير البيانات.
    """
    serializer_class = ExportRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # المدراء يشاهدون كل الطلبات (أو من لديهم صلاحية secretariat.task.execute)
        if user.is_superuser or user.has_perm('secretariat.task.execute'):
            return ExportRequest.objects.all()
        # المستخدم العادي يرى طلباته فقط
        return ExportRequest.objects.filter(requested_by=user)

    def perform_create(self, serializer):
        serializer.save(requested_by=self.request.user)

    @action(detail=True, methods=['post'], url_path='approve')
    def approve(self, request, pk=None):
        user = request.user
        if not (user.is_superuser or user.has_perm('secretariat.task.execute')):
            return Response({"error": "لا تملك صلاحية الموافقة."}, status=status.HTTP_403_FORBIDDEN)
            
        export_req = self.get_object()
        if export_req.status != ExportRequest.Status.PENDING:
            return Response({"error": "الطلب ليس قيد المراجعة."}, status=status.HTTP_400_BAD_REQUEST)
            
        notes = request.data.get('approval_notes', '')
        
        export_req.status = ExportRequest.Status.APPROVED
        export_req.approved_by = user
        export_req.approval_notes = notes
        # إعطاء صلاحية 24 ساعة للتصدير بعد الموافقة
        export_req.expires_at = timezone.now() + timedelta(hours=24)
        export_req.save()
        
        return Response(ExportRequestSerializer(export_req).data)

    @action(detail=True, methods=['post'], url_path='reject')
    def reject(self, request, pk=None):
        user = request.user
        if not (user.is_superuser or user.has_perm('secretariat.task.execute')):
            return Response({"error": "لا تملك صلاحية الرفض."}, status=status.HTTP_403_FORBIDDEN)
            
        export_req = self.get_object()
        if export_req.status != ExportRequest.Status.PENDING:
            return Response({"error": "الطلب ليس قيد المراجعة."}, status=status.HTTP_400_BAD_REQUEST)
            
        notes = request.data.get('approval_notes', '')
        
        export_req.status = ExportRequest.Status.REJECTED
        export_req.approved_by = user
        export_req.approval_notes = notes
        export_req.save()
        
        return Response(ExportRequestSerializer(export_req).data)

    @action(detail=True, methods=['get'], url_path='download')
    def download(self, request, pk=None):
        from systems.reports.utils.report_services import generate_export_response

        export_req = self.get_object()
        
        # Check permissions and expiry
        if export_req.requested_by != request.user and not request.user.is_superuser:
            return Response({"error": "لا تملك صلاحية الوصول لهذا التصدير."}, status=status.HTTP_403_FORBIDDEN)
            
        if export_req.status != ExportRequest.Status.APPROVED:
            return Response({"error": "هذا الطلب غير معتمد للتحميل."}, status=status.HTTP_400_BAD_REQUEST)
            
        if export_req.expires_at and timezone.now() > export_req.expires_at:
            export_req.status = ExportRequest.Status.EXPIRED
            export_req.save()
            return Response({"error": "انتهت صلاحية رابط التحميل."}, status=status.HTTP_400_BAD_REQUEST)

        # Delegate logic to report services
        return generate_export_response(export_req, request)

