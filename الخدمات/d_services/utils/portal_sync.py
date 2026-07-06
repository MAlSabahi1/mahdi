"""
Portal Pull Sync — يعمل على جانب QAS/المدارس/الجامعات
يسحب الطلبات من البوابة (Export API) ويحفظها كـ ServiceRequest
"""
import logging
import requests as http_requests

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.db import transaction
from django.utils.translation import gettext_lazy as _

from d_services.models.Service import Service
from d_services.models.ServiceRequest import ServiceRequest
from d_services.models.OrganizationServiceConfig import OrganizationServiceConfig
from d_services.choices.choices import (
    ServiceStatusChoice,
    PaymentStatusChoice,
    RequestSourceChoice,
)
from d_services.utils.portal_resolver import PortalTargetResolver
from d_services.utils.response_handler import ResponseHandler
from d_services.utils.calculation_handler import CalculationHandler
from d_services.utils.workflow_handler import WorkflowHandler

from OpenSoftCoreV4.common.models.Branch import Organization

logger = logging.getLogger(__name__)


class PortalPullSyncView(APIView):
    """
    Pull Sync — يسحب الطلبات من البوابة ويحفظها في QAS.

    POST /api/d-services/portal/sync/
    
    Body (اختياري):
    {
        "fk_org_service_config": <id>  // لتحديد خدمة/منظمة معينة
    }
    
    أو يستخدم المنظمة من المستخدم مباشرة.
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # نوع هذا النظام
        system_type = getattr(settings, 'PORTAL_SYNC_SYSTEM_TYPE', None)
        if not system_type:
            return ResponseHandler.bad_request(
                _('PORTAL_SYNC_SYSTEM_TYPE غير محدد في الإعدادات')
            )
        
        portal_url = getattr(settings, 'PORTAL_API_URL', None)
        if not portal_url:
            return ResponseHandler.bad_request(
                _('PORTAL_API_URL غير محدد في الإعدادات')
            )
        
        # تحديد المنظمة
        org = None
        org_ex_id = getattr(request.user, 'ogranizatoin_ex_id', None)
        if org_ex_id:
            org = Organization.objects.filter(ex_id=org_ex_id).first()
        
        if not org and request.user.fk_organization_id:
            org = request.user.fk_organization
        
        if not org:
            return ResponseHandler.bad_request(_('لا يمكن تحديد المنظمة من المستخدم'))
        
        # -----------------------------------------------------------------
        # 1. جلب الطلبات من البوابة (Export API)
        # -----------------------------------------------------------------
        try:
            # نستخدم التوكن الحالي للمصادقة مع البوابة (SSO موحد)
            auth_header = request.META.get('HTTP_AUTHORIZATION', '')
            
            export_response = http_requests.get(
                f'{portal_url.rstrip("/")}/api/d-services/portal/export-requests/',
                params={'system': system_type},
                headers={
                    'Authorization': auth_header,
                    'Content-Type': 'application/json',
                },
                timeout=30,
            )
            export_response.raise_for_status()
            export_data = export_response.json()
            portal_items = export_data.get('items', [])
        except http_requests.RequestException as e:
            logger.error(f'Portal export fetch failed: {e}')
            return ResponseHandler.error(
                _('فشل الاتصال بنظام البوابة'),
                details={'error': str(e)}
            )
        
        if not portal_items:
            return ResponseHandler.success(
                message=_('لا توجد طلبات جديدة للمزامنة'),
                data={'created': 0, 'failed': 0, 'skipped': 0}
            )
        
        # -----------------------------------------------------------------
        # 2. معالجة كل طلب
        # -----------------------------------------------------------------
        results = {
            'created': 0, 'failed': 0, 'skipped': 0,
            'synced_ids': [], 'failed_items': [], 'errors': [],
        }
        
        for item in portal_items:
            try:
                sync_id = item.get('id')  # ServiceRequestSync.id
                service_code = item.get('service_code')
                portal_request_id = item.get('portal_request_id')
                
                if not service_code:
                    results['failed'] += 1
                    results['failed_items'].append({
                        'sync_id': sync_id, 'error': 'service_code مفقود',
                    })
                    continue
                
                # التحقق من عدم التكرار
                if portal_request_id and ServiceRequest.objects.filter(
                    request_source=RequestSourceChoice.PORTAL,
                    base_component_data__portal_request_id=str(portal_request_id),
                    is_deleted=False,
                ).exists():
                    results['skipped'] += 1
                    results['synced_ids'].append(sync_id)
                    continue
                
                # جلب الخدمة
                service = Service.objects.filter(code=service_code).first()
                if not service:
                    results['failed'] += 1
                    results['failed_items'].append({
                        'sync_id': sync_id,
                        'error': f'الخدمة غير موجودة: {service_code}',
                    })
                    continue
                
                # جلب org_config
                org_config = OrganizationServiceConfig.objects.filter(
                    fk_service=service,
                    fk_organization=org,
                    is_active=True,
                    is_deleted=False,
                ).first()
                if not org_config:
                    results['failed'] += 1
                    results['failed_items'].append({
                        'sync_id': sync_id,
                        'error': f'الخدمة غير مفعلة للمنظمة: {service.code}',
                    })
                    continue
                
                # تحويل target data
                target_data = item.get('target_audience_data', {})
                qas_target = PortalTargetResolver.resolve(service, target_data)
                
                # إنشاء الطلب
                with transaction.atomic():
                    service_request = _create_service_request(
                        service=service,
                        organization=org,
                        org_config=org_config,
                        portal_item=item,
                        qas_target_data=qas_target,
                    )
                
                results['created'] += 1
                results['synced_ids'].append(sync_id)
                
                logger.info(
                    f'Portal sync OK: {service_request.request_number} '
                    f'(portal_id={portal_request_id})'
                )
                
            except Exception as e:
                results['failed'] += 1
                results['failed_items'].append({
                    'sync_id': item.get('id'),
                    'error': str(e),
                })
                logger.error(f'Portal sync item failed: {e}', exc_info=True)
        
        # -----------------------------------------------------------------
        # 3. إبلاغ البوابة بالنتائج (mark-synced)
        # -----------------------------------------------------------------
        try:
            http_requests.post(
                f'{portal_url.rstrip("/")}/api/d-services/portal/mark-synced/',
                json={
                    'system': system_type,
                    'synced_ids': results['synced_ids'],
                    'failed_items': results['failed_items'],
                },
                headers={
                    'Authorization': auth_header,
                    'Content-Type': 'application/json',
                },
                timeout=15,
            )
        except http_requests.RequestException as e:
            logger.warning(f'Mark-synced call failed: {e}')
            # لا نفشل العملية — البيانات محفوظة
        
        return ResponseHandler.success(
            message=_(
                f'تمت المزامنة: {results["created"]} جديد'
                f'{", " + str(results["skipped"]) + " تم تخطيه" if results["skipped"] else ""}'
                f'{", " + str(results["failed"]) + " فشل" if results["failed"] else ""}'
            ),
            data={
                'created': results['created'],
                'failed': results['failed'],
                'skipped': results['skipped'],
                'errors': results['errors'],
            }
        )


def _create_service_request(service, organization, org_config, portal_item, qas_target_data):
    """إنشاء ServiceRequest من بيانات البوابة"""
    from django.utils import timezone
    
    # رقم الطلب
    request_number = CalculationHandler.generate_request_number(
        organization, org_config
    )
    
    # الرسوم
    fees = CalculationHandler.calculate_fees(
        service, org_config, organization,
        requester_id=portal_item.get('requester_id')
    )
    
    current_version = service.versions.filter(is_current=True).first()
    
    from d_services.utils.image_handler import ERPHandler
    erp_data = {}
    
    fee_amount = fees.get('total_fee', 0)
    fee_currency_id = org_config.fk_currency_id if org_config.fk_currency_id else None
    
    base_data = portal_item.get('base_component_data', {})
    if not isinstance(base_data, dict):
        base_data = {}
    base_data['portal_request_id'] = str(portal_item.get('portal_request_id', ''))
    base_data['portal_sync_at'] = timezone.now().isoformat()
    
    return ServiceRequest.objects.create(
        fk_organization=organization,
        fk_service=service,
        fk_service_version=current_version,
        requester_name=portal_item.get('requester_name', ''),
        requester_description=portal_item.get('requester_description', ''),
        requester_id=portal_item.get('requester_id'),
        request_number=request_number,
        request_source=RequestSourceChoice.PORTAL,
        target_audience_component=service.target_audience_component,
        target_audience_data=qas_target_data,
        base_audience_component=service.base_audience_component,
        base_component_data=base_data,
        version_data=portal_item.get('version_data'),
        output_template_type=service.output_template_type,
        input_template_type=service.input_template_type,
        output_data_function=service.output_data_function,
        input_data_function=service.input_data_function,
        status=ServiceStatusChoice.PENDING,
        priority=portal_item.get('priority', 'normal'),
        has_approvals=service.requires_approval,
        total_fee=fee_amount,
        discounted_fee=fees.get('discounted_fee', 0),
        discounted_fee_reason=fees.get('discounted_fee_reason'),
        amount_paid=fees.get('amount_paid', 0),
        remaining_amount=fees.get('remaining_amount', 0),
        payment_status=fees.get('payment_status', PaymentStatusChoice.UNPAID),
        fk_currency_id=fee_currency_id,
        workflow_stages_snapshot=WorkflowHandler.get_workflow_snapshot(service),
        prerequisites_snapshot=WorkflowHandler.get_prerequisites_snapshot(service),
        # ERP integration
        is_donor_invoice_allowed=ERPHandler.get_field(erp_data, 'is_donor_invoice_allowed', org_config.is_donor_invoice_allowed),
        is_discount_allowed=ERPHandler.get_field(erp_data, 'is_discount_allowed', org_config.is_discount_allowed),
        erp_product_id=ERPHandler.get_field(erp_data, 'erp_product_id', org_config.erp_product_id),
        erp_product_name=ERPHandler.get_field(erp_data, 'erp_product_name', org_config.erp_product_name),
        erp_product_for_discount_id=ERPHandler.get_field(erp_data, 'erp_product_for_discount_id', org_config.erp_product_for_discount_id),
        erp_product_for_discount_name=ERPHandler.get_field(erp_data, 'erp_product_for_discount_name', org_config.erp_product_for_discount_name),
        erp_product_for_internal_donors_id=ERPHandler.get_field(erp_data, 'erp_product_for_internal_donors_id', org_config.erp_product_for_internal_donors_id),
        erp_product_for_internal_donors_name=ERPHandler.get_field(erp_data, 'erp_product_for_internal_donors_name', org_config.erp_product_for_internal_donors_name),
        erp_project_id=ERPHandler.get_field(erp_data, 'erp_project_id', org_config.erp_project_id),
        erp_project_name=ERPHandler.get_field(erp_data, 'erp_project_name', org_config.erp_project_name),
        erp_activity_id=ERPHandler.get_field(erp_data, 'erp_activity_id', org_config.erp_activity_id),
        erp_activity_name=ERPHandler.get_field(erp_data, 'erp_activity_name', org_config.erp_activity_name),
        erp_cost_center_id=ERPHandler.get_field(erp_data, 'erp_cost_center_id', org_config.erp_cost_center_id),
        erp_cost_center_name=ERPHandler.get_field(erp_data, 'erp_cost_center_name', org_config.erp_cost_center_name),
    )
