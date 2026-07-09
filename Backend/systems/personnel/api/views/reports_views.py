from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django.db.models import Count
from systems.personnel.models import PersonnelMaster

class WorkforceSummaryReportView(APIView):
    """
    تقرير خلاصة القوة العاملة بحسب الرتبة.
    يسمح بالتجميع بناءً على مستوى الهيكل التنظيمي المحدد في ?level=
    Levels: 'central', 'branch', 'district', 'security_admin'
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        level = request.query_params.get('level', 'central')
        
        # خريطة لربط المستوى بالحقل المناسب في قاعدة البيانات
        level_field_map = {
            'central': 'central_department__name',
            'branch': 'branch__name',
            'district': 'district_police__name',
            'security_admin': 'security_admin__name',
        }
        
        if level not in level_field_map and level != 'all':
            raise ValidationError({"error": "Invalid level specified. Choose from: central, branch, district, security_admin, all"})
            
        from django.db.models.functions import Coalesce
        from core.models.organization import CentralDepartment, Branch, DistrictPolice, SecurityAdministration
        
        # Pre-fill data_map with all active units to ensure 0-count units appear
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
                "ranks": {},
                "total": 0
            }
            
        # الفلترة الأساسية: القوة العاملة الفعلية
        qs = PersonnelMaster.objects.filter(
            current_status__classification__startswith='active'
        )
        
        if level == 'all':
            qs = qs.annotate(
                unit_name=Coalesce('central_department__name', 'branch__name', 'district_police__name')
            ).values(
                'unit_name', 
                'current_rank__name'
            ).annotate(
                count=Count('military_number')
            )
            group_field = 'unit_name'
        else:
            group_field = level_field_map[level]
            qs = qs.filter(**{f"{group_field.split('__')[0]}__isnull": False}).values(
                group_field, 
                'current_rank__name'
            ).annotate(
                count=Count('military_number')
            )
        
        grand_totals = {}
        
        for row in qs:
            unit = row[group_field] or 'غير محدد'
            rank = row['current_rank__name'] or 'غير محدد'
            count = row['count']
            
            # تهيئة الوحدة إذا لم تكن موجودة
            if unit not in data_map:
                data_map[unit] = {
                    "unit_name": unit,
                    "ranks": {},
                    "total": 0
                }
                
            # إضافة العدد للرتبة
            data_map[unit]["ranks"][rank] = data_map[unit]["ranks"].get(rank, 0) + count
            data_map[unit]["total"] += count
            
            # الإجمالي العام للرتبة
            grand_totals[rank] = grand_totals.get(rank, 0) + count
            
        data_list = list(data_map.values())
        data_list.sort(key=lambda x: x['unit_name'])
        
        return Response({
            "level": level,
            "data": data_list,
            "totals": grand_totals
        })
