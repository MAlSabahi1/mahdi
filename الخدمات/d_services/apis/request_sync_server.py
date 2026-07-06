"""
Server API — مزامنة الطلبات من النظام الفرعي إلى البوابة
يعمل على النظام الفرعي (QAS) — على مستوى منظمة المستخدم

POST /api/d-services/portal/trigger-request-sync/
"""
import logging
import json
import requests as http_requests

from django.conf import settings
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from d_services.models.ServiceRequest import ServiceRequest
from d_services.models.ServiceRequestSync import ServiceRequestSync, ServiceRequestSyncStatus
from d_services.serializers.request_sync_serializers import SyncRequestExportSerializer

logger = logging.getLogger(__name__)


def _require_manager(user):
    """تحقق أن المستخدم مدير منظمة أو سوبر أدمن"""
    from d_services.utils.exception_handler import ValidationException
    if not (user.is_superuser or getattr(user, 'is_manager', False)):
        raise ValidationException('هذه العملية متاحة فقط لمدير المنظمة')


def _get_system_field():
    """إرجاع اسم حقل النظام المقابل لـ PORTAL_SYNC_SYSTEM_TYPE"""
    system_type = getattr(settings, 'PORTAL_SYNC_SYSTEM_TYPE', 'university')
    return system_type  # school / university / institute


class TriggerRequestSyncView(APIView):
    """
    Trigger request sync — يُستدعى من الفرونت في النظام الفرعي
    يجلب الطلبات غير المتزامنة لمنظمة المستخدم ويرسلها للبوابة
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        _require_manager(request.user)

        user_org = getattr(request.user, 'fk_organization', None)
        if not user_org:
            return Response({
                'error': 'المستخدم غير مرتبط بمنظمة',
            }, status=status.HTTP_400_BAD_REQUEST)

        system_field = _get_system_field()

        # ── 1. جلب الطلبات غير المتزامنة لهذا النظام ولمنظمة المستخدم ──
        pending_filter = {
            f'{system_field}__in': [
                ServiceRequestSyncStatus.NOT_SYNCED,
                ServiceRequestSyncStatus.FAILED,
            ],
            'fk_service_request__fk_organization': user_org,
        }
        pending_records = ServiceRequestSync.objects.filter(
            **pending_filter
        ).select_related('fk_service_request')

        if not pending_records.exists():
            return Response({
                'message': 'لا توجد طلبات تحتاج مزامنة',
                'total': 0,
            }, status=status.HTTP_200_OK)

        # ── 2. جلب بيانات الطلبات ──
        request_ids = pending_records.values_list('fk_service_request_id', flat=True)
        requests_qs = ServiceRequest.objects.filter(
            id__in=request_ids, is_deleted=False
        ).select_related(
            'fk_organization', 'fk_service', 'fk_service_version',
            'fk_requester', 'fk_grant_source',
            'grant_assigned_by', 'grant_cancel_by', 'grant_rejected_by',
            'discount_by', 'discount_rejected_by', 'discount_canceled_by',
        ).prefetch_related(
            'actions__fk_workflow_step',
            'actions__checklist_items',
            'installments',
            'attachments',
            'notes',
            'return_logs',
        )

        serializer = SyncRequestExportSerializer(requests_qs, many=True)
        payload = serializer.data

        # ── 3. إرسال إلى البوابة ──
        portal_url = getattr(settings, 'PORTAL_API_URL', '')
        if not portal_url:
            return Response({
                'error': 'PORTAL_API_URL غير مُعدّ في الإعدادات',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        receive_url = f'{portal_url}/api/d-services/portal/receive-requests-sync/'
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        headers = {
            'Content-Type': 'application/json',
            'Authorization': auth_header,
        }

        now = timezone.now()
        try:
            timeout = getattr(settings, 'PLATFORM_SYNC_REQUEST_TIMEOUT', 30)
            response = http_requests.post(
                receive_url,
                data=json.dumps({'items': payload}, default=str),
                headers=headers,
                timeout=(5, timeout),
            )
            response.raise_for_status()
            result = response.json()
        except http_requests.exceptions.Timeout:
            pending_records.update(**{
                system_field: ServiceRequestSyncStatus.FAILED,
                f'{system_field}_error': f'انتهت مهلة الاتصال بالبوابة',
                'last_sync_attempt': now,
            })
            return Response({
                'error': f'انتهت مهلة الاتصال بالبوابة ({timeout}s)',
            }, status=status.HTTP_504_GATEWAY_TIMEOUT)

        except http_requests.exceptions.ConnectionError:
            pending_records.update(**{
                system_field: ServiceRequestSyncStatus.FAILED,
                f'{system_field}_error': f'فشل الاتصال بالبوابة: {receive_url}',
                'last_sync_attempt': now,
            })
            return Response({
                'error': f'فشل الاتصال بالبوابة',
            }, status=status.HTTP_502_BAD_GATEWAY)

        except http_requests.exceptions.HTTPError as e:
            error_text = getattr(e.response, 'text', str(e))[:500]
            status_code = getattr(e.response, 'status_code', 0)
            pending_records.update(**{
                system_field: ServiceRequestSyncStatus.FAILED,
                f'{system_field}_error': f'HTTP {status_code}: {error_text}',
                'last_sync_attempt': now,
            })
            return Response({
                'error': f'البوابة رفضت الطلب (HTTP {status_code})',
            }, status=status.HTTP_502_BAD_GATEWAY)

        except Exception as e:
            logger.error('Unexpected request sync error: %s', e)
            pending_records.update(**{
                system_field: ServiceRequestSyncStatus.FAILED,
                f'{system_field}_error': str(e)[:500],
                'last_sync_attempt': now,
            })
            return Response({
                'error': f'خطأ غير متوقع: {str(e)[:200]}',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # ── 4. تحديث جدول المزامنة ──
        synced_ex_ids = result.get('created', []) + result.get('updated', [])
        if synced_ex_ids:
            ServiceRequestSync.objects.filter(
                fk_service_request__ex_id__in=synced_ex_ids
            ).update(**{
                system_field: ServiceRequestSyncStatus.SYNCED,
                f'{system_field}_error': '',
                'last_sync_attempt': now,
            })

        failed_items = result.get('failed', [])
        for item in failed_items:
            ex_id = item.get('ex_id')
            error = item.get('error', 'خطأ غير معروف')
            ServiceRequestSync.objects.filter(
                fk_service_request__ex_id=ex_id
            ).update(**{
                system_field: ServiceRequestSyncStatus.FAILED,
                f'{system_field}_error': error[:1000],
                'last_sync_attempt': now,
            })

        return Response({
            'message': 'تمت عملية مزامنة الطلبات',
            'total': len(payload),
            'synced': len(synced_ex_ids),
            'failed': len(failed_items),
            'details': result,
        }, status=status.HTTP_200_OK)
