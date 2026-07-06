"""
Server API — يعمل على النظام الفرعي (QAS)
يُنظّم عملية المزامنة: يجلب الخدمات غير المتزامنة ويرسلها إلى البوابة

POST /api/d-services/portal/trigger-service-sync/
"""
import logging
import requests as http_requests
import json

from django.conf import settings
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from d_services.models.Service import Service
from d_services.models.ServiceSync import ServiceSync, ServiceSyncStatus
from d_services.serializers.service_sync_serializers import SyncServiceExportSerializer

logger = logging.getLogger(__name__)


def _require_superuser(user):
    """تحقق أن المستخدم سوبر أدمن"""
    from d_services.utils.exception_handler import ValidationException
    if not user.is_superuser:
        raise ValidationException('هذه العملية متاحة فقط لمدير النظام (SuperAdmin)')


class TriggerServiceSyncView(APIView):
    """
    Trigger sync — يُستدعى من الفرونت في النظام الفرعي
    يجلب الخدمات غير المتزامنة ويرسلها للبوابة
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        _require_superuser(request.user)

        # ── 1. جلب السجلات التي تحتاج مزامنة ──────────────────
        pending_records = ServiceSync.objects.filter(
            status__in=[ServiceSyncStatus.NOT_SYNCED, ServiceSyncStatus.FAILED]
        ).select_related('fk_service')

        if not pending_records.exists():
            return Response({
                'message': 'لا توجد خدمات تحتاج مزامنة',
                'total': 0,
            }, status=status.HTTP_200_OK)

        # ── 2. جلب بيانات الخدمات ──────────────────────────────
        service_ids = pending_records.values_list('fk_service_id', flat=True)
        services = Service.objects.filter(
            id__in=service_ids, is_deleted=False
        ).prefetch_related(
            'workflow_steps__fk_stage',
            'workflow_steps__permissions',
            'prerequisites',
            'versions',
            'org_configs__fk_organization',
            'org_configs__fk_currency',
            'org_configs__installment_plans',
            'org_configs__service_specialization_settings',
            'org_configs__checklist_templates',
            'org_configs__workflow_step_print_settings',
        )

        # تعبئة target_system_type من الإعدادات
        system_type = getattr(settings, 'PORTAL_SYNC_SYSTEM_TYPE', '')
        for svc in services:
            if not svc.target_system_type and system_type:
                svc.target_system_type = system_type
                svc.save(update_fields=['target_system_type'])

        serializer = SyncServiceExportSerializer(services, many=True)
        payload = serializer.data

        # ── 3. إرسال إلى البوابة ───────────────────────────────
        portal_url = getattr(settings, 'PORTAL_API_URL', '')
        if not portal_url:
            return Response({
                'error': 'PORTAL_API_URL غير مُعدّ في الإعدادات',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        receive_url = f'{portal_url}/api/d-services/portal/receive-services/'

        # استخدام SSO token من المستخدم الحالي
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        headers = {
            'Content-Type': 'application/json',
            'Authorization': auth_header,
        }

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
            # فشل بسبب timeout — تسجيل الكل كفشل
            now = timezone.now()
            pending_records.update(
                status=ServiceSyncStatus.FAILED,
                error_message=f'انتهت مهلة الاتصال بالبوابة: {receive_url}',
                last_synced_at=now,
            )
            return Response({
                'error': f'انتهت مهلة الاتصال بالبوابة ({timeout}s)',
                'total': pending_records.count(),
                'synced': 0,
                'failed': pending_records.count(),
            }, status=status.HTTP_504_GATEWAY_TIMEOUT)

        except http_requests.exceptions.ConnectionError:
            now = timezone.now()
            pending_records.update(
                status=ServiceSyncStatus.FAILED,
                error_message=f'فشل الاتصال بالبوابة: {receive_url}',
                last_synced_at=now,
            )
            return Response({
                'error': f'فشل الاتصال بالبوابة: {receive_url}',
                'total': pending_records.count(),
                'synced': 0,
                'failed': pending_records.count(),
            }, status=status.HTTP_502_BAD_GATEWAY)

        except http_requests.exceptions.HTTPError as e:
            error_text = getattr(e.response, 'text', str(e))[:500]
            status_code = getattr(e.response, 'status_code', 0)
            now = timezone.now()
            pending_records.update(
                status=ServiceSyncStatus.FAILED,
                error_message=f'HTTP {status_code}: {error_text}',
                last_synced_at=now,
            )
            return Response({
                'error': f'البوابة رفضت الطلب (HTTP {status_code})',
                'details': error_text,
            }, status=status.HTTP_502_BAD_GATEWAY)

        except Exception as e:
            logger.error('Unexpected sync error: %s', e)
            now = timezone.now()
            pending_records.update(
                status=ServiceSyncStatus.FAILED,
                error_message=str(e)[:500],
                last_synced_at=now,
            )
            return Response({
                'error': f'خطأ غير متوقع: {str(e)[:200]}',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # ── 4. تحديث جدول المزامنة بناءً على النتائج ──────────
        now = timezone.now()

        # الناجحة (created + updated)
        synced_ex_ids = result.get('created', []) + result.get('updated', [])
        if synced_ex_ids:
            ServiceSync.objects.filter(
                fk_service__ex_id__in=synced_ex_ids
            ).update(
                status=ServiceSyncStatus.SUCCESS,
                error_message='',
                last_synced_at=now,
            )

        # الفاشلة
        failed_items = result.get('failed', [])
        for item in failed_items:
            ex_id = item.get('ex_id')
            error = item.get('error', 'خطأ غير معروف')
            ServiceSync.objects.filter(
                fk_service__ex_id=ex_id
            ).update(
                status=ServiceSyncStatus.FAILED,
                error_message=error[:1000],
                last_synced_at=now,
            )

        return Response({
            'message': 'تمت عملية المزامنة',
            'total': len(payload),
            'synced': len(synced_ex_ids),
            'failed': len(failed_items),
            'details': result,
        }, status=status.HTTP_200_OK)
