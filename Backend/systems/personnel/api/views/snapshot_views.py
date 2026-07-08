from rest_framework import viewsets, status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db import transaction
from django.core.serializers.json import DjangoJSONEncoder
from django.forms.models import model_to_dict
import json

from ...models import PersonnelMaster, MonthlySnapshot

class MonthlySnapshotView(views.APIView):
    """
    API endpoint to generate and list monthly snapshots.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        List summary of all snapshots available (grouped by month).
        """
        # We group by snapshot_date and count
        from django.db.models import Count
        snapshots = MonthlySnapshot.objects.values('snapshot_date').annotate(
            total_personnel=Count('id')
        ).order_by('-snapshot_date')
        
        return Response(snapshots)

    def post(self, request, *args, **kwargs):
        """
        Generate a new snapshot for the requested month.
        Expected data: {"month": "YYYY-MM"}
        If month is not provided, defaults to current month.
        """
        month = request.data.get('month')
        if not month:
            # Default to current year-month
            month = timezone.now().strftime('%Y-%m')
            
        # Check if snapshot already exists
        if MonthlySnapshot.objects.filter(snapshot_date=month).exists():
            return Response(
                {"error": f"تم إصدار اللقطة لشهر {month} مسبقاً."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Generate Snapshot
        active_personnel = PersonnelMaster.objects.all()
        
        snapshot_records = []
        with transaction.atomic():
            for p in active_personnel:
                p_dict = model_to_dict(p)
                # Ensure files and images are converted to string paths
                from django.db.models.fields.files import FieldFile
                for key, value in p_dict.items():
                    if isinstance(value, FieldFile):
                        p_dict[key] = value.name if value else None
                        
                # Ensure all datetime objects are serialized
                p_json_string = json.dumps(p_dict, cls=DjangoJSONEncoder)
                p_json = json.loads(p_json_string)
                
                unit_name = "غير محدد"
                if p.central_department:
                    unit_name = p.central_department.name
                elif p.branch:
                    unit_name = p.branch.name
                elif p.district_police:
                    unit_name = p.district_police.name
                    
                snapshot = MonthlySnapshot(
                    personnel=p,
                    snapshot_date=month,
                    rank=p.current_rank.name if p.current_rank else None,
                    status_name=p.current_status.name if p.current_status else None,
                    unit_name=unit_name,
                    snapshot_data=p_json,
                    created_by=request.user
                )
                snapshot_records.append(snapshot)
                
            # Bulk create to speed up
            MonthlySnapshot.objects.bulk_create(snapshot_records)
            
        return Response({
            "message": f"تم إصدار لقطة الشهر ({month}) بنجاح.",
            "total_records": len(snapshot_records)
        }, status=status.HTTP_201_CREATED)
