
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

    def parse_month_range(self):
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
        
        sa_ids = None
        if not request.user.is_superuser:
            try:
                sa_ids = request.user.authz_profile.get_accessible_security_admin_ids()
            except Exception:
                sa_ids = []

        def get_units(model_class):
            qs = model_class.objects.all()
            if sa_ids is not None:
                if model_class.__name__ in ['CentralDepartment', 'Branch', 'DistrictPolice']:
                    qs = qs.filter(security_admin_id__in=sa_ids)
                elif model_class.__name__ == 'SecurityAdministration':
                    qs = qs.filter(id__in=sa_ids)
            return list(qs.values_list('name', flat=True))

        data_map = {}
        if level == 'all':
            units = get_units(CentralDepartment) + get_units(Branch) + get_units(DistrictPolice)
        elif level == 'central':
            units = get_units(CentralDepartment)
        elif level == 'branch':
            units = get_units(Branch)
        elif level == 'district':
            units = get_units(DistrictPolice)
        else:
            units = get_units(SecurityAdministration)
            
        for u in units:
            data_map[u] = {
                "unit_name": u,
                "categories": {},
                "total": 0
            }
        
        from infra.authorization.services.permission_service import PermissionService
        
        # تجميع البيانات: فقط لمن هم "بالخدمة" حسب الفئة
        qs = PersonnelMaster.objects.filter(
            current_status__classification__startswith='active'
        )
        qs = PermissionService.get_scoped_queryset(
            self.request.user, qs, 'personnel.view.*'
        )
        
        date_from, date_to = self.parse_month_range()
        if date_from:
            qs = qs.filter(updated_at__date__gte=date_from, updated_at__date__lte=date_to)
        
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
        
        # Get active job categories sorted by sort_order
        ordered_categories = list(JobCategory.objects.order_by('sort_order', 'name').values_list('name', flat=True))
        
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

    def parse_month_range(self):
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
        
        from infra.authorization.services.permission_service import PermissionService
        
        # القوة غير العاملة فقط بحسب الحالات المسحوبة من قاعدة البيانات
        qs = PersonnelMaster.objects.filter(
            current_status__name__in=dynamic_statuses
        )
        qs = PermissionService.get_scoped_queryset(
            self.request.user, qs, 'personnel.view.*'
        )
        
        date_from, date_to = self.parse_month_range()
        if date_from:
            qs = qs.filter(updated_at__date__gte=date_from, updated_at__date__lte=date_to)
        
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


class MonthlyServicesReportView(APIView):
    """
    تقرير: تصدير الخدمات والكشوفات الشهرية
    يدعم وضعين:
    - roster_mode=monthly_changes (افتراضي): يعرض فقط من لديهم إجراءات معتمدة هذا الشهر
    - roster_mode=all: يعرض كل الأفراد المسجلين مع بيانات إجراءاتهم إن وُجدت
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        month = request.query_params.get('month')
        year = request.query_params.get('year')
        roster_mode = request.query_params.get('roster_mode', 'monthly_changes')  # 'all' | 'monthly_changes'

        # Advanced filters on personnel
        rank_id = request.query_params.get('rank')
        category_id = request.query_params.get('category')
        security_admin_id = request.query_params.get('security_admin')
        central_department_id = request.query_params.get('central_department')
        branch_id = request.query_params.get('branch')
        district_police_id = request.query_params.get('district_police')
        division_id = request.query_params.get('division')
        unit_id = request.query_params.get('unit')
        position_id = request.query_params.get('position')
        qualification_id = request.query_params.get('qualification')
        force_class = request.query_params.get('force_classification')
        military_number_search = request.query_params.get('military_number')
        name_search = request.query_params.get('name')

        from systems.services.models import StatusChangeForm, ServiceCatalog
        from systems.personnel.models import PersonnelMaster

        catalog_map = {}
        for sc in ServiceCatalog.objects.values('code', 'form_type', 'name_ar'):
            catalog_map[sc['code']] = sc['name_ar']
            if sc['form_type']:
                catalog_map[sc['form_type']] = sc['name_ar']

        # Determine roster type string
        import datetime
        ARABIC_MONTHS = {
            1: 'يناير', 2: 'فبراير', 3: 'مارس', 4: 'أبريل', 5: 'مايو', 6: 'يونيو',
            7: 'يوليو', 8: 'أغسطس', 9: 'سبتمبر', 10: 'أكتوبر', 11: 'نوفمبر', 12: 'ديسمبر'
        }
        current_date = datetime.date.today()
        
        # Parse multiple months/years
        month_list = []
        if month:
            month_list = [int(m.strip()) for m in month.split(',') if m.strip().isdigit()]
        if not month_list:
            month_list = [current_date.month]
            
        year_list = []
        if year:
            year_list = [int(y.strip()) for y in year.split(',') if y.strip().isdigit()]
        if not year_list:
            year_list = [current_date.year]

        month_names_ar = ' و '.join([ARABIC_MONTHS.get(m, str(m)) for m in month_list])
        years_str = ' و '.join(map(str, year_list))
        roster_type_val = f"{month_names_ar} {years_str}"

        # ─── Helper: Build personnel filters ────────────────────────────────
        def apply_personnel_filters(qs, prefix=''):
            if rank_id:
                rank_id_list = [int(rid.strip()) for rid in rank_id.split(',') if rid.strip().isdigit()]
                if rank_id_list:
                    qs = qs.filter(**{f'{prefix}current_rank_id__in': rank_id_list})
            if category_id:
                category_id_list = [int(cid.strip()) for cid in category_id.split(',') if cid.strip().isdigit()]
                if category_id_list:
                    qs = qs.filter(**{f'{prefix}category_id__in': category_id_list})
            if security_admin_id:
                admin_id_list = [int(x.strip()) for x in security_admin_id.split(',') if x.strip().isdigit()]
                if admin_id_list:
                    qs = qs.filter(**{f'{prefix}security_admin_id__in': admin_id_list})
            if central_department_id:
                dept_id_list = [int(x.strip()) for x in central_department_id.split(',') if x.strip().isdigit()]
                if dept_id_list:
                    qs = qs.filter(**{f'{prefix}central_department_id__in': dept_id_list})
            if branch_id:
                branch_id_list = [int(x.strip()) for x in branch_id.split(',') if x.strip().isdigit()]
                if branch_id_list:
                    qs = qs.filter(**{f'{prefix}branch_id__in': branch_id_list})
            if district_police_id:
                dist_police_list = [int(x.strip()) for x in district_police_id.split(',') if x.strip().isdigit()]
                if dist_police_list:
                    qs = qs.filter(**{f'{prefix}district_police_id__in': dist_police_list})
            if position_id:
                position_id_list = [int(x.strip()) for x in position_id.split(',') if x.strip().isdigit()]
                if position_id_list:
                    qs = qs.filter(**{f'{prefix}position_id__in': position_id_list})
            if qualification_id:
                qual_id_list = [int(x.strip()) for x in qualification_id.split(',') if x.strip().isdigit()]
                if qual_id_list:
                    qs = qs.filter(**{f'{prefix}qualification_id__in': qual_id_list})
            
            
            # Age and Service Duration Filters
            def get_past_date(years_to_subtract):
                try:
                    return current_date.replace(year=current_date.year - years_to_subtract)
                except ValueError:
                    return current_date.replace(year=current_date.year - years_to_subtract, day=28)

            age_min = request.query_params.get('age_min')
            if age_min and age_min.isdigit():
                qs = qs.filter(**{f'{prefix}birth_date__lte': get_past_date(int(age_min))})
            age_max = request.query_params.get('age_max')
            if age_max and age_max.isdigit():
                qs = qs.filter(**{f'{prefix}birth_date__gt': get_past_date(int(age_max) + 1)})
                
            service_min = request.query_params.get('service_min')
            if service_min and service_min.isdigit():
                qs = qs.filter(**{f'{prefix}join_date__lte': get_past_date(int(service_min))})
            service_max = request.query_params.get('service_max')
            if service_max and service_max.isdigit():
                qs = qs.filter(**{f'{prefix}join_date__gt': get_past_date(int(service_max) + 1)})

            # Status Filters
            status_classification = request.query_params.get('status_classification')
            if status_classification:
                classification_list = [sc.strip() for sc in status_classification.split(',') if sc.strip()]
                if classification_list:
                    qs = qs.filter(**{f'{prefix}current_status__classification__in': classification_list})
                
            status_id = request.query_params.get('status_id')
            if status_id:
                status_id_list = [sid.strip() for sid in status_id.split(',') if sid.strip()]
                if status_id_list:
                    qs = qs.filter(**{f'{prefix}current_status_id__in': status_id_list})
            
            # New Filters: Birth & Residence Geography
            birth_gov = request.query_params.get('birth_governorate')
            if birth_gov:
                birth_gov_list = [int(x.strip()) for x in birth_gov.split(',') if x.strip().isdigit()]
                if birth_gov_list:
                    qs = qs.filter(**{f'{prefix}birth_governorate_id__in': birth_gov_list})
            birth_district = request.query_params.get('birth_district')
            if birth_district:
                birth_dist_list = [int(x.strip()) for x in birth_district.split(',') if x.strip().isdigit()]
                if birth_dist_list:
                    qs = qs.filter(**{f'{prefix}birth_district_id__in': birth_dist_list})
            birth_sub_district = request.query_params.get('birth_sub_district')
            if birth_sub_district:
                birth_sub_dist_list = [int(x.strip()) for x in birth_sub_district.split(',') if x.strip().isdigit()]
                if birth_sub_dist_list:
                    qs = qs.filter(**{f'{prefix}birth_sub_district_id__in': birth_sub_dist_list})
            birth_village = request.query_params.get('birth_village')
            if birth_village:
                birth_vill_list = [int(x.strip()) for x in birth_village.split(',') if x.strip().isdigit()]
                if birth_vill_list:
                    qs = qs.filter(**{f'{prefix}birth_village_id__in': birth_vill_list})
            
            residence_gov = request.query_params.get('residence_governorate')
            if residence_gov:
                residence_gov_list = [int(x.strip()) for x in residence_gov.split(',') if x.strip().isdigit()]
                if residence_gov_list:
                    qs = qs.filter(**{f'{prefix}residence_governorate_id__in': residence_gov_list})
            residence_district = request.query_params.get('residence_district')
            if residence_district:
                residence_dist_list = [int(x.strip()) for x in residence_district.split(',') if x.strip().isdigit()]
                if residence_dist_list:
                    qs = qs.filter(**{f'{prefix}residence_district_id__in': residence_dist_list})
            residence_sub_district = request.query_params.get('residence_sub_district')
            if residence_sub_district:
                residence_sub_dist_list = [int(x.strip()) for x in residence_sub_district.split(',') if x.strip().isdigit()]
                if residence_sub_dist_list:
                    qs = qs.filter(**{f'{prefix}residence_sub_district_id__in': residence_sub_dist_list})
            residence_village = request.query_params.get('residence_village')
            if residence_village:
                residence_vill_list = [int(x.strip()) for x in residence_village.split(',') if x.strip().isdigit()]
                if residence_vill_list:
                    qs = qs.filter(**{f'{prefix}residence_village_id__in': residence_vill_list})
            
            if force_class:
                force_class_list = [int(fc.strip()) for fc in force_class.split(',') if fc.strip().isdigit()]
                if force_class_list:
                    qs = qs.filter(**{f'{prefix}force_classification_id__in': force_class_list})
            if military_number_search:
                qs = qs.filter(**{f'{prefix}military_number__icontains': military_number_search})
            if name_search:
                qs = qs.filter(**{f'{prefix}full_name__icontains': name_search})
            return qs

        # ─── Helper: build a row dict from a personnel object ────────────────
        def build_row(index, p, variables_str=''):
            try:
                status_display = p.current_status.get_classification_display() if p.current_status else '-'
            except Exception:
                status_display = '-'
            try:
                status_type = p.current_status.name if p.current_status else '-'
            except Exception:
                status_type = '-'
            try:
                force_cls = p.force_classification.name if p.force_classification else '-'
            except Exception:
                force_cls = '-'
            try:
                expense = p.get_expense_status_display() if p.expense_status else '-'
            except Exception:
                expense = '-'
            
            # منع ظهور الحالات التي ليس لها تصنيف بشكل فارغ، نضع '-'
            if not status_display or status_display.strip() == '':
                status_display = '-'
            
            return {
                'index': index,
                'officer_number': '',
                'rank': p.current_rank.name if p.current_rank else '-',
                'military_number': p.military_number or '',
                'national_id': p.national_id or '-',
                'full_name': p.full_name or '',
                'service_roster_type': roster_type_val,
                'unit': p.security_admin.name if p.security_admin else '-',
                'directorate': p.central_department.name if p.central_department else (p.branch.name if p.branch else (p.district_police.name if p.district_police else '-')),
                'affiliated_unit': p.division.name if getattr(p, 'division', None) else (p.unit.name if getattr(p, 'unit', None) else '-'),
                'position': p.position.name if p.position else '-',
                'job_title': p.job_title.name if p.job_title else '-',
                'category': p.category.name if p.category else '-',
                'status': status_display,
                'status_type': status_type,
                'force_classification': force_cls,
                'qualification': p.qualification.name if p.qualification else '-',
                'phone': p.phone_number or '-',
                'expense_status': expense,
                'monthly_variables': variables_str,
                'notes': p.notes or '',
                'appointment_info': p.appointment_info or '',
                'quality': f"{p.data_quality_score}%",
                'join_date': str(p.join_date) if p.join_date else '-',
                'birth_governorate': p.birth_governorate.name_ar if getattr(p, 'birth_governorate', None) else '-',
                'birth_district': p.birth_district.name_ar if getattr(p, 'birth_district', None) else '-',
                'birth_sub_district': p.birth_sub_district.name_ar if getattr(p, 'birth_sub_district', None) else '-',
                'birth_village': p.birth_village.name_ar if getattr(p, 'birth_village', None) else '-',
                'residence_governorate': p.residence_governorate.name_ar if getattr(p, 'residence_governorate', None) else '-',
                'residence_district': p.residence_district.name_ar if getattr(p, 'residence_district', None) else '-',
                'residence_sub_district': p.residence_sub_district.name_ar if getattr(p, 'residence_sub_district', None) else '-',
                'residence_village': p.residence_village.name_ar if getattr(p, 'residence_village', None) else '-',
            }

        data = []

        if roster_mode == 'all':
            # ═══ وضع الكشف الشامل: كل الأفراد المسجلين ═══════════════════════
            p_qs = PersonnelMaster.objects.select_related(
                'current_rank', 'qualification', 'security_admin',
                'central_department', 'branch', 'district_police', 'division', 'unit',
                'position', 'job_title', 'category', 'current_status',
                'force_classification', 'birth_governorate', 'birth_district', 'birth_sub_district', 'birth_village',
                'residence_governorate', 'residence_district', 'residence_sub_district', 'residence_village'
            )
            p_qs = apply_personnel_filters(p_qs, prefix='')

            # جلب إجراءات الشهر لتعبئة عمود المتغيرات
            forms_qs = StatusChangeForm.objects.filter(status='approved')
            if year_list:
                forms_qs = forms_qs.filter(created_at__year__in=year_list)
            if month_list:
                forms_qs = forms_qs.filter(created_at__month__in=month_list)

            personnel_latest_form = {}
            for f in forms_qs.order_by('created_at'):
                personnel_latest_form[f.personnel_id] = f

            try:
                from infra.authorization.services.permission_service import PermissionService
                p_qs = PermissionService.get_scoped_queryset(request.user, p_qs, 'personnel.view.*')
            except Exception:
                pass

            for index, p in enumerate(p_qs.order_by('current_rank__order', 'full_name'), 1):
                variables_str = ''
                latest = personnel_latest_form.get(p.pk)
                if latest:
                    try:
                        ft_display = catalog_map.get(latest.form_type) or dict(latest.FORM_TYPE_CHOICES).get(latest.form_type) or latest.form_type
                        variables_str = ft_display
                        if latest.notes and latest.notes.strip() not in ['-', '']:
                            variables_str += f" - {latest.notes.strip()}"
                    except Exception:
                        variables_str = str(latest.form_type)
                data.append(build_row(index, p, variables_str))

        else:
            # ═══ وضع تغييرات الشهر فقط ══════════════════════════
            qs = StatusChangeForm.objects.select_related(
                'personnel', 'personnel__current_rank', 'submitted_by',
                'personnel__qualification', 'personnel__security_admin',
                'personnel__central_department', 'personnel__branch',
                'personnel__district_police', 'personnel__division', 'personnel__unit', 'personnel__position',
                'personnel__job_title', 'personnel__category',
                'personnel__current_status', 'personnel__force_classification',
                'personnel__birth_governorate', 'personnel__birth_district', 'personnel__birth_sub_district', 'personnel__birth_village',
                'personnel__residence_governorate', 'personnel__residence_district', 'personnel__residence_sub_district', 'personnel__residence_village'
            )

            if year_list:
                qs = qs.filter(created_at__year__in=year_list)
            if month_list:
                qs = qs.filter(created_at__month__in=month_list)

            qs = qs.filter(status='approved')
            qs = apply_personnel_filters(qs, prefix='personnel__')

            try:
                from infra.authorization.services.permission_service import PermissionService
                qs = PermissionService.get_scoped_queryset(request.user, qs, 'services.view.*')
            except Exception:
                pass

            personnel_forms = {}
            for form in qs.order_by('created_at'):
                pid = form.personnel_id
                if not pid:
                    continue
                if pid not in personnel_forms:
                    personnel_forms[pid] = {'personnel': form.personnel, 'forms': []}
                personnel_forms[pid]['forms'].append(form)

            for index, (pid, p_data) in enumerate(personnel_forms.items(), 1):
                p = p_data['personnel']
                forms = p_data['forms']

                latest_form = forms[-1]
                try:
                    latest_ft_display = catalog_map.get(latest_form.form_type) or dict(latest_form.FORM_TYPE_CHOICES).get(latest_form.form_type) or latest_form.form_type
                    variables_str = latest_ft_display
                    if latest_form.notes and latest_form.notes.strip() not in ['-', '']:
                        variables_str += f" - {latest_form.notes.strip()}"
                except Exception:
                    variables_str = str(latest_form.form_type)

                data.append(build_row(index, p, variables_str))

        return Response({'data': data})

