from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.models import Q, F, CharField
from django.db.models.functions import Coalesce

from ...models import PersonnelMaster

class BaseDetailedReportView(APIView):
    """
    Base view for detailed personnel reports (Models 4-25).
    Supports optional ?month=YYYY-MM filter for monthly reporting.
    """
    permission_classes = [IsAuthenticated]

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

    def parse_month_range(self):
        """
        Parse ?month=YYYY-MM query param.
        Returns (date_from, date_to) or (None, None) if not provided.
        Usage:
            date_from, date_to = self.parse_month_range()
            if date_from:
                qs = qs.filter(updated_at__date__gte=date_from,
                               updated_at__date__lte=date_to)
        """
        import calendar
        from datetime import date
        month_str = self.request.query_params.get('month', '').strip()
        if not month_str:
            return None, None
        try:
            year, month = map(int, month_str.split('-'))
            date_from = date(year, month, 1)
            last_day  = calendar.monthrange(year, month)[1]
            date_to   = date(year, month, last_day)
            return date_from, date_to
        except (ValueError, AttributeError):
            return None, None

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

        # فلتر شهري: يعرض من انتقل إلى القوة العاملة خلال الشهر المحدد
        date_from, date_to = self.parse_month_range()
        if date_from:
            qs = qs.filter(updated_at__date__gte=date_from, updated_at__date__lte=date_to)

        data_list = []
        for idx, p in enumerate(qs, start=1):
            row = self.format_base_data(p, idx)
            row['service_type']  = p.current_status.name if p.current_status else 'قوة عاملة'
            row['national_id']   = p.national_id
            row['qualification'] = p.qualification.name if p.qualification else 'بدون مؤهل'
            data_list.append(row)

        return Response({'data': data_list, 'total_count': len(data_list),
                         'month_filter': request.query_params.get('month', 'الكل')})


class TempInactiveReportsView(BaseDetailedReportView):
    """
    نماذج رقم (5-11): كشوفات القوة غير العاملة مؤقتاً
    """
    def get(self, request, *args, **kwargs):
        report_id = request.query_params.get('report_id')
        qs = self.get_queryset().filter(current_status__classification='inactive_temp')

        # Map report_id to the specific status name (these should match DB status names)
        # Assuming DB has statuses like 'أمراض ومصابين', 'سجناء', 'مفرغين للمرافقة', etc.
        status_map = {
            'report_5': 'أمراض',        # أمراض ومصابين
            'report_6': 'مرافقة',       # مفرغين للمرافقة
            'report_7': 'منتدبين',      # منتدبين لدى جهات
            'report_8': 'دراسة',        # مفرغين للدراسة
            'report_9': 'سجناء',        # سجناء
            'report_10': 'إجازات',      # إجازات
            'report_11': 'مفقودين',     # مفقودين
        }

        target_status = status_map.get(report_id)
        if target_status:
            qs = qs.filter(current_status__name__contains=target_status)

        # فلتر شهري: من انتقل إلى هذه الحالة خلال الشهر المحدد
        date_from, date_to = self.parse_month_range()
        if date_from:
            qs = qs.filter(updated_at__date__gte=date_from, updated_at__date__lte=date_to)

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
            
            if temp_details and temp_details.get("notes"):
                row["notes"] = temp_details.get("notes")
            
            if report_id == 'report_5':
                row["hospital"] = temp_details.get("hospital", "غير مدخل")
                row["entry_date"] = temp_details.get("entry_date", "غير مدخل")
                row["medical_report"] = temp_details.get("medical_report", "غير مدخل")
            elif report_id == 'report_6':
                row["order_source"] = temp_details.get("order_source", temp_details.get("escort_source", "غير مدخل"))
                row["dignitary_name"] = temp_details.get("dignitary_name", temp_details.get("escort_name", "غير مدخل"))
                row["dignitary_position"] = temp_details.get("dignitary_position", temp_details.get("escort_position", "غير مدخل"))
                row["start_date"] = temp_details.get("start_date", temp_details.get("duration_from", "غير مدخل"))
                row["end_date"] = temp_details.get("end_date", temp_details.get("duration_to", "غير مدخل"))
            elif report_id == 'report_7':
                row["order_source"] = temp_details.get("order_source", "غير مدخل")
                row["secondment_place"] = temp_details.get("secondment_place", temp_details.get("delegate_to", temp_details.get("destination", "غير مدخل")))
                row["reason"] = temp_details.get("reason", temp_details.get("delegate_purpose", temp_details.get("purpose", "غير مدخل")))
                row["start_date"] = temp_details.get("start_date", temp_details.get("duration_from", temp_details.get("date_from", "غير مدخل")))
                row["end_date"] = temp_details.get("end_date", temp_details.get("duration_to", temp_details.get("date_to", "غير مدخل")))
            elif report_id == 'report_8':
                row["study_type"] = temp_details.get("study_type", "غير مدخل")
                row["institution"] = temp_details.get("institution", temp_details.get("study_location", "غير مدخل"))
                row["order_source"] = temp_details.get("order_source", temp_details.get("order_number", "غير مدخل"))
                row["start_date"] = temp_details.get("start_date", temp_details.get("duration_from", "غير مدخل"))
                row["end_date"] = temp_details.get("end_date", temp_details.get("duration_to", "غير مدخل"))
            elif report_id == 'report_9':
                row["case_type"] = temp_details.get("case_type", "غير مدخل")
                row["arrest_date"] = temp_details.get("arrest_date", "غير مدخل")
                row["verdict_type"] = temp_details.get("verdict_type", temp_details.get("ruling_type", temp_details.get("sentence_duration", "غير مدخل")))
                row["ruling_date"] = temp_details.get("ruling_date", "غير مدخل")
                row["duration_from"] = temp_details.get("duration_from", temp_details.get("sentence_start_date", temp_details.get("start_date", "غير مدخل")))
                row["duration_to"] = temp_details.get("duration_to", temp_details.get("sentence_end_date", temp_details.get("end_date", "غير مدخل")))
            elif report_id == 'report_10':
                row["leave_type"] = temp_details.get("leave_type", temp_details.get("vacation_type", "غير مدخل"))
                row["order_source"] = temp_details.get("order_source", "غير مدخل")
                row["start_date"] = temp_details.get("start_date", temp_details.get("duration_from", "غير مدخل"))
                row["end_date"] = temp_details.get("end_date", temp_details.get("duration_to", "غير مدخل"))
            elif report_id == 'report_11':
                row["missing_date"] = temp_details.get("missing_date", "غير مدخل")
                
                # Fetch attachments status from the most recent form if not already queried
                local_form = locals().get('last_form')
                if not local_form:
                    local_form = SCForm.objects.filter(
                        personnel=p,
                        form_type__icontains='missing',
                        status='approved'
                    ).order_by('-updated_at').first()
                
                if local_form:
                    row["is_complete"] = "✔" if local_form.attachments_complete else ""
                    row["is_incomplete"] = "" if local_form.attachments_complete else "✔"
                else:
                    row["is_complete"] = ""
                    row["is_incomplete"] = "✔"

            data_list.append(row)

        return Response({'data': data_list, 'total_count': len(data_list),
                         'month_filter': request.query_params.get('month', 'الكل')})


class PermInactiveReportsView(BaseDetailedReportView):
    """
    نماذج رقم (12-17): كشوفات القوة غير العاملة نهائياً
    """
    def get(self, request, *args, **kwargs):
        report_id = request.query_params.get('report_id')
        qs = self.get_queryset().filter(current_status__classification='inactive_perm')

        # ═══════════════════════════════════════════════════════════════
        # نموذج 14 — كشف مرشحين للتقاعد (تجميعي تلقائي)
        # ═══════════════════════════════════════════════════════════════
        # هذا الكشف يجمع تلقائياً كل من انطبقت عليه إحدى الحالات الثلاث:
        #   • كبار السن (بلوغ السن القانوني)      ← استمارة retirement_age
        #   • إنهاء المدة (نهاية الخدمة التعاقدية) ← استمارة end_of_service
        #   • عدم اللياقة الصحية                   ← استمارة medical_unfit
        # لا يحتاج هذا الكشف استمارة منفصلة «مرشح تقاعد».
        # عند اعتماد «استمارة محال للتقاعد» للفرد تتغير حالته إلى «متقاعدين»
        # فيختفي تلقائياً من هذا الكشف ومن كشفه الأصلي في نفس الوقت.
        # ═══════════════════════════════════════════════════════════════
        if report_id == 'report_14':
            # ═══════════════════════════════════════════════════════════════
            # الحالات الثلاث التي تُشكّل «مرشحي التقاعد» — مطابقة جدول الـ 25 حالة حرفياً:
            #   • «بلوغ السن القانوني»  ← الاسم الحرفي في قاعدة البيانات
            #   • «إنهاء المدة القانونية» ← الاسم الحرفي في قاعدة البيانات
            #   • «عدم لياقة»            ← الاسم الحرفي في قاعدة البيانات
            # ═══════════════════════════════════════════════════════════════
            # أسماء الحالات الثلاث كما هي حرفياً في جدول الـ 25 حالة
            RETIREMENT_CANDIDATE_STATUSES = [
                'بلوغ السن القانوني',     # استمارة retirement_age → كشف 12
                'إنهاء المدة القانونية',  # استمارة end_of_service  → كشف 13
                'عدم لياقة',             # استمارة medical_unfit   → كشف 15
            ]

            # خريطة: اسم الحالة → form_type للـ Fallback
            STATUS_TO_FORM_TYPE = {
                'بلوغ السن القانوني':    ['retirement_age'],
                'إنهاء المدة القانونية': ['end_of_service'],
                'عدم لياقة':            ['medical_unfit'],
            }

            candidate_qs = self.get_queryset().filter(
                current_status__classification='inactive_perm',
                current_status__name__in=RETIREMENT_CANDIDATE_STATUSES
            )

            # فلتر شهري: من أصبح مرشحاً للتقاعد خلال الشهر المحدد
            date_from, date_to = self.parse_month_range()
            if date_from:
                candidate_qs = candidate_qs.filter(
                    updated_at__date__gte=date_from,
                    updated_at__date__lte=date_to
                )

            from systems.services.infrastructure.models.status_change import StatusChangeForm as SCForm

            data_list = []
            for idx, p in enumerate(candidate_qs, start=1):
                row = self.format_base_data(p, idx)
                row['birth_date']  = p.birth_date or 'غير مدخل'
                row['join_date']   = p.join_date  or 'غير مدخل'
                # نوع الحالة: يعرض الاسم الحرفي من قاعدة البيانات مباشرة
                status_name        = p.current_status.name if p.current_status else 'غير محدد'
                row['status_type'] = status_name
                row['procedures']  = 'مستكمل'

                perm_details = p.perm_status_details or {}

                # Fallback: اقرأ من آخر استمارة معتمدة إذا كانت التفاصيل فارغة
                if not perm_details:
                    form_types = STATUS_TO_FORM_TYPE.get(status_name, [])
                    if form_types:
                        last_form = SCForm.objects.filter(
                            personnel=p,
                            form_type__in=form_types,
                            status='approved'
                        ).order_by('-updated_at').first()
                        if last_form and last_form.form_data:
                            perm_details = last_form.form_data

                # حقول مشتركة بين الحالات الثلاث
                # حقول خاصة بحالة عدم اللياقة فقط
                row['disease_type']     = perm_details.get('disease_type', '')
                row['disability_ratio'] = perm_details.get(
                    'disability_ratio', perm_details.get('disability_percentage', ''))
                row['incident_type']    = perm_details.get(
                    'incident_type', perm_details.get('injury_context', ''))

                data_list.append(row)

            return Response({'data': data_list, 'total_count': len(data_list),
                             'month_filter': request.query_params.get('month', 'الكل')})

        # ═══════════════════════════════════════════════════════════════
        # نماذج 12, 13, 15, 16, 17 — كشوفات الحالات الفردية
        # ═══════════════════════════════════════════════════════════════
        status_map = {
            'report_12': 'بلوغ السن',
            'report_13': 'إنهاء المدة',
            'report_15': 'عدم لياقة',
            'report_17': 'متقاعد'
        }

        target_status = status_map.get(report_id)
        if target_status:
            qs = qs.filter(current_status__name__icontains=target_status)
        elif report_id == 'report_16':
            qs = qs.filter(
                Q(current_status__name__icontains='شهيد') |
                Q(current_status__name__icontains='شهداء') |
                Q(current_status__name__icontains='متوفى') |
                Q(current_status__name__icontains='وفيات')
            )

        # فلتر شهري: من انتقل إلى هذه الحالة النهائية خلال الشهر المحدد
        date_from, date_to = self.parse_month_range()
        if date_from:
            qs = qs.filter(updated_at__date__gte=date_from, updated_at__date__lte=date_to)

        # خريطة form_type للبحث في StatusChangeForm كـ Fallback
        perm_report_form_type = {
            'report_12': 'retirement_age',
            'report_13': 'end_of_service',
            'report_15': 'medical_unfit',
            'report_16': ['martyr', 'death'],
            'report_17': 'retired',
        }

        from systems.services.infrastructure.models.status_change import StatusChangeForm as SCForm

        data_list = []
        for idx, p in enumerate(qs, start=1):
            row = self.format_base_data(p, idx)
            row['birth_date'] = p.birth_date or 'غير مدخل'
            row['join_date']  = p.join_date  or 'غير مدخل'

            perm_details = p.perm_status_details or {}

            # Fallback: إذا كان perm_status_details فارغاً، نقرأ من آخر استمارة معتمدة
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
                row['personal_request'] = 'مستكمل'
            elif report_id == 'report_13':
                row['total_years']   = perm_details.get('age', perm_details.get('total_years', 'غير مدخل'))
                row['person_request'] = 'مستكمل'
            elif report_id == 'report_15':
                row['disease_type']     = perm_details.get('disease_type', 'غير مدخل')
                row['disability_ratio'] = perm_details.get(
                    'disability_ratio', perm_details.get('disability_percentage', 'غير مدخل'))
                row['incident_date']    = perm_details.get(
                    'incident_date', perm_details.get('injury_date', 'غير مدخل'))
                row['medical_source']   = perm_details.get('medical_source', 'غير مدخل')
                row['incident_type']    = perm_details.get(
                    'incident_type', perm_details.get('injury_context', 'غير مدخل'))
            elif report_id == 'report_16':
                row['case_type']    = p.current_status.name if p.current_status else 'غير مدخل'
                row['death_date']   = perm_details.get(
                    'death_date', perm_details.get('martyrdom_date', 'غير مدخل'))
                row['incident_type'] = perm_details.get(
                    'incident_type', perm_details.get('occurrence_context', 'غير مدخل'))
            elif report_id == 'report_17':
                row['decision_number'] = perm_details.get('decision_number', 'غير مدخل')
                row['decision_date']   = perm_details.get('decision_date',   'غير مدخل')

            data_list.append(row)

        return Response({'data': data_list, 'total_count': len(data_list),
                         'month_filter': request.query_params.get('month', 'الكل')})


class AuditMovementReportsView(BaseDetailedReportView):
    """
    نماذج رقم (18-25): كشوفات التدقيق وحركة القوة
    """
    def get(self, request, *args, **kwargs):
        report_id = request.query_params.get('report_id')
        from systems.services.infrastructure.models.status_change import StatusChangeForm as SCForm

        date_from, date_to = self.parse_month_range()
        month_label = request.query_params.get('month', 'الكل')

        # ── نموذج 23: المطلوب تصحيح أسمائهم — من جدول SuggestedCorrection ──
        if report_id == 'report_23':
            from systems.personnel.models import SuggestedCorrection
            # ── الاستعلام يشمل كل طلبات تصحيح الاسم بغض النظر عن field_name ──
            # correction_type='name_correction' هو المعيار الثابت الذي يُرسله الفرونت إند دائماً
            corrections = SuggestedCorrection.objects.select_related(
                'personnel__current_rank'
            ).filter(
                correction_type='name_correction',
                status='pending'
            ).order_by('created_at')
            # فلتر شهري: تصحيحات الأسماء المقدمة خلال الشهر
            if date_from:
                corrections = corrections.filter(
                    created_at__date__gte=date_from,
                    created_at__date__lte=date_to
                )
            data_list = []
            for idx, c in enumerate(corrections, start=1):
                p = c.personnel
                # تحديد المطلوب تصحيحه من notes إذا كان مخزناً هناك، وإلا من field_name
                raw_notes = c.notes or ''
                correction_target = ''
                parsed_notes = raw_notes
                import re
                target_match = re.search(r'المطلوب تصحيح[هة]:\s*([\s\S]*?)(?=\s*المبررات:|$)', raw_notes)
                reason_match = re.search(r'المبررات:\s*([\s\S]*)', raw_notes)
                if target_match and target_match.group(1).strip():
                    correction_target = target_match.group(1).strip()
                    parsed_notes = reason_match.group(1).strip() if reason_match else '—'
                else:
                    # fallback: استخدم field_name كمطلوب تصحيحه
                    field_label_map = {
                        'full_name': 'الاسم الكامل',
                        'name_correction': 'تصحيح الاسم',
                        'first_name': 'الاسم الأول',
                        'second_name': 'الاسم الثاني',
                        'third_name': 'الاسم الثالث',
                        'fourth_name': 'الاسم الرابع',
                        'last_name': 'اللقب',
                    }
                    correction_target = field_label_map.get(c.field_name, c.field_name or 'تصحيح الاسم')

                data_list.append({
                    'index': idx,
                    'rank': p.current_rank.name if p.current_rank else 'غير محدد',
                    'military_number': p.military_number,
                    'full_name': p.full_name,
                    'national_id': p.national_id,
                    'wrong_name': c.old_value or p.full_name,
                    'correct_name': c.new_value or 'غير مدخل',
                    'correction_target': correction_target,
                    'notes': parsed_notes
                })
            return Response({'data': data_list, 'total_count': len(data_list),
                             'month_filter': month_label})

        # ── نموذج 25: الملتحقين بالعدوان — من حالة PersonnelMaster ──
        if report_id == 'report_25':
            qs = self.get_queryset().filter(current_status__name__icontains='العدوان')
            if date_from:
                qs = qs.filter(updated_at__date__gte=date_from, updated_at__date__lte=date_to)
            data_list = []
            for idx, p in enumerate(qs, start=1):
                row = self.format_base_data(p, idx)
                row['national_id'] = p.national_id
                details = p.audit_movement_details or {}
                if not details:
                    last_form = SCForm.objects.filter(
                        personnel=p, status='approved'
                    ).order_by('-updated_at').first()
                    if last_form and last_form.form_data:
                        details = last_form.form_data
                row['reporter_entity']   = details.get('reporter_entity', 'غير مدخل')
                row['taken_procedures']  = details.get('taken_procedures', 'غير مدخل')
                data_list.append(row)
            return Response({'data': data_list, 'total_count': len(data_list),
                             'month_filter': month_label})

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
            # فلتر شهري: استمارات تمت الموافقة عليها خلال الشهر المحدد
            if date_from:
                scforms = scforms.filter(
                    updated_at__date__gte=date_from,
                    updated_at__date__lte=date_to
                )

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

            return Response({'data': data_list, 'total_count': len(data_list),
                             'month_filter': month_label})

        # Fallback عام إذا لم يُعرف النوع
        return Response({'data': [], 'total_count': 0, 'month_filter': month_label,
                         'message': 'نوع التقرير غير محدد'})


