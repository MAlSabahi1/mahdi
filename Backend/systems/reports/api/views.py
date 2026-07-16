
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
    يعرض الإجراءات (StatusChangeForm) خلال شهر وسنة محددين.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        month = request.query_params.get('month')
        year = request.query_params.get('year')
        status_param = request.query_params.get('status', 'all')
        
        # Advanced filters on personnel
        rank_id = request.query_params.get('rank')
        category_id = request.query_params.get('category')
        security_admin_id = request.query_params.get('security_admin')
        central_department_id = request.query_params.get('central_department')
        branch_id = request.query_params.get('branch')
        district_police_id = request.query_params.get('district_police')
        position_id = request.query_params.get('position')
        qualification_id = request.query_params.get('qualification')
        force_class = request.query_params.get('force_classification')  # active / inactive
        military_number_search = request.query_params.get('military_number')
        name_search = request.query_params.get('name')
        
        from systems.services.models import StatusChangeForm, ServiceCatalog
        
        qs = StatusChangeForm.objects.select_related(
            'personnel', 'personnel__current_rank', 'submitted_by',
            'personnel__qualification', 'personnel__security_admin',
            'personnel__central_department', 'personnel__branch',
            'personnel__district_police', 'personnel__position',
            'personnel__job_title', 'personnel__category',
            'personnel__current_status'
        )
        
        if year:
            qs = qs.filter(created_at__year=year)
        if month:
            qs = qs.filter(created_at__month=month)
            
        if status_param != 'all':
            qs = qs.filter(status=status_param)
        
        # Advanced personnel filters
        if rank_id:
            qs = qs.filter(personnel__current_rank_id=rank_id)
        if category_id:
            qs = qs.filter(personnel__category_id=category_id)
        if security_admin_id:
            qs = qs.filter(personnel__security_admin_id=security_admin_id)
        if central_department_id:
            qs = qs.filter(personnel__central_department_id=central_department_id)
        if branch_id:
            qs = qs.filter(personnel__branch_id=branch_id)
        if district_police_id:
            qs = qs.filter(personnel__district_police_id=district_police_id)
        if position_id:
            qs = qs.filter(personnel__position_id=position_id)
        if qualification_id:
            qs = qs.filter(personnel__qualification_id=qualification_id)
        if force_class == 'active':
            qs = qs.filter(personnel__current_status__classification__startswith='active')
        elif force_class == 'inactive':
            qs = qs.exclude(personnel__current_status__classification__startswith='active')
        if military_number_search:
            qs = qs.filter(personnel__military_number__icontains=military_number_search)
        if name_search:
            qs = qs.filter(personnel__full_name__icontains=name_search)
            
        # Scope by user permissions
        from infra.authorization.services.permission_service import PermissionService
        try:
            qs = PermissionService.get_scoped_queryset(request.user, qs, 'services.view.*')
        except Exception:
            pass

        catalog_map = {}
        for sc in ServiceCatalog.objects.values('code', 'form_type', 'name_ar'):
            catalog_map[sc['code']] = sc['name_ar']
            if sc['form_type']:
                catalog_map[sc['form_type']] = sc['name_ar']
                
        data = []
        for index, form in enumerate(qs.order_by('-created_at'), 1):
            p = form.personnel
            if not p:
                continue
            
            ft_display = catalog_map.get(form.form_type) or dict(form.FORM_TYPE_CHOICES).get(form.form_type) or form.form_type
            
            unit = 'غير محدد'
            if p.central_department:
                unit = p.central_department.name
            elif p.branch:
                unit = p.branch.name
            elif p.district_police:
                unit = p.district_police.name
            elif p.security_admin:
                unit = p.security_admin.name
            
            data.append({
                'index': index,
                'rank': p.current_rank.name if p.current_rank else 'بدون رتبة',
                'military_number': p.military_number,
                'national_id': p.national_id or 'غير مدخل',
                'full_name': p.full_name,
                'unit': p.security_admin.name if p.security_admin else 'غير مدخل',
                'directorate': p.central_department.name if p.central_department else 'غير مدخل',
                'department': p.district_police.name if p.district_police else 'غير مدخل',
                'affiliated_unit': p.branch.name if p.branch else 'غير مدخل',
                'position': p.position.name if p.position else 'غير مدخل',
                'job_title': p.job_title.name if p.job_title else 'غير مدخل',
                'category': p.category.name if p.category else 'غير مدخل',
                'status': p.current_status.name if p.current_status else 'غير مدخل',
                'status_type': ft_display,
                'force_classification': 'قوة عاملة' if p.current_status and 'active' in p.current_status.classification else 'قوة غير عاملة',
                'qualification': p.qualification.name if p.qualification else 'غير مدخل',
                'phone': p.phone_number or 'غير مدخل',
                'old_military_number': p.old_military_number or 'غير مدخل',
                'expense_status': dict(p.EXPENSE_STATUS_CHOICES).get(p.expense_status, 'غير مدخل') if hasattr(p, 'EXPENSE_STATUS_CHOICES') else 'غير مدخل',
                'appointment_info': p.appointment_info or 'غير مدخل',
                'quality': f"{p.data_quality_score}%",
                'join_date': str(p.join_date) if p.join_date else 'غير مدخل',
            })
            
        return Response({
            'data': data
        })
