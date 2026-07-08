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
        
        if level not in level_field_map:
            raise ValidationError({"error": "Invalid level specified. Choose from: central, branch, district, security_admin"})
            
        group_field = level_field_map[level]
        
        # الفلترة الأساسية: القوة العاملة الفعلية (بالخدمة)
        qs = PersonnelMaster.objects.filter(
            current_status__name='بالخدمة'
        ).values(
            group_field, 
            'current_rank__name'
        ).annotate(
            count=Count('military_number')
        )
        
        # تجميع ومعالجة البيانات لتناسب شكل التقرير
        data_map = {}
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
