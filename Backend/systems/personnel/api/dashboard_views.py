from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Avg, F, Q
from django.utils import timezone
from datetime import timedelta
from core.models import Branch, SecurityAdministration, GeoGovernorate, Rank, ForceType
from systems.personnel.models import PersonnelMaster
from django.db.models.functions import TruncDate

class DashboardStatsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        total_personnel = PersonnelMaster.objects.count()
        active_branches = Branch.objects.count()
        completed = PersonnelMaster.objects.filter(is_complete=True).count()
        critical_alerts = PersonnelMaster.objects.filter(data_quality_score__lt=50).count()
        
        # System Activity (Last 30 Days trend)
        thirty_days_ago = timezone.now() - timedelta(days=30)
        system_activity = list(PersonnelMaster.objects.filter(created_at__gte=thirty_days_ago)
                               .annotate(date=TruncDate('created_at'))
                               .values('date')
                               .annotate(count=Count('military_number'))
                               .order_by('date'))
        
        # Recent Activities (Last 4 additions)
        recent_activities = list(PersonnelMaster.objects.order_by('-created_at')[:4].values(
            'military_number', 'full_name', 'created_at'
        ))
        
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
        # 1. Force Distribution
        force_distribution = list(PersonnelMaster.objects.exclude(force_classification__isnull=True).values(
            name=F('force_classification__name')
        ).annotate(value=Count('military_number')))
        
        # 2. Geographic Distribution
        geographic_distribution = list(PersonnelMaster.objects.exclude(geo_location__isnull=True).values(
            name=F('geo_location__name_ar')
        ).annotate(value=Count('military_number')).order_by('-value')[:10])

        # 3. Status Distribution
        status_distribution = list(PersonnelMaster.objects.exclude(current_status__isnull=True).values(
            name=F('current_status__name')
        ).annotate(value=Count('military_number')).order_by('-value'))

        # 4. Rank Distribution
        rank_distribution = list(PersonnelMaster.objects.exclude(current_rank__isnull=True).values(
            name=F('current_rank__name')
        ).annotate(value=Count('military_number')).order_by('-value')[:15])

        # 5. Trend (Last 7 Days)
        seven_days_ago = timezone.now() - timedelta(days=7)
        trend = list(PersonnelMaster.objects.filter(created_at__gte=seven_days_ago)
                     .annotate(date=TruncDate('created_at'))
                     .values('date')
                     .annotate(count=Count('military_number'))
                     .order_by('date'))
                     
        if not trend:
            trend = list(PersonnelMaster.objects.annotate(date=TruncDate('created_at'))
                     .values('date')
                     .annotate(count=Count('military_number'))
                     .order_by('-date')[:7])
                     
        return Response({
            "force_distribution": force_distribution,
            "geographic_distribution": geographic_distribution,
            "status_distribution": status_distribution,
            "rank_distribution": rank_distribution,
            "trend": trend
        })

from systems.personnel.models import PersonnelMaster, SuggestedCorrection, RankSettlement

class DashboardAlertsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # 1. Data Quality Alerts
        alerts = PersonnelMaster.objects.filter(data_quality_score__lt=70).values(
            'military_number', 'full_name', 'data_quality_score'
        ).order_by('data_quality_score')[:15]
        
        # 2. Pending Requests
        pending_requests = []
        
        # Suggested Corrections
        corrections = SuggestedCorrection.objects.filter(status='pending').select_related('personnel', 'personnel__security_admin', 'requested_by')[:10]
        for c in corrections:
            pending_requests.append({
                "id": f"corr_{c.id}",
                "title": f"طلب تصحيح بيانات: {c.get_correction_type_display()}",
                "description": f"طلب تصحيح بيانات للفرد: {c.personnel.full_name}",
                "time": c.requested_at,
                "requester": c.requested_by.get_full_name() if c.requested_by else "النظام",
                "department": c.personnel.security_admin.name if c.personnel and c.personnel.security_admin else "غير محدد"
            })
            
        # Rank Settlements
        settlements = RankSettlement.objects.filter(status='pending').select_related('personnel', 'personnel__security_admin')[:10]
        for s in settlements:
            pending_requests.append({
                "id": f"rank_{s.id}",
                "title": f"طلب تسوية رتبة: {s.get_settlement_type_display()}",
                "description": f"رقم القرار: {s.decision_number} للفرد: {s.personnel.full_name}",
                "time": s.created_at,
                "requester": "إدارة الموارد البشرية",
                "department": s.personnel.security_admin.name if s.personnel and s.personnel.security_admin else "غير محدد"
            })
            
        # Sort pending_requests by time descending
        pending_requests.sort(key=lambda x: x['time'], reverse=True)
        
        # 3. Processed Today
        today = timezone.now().date()
        processed_corrections = SuggestedCorrection.objects.filter(
            reviewed_at__date=today,
            status__in=['approved', 'rejected']
        ).count()
        processed_settlements = RankSettlement.objects.filter(
            updated_at__date=today,
            status__in=['approved', 'rejected', 'applied']
        ).count()
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
        compliance = list(PersonnelMaster.objects.exclude(security_admin__isnull=True).values(
            region=F('security_admin__name')
        ).annotate(
            avg_score=Avg('data_quality_score'),
            total_personnel=Count('military_number')
        ).order_by('-avg_score'))
        
        return Response({
            "compliance_by_region": compliance
        })
