from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Avg, F, Q
from django.utils import timezone
from datetime import timedelta
from core.models import Branch, SecurityAdministration, GeoGovernorate, Rank, ForceType
from systems.personnel.models import PersonnelMaster
from django.db.models.functions import TruncDate
from infra.authorization.services.permission_service import PermissionService


def _scoped_personnel(user):
    """إرجاع QuerySet للأفراد مُقيَّد بنطاق المحافظة الخاص بالمستخدم."""
    qs = PersonnelMaster.objects.all()
    return PermissionService.get_scoped_queryset(user, qs, 'personnel.view.*')


def _scoped_branches(user):
    """إرجاع عدد الفروع ضمن نطاق المحافظة."""
    if user.is_superuser:
        return Branch.objects.count()
    try:
        sa_ids = user.authz_profile.get_accessible_security_admin_ids()
        return Branch.objects.filter(security_admin_id__in=sa_ids).count()
    except Exception:
        return 0


class DashboardStatsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        qs = _scoped_personnel(request.user)

        total_personnel = qs.count()
        active_branches = _scoped_branches(request.user)
        completed = qs.filter(is_complete=True).count()
        critical_alerts = qs.filter(data_quality_score__lt=50).count()
        
        # System Activity (Last 30 Days trend)
        thirty_days_ago = timezone.now() - timedelta(days=30)
        system_activity = list(
            qs.filter(created_at__gte=thirty_days_ago)
            .annotate(date=TruncDate('created_at'))
            .values('date')
            .annotate(count=Count('military_number'))
            .order_by('date')
        )
        
        # Recent Activities (Last 4 additions)
        recent_activities = list(
            qs.order_by('-created_at')[:4]
            .values('military_number', 'full_name', 'created_at')
        )
        
        return Response({
            "total_personnel": total_personnel,
            "active_branches": active_branches,
            "completed_profiles": completed,
            "critical_alerts": critical_alerts,
            "system_activity": system_activity,
            "storage_usage": {
                "database": 78,
                "files": 45
            },
            "recent_activities": recent_activities
        })


class DashboardAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        qs = _scoped_personnel(request.user)

        # 1. Force Distribution
        force_distribution = list(
            qs.exclude(force_classification__isnull=True)
            .values(name=F('force_classification__name'))
            .annotate(value=Count('military_number'))
        )
        
        # 2. Geographic Distribution (by security_admin for provincial admins)
        geographic_distribution = list(
            qs.exclude(security_admin__isnull=True)
            .values(name=F('security_admin__name'))
            .annotate(value=Count('military_number'))
            .order_by('-value')[:10]
        )

        # 3. Status Distribution
        status_distribution = list(
            qs.exclude(current_status__isnull=True)
            .values(name=F('current_status__name'))
            .annotate(value=Count('military_number'))
            .order_by('-value')
        )

        # 4. Rank Distribution
        rank_distribution = list(
            qs.exclude(current_rank__isnull=True)
            .values(name=F('current_rank__name'))
            .annotate(value=Count('military_number'))
            .order_by('-value')[:15]
        )

        # 5. Trend (Last 7 Days)
        seven_days_ago = timezone.now() - timedelta(days=7)
        trend = list(
            qs.filter(created_at__gte=seven_days_ago)
            .annotate(date=TruncDate('created_at'))
            .values('date')
            .annotate(count=Count('military_number'))
            .order_by('date')
        )
                     
        if not trend:
            trend = list(
                qs.annotate(date=TruncDate('created_at'))
                .values('date')
                .annotate(count=Count('military_number'))
                .order_by('-date')[:7]
            )
            
        # 6. Qualification Distribution
        qualification_distribution = list(
            qs.exclude(qualification__isnull=True)
            .values(name=F('qualification__name'))
            .annotate(value=Count('military_number'))
            .order_by('-value')
        )
        
        # 7. Expense Status Distribution
        expense_distribution = list(
            qs.exclude(expense_status__isnull=True)
            .values(name=F('expense_status'))
            .annotate(value=Count('military_number'))
        )
        
        # 8. Data Quality Distribution
        data_quality_stats = {
            "clean_data": qs.filter(is_data_clean=True).count(),
            "unclean_data": qs.filter(is_data_clean=False).count(),
            "complete_profiles": qs.filter(is_complete=True).count(),
            "incomplete_profiles": qs.filter(is_complete=False).count(),
            "average_score": qs.aggregate(avg=Avg('data_quality_score'))['avg'] or 0
        }
                     
        return Response({
            "force_distribution": force_distribution,
            "geographic_distribution": geographic_distribution,
            "status_distribution": status_distribution,
            "rank_distribution": rank_distribution,
            "trend": trend,
            "qualification_distribution": qualification_distribution,
            "expense_distribution": expense_distribution,
            "data_quality_stats": data_quality_stats
        })


from systems.personnel.models import PersonnelMaster, SuggestedCorrection, RankSettlement

class DashboardAlertsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        qs = _scoped_personnel(request.user)

        # 1. Data Quality Alerts — مُقيَّد بنطاق المحافظة
        alerts = qs.filter(data_quality_score__lt=70).values(
            'military_number', 'full_name', 'data_quality_score'
        ).order_by('data_quality_score')[:15]
        
        # 2. Pending Requests — مُقيَّد بنطاق المحافظة
        pending_requests = []

        # جلب sa_ids لتصفية الطلبات
        sa_ids = None
        if not request.user.is_superuser:
            try:
                sa_ids = request.user.authz_profile.get_accessible_security_admin_ids()
            except Exception:
                sa_ids = []

        # Suggested Corrections
        corrections_qs = SuggestedCorrection.objects.filter(status='pending').select_related(
            'personnel', 'personnel__security_admin', 'requested_by'
        )
        if sa_ids is not None:
            corrections_qs = corrections_qs.filter(personnel__security_admin_id__in=sa_ids)
        corrections_qs = corrections_qs[:10]

        for c in corrections_qs:
            pending_requests.append({
                "id": f"corr_{c.id}",
                "title": f"طلب تصحيح بيانات: {c.get_correction_type_display()}",
                "description": f"طلب تصحيح بيانات للفرد: {c.personnel.full_name}",
                "time": c.requested_at,
                "requester": c.requested_by.get_full_name() if c.requested_by else "النظام",
                "department": c.personnel.security_admin.name if c.personnel and c.personnel.security_admin else "غير محدد"
            })
            
        # Rank Settlements
        settlements_qs = RankSettlement.objects.filter(status='pending').select_related(
            'personnel', 'personnel__security_admin'
        )
        if sa_ids is not None:
            settlements_qs = settlements_qs.filter(personnel__security_admin_id__in=sa_ids)
        settlements_qs = settlements_qs[:10]

        for s in settlements_qs:
            pending_requests.append({
                "id": f"rank_{s.id}",
                "title": f"طلب تسوية رتبة: {s.get_settlement_type_display()}",
                "description": f"رقم القرار: {s.decision_number} للفرد: {s.personnel.full_name}",
                "time": s.created_at,
                "requester": "إدارة الموارد البشرية",
                "department": s.personnel.security_admin.name if s.personnel and s.personnel.security_admin else "غير محدد"
            })
            
        pending_requests.sort(key=lambda x: x['time'], reverse=True)
        
        # 3. Processed Today — مُقيَّد بنطاق المحافظة
        today = timezone.now().date()

        corrections_filter = {'reviewed_at__date': today, 'status__in': ['approved', 'rejected']}
        if sa_ids is not None:
            corrections_filter['personnel__security_admin_id__in'] = sa_ids
        processed_corrections = SuggestedCorrection.objects.filter(**corrections_filter).count()

        settlements_filter = {'updated_at__date': today, 'status__in': ['approved', 'rejected', 'applied']}
        if sa_ids is not None:
            settlements_filter['personnel__security_admin_id__in'] = sa_ids
        processed_settlements = RankSettlement.objects.filter(**settlements_filter).count()

        processed_today = processed_corrections + processed_settlements
        
        return Response({
            "data_quality_alerts": list(alerts),
            "pending_requests": pending_requests[:15],
            "stats": {
                "critical_alerts": len([a for a in alerts if a['data_quality_score'] < 50]),
                "pending_requests_count": len(pending_requests),
                "processed_today": processed_today
            }
        })


class DashboardComplianceView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        qs = _scoped_personnel(request.user)

        compliance = list(
            qs.exclude(security_admin__isnull=True)
            .values(region=F('security_admin__name'))
            .annotate(
                avg_score=Avg('data_quality_score'),
                total_personnel=Count('military_number')
            )
            .order_by('-avg_score')
        )
        
        return Response({
            "compliance_by_region": compliance
        })
