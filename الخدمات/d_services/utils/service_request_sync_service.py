"""
Service Request Sync Service — دوال مساعدة لتتبع مزامنة الطلبات
نفس نمط object_sync_service.py في الكور
"""
import logging
from django.utils import timezone

from d_services.models.ServiceRequestSync import (
    ServiceRequestSync,
    ServiceRequestSyncStatus,
)
from OpenSoftCoreV4.platform_sync.platform_sync_settings import TypeOfMainSystemChoices

logger = logging.getLogger(__name__)


# ── System fields mapping ─────────────────────────────────────────
SYSTEM_FIELDS = ('school', 'university', 'institute')

SYSTEM_FIELD_TO_ROLE = {
    'school': TypeOfMainSystemChoices.SCHOOL,
    'university': TypeOfMainSystemChoices.UNIVERSITY,
    'institute': TypeOfMainSystemChoices.INSTITUTE,
}

ROLE_TO_SYSTEM_FIELD = {v: k for k, v in SYSTEM_FIELD_TO_ROLE.items()}

SYSTEM_ERROR_FIELDS = {field: f'{field}_error' for field in SYSTEM_FIELDS}


def track_request_created(service_request, portal_request_id=''):

    """
    تسجيل طلب جديد في جدول المزامنة.
    يقرأ target_system_type من الخدمة:
    - النظام المستهدف → NOT_SYNCED
    - البقية → CANNOT_SYNC
    """

    try:
        target_role = service_request.fk_service.target_system_type
        
        defaults = {}
        for field, role in SYSTEM_FIELD_TO_ROLE.items():
            if role == target_role:
                defaults[field] = ServiceRequestSyncStatus.NOT_SYNCED
            else:
                defaults[field] = ServiceRequestSyncStatus.CANNOT_SYNC
        
        ServiceRequestSync.objects.create(
            fk_service_request=service_request,
            portal_request_id=str(portal_request_id) if portal_request_id else '',
            **defaults,
        )
    except Exception as exc:
        logger.warning(
            'Failed to create ServiceRequestSync for request %s: %s',
            getattr(service_request, 'request_number', '?'), exc,
        )

def mark_request_modified(service_request_id):
    """
    عند تعديل طلب مزامن: SYNCED → MODIFIED_AFTER_SYNC
    الأنظمة التي حالتها NOT_SYNCED أو CANNOT_SYNC لا تتغير
    """
    try:
        sync_obj = ServiceRequestSync.objects.filter(
            fk_service_request_id=service_request_id
        ).first()
        if not sync_obj:
            return
        
        updated_fields = []
        for field in SYSTEM_FIELDS:
            if getattr(sync_obj, field) == ServiceRequestSyncStatus.SYNCED:
                setattr(sync_obj, field, ServiceRequestSyncStatus.MODIFIED_AFTER_SYNC)
                updated_fields.append(field)
        
        if updated_fields:
            sync_obj.save(update_fields=updated_fields)
    except Exception as exc:
        logger.warning(
            'Failed to mark modified for request %s: %s',
            service_request_id, exc,
        )


def get_pending_for_system(system_field, organization=None, service_code=None):
    """
    جلب سجلات المزامنة المعلقة لنظام معين.
    (NOT_SYNCED, MODIFIED_AFTER_SYNC, FAILED)
    """
    from django.db.models import Q
    
    qs = ServiceRequestSync.objects.filter(
        Q(**{system_field: ServiceRequestSyncStatus.NOT_SYNCED})
        | Q(**{system_field: ServiceRequestSyncStatus.MODIFIED_AFTER_SYNC})
        | Q(**{system_field: ServiceRequestSyncStatus.FAILED}),
        is_deleted=False,
    ).select_related(
        'fk_service_request',
        'fk_service_request__fk_service',
        'fk_service_request__fk_organization',
    )
    
    if organization:
        qs = qs.filter(fk_service_request__fk_organization=organization)
    
    if service_code:
        qs = qs.filter(fk_service_request__fk_service__code=service_code)
    
    return qs


def mark_system_synced(sync_ids, system_field):
    """
    تحديث حالة الأنظمة → SYNCED وحذف الخطأ
    """
    if not sync_ids:
        return 0
    
    error_field = SYSTEM_ERROR_FIELDS.get(system_field, '')
    update_kwargs = {
        system_field: ServiceRequestSyncStatus.SYNCED,
        'last_sync_attempt': timezone.now(),
    }
    if error_field:
        update_kwargs[error_field] = ''
    
    return ServiceRequestSync.objects.filter(
        id__in=list(sync_ids),
    ).update(**update_kwargs)


def mark_system_failed(sync_ids, system_field, error_message):
    """
    تحديث حالة الأنظمة → FAILED مع رسالة الخطأ
    """
    if not sync_ids:
        return 0
    
    error_field = SYSTEM_ERROR_FIELDS.get(system_field, '')
    update_kwargs = {
        system_field: ServiceRequestSyncStatus.FAILED,
        'last_sync_attempt': timezone.now(),
    }
    if error_field:
        update_kwargs[error_field] = str(error_message)[:2000]
    
    return ServiceRequestSync.objects.filter(
        id__in=list(sync_ids),
    ).update(**update_kwargs)


def mark_system_failed_per_item(failed_items, system_field):
    """
    تحديث كل عنصر بخطأ مخصص
    failed_items: [{'sync_id': id, 'error': 'message'}, ...]
    """
    error_field = SYSTEM_ERROR_FIELDS.get(system_field, '')
    now = timezone.now()
    count = 0
    
    for item in failed_items:
        sync_id = item.get('sync_id')
        error_msg = item.get('error', 'خطأ غير معروف')
        if not sync_id:
            continue
        
        update_kwargs = {
            system_field: ServiceRequestSyncStatus.FAILED,
            'last_sync_attempt': now,
        }
        if error_field:
            update_kwargs[error_field] = str(error_msg)[:2000]
        
        count += ServiceRequestSync.objects.filter(
            id=sync_id,
        ).update(**update_kwargs)
    
    return count
