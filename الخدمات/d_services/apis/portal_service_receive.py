"""
Client API — يعمل على نظام البوابة
يستقبل الخدمات من النظام الفرعي ويحفظها/يحدثها محلياً

POST /api/d-services/portal/receive-services/
"""
import logging
import traceback

from django.db import transaction
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from d_services.models.Service import Service
from d_services.models.OrganizationServiceConfig import OrganizationServiceConfig
from d_services.models.ServiceERPSettings import ServiceERPSettings
from d_services.models.ServiceInstallmentPlan import ServiceInstallmentPlan
from d_services.models.ServicePrerequisite import ServicePrerequisite
from d_services.models.ServiceVersion import ServiceVersion
from d_services.models.ServiceWorkflowStep import ServiceWorkflowStep
from d_services.models.ServiceWorkFlowStepPermission import ServiceWorkFlowStepPermission
from d_services.models.StageChecklistItem import WorkflowStepChecklistTemplate
from d_services.models.WorkflowStage import WorkflowStage
from d_services.models.WorkflowStepPrintReportSetting import WorkflowStepPrintReportSetting

logger = logging.getLogger(__name__)


def _require_superuser(user):
    from d_services.utils.exception_handler import ValidationException
    if not user.is_superuser:
        raise ValidationException('هذه العملية متاحة فقط لمدير النظام (SuperAdmin)')


def _get_or_create_by_ex_id(model, ex_id, defaults=None):
    """
    بحث عن عنصر بـ ex_id — إذا موجود يحدثه، وإلا ينشئ جديداً.
    يرجع (instance, created)
    """
    defaults = defaults or {}
    try:
        # Some models use SoftDeleteManager which filters is_deleted=False
        # Use all_objects if available to find even soft-deleted records
        manager = getattr(model, 'objects', None)
        if hasattr(manager, 'all_objects'):
            instance = manager.all_objects().filter(ex_id=ex_id).first()
        else:
            instance = model.objects.filter(ex_id=ex_id).first()

        if instance:
            # تحديث الحقول
            for key, val in defaults.items():
                setattr(instance, key, val)
            if hasattr(instance, 'is_deleted'):
                instance.is_deleted = False
            instance.save()
            return instance, False
        else:
            instance = model(ex_id=ex_id, **defaults)
            instance.save()
            return instance, True
    except Exception as e:
        raise ValueError(f'خطأ في حفظ {model.__name__} (ex_id={ex_id}): {str(e)}')


def _resolve_organization(org_ex_id):
    """بحث عن Organization بـ ex_id"""
    from OpenSoftCoreV4.common.models.Branch import Organization
    org = Organization.objects.filter(ex_id=org_ex_id).first()
    if not org:
        raise ValueError(f'المنظمة غير موجودة: ex_id={org_ex_id}')
    return org


def _save_service_data(item):
    """
    حفظ خدمة واحدة مع كل علاقاتها في transaction واحد.
    يرمي exception عند أي خطأ ليتم الـ rollback.
    """
    service_ex_id = item['ex_id']

    # ── 1. WorkflowStage (مستقلة — ليس لها FK للخدمة) ──────
    stages_data = item.get('workflow_stages', [])
    stage_map = {}  # ex_id → local instance
    for stage_item in stages_data:
        stage, _ = _get_or_create_by_ex_id(WorkflowStage, stage_item['ex_id'], {
            'name_ar': stage_item['name_ar'],
            'name_en': stage_item.get('name_en'),
            'stage_type': stage_item['stage_type'],
            'is_final_stage': stage_item.get('is_final_stage', False),
            'is_execution_stage': stage_item.get('is_execution_stage', False),
            'expected_duration_days': stage_item.get('expected_duration_days', 1),
        })
        stage_map[str(stage_item['ex_id'])] = stage

    # ── 2. Service ─────────────────────────────────────────────
    service_fields = {
        'code': item['code'],
        'name_ar': item['name_ar'],
        'name_en': item.get('name_en'),
        'description': item.get('description'),
        'category': item.get('category', 'other'),
        'icon': item.get('icon'),
        'requires_approval': item.get('requires_approval', True),
        'is_repeatable': item.get('is_repeatable', True),
        'is_active': item.get('is_active', True),
        'start_date': item.get('start_date'),
        'output_template_type': item.get('output_template_type'),
        'input_template_type': item.get('input_template_type'),
        'output_data_function': item.get('output_data_function'),
        'input_data_function': item.get('input_data_function'),
        'erp_data_function': item.get('erp_data_function'),
        'erp_specialization_data_autolist': item.get('erp_specialization_data_autolist'),
        'erp_study_system_data_autolist': item.get('erp_study_system_data_autolist'),
        'target_audience_component': item.get('target_audience_component'),
        'base_audience_component': item.get('base_audience_component'),
        'requester_image_function': item.get('requester_image_function'),
        'requester_info_function': item.get('requester_info_function'),
        'target_system_type': item.get('target_system_type'),
    }
    service, service_created = _get_or_create_by_ex_id(Service, service_ex_id, service_fields)

    # ── 3. ServicePrerequisite ─────────────────────────────────
    for prereq_item in item.get('prerequisites', []):
        _get_or_create_by_ex_id(ServicePrerequisite, prereq_item['ex_id'], {
            'fk_service': service,
            'name_ar': prereq_item['name_ar'],
            'name_en': prereq_item.get('name_en'),
            'description': prereq_item.get('description'),
            'status': prereq_item.get('status', 'mandatory'),
            'validation_procedure_name': prereq_item.get('validation_procedure_name'),
            'order': prereq_item.get('order', 1),
        })

    # ── 4. ServiceVersion ──────────────────────────────────────
    for ver_item in item.get('versions', []):
        _get_or_create_by_ex_id(ServiceVersion, ver_item['ex_id'], {
            'fk_service': service,
            'version_name': ver_item['version_name'],
            'component_type': ver_item.get('component_type', 'form'),
            'is_current': ver_item.get('is_current', False),
            'fields_schema': ver_item.get('fields_schema', {}),
            'is_locked': ver_item.get('is_locked', False),
        })

    # ── 5. ServiceWorkflowStep + Permissions ──────────────────
    step_map = {}  # ex_id → local instance
    for step_item in item.get('workflow_steps', []):
        stage_ex_id = str(step_item.get('stage_ex_id', ''))
        stage = stage_map.get(stage_ex_id)
        if not stage:
            stage = WorkflowStage.objects.filter(ex_id=stage_ex_id).first()
        if not stage:
            raise ValueError(f'WorkflowStage غير موجود: ex_id={stage_ex_id}')

        step, _ = _get_or_create_by_ex_id(ServiceWorkflowStep, step_item['ex_id'], {
            'fk_service': service,
            'fk_stage': stage,
            'order': step_item['order'],
            'description': step_item.get('description'),
            'is_final_step': step_item.get('is_final_step', False),
            'is_execution_step': step_item.get('is_execution_step', False),
            'has_custom_output': step_item.get('has_custom_output', False),
            'has_approval': step_item.get('has_approval', False),
            'custom_output_template': step_item.get('custom_output_template'),
            'custom_output_function': step_item.get('custom_output_function'),
            'has_custom_input': step_item.get('has_custom_input', False),
            'custom_input_template': step_item.get('custom_input_template'),
            'custom_input_function': step_item.get('custom_input_function'),
            'start_offset_days': step_item.get('start_offset_days', 0),
            'delivery_offset_days': step_item.get('delivery_offset_days', 1),
            'execution_procedure_name': step_item.get('execution_procedure_name'),
            'icon': step_item.get('icon'),
        })
        step_map[str(step_item['ex_id'])] = step

        # Permissions
        for perm_item in step_item.get('permissions', []):
            _get_or_create_by_ex_id(ServiceWorkFlowStepPermission, perm_item['ex_id'], {
                'fk_workflow_step': step,
                'permission_type': perm_item['permission_type'],
            })

    # ── 6. OrganizationServiceConfig + children ───────────────
    for osc_item in item.get('org_configs', []):
        org_ex_id = osc_item.get('organization_ex_id')
        org = _resolve_organization(org_ex_id)

        currency_id = osc_item.get('currency_id')

        osc_fields = {
            'fk_service': service,
            'fk_organization': org,
            'fk_currency_id': currency_id,
            'is_installment_allowed': osc_item.get('is_installment_allowed', False),
            'installments_count': osc_item.get('installments_count', 1),
            'is_paid': osc_item.get('is_paid', True),
            'free_limit_per_year': osc_item.get('free_limit_per_year', 0),
            'fee_amount': osc_item.get('fee_amount', 0),
            'installment_period': osc_item.get('installment_period'),
            'request_prefix': osc_item.get('request_prefix'),
            'is_active': osc_item.get('is_active', True),
            'is_locked': osc_item.get('is_locked', False),
            'locked_reason': osc_item.get('locked_reason'),
            # ERP fields
            'is_donor_invoice_allowed': osc_item.get('is_donor_invoice_allowed', True),
            'is_discount_allowed': osc_item.get('is_discount_allowed', True),
            'erp_product_id': osc_item.get('erp_product_id'),
            'erp_product_name': osc_item.get('erp_product_name'),
            'erp_product_for_discount_id': osc_item.get('erp_product_for_discount_id'),
            'erp_product_for_discount_name': osc_item.get('erp_product_for_discount_name'),
            'erp_product_for_internal_donors_id': osc_item.get('erp_product_for_internal_donors_id'),
            'erp_product_for_internal_donors_name': osc_item.get('erp_product_for_internal_donors_name'),
            'erp_project_id': osc_item.get('erp_project_id'),
            'erp_project_name': osc_item.get('erp_project_name'),
            'erp_activity_id': osc_item.get('erp_activity_id'),
            'erp_activity_name': osc_item.get('erp_activity_name'),
            'erp_cost_center_id': osc_item.get('erp_cost_center_id'),
            'erp_cost_center_name': osc_item.get('erp_cost_center_name'),
        }
        osc, _ = _get_or_create_by_ex_id(OrganizationServiceConfig, osc_item['ex_id'], osc_fields)

        # ── 6a. ServiceInstallmentPlan ─────────────────────────
        for plan_item in osc_item.get('installment_plans', []):
            _get_or_create_by_ex_id(ServiceInstallmentPlan, plan_item['ex_id'], {
                'fk_org_service_config': osc,
                'amount': plan_item['amount'],
                'order': plan_item['order'],
                'due_days_from_request': plan_item['due_days_from_request'],
            })

        # ── 6b. ServiceERPSettings ─────────────────────────────
        for erp_item in osc_item.get('erp_settings', []):
            _get_or_create_by_ex_id(ServiceERPSettings, erp_item['ex_id'], {
                'fk_org_service_config': osc,
                'specialization_id': erp_item['specialization_id'],
                'study_system_id': erp_item.get('study_system_id'),
                'service_fee': erp_item.get('service_fee', 0),
                'is_donor_invoice_allowed': erp_item.get('is_donor_invoice_allowed', True),
                'is_discount_allowed': erp_item.get('is_discount_allowed', True),
                'erp_product_id': erp_item.get('erp_product_id'),
                'erp_product_name': erp_item.get('erp_product_name'),
                'erp_product_for_discount_id': erp_item.get('erp_product_for_discount_id'),
                'erp_product_for_discount_name': erp_item.get('erp_product_for_discount_name'),
                'erp_product_for_internal_donors_id': erp_item.get('erp_product_for_internal_donors_id'),
                'erp_product_for_internal_donors_name': erp_item.get('erp_product_for_internal_donors_name'),
                'erp_project_id': erp_item.get('erp_project_id'),
                'erp_project_name': erp_item.get('erp_project_name'),
                'erp_activity_id': erp_item.get('erp_activity_id'),
                'erp_activity_name': erp_item.get('erp_activity_name'),
                'erp_cost_center_id': erp_item.get('erp_cost_center_id'),
                'erp_cost_center_name': erp_item.get('erp_cost_center_name'),
            })

        # ── 6c. WorkflowStepChecklistTemplate ──────────────────
        for tmpl_item in osc_item.get('checklist_templates', []):
            ws_ex_id = str(tmpl_item.get('workflow_step_ex_id', ''))
            ws = step_map.get(ws_ex_id)
            if not ws:
                ws = ServiceWorkflowStep.objects.filter(ex_id=ws_ex_id).first()
            if not ws:
                raise ValueError(f'ServiceWorkflowStep غير موجود: ex_id={ws_ex_id}')

            _get_or_create_by_ex_id(WorkflowStepChecklistTemplate, tmpl_item['ex_id'], {
                'fk_org_service_config': osc,
                'fk_workflow_step': ws,
                'title': tmpl_item['title'],
                'description': tmpl_item.get('description'),
                'order': tmpl_item.get('order', 0),
                'is_required': tmpl_item.get('is_required', True),
            })

        # ── 6d. WorkflowStepPrintReportSetting ─────────────────
        for prs_item in osc_item.get('print_report_settings', []):
            ws_ex_id = str(prs_item.get('workflow_step_ex_id', ''))
            ws = step_map.get(ws_ex_id)
            if not ws:
                ws = ServiceWorkflowStep.objects.filter(ex_id=ws_ex_id).first()
            if not ws:
                raise ValueError(f'ServiceWorkflowStep غير موجود: ex_id={ws_ex_id}')

            _get_or_create_by_ex_id(WorkflowStepPrintReportSetting, prs_item['ex_id'], {
                'fk_org_service_config': osc,
                'fk_workflow_step': ws,
            })

    return service, service_created


class PortalServiceReceiveView(APIView):
    """
    Client API — يعمل على البوابة
    يستقبل خدمات من النظام الفرعي ويحفظها محلياً
    كل خدمة في transaction مستقل — عند الخطأ يلغي الخدمة فقط
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        _require_superuser(request.user)

        items = request.data.get('items', [])
        if not items:
            return Response({
                'error': 'لا توجد بيانات للمزامنة (items فارغة)',
            }, status=status.HTTP_400_BAD_REQUEST)

        created_ids = []
        updated_ids = []
        failed_items = []

        for item in items:
            ex_id = item.get('ex_id', 'unknown')
            try:
                with transaction.atomic():
                    service, was_created = _save_service_data(item)
                    if was_created:
                        created_ids.append(str(ex_id))
                    else:
                        updated_ids.append(str(ex_id))

            except Exception as e:
                logger.error(
                    'فشل حفظ الخدمة ex_id=%s: %s\n%s',
                    ex_id, e, traceback.format_exc()
                )
                failed_items.append({
                    'ex_id': str(ex_id),
                    'error': str(e)[:500],
                })

        return Response({
            'created': created_ids,
            'updated': updated_ids,
            'failed': failed_items,
            'total': len(items),
            'success_count': len(created_ids) + len(updated_ids),
            'failed_count': len(failed_items),
        }, status=status.HTTP_200_OK)
