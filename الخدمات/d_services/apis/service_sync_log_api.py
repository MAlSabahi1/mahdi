"""
API سجل مزامنة الخدمات — Service Sync Log

GET /api/d-services/portal/service-sync-log/
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.permissions import IsAuthenticated

from d_services.models.ServiceSync import ServiceSync, ServiceSyncStatus


class ServiceSyncSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    service_code = serializers.CharField(source='fk_service.code', read_only=True)

    class Meta:
        model = ServiceSync
        fields = [
            'id', 'fk_service_id', 'service_code', 'service_name',
            'status', 'status_display', 'error_message',
            'last_synced_at', 'created_at',
        ]


def _require_superuser(user):
    from d_services.utils.exception_handler import ValidationException
    if not user.is_superuser:
        raise ValidationException('هذه العملية متاحة فقط لمدير النظام (SuperAdmin)')


class ServiceSyncLogView(APIView):
    """
    عرض سجل مزامنة الخدمات مع فلترة اختيارية
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        _require_superuser(request.user)

        qs = ServiceSync.objects.select_related('fk_service').order_by('-created_at')

        # فلترة حسب الحالة
        sync_status = request.query_params.get('status')
        if sync_status:
            try:
                sync_status = int(sync_status)
                qs = qs.filter(status=sync_status)
            except (ValueError, TypeError):
                pass

        # فلترة حسب اسم الخدمة
        service_name = request.query_params.get('service_name')
        if service_name:
            qs = qs.filter(service_name__icontains=service_name)

        serializer = ServiceSyncSerializer(qs, many=True)

        # إحصائيات
        total = qs.count()
        stats = {
            'total': total,
            'not_synced': qs.filter(status=ServiceSyncStatus.NOT_SYNCED).count(),
            'success': qs.filter(status=ServiceSyncStatus.SUCCESS).count(),
            'failed': qs.filter(status=ServiceSyncStatus.FAILED).count(),
        }

        return Response({
            'stats': stats,
            'items': serializer.data,
        }, status=status.HTTP_200_OK)
