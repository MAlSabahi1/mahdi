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
        from infra.authorization.services.permission_service import PermissionService
        qs = PersonnelMaster.objects.select_related(
            'current_rank', 
            'current_status', 
            'central_department', 
            'branch', 
            'district_police',
            'qualification'
        ).filter(is_deleted=False)
        return PermissionService.get_scoped_queryset(
            self.request.user, qs, 'personnel.view.*'
        )

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
            'report_5': 'الأمراض',        # الأمراض والمصابين
            'report_6': 'المرافقة',     # المفرغين للمرافقة
            'report_7': 'المنتدبين',    # المنتدبين لدى جهات
            'report_8': 'للدراسة',      # المفرغين للدراسة
            'report_9': 'السجناء',       # السجناء
            'report_10': 'الإجازات',    # الإجازات
            'report_11': 'المفقودين',   # المفقودين
        }

        target_status = status_map.get(report_id)
        if target_status:
            qs = qs.filter(current_status__name__contains=target_status)

        data_list = []
        
        # خريطة: نوع التقرير → form_type الخاص به في StatusChangeForm
        report_to_form_type = {
            'report_5': 'sick',
            'report_6': 'escort',
            'report_7': 'seconded',      # اسم الاستمارة في قاعدة البيانات هو seconded
            'report_8': 'study_leave',  # الاسم الحقيقي في DB
            'report_9': 'imprisoned',
            'report_10': 'vacation',
            'report_11': 'missing',
        }
        
        from systems.services.infrastructure.models.status_change import StatusChangeForm as SCForm
        
        for idx, p in enumerate(qs, start=1):
            row = self.format_base_data(p, idx)
            temp_details = p.temp_status_details or {}
            
            # ── Fallback: إذا كان temp_status_details فارغاً، نقرأ من آخر استمارة معتمدة ──
            if not temp_details and report_id in report_to_form_type:
                form_type_key = report_to_form_type[report_id]
                last_form = SCForm.objects.filter(
                    personnel=p,
                    form_type__icontains=form_type_key,
                    status='approved'
                ).order_by('-updated_at').first()
                if last_form and last_form.form_data:
                    temp_details = last_form.form_data
            
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
                # مفاتيح بديلة: destination أو delegate_to أو delegate_destination
                row["delegate_to"] = temp_details.get("delegate_to",
                    temp_details.get("destination",
                    temp_details.get("delegate_destination", "غير مدخل")))
                # مفاتيح بديلة: reason أو delegate_purpose أو purpose
                row["delegate_purpose"] = temp_details.get("delegate_purpose",
                    temp_details.get("reason",
                    temp_details.get("purpose", "غير مدخل")))
                # مفاتيح بديلة: start_date أو duration_from أو date_from
                row["duration_from"] = temp_details.get("duration_from",
                    temp_details.get("start_date",
                    temp_details.get("date_from", "غير مدخل")))
                # مفاتيح بديلة: end_date أو duration_to أو date_to
                row["duration_to"] = temp_details.get("duration_to",
                    temp_details.get("end_date",
                    temp_details.get("date_to", "غير مدخل")))
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

        # خريطة form_type للتقارير 12-17 للبحث في StatusChangeForm ك**Fallback**
        perm_report_form_type = {
            'report_12': 'retirement_age',
            'report_13': 'end_of_service',
            'report_14': 'retirement_candidate',
            'report_15': 'medical_unfit',
            'report_16': ['martyr', 'death'],
            'report_17': 'retired',
        }
        
        from systems.services.infrastructure.models.status_change import StatusChangeForm as SCForm

        data_list = []
        for idx, p in enumerate(qs, start=1):
            row = self.format_base_data(p, idx)
            row["birth_date"] = p.birth_date or "غير مدخل"
            row["join_date"] = p.join_date or "غير مدخل"
            
            perm_details = p.perm_status_details or {}
            
            # ── Fallback: إذا كان perm_status_details فارغاً، نقرأ من آخر استمارة معتمدة ──
            if not perm_details and report_id in perm_report_form_type:
                ft = perm_report_form_type[report_id]
                form_types = ft if isinstance(ft, list) else [ft]
                last_form = SCForm.objects.filter(
                    personnel=p,
                    form_type__in=form_types,
                    status='approved'
                ).order_by('-updated_at').first()
                if last_form and last_form.form_data:
                    perm_details = last_form.form_data
            
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
        from systems.services.infrastructure.models.status_change import StatusChangeForm as SCForm

        # ── نموذج 23: المطلوب تصحيح أسمائهم — من جدول SuggestedCorrection ──
        if report_id == 'report_23':
            from systems.personnel.models import SuggestedCorrection
            corrections = SuggestedCorrection.objects.select_related(
                'personnel__current_rank'
            ).filter(
                field_name__in=['full_name', 'name_correction'],
                status='pending'
            ).order_by('created_at')
            
            data_list = []
            for idx, c in enumerate(corrections, start=1):
                p = c.personnel
                data_list.append({
                    "index": idx,
                    "rank": p.current_rank.name if p.current_rank else "غير محدد",
                    "military_number": p.military_number,
                    "full_name": p.full_name,
                    "national_id": p.national_id,
                    "wrong_name": c.old_value or p.full_name,
                    "correction_target": c.new_value or "غير مدخل",
                    "notes": c.notes or ""
                })
            return Response({"data": data_list, "total_count": len(data_list)})

        # ── نموذج 25: الملتحقين بالعدوان — من حالة PersonnelMaster ──
        if report_id == 'report_25':
            qs = self.get_queryset().filter(
                current_status__name__icontains='العدوان'
            )
            data_list = []
            for idx, p in enumerate(qs, start=1):
                row = self.format_base_data(p, idx)
                row["national_id"] = p.national_id
                # حاول قراءة التفاصيل من audit_movement_details أو StatusChangeForm
                details = p.audit_movement_details or {}
                if not details:
                    last_form = SCForm.objects.filter(
                        personnel=p, status='approved'
                    ).order_by('-updated_at').first()
                    if last_form and last_form.form_data:
                        details = last_form.form_data
                row["reporter_entity"] = details.get("reporter_entity", "غير مدخل")
                row["taken_procedures"] = details.get("taken_procedures", "غير مدخل")
                data_list.append(row)
            return Response({"data": data_list, "total_count": len(data_list)})

        # ── نماذج 18-22, 24أ, 24ب: تقرأ من StatusChangeForm حسب نوع الاستمارة ──
        # خريطة التقرير → (form_type, الحقول المطلوبة)
        form_type_map = {
            'report_18': 'arrived',         # واصلين من الوزارة
            'report_19': 'transfer_out',    # عازمين للوزارة
            'report_20': 'transfer_detail', # عازمين (مقارن)
            'report_21': 'internal_seconded', # انتداب للداخل
            'report_22': 'external_seconded', # انتداب للخارج
            'report_24a': 'absence_temp',   # غياب مؤقت
            'report_24b': 'absence_perm',   # فرار/غياب مستمر
        }

        ft = form_type_map.get(report_id)
        
        # إذا كان النوع معروفاً، نقرأ من StatusChangeForm مباشرة
        if ft:
            scforms = SCForm.objects.select_related(
                'personnel__current_rank'
            ).filter(
                form_type__icontains=ft,
                status='approved'
            ).order_by('-updated_at')

            data_list = []
            for idx, f in enumerate(scforms, start=1):
                p = f.personnel
                if not p:
                    continue
                fd = f.form_data or {}
                row = {
                    "index": idx,
                    "rank": p.current_rank.name if p.current_rank else "غير محدد",
                    "military_number": p.military_number,
                    "full_name": p.full_name,
                    "unit": "",
                    "notes": ""
                }
                if report_id == 'report_18':
                    row["new_workplace"] = fd.get("new_workplace", fd.get("destination", "غير مدخل"))
                    row["arrived_from"] = fd.get("arrived_from", fd.get("source", "غير مدخل"))
                    row["start_date"] = fd.get("start_date", fd.get("date", "غير مدخل"))
                elif report_id == 'report_19':
                    row["old_workplace"] = fd.get("old_workplace", fd.get("unit", "غير مدخل"))
                    row["old_service_type"] = fd.get("old_service_type", "غير مدخل")
                    row["transfer_date"] = fd.get("transfer_date", fd.get("date", "غير مدخل"))
                    row["transfer_reason"] = fd.get("transfer_reason", fd.get("reason", "غير مدخل"))
                elif report_id == 'report_20':
                    row["old_workplace"] = fd.get("old_workplace", "غير مدخل")
                    row["old_service_type"] = fd.get("old_service_type", "غير مدخل")
                    row["new_directed_workplace"] = fd.get("new_directed_workplace", fd.get("destination", "غير مدخل"))
                    row["new_service_type"] = fd.get("new_service_type", "غير مدخل")
                elif report_id == 'report_21':
                    row["current_workplace"] = fd.get("current_workplace", fd.get("destination", "غير مدخل"))
                    row["actual_service_type"] = fd.get("actual_service_type", "غير مدخل")
                    row["salary_source"] = fd.get("salary_source", fd.get("order_source", "غير مدخل"))
                    row["start_date"] = fd.get("start_date", "غير مدخل")
                elif report_id == 'report_22':
                    row["old_workplace"] = fd.get("old_workplace", "غير مدخل")
                    row["old_service_type"] = fd.get("old_service_type", "غير مدخل")
                    row["transfer_date"] = fd.get("transfer_date", fd.get("start_date", "غير مدخل"))
                    row["external_delegate_target"] = fd.get("external_delegate_target", fd.get("destination", "غير مدخل"))
                elif report_id == 'report_24a':
                    row["national_id"] = p.national_id
                    row["stop_reason"] = fd.get("stop_reason", fd.get("reason", "غير مدخل"))
                    row["absence_days"] = fd.get("absence_days", fd.get("days", "غير مدخل"))
                elif report_id == 'report_24b':
                    row["national_id"] = p.national_id
                    row["stop_reason"] = fd.get("stop_reason", fd.get("reason", "غير مدخل"))
                    row["continuous_absence_duration"] = fd.get("continuous_absence_duration", fd.get("duration", "غير مدخل"))
                data_list.append(row)
            
            return Response({"data": data_list, "total_count": len(data_list)})

        # Fallback عام إذا لم يُعرف النوع
        return Response({"data": [], "total_count": 0, "message": "نوع التقرير غير محدد"})


