"""
Portal Export API — يعمل على جانب البوابة
يصدّر الطلبات غير المتزامنة ويستقبل تأكيد المزامنة
"""
import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils.translation import gettext_lazy as _

from OpenSoftCoreV4.common.models.Branch import Organization

from d_services.models.ServiceRequestSync import ServiceRequestSyncStatus
from d_services.serializers.ServiceRequestSync import ServiceRequestSyncSerializer
from d_services.utils.service_request_sync_service import (
    get_pending_for_system,
    mark_system_synced,
    mark_system_failed_per_item,
    SYSTEM_FIELDS,
)

logger = logging.getLogger(__name__)


class PortalExportView(APIView):
    """
    Export API — يصدّر طلبات الخدمة غير المتزامنة لنظام معين.
    يعمل على جانب البوابة.
    
    GET /api/d-services/portal/export-requests/?system=university
    
    المصادقة: SSO Token (Keycloak)
    الفلترة:
    - system: نوع النظام (school / university / institute)
    - المنظمة: من ogranizatoin_ex_id في المستخدم (من التوكن)
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        system = request.query_params.get('system')
        
        # التحقق من النظام
        if not system or system not in SYSTEM_FIELDS:
            return Response({
                'error': f'يجب تحديد النظام: {", ".join(SYSTEM_FIELDS)}',
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # المنظمة من المستخدم (SSO Token)
        org_ex_id = getattr(request.user, 'ogranizatoin_ex_id', None)
        if not org_ex_id:
            return Response({
                'error': 'المستخدم لا يمتلك معرف منظمة (ogranizatoin_ex_id)',
            }, status=status.HTTP_400_BAD_REQUEST)
        
        org = Organization.objects.filter(ex_id=org_ex_id).first()
        if not org:
            return Response({
                'error': f'المنظمة غير موجودة: ex_id={org_ex_id}',
            }, status=status.HTTP_404_NOT_FOUND)
        
        # جلب الطلبات المعلقة
        pending = get_pending_for_system(
            system_field=system,
            organization=org,
        )
        
        serializer = ServiceRequestSyncSerializer(pending, many=True)
        
        return Response({
            'system': system,
            'organization_ex_id': str(org_ex_id),
            'count': len(serializer.data),
            'items': serializer.data,
        }, status=status.HTTP_200_OK)


class PortalMarkSyncedView(APIView):
    """
    تأكيد المزامنة — يستقبل من النظام الفرعي تأكيد نجاح/فشل المزامنة.

    POST /api/d-services/portal/mark-synced/
    
    Body:
    {
        "system": "university",
        "synced_ids": [1, 2, 3],
        "failed_items": [
            {"sync_id": 4, "error": "... خطأ ..."}
        ]
    }
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        system = request.data.get('system')
        synced_ids = request.data.get('synced_ids', [])
        failed_items = request.data.get('failed_items', [])
        
        if not system or system not in SYSTEM_FIELDS:
            return Response({
                'error': f'يجب تحديد النظام: {", ".join(SYSTEM_FIELDS)}',
            }, status=status.HTTP_400_BAD_REQUEST)
        
        synced_count = 0
        failed_count = 0
        
        if synced_ids:
            synced_count = mark_system_synced(synced_ids, system)
        
        if failed_items:
            failed_count = mark_system_failed_per_item(failed_items, system)
        
        return Response({
            'system': system,
            'synced': synced_count,
            'failed': failed_count,
        }, status=status.HTTP_200_OK)
