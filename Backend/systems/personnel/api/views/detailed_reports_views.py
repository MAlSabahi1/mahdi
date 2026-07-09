from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.models import Q, F, CharField
from django.db.models.functions import Coalesce

from ...models import PersonnelMaster

class BaseDetailedReportView(APIView):
    """
    Base view for detailed personnel reports (Models 4 to 11).
    """
    permission_classes = [IsAuthenticated] # Should be BaseReportPermission in production

    def get_queryset(self):
        return PersonnelMaster.objects.select_related(
            'current_rank', 
            'current_status', 
            'central_department', 
            'branch', 
            'district_police',
            'qualification'
        ).filter(is_deleted=False)

    def get_unit_name(self, p):
        if p.central_department:
            return p.central_department.name
        if p.branch:
            return p.branch.name
        if p.district_police:
            return p.district_police.name
        if p.security_admin:
            return p.security_admin.name
        return "غير محدد"

    def format_base_data(self, p, idx):
        return {
            "index": idx,
            "rank": p.current_rank.name if p.current_rank else "غير محدد",
            "military_number": p.military_number,
            "full_name": p.full_name,
            "unit": self.get_unit_name(p),
            "notes": p.notes or ""
        }


class ActiveForceReportView(BaseDetailedReportView):
    """
    نموذج رقم (4): كشف القوة العاملة فعلياً
    """
    def get(self, request, *args, **kwargs):
        level_filter = request.query_params.get('level', 'all')
        qs = self.get_queryset().filter(current_status__classification='active_full')

        if level_filter == 'central':
            qs = qs.filter(central_department__isnull=False)
        elif level_filter == 'branch':
            qs = qs.filter(branch__isnull=False)
        elif level_filter == 'district':
            qs = qs.filter(district_police__isnull=False)

        # Pagination could be added here for large datasets, but for reports we usually return all or paginate explicitly
        data_list = []
        for idx, p in enumerate(qs, start=1):
            row = self.format_base_data(p, idx)
            row["service_type"] = p.current_status.name if p.current_status else "قوة عاملة"
            row["national_id"] = p.national_id
            row["qualification"] = p.qualification.name if p.qualification else "بدون مؤهل"
            data_list.append(row)

        return Response({
            "data": data_list,
            "total_count": len(data_list)
        })


class TempInactiveReportsView(BaseDetailedReportView):
    """
    نماذج رقم (5-11): كشوفات القوة غير العاملة مؤقتاً
    """
    def get(self, request, *args, **kwargs):
        report_id = request.query_params.get('report_id')
        qs = self.get_queryset().filter(current_status__classification='inactive_temp')

        # Map report_id to the specific status name (these should match DB status names)
        # Assuming DB has statuses like 'مريض', 'مسجون', 'مرافق', etc.
        status_map = {
            'report_5': 'مريض',
            'report_6': 'مرافق',
            'report_7': 'منتدب',
            'report_8': 'مفرغ للدراسة',
            'report_9': 'مسجون',
            'report_10': 'إجازة رسمية',
            'report_11': 'مفقود'
        }

        target_status = status_map.get(report_id)
        if target_status:
            qs = qs.filter(current_status__name__contains=target_status)

        data_list = []
        for idx, p in enumerate(qs, start=1):
            row = self.format_base_data(p, idx)
            temp_details = p.temp_status_details or {}
            
            if report_id == 'report_5':
                row["hospital"] = temp_details.get("hospital", "غير مدخل")
                row["entry_date"] = temp_details.get("entry_date", "غير مدخل")
                row["medical_report"] = temp_details.get("medical_report", "غير مدخل")
            elif report_id == 'report_6':
                row["order_source"] = temp_details.get("escort_source", temp_details.get("order_source", "غير مدخل"))
                row["escort_name"] = temp_details.get("escort_name", "غير مدخل")
                row["escort_position"] = temp_details.get("escort_position", temp_details.get("dignitary_position", "غير مدخل"))
                row["duration_from"] = temp_details.get("duration_from", temp_details.get("start_date", "غير مدخل"))
                row["duration_to"] = temp_details.get("duration_to", temp_details.get("end_date", "غير مدخل"))
            elif report_id == 'report_7':
                row["order_source"] = temp_details.get("order_source", "غير مدخل")
                row["delegate_to"] = temp_details.get("delegate_to", temp_details.get("destination", "غير مدخل"))
                row["delegate_purpose"] = temp_details.get("delegate_purpose", temp_details.get("reason", "غير مدخل"))
                row["duration_from"] = temp_details.get("duration_from", temp_details.get("start_date", "غير مدخل"))
                row["duration_to"] = temp_details.get("duration_to", temp_details.get("end_date", "غير مدخل"))
            elif report_id == 'report_8':
                row["study_type"] = temp_details.get("study_type", "غير مدخل")
                row["study_location"] = temp_details.get("study_location", temp_details.get("institution", "غير مدخل"))
                row["order_number"] = temp_details.get("order_number", temp_details.get("order_source", "غير مدخل"))
                row["duration_from"] = temp_details.get("duration_from", temp_details.get("start_date", "غير مدخل"))
                row["duration_to"] = temp_details.get("duration_to", temp_details.get("end_date", "غير مدخل"))
            elif report_id == 'report_9':
                row["case_type"] = temp_details.get("case_type", "غير مدخل")
                row["arrest_date"] = temp_details.get("arrest_date", "غير مدخل")
                row["verdict_type"] = temp_details.get("verdict_type", temp_details.get("sentence_duration", "غير مدخل"))
                row["duration_from"] = temp_details.get("duration_from", temp_details.get("start_date", "غير مدخل"))
                row["duration_to"] = temp_details.get("duration_to", temp_details.get("end_date", "غير مدخل"))
            elif report_id == 'report_10':
                row["vacation_type"] = temp_details.get("vacation_type", "غير مدخل")
                row["order_source"] = temp_details.get("order_source", "غير مدخل")
                row["duration_from"] = temp_details.get("duration_from", temp_details.get("start_date", "غير مدخل"))
                row["duration_to"] = temp_details.get("duration_to", temp_details.get("end_date", "غير مدخل"))
            elif report_id == 'report_11':
                row["missing_date"] = temp_details.get("missing_date", "غير مدخل")
                row["procedures_status"] = temp_details.get("legal_status", temp_details.get("procedures_status", "غير مستكمل"))

            data_list.append(row)

        return Response({
            "data": data_list,
            "total_count": len(data_list)
        })


class PermInactiveReportsView(BaseDetailedReportView):
    """
    نماذج رقم (12-17): كشوفات القوة غير العاملة نهائياً
    """
    def get(self, request, *args, **kwargs):
        report_id = request.query_params.get('report_id')
        qs = self.get_queryset().filter(current_status__classification='inactive_perm')

        status_map = {
            'report_12': 'بلوغ السن',
            'report_13': 'إنهاء المدة',
            'report_14': 'مرشح تقاعد',
            'report_15': 'عدم لياقة',
            'report_17': 'متقاعد'
        }
        
        # In a real app we might map 'متوفى' and 'شهيد' to report_16, for simplicity we filter generally or specifically
        target_status = status_map.get(report_id)
        if target_status:
            qs = qs.filter(current_status__name__contains=target_status)
        elif report_id == 'report_16':
            qs = qs.filter(Q(current_status__name__contains='شهيد') | Q(current_status__name__contains='شهداء') | Q(current_status__name__contains='متوفى') | Q(current_status__name__contains='وفيات'))

        data_list = []
        for idx, p in enumerate(qs, start=1):
            row = self.format_base_data(p, idx)
            row["birth_date"] = p.birth_date or "غير مدخل"
            row["join_date"] = p.join_date or "غير مدخل"
            
            perm_details = p.perm_status_details or {}
            
            if report_id == 'report_12':
                row["personal_request"] = perm_details.get("personal_request", "غير مدخل")
            elif report_id == 'report_13':
                row["total_years"] = perm_details.get("total_years", "غير مدخل")
                row["person_request"] = perm_details.get("person_request", "غير مدخل")
            elif report_id == 'report_14':
                row["reason"] = perm_details.get("reason", "غير مدخل")
                row["procedures"] = perm_details.get("procedures", "غير مدخل")
            elif report_id == 'report_15':
                row["disease_type"] = perm_details.get("disease_type", "غير مدخل")
                row["disability_ratio"] = perm_details.get("disability_ratio", "غير مدخل")
                row["incident_date"] = perm_details.get("incident_date", "غير مدخل")
                row["medical_source"] = perm_details.get("medical_source", "غير مدخل")
                row["incident_type"] = perm_details.get("incident_type", "غير مدخل")
            elif report_id == 'report_16':
                row["case_type"] = p.current_status.name if p.current_status else "غير مدخل"
                row["death_date"] = perm_details.get("death_date", "غير مدخل")
                row["incident_type"] = perm_details.get("incident_type", "غير مدخل")
            elif report_id == 'report_17':
                row["decision_number"] = perm_details.get("decision_number", "غير مدخل")
                row["decision_date"] = perm_details.get("decision_date", "غير مدخل")

            data_list.append(row)

        return Response({
            "data": data_list,
            "total_count": len(data_list)
        })


class AuditMovementReportsView(BaseDetailedReportView):
    """
    نماذج رقم (18-25): كشوفات التدقيق وحركة القوة
    """
    def get(self, request, *args, **kwargs):
        report_id = request.query_params.get('report_id')
        
        # Only fetch personnel with audit_movement_details
        qs = self.get_queryset().filter(audit_movement_details__isnull=False)

        # Apply specific filters based on report_id by checking for required keys
        if report_id == 'report_18':
            qs = qs.filter(audit_movement_details__has_key='arrived_from')
        elif report_id == 'report_19':
            qs = qs.filter(audit_movement_details__has_key='transfer_reason')
        elif report_id == 'report_20':
            qs = qs.filter(audit_movement_details__has_key='new_directed_workplace')
        elif report_id == 'report_21':
            qs = qs.filter(audit_movement_details__has_key='salary_source')
        elif report_id == 'report_22':
            qs = qs.filter(audit_movement_details__has_key='external_delegate_target')
        elif report_id == 'report_23':
            qs = qs.filter(audit_movement_details__has_key='wrong_name')
        elif report_id == 'report_24a':
            qs = qs.filter(audit_movement_details__has_key='absence_days')
        elif report_id == 'report_24b':
            qs = qs.filter(audit_movement_details__has_key='continuous_absence_duration')
        elif report_id == 'report_25':
            qs = qs.filter(audit_movement_details__has_key='reporter_entity')

        data_list = []
        for idx, p in enumerate(qs, start=1):
            row = self.format_base_data(p, idx)
            audit_details = p.audit_movement_details or {}
            
            if report_id == 'report_18':
                row["new_workplace"] = audit_details.get("new_workplace", "غير مدخل")
                row["arrived_from"] = audit_details.get("arrived_from", "غير مدخل")
                row["start_date"] = audit_details.get("start_date", "غير مدخل")
            elif report_id == 'report_19':
                row["old_workplace"] = audit_details.get("old_workplace", "غير مدخل")
                row["old_service_type"] = audit_details.get("old_service_type", "غير مدخل")
                row["transfer_date"] = audit_details.get("transfer_date", "غير مدخل")
                row["transfer_reason"] = audit_details.get("transfer_reason", "غير مدخل")
            elif report_id == 'report_20':
                row["old_workplace"] = audit_details.get("old_workplace", "غير مدخل")
                row["old_service_type"] = audit_details.get("old_service_type", "غير مدخل")
                row["new_directed_workplace"] = audit_details.get("new_directed_workplace", "غير مدخل")
                row["new_service_type"] = audit_details.get("new_service_type", "غير مدخل")
            elif report_id == 'report_21':
                row["current_workplace"] = audit_details.get("current_workplace", "غير مدخل")
                row["actual_service_type"] = audit_details.get("actual_service_type", "غير مدخل")
                row["salary_source"] = audit_details.get("salary_source", "غير مدخل")
                row["start_date"] = audit_details.get("start_date", "غير مدخل")
            elif report_id == 'report_22':
                row["old_workplace"] = audit_details.get("old_workplace", "غير مدخل")
                row["old_service_type"] = audit_details.get("old_service_type", "غير مدخل")
                row["transfer_date"] = audit_details.get("transfer_date", "غير مدخل")
                row["external_delegate_target"] = audit_details.get("external_delegate_target", "غير مدخل")
            elif report_id == 'report_23':
                row["national_id"] = p.national_id
                row["wrong_name"] = audit_details.get("wrong_name", "غير مدخل")
                row["correction_target"] = audit_details.get("correction_target", "غير مدخل")
            elif report_id == 'report_24a':
                row["national_id"] = p.national_id
                row["stop_reason"] = audit_details.get("stop_reason", "غير مدخل")
                row["absence_days"] = audit_details.get("absence_days", "غير مدخل")
            elif report_id == 'report_24b':
                row["national_id"] = p.national_id
                row["stop_reason"] = audit_details.get("stop_reason", "غير مدخل")
                row["continuous_absence_duration"] = audit_details.get("continuous_absence_duration", "غير مدخل")
            elif report_id == 'report_25':
                row["national_id"] = p.national_id
                row["reporter_entity"] = audit_details.get("reporter_entity", "غير مدخل")
                row["taken_procedures"] = audit_details.get("taken_procedures", "غير مدخل")

            data_list.append(row)

        return Response({
            "data": data_list,
            "total_count": len(data_list)
        })
