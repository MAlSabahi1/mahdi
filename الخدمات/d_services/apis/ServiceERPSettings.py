"""
ServiceERPSettings API
- list:   returns all_settings scoped to request.user's organization + org_config defaults
- create: bulk sync (create/update/delete) with erp_data_function defaults
"""
import logging
from django.utils.translation import gettext_lazy as _

from d_services.models.ServiceERPSettings import ServiceERPSettings
from d_services.models.OrganizationServiceConfig import OrganizationServiceConfig
from d_services.models.Service import Service
from d_services.serializers.ServiceERPSettings import ServiceERPSettingsSerializer
from d_services.serializers.services import OrganizationServiceConfigSerializer
from config.imports.viewmodel_core import AllMVS
from d_services.utils.exception_handler import handle_exceptions
from d_services.utils.permission_checker import PermissionChecker
from d_services.utils.bulk_sync_handler import BulkSyncHandler
from d_services.utils.response_handler import ResponseHandler
from d_services.utils.service_config_handler import ServiceConfigHandler
from d_services.apis.external_methods.base import ExternalMethodHandler, FunctionType

logger = logging.getLogger(__name__)

# Fields that the erp_data_function can provide as defaults
ERP_DEFAULT_FIELDS = [
    'service_fee',
    'fk_currency',
    'is_donor_invoice_allowed',
    'is_discount_allowed',
    'erp_product_id',
    'erp_product_name',
    'erp_product_for_discount_id',
    'erp_product_for_discount_name',
    'erp_product_for_internal_donors_id',
    'erp_product_for_internal_donors_name',
    'erp_project_id',
    'erp_project_name',
    'erp_activity_id',
    'erp_activity_name',
    'erp_cost_center_id',
    'erp_cost_center_name',
]

# Fields that BulkSyncHandler is allowed to update
UPDATABLE_FIELDS = [
    'specialization_id',
    'study_system_id',
    'fk_currency',
    'service_fee',
    'is_donor_invoice_allowed',
    'is_discount_allowed',
    'erp_product_id',
    'erp_product_name',
    'erp_product_for_discount_id',
    'erp_product_for_discount_name',
    'erp_product_for_internal_donors_id',
    'erp_product_for_internal_donors_name',
    'erp_project_id',
    'erp_project_name',
    'erp_activity_id',
    'erp_activity_name',
    'erp_cost_center_id',
    'erp_cost_center_name',
]


def _get_org_config_defaults(org_config):
    """Build a dict of ERP defaults from the org_config (fallback values)."""
    return {
        'service_fee': org_config.fee_amount,
        'fk_currency': org_config.fk_currency.code if org_config.fk_currency else None,
        'is_donor_invoice_allowed': org_config.is_donor_invoice_allowed,
        'is_discount_allowed': org_config.is_discount_allowed,
        'erp_product_id': org_config.erp_product_id,
        'erp_product_name': org_config.erp_product_name,
        'erp_product_for_discount_id': org_config.erp_product_for_discount_id,
        'erp_product_for_discount_name': org_config.erp_product_for_discount_name,
        'erp_product_for_internal_donors_id': org_config.erp_product_for_internal_donors_id,
        'erp_product_for_internal_donors_name': org_config.erp_product_for_internal_donors_name,
        'erp_project_id': org_config.erp_project_id,
        'erp_project_name': org_config.erp_project_name,
        'erp_activity_id': org_config.erp_activity_id,
        'erp_activity_name': org_config.erp_activity_name,
        'erp_cost_center_id': org_config.erp_cost_center_id,
        'erp_cost_center_name': org_config.erp_cost_center_name,
    }


def _call_erp_data_function(service, org_config, specialization_id, study_system_id=None):
    """
    Call the service's erp_data_function if configured.
    Returns the function result dict, or None if not configured / failed.
    """
    erp_func_name = getattr(service, 'erp_data_function', None)
    if not erp_func_name:
        return None

    success, result = ExternalMethodHandler.call_function(
        erp_func_name,
        org_config,
        specialization_id,
        study_system_id,
        function_type=FunctionType.ERP_DATA,
    )
    if success and isinstance(result, dict):
        return result

    logger.warning("erp_data_function '%s' failed or returned non-dict: %s", erp_func_name, result)
    return None


def _apply_defaults(item_data, defaults):
    """
    For each ERP_DEFAULT_FIELDS key, if the key is missing from item_data,
    fill it from defaults.
    """
    for field in ERP_DEFAULT_FIELDS:
        if field not in item_data or item_data[field] is None:
            if field in defaults and defaults[field] is not None:
                item_data[field] = defaults[field]


class ServiceERPSettingsMVS(AllMVS):
    """ViewSet for ServiceERPSettings — org-scoped list & bulk sync"""
    queryset = ServiceERPSettings.objects.select_related(
        'fk_org_service_config',
        'fk_org_service_config__fk_service',
        'fk_org_service_config__fk_organization',
        'fk_currency',
    )
    serializer_class = ServiceERPSettingsSerializer
    enable_actions = ['all','select','list','second_list','filter','filter_paginate',]

    # ------------------------------------------------------------------ list
    @handle_exceptions
    def list(self, request, *args, **kwargs):
        """
        Return ServiceERPSettings for the user's organization.
        Query param:  ?fk_service=<id>   (derives org_config automatically)
        Response includes org_config defaults for the frontend.
        """
        user_org = PermissionChecker.get_user_organization(request.user)

        queryset = self.get_queryset().filter(
            fk_org_service_config__fk_organization=user_org
        )

        # Optional filter by service — derive org_config from user org + service
        service_id = request.query_params.get('fk_service')
        org_config = None
        if service_id:
            org_config = ServiceConfigHandler.get_active_config(service_id, user_org)
            if org_config:
                queryset = queryset.filter(fk_org_service_config=org_config)
            else:
                queryset = queryset.none()

        queryset = queryset.order_by('fk_org_service_config', 'specialization_id')

        serializer = self.get_serializer(queryset, many=True)

        # Build response extras
        extra = {'count': queryset.count()}

        # Include org_config defaults so the frontend can use them
        if org_config:
            extra['org_config'] = OrganizationServiceConfigSerializer(org_config).data
            extra['org_config_defaults'] = _get_org_config_defaults(org_config)

        return ResponseHandler.success(
            _('تم جلب إعدادات ERP بنجاح'),
            data=serializer.data,
            extra=extra,
        )

    # -------------------------------------------------------------- create
    @handle_exceptions
    def create(self, request, *args, **kwargs):
        """
        Bulk sync ServiceERPSettings for the user's organization.
        Expects:
        {
            "fk_service": <id>,
            "all_settings": [ { ...fields... }, ... ]
        }
        org_config is derived from request.user.fk_organization + fk_service.

        If the service has erp_data_function configured, it is called per-item
        to fill in missing default values (service_fee, fk_currency, ERP IDs …).
        Otherwise org_config ERP fields are used as fallback.

        Creates new / updates existing / deletes removed — all in one atomic op.
        """
        user_org = PermissionChecker.get_user_organization(request.user)

        # --- validate input ------------------------------------------------
        service_id = request.data.get('fk_service')
        settings_data = request.data.get('all_settings', [])

        if not service_id:
            return ResponseHandler.bad_request(
                _('معرف الخدمة مطلوب (fk_service)')
            )

        if not isinstance(settings_data, list):
            return ResponseHandler.bad_request(
                _('يجب إرسال مصفوفة من الإعدادات (all_settings)')
            )

        # --- get org config from user's org + service ----------------------
        org_config = ServiceConfigHandler.get_active_config(service_id, user_org)
        if not org_config:
            return ResponseHandler.not_found(
                _('إعدادات الخدمة غير موجودة لمنظمتك')
            )

        # --- bulk sync -----------------------------------------------------
        result = BulkSyncHandler.sync_by_id(
            model_class=ServiceERPSettings,
            parent_field='fk_org_service_config',
            parent_instance=org_config,
            items_data=settings_data,
            field_mapping={'fk_currency': 'fk_currency_id'},
            updatable_fields=UPDATABLE_FIELDS,
        )

        # --- return all current all_settings -----------------------------------
        all_settings = ServiceERPSettings.objects.filter(
            fk_org_service_config=org_config,
        ).order_by('specialization_id')

        return ResponseHandler.success(
            _('تم تحديث إعدادات ERP بنجاح'),
            extra={
                **result.to_dict(),
                'all_settings': ServiceERPSettingsSerializer(all_settings, many=True).data,
            },
        )
