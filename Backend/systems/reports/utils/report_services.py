import io
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

from systems.personnel.api.views.reports_views import WorkforceSummaryReportView
from systems.reports.api.views import CategoricalWorkforceReportView, NonWorkforceReportView
from systems.personnel.api.views.detailed_reports_views import (
    ActiveForceReportView, 
    TempInactiveReportsView,
    PermInactiveReportsView,
    AuditMovementReportsView
)
from systems.reports.utils.excel_generator import generate_report_excel
from systems.reports.models import ExportRequest

def generate_export_response(export_req, request):
    """
    Handles fetching data for a given export request and generating the Excel file.
    """
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
    
    view_instance = view_class()
    
    # Add report_id to query_params for views to filter correctly
    request.GET = request.GET.copy()
    request.GET['report_id'] = export_req.report_id
    
    response = view_instance.get(request)
    if response.status_code != 200:
        return Response({"error": "فشل في تجميع بيانات التقرير."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    data = response.data
    data_list = data.get('data', [])
    grand_totals = data.get('totals', {})
    
    if not data_list:
        return Response({"error": "لا توجد بيانات لتصديرها."}, status=status.HTTP_400_BAD_REQUEST)

    if export_req.report_id in ['report_1', 'report_2', 'report_3']:
        columns = ["م", "الجهة"]
        
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
            
        total_row = ["", "الإجمالي العام"]
        total_sum = 0
        for col in dynamic_cols:
            val = grand_totals.get(col, 0)
            total_row.append(val)
            total_sum += val
        total_row.append(total_sum)
    else:
        first_row = data_list[0]
        
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
            'notes': 'ملاحظات',
            'birth_date': 'تاريخ الميلاد',
            'join_date': 'تاريخ الالتحاق',
            'personal_request': 'بناء على طلب شخصي',
            'total_years': 'إجمالي سنوات الخدمة',
            'person_request': 'طلب شخصي',
            'reason': 'السبب',
            'procedures': 'الإجراءات',
            'disease_type': 'نوع المرض/الإصابة',
            'disability_ratio': 'نسبة العجز',
            'incident_date': 'تاريخ الواقعة',
            'medical_source': 'مصدر التقرير',
            'incident_type': 'نوع الواقعة',
            'death_date': 'تاريخ الوفاة',
            'decision_number': 'رقم القرار',
            'decision_date': 'تاريخ القرار',
            'new_workplace': 'جهة العمل الجديدة',
            'arrived_from': 'واصل من',
            'start_date': 'تاريخ المباشرة',
            'old_workplace': 'جهة العمل السابقة',
            'old_service_type': 'نوع الخدمة السابقة',
            'transfer_date': 'تاريخ النقل',
            'transfer_reason': 'سبب النقل',
            'new_directed_workplace': 'الجهة الموجه إليها',
            'new_service_type': 'نوع الخدمة الجديدة',
            'current_workplace': 'جهة العمل الحالية',
            'actual_service_type': 'نوع الخدمة الفعلي',
            'salary_source': 'جهة صرف الراتب',
            'external_delegate_target': 'جهة الانتداب الخارجي',
            'national_id': 'الرقم الوطني',
            'wrong_name': 'الاسم الخطأ',
            'correction_target': 'الاسم الصحيح',
            'stop_reason': 'سبب الإيقاف',
            'absence_days': 'أيام الغياب',
            'continuous_absence_duration': 'مدة الانقطاع/الفرار',
            'reporter_entity': 'الجهة المبلغة',
            'taken_procedures': 'الإجراءات المتخذة'
        }
        
        columns = [header_translation.get(k, k) for k in first_row.keys()]
        rows = [[item.get(k, "") for k in first_row.keys()] for item in data_list]
        total_row = None
    
    excel_buffer = generate_report_excel(report_title, columns, rows, total_row)
    
    http_response = HttpResponse(
        excel_buffer.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    http_response['Content-Disposition'] = f'attachment; filename="export_{export_req.report_id}.xlsx"'
    return http_response
