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
        
        if level not in level_field_map:
            raise ValidationError({"error": "Invalid level specified."})
            
        group_field = level_field_map[level]
        
        # تجميع البيانات: فقط لمن هم "بالخدمة" حسب الفئة
        qs = PersonnelMaster.objects.filter(
            current_status__name='بالخدمة'
        ).values(
            group_field, 
            'category__name'
        ).annotate(
            count=Count('military_number')
        )
        
        data_map = {}
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
        
        return Response({
            "level": level,
            "data": data_list,
            "totals": grand_totals
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
        
        if level not in level_field_map:
            raise ValidationError({"error": "Invalid level specified."})
            
        # هنا لا نحتاج للـ group_field كصف، بل نستخدمه للفلترة إذا لزم الأمر، 
        # لكن التقرير يتطلب إحصائية عن الجهة بأكملها، الصفوف هي الحالات (current_status).
        
        # استبعاد "بالخدمة" وكل من ليس لديه حالة
        qs = PersonnelMaster.objects.exclude(
            current_status__name__in=['بالخدمة', None, '']
        ).values(
            'current_status__name', 
            'current_rank__name'
        ).annotate(
            count=Count('military_number')
        )
        
        data_map = {}
        grand_totals = {}
        
        for row in qs:
            status = row['current_status__name'] or 'غير محدد'
            rank = row['current_rank__name'] or 'بدون رتبة'
            count = row['count']
            
            if status not in data_map:
                data_map[status] = {
                    "unit_name": status, # Using unit_name as a generic row label for frontend ReportTable
                    "ranks": {},
                    "total": 0
                }
                
            data_map[status]["ranks"][rank] = data_map[status]["ranks"].get(rank, 0) + count
            data_map[status]["total"] += count
            
            grand_totals[rank] = grand_totals.get(rank, 0) + count
            
        data_list = list(data_map.values())
        data_list.sort(key=lambda x: x['unit_name'])
        
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
        from django.http import HttpResponse
        from systems.personnel.api.views.reports_views import WorkforceSummaryReportView
        from systems.reports.utils.excel_generator import generate_report_excel

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

        # Map report_id to the actual view class to fetch data
        from ..personnel.api.views.detailed_reports_views import (
            ActiveForceReportView, 
            TempInactiveReportsView,
            PermInactiveReportsView,
            AuditMovementReportsView
        )
        
        report_map = {
            'report_1': (WorkforceSummaryReportView, "خلاصة القوة العاملة بحسب الرتبة"),
            'report_2': (CategoricalWorkforceReportView, "خلاصة القوة العاملة - فئوي"),
            'report_3': (NonWorkforceReportView, "خلاصة القوة غير العاملة"),
            'report_4': (ActiveForceReportView, "كشف القوة العاملة فعلياً"),
            'report_5': (TempInactiveReportsView, "كشف المرضى المتواجدين في المستشفى"),
            'report_6': (TempInactiveReportsView, "كشف بالقوة غير العاملة مؤقتاً مرافقين"),
            'report_7': (TempInactiveReportsView, "كشف المنتدبين لدى جهات"),
            'report_8': (TempInactiveReportsView, "كشف المفرغين للدراسة"),
            'report_9': (TempInactiveReportsView, "كشف السجناء"),
            'report_10': (TempInactiveReportsView, "كشف الإجازات الرسمية"),
            'report_11': (TempInactiveReportsView, "كشف بالقوة غير العاملة مؤقتاً مفقودين"),
            'report_12': (PermInactiveReportsView, "كشف كبار السن"),
            'report_13': (PermInactiveReportsView, "كشف إنهاء الخدمة"),
            'report_14': (PermInactiveReportsView, "كشف مرشحين للتقاعد"),
            'report_15': (PermInactiveReportsView, "كشف عدم اللياقة (عجز طبي)"),
            'report_16': (PermInactiveReportsView, "كشف شهداء ووفيات"),
            'report_17': (PermInactiveReportsView, "كشف متقاعدين (القرار النهائي)"),
            'report_18': (AuditMovementReportsView, "كشف الواصلين من الوزارة"),
            'report_19': (AuditMovementReportsView, "كشف العازمين إلى الوزارة"),
            'report_20': (AuditMovementReportsView, "كشف العازمين - تفصيلي مقارن"),
            'report_21': (AuditMovementReportsView, "كشف العاملين لدينا (انتداب للداخل)"),
            'report_22': (AuditMovementReportsView, "كشف العاملين بالخارج (انتداب للخارج)"),
            'report_23': (AuditMovementReportsView, "كشف المطلوب تصحيح أسماؤهم"),
            'report_24a': (AuditMovementReportsView, "كشف الغياب المؤقت"),
            'report_24b': (AuditMovementReportsView, "كشف الفرار (الغياب المستمر)"),
            'report_25': (AuditMovementReportsView, "كشف الملتحقين بالعدوان"),
        }
        
        if export_req.report_id not in report_map:
            return Response({"error": "هذا التقرير غير مدعوم للتصدير حالياً."}, status=status.HTTP_400_BAD_REQUEST)
            
        view_class, report_title = report_map[export_req.report_id]
        
        # Call the view to get the aggregated data
        view_instance = view_class()
        
        # Add report_id to query_params for TempInactiveReportsView to filter correctly
        request.GET = request.GET.copy()
        request.GET['report_id'] = export_req.report_id
        
        # We need to simulate a request or just pass the current request
        response = view_instance.get(request)
        if response.status_code != 200:
            return Response({"error": "فشل في تجميع بيانات التقرير."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        data = response.data
        data_list = data.get('data', [])
        grand_totals = data.get('totals', {})
        
        if not data_list:
            return Response({"error": "لا توجد بيانات لتصديرها."}, status=status.HTTP_400_BAD_REQUEST)

        # Build columns and rows based on report type
        if export_req.report_id in ['report_1', 'report_2', 'report_3']:
            columns = ["م", "الجهة"]
            
            # Get dynamic columns from the first row's keys
            first_row = data_list[0]
            dynamic_keys_field = 'ranks' if 'ranks' in first_row else 'categories'
            dynamic_cols = list(first_row.get(dynamic_keys_field, {}).keys())
            
            columns.extend(dynamic_cols)
            columns.append("المجموع")
            
            rows = []
            for idx, item in enumerate(data_list, start=1):
                row = [idx, item.get('unit_name', 'غير محدد')]
                for col in dynamic_cols:
                    row.append(item.get(dynamic_keys_field, {}).get(col, 0))
                row.append(item.get('total', 0))
                rows.append(row)
                
            # Build totals row
            total_row = ["", "الإجمالي العام"]
            total_sum = 0
            for col in dynamic_cols:
                val = grand_totals.get(col, 0)
                total_row.append(val)
                total_sum += val
            total_row.append(total_sum)
        else:
            # For detailed reports 4-11
            # Dynamic columns based on the keys of the first item
            first_row = data_list[0]
            
            # Translate keys to Arabic headers
            header_translation = {
                'index': 'م',
                'rank': 'الرتبة',
                'military_number': 'الرقم العسكري',
                'full_name': 'الاسم',
                'unit': 'الإدارة / الجهة',
                'position': 'المنصب / العمل الحالي',
                'hospital': 'اسم المستشفى',
                'entry_date': 'تاريخ الدخول',
                'medical_report': 'التقرير الطبي',
                'escort_source': 'مصدر الأمر',
                'escort_name': 'اسم الشخصية',
                'duration_from': 'من تاريخ',
                'duration_to': 'إلى تاريخ',
                'delegate_to': 'جهة الانتداب',
                'delegate_purpose': 'الغرض من الانتداب',
                'study_type': 'نوع الدراسة',
                'study_location': 'جهة الدراسة',
                'case_type': 'نوع القضية',
                'arrest_date': 'تاريخ التوقيف',
                'verdict_type': 'نوع الحكم',
                'vacation_type': 'نوع الإجازة',
                'missing_date': 'تاريخ الفقدان',
                'court_order': 'حكم شرعي بالفقدان',
                'notes': 'ملاحظات'
            }
            
            columns = [header_translation.get(k, k) for k in first_row.keys()]
            rows = [[item.get(k, "") for k in first_row.keys()] for item in data_list]
            total_row = None
        
        # Generate Excel
        excel_buffer = generate_report_excel(report_title, columns, rows, total_row)
        
        # Return as downloadable file
        http_response = HttpResponse(
            excel_buffer.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        # Safe ascii filename, will use report_id
        http_response['Content-Disposition'] = f'attachment; filename="export_{export_req.report_id}.xlsx"'
        return http_response
