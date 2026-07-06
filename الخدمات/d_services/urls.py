
from d_services.apis.services import ServiceMVS
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from d_services.apis.GrantSource import GrantSourceMVS
from d_services.apis.services import (
     ServiceInstallmentPlanMVS,
     ServiceVersionMVS,
    OrganizationServiceConfigMVS,
    ServicePrerequisiteMVS,
    WorkflowStageMVS,
    ServiceWorkflowStepMVS,
    WorkflowStepChecklistTemplateMVS,
    WorkflowStepPrintReportSettingMVS
    
)
from d_services.apis.requests import ServiceCallResultMVS, ServiceRequestMVS
from d_services.apis.permissions import (
    GroupServicePermissionMVS,
    ServicePermissionMVS,
    StagePermissionMVS
)
from d_services.apis.actions import RequestActionMVS, RequestAttachmentMVS, RequestNoteMVS
from d_services.apis.ServiceERPSettings import ServiceERPSettingsMVS
from d_services.apis.component import ServiceSchemaAPIView
from d_services.apis.external_methods.views import AvailableFunctionsView

from d_services.apis.service_logs_api import ServiceLogsMVS
from d_services.apis.request_logs_api import RequestLogsMVS, WorkflowLogsMVS
from d_services.apis.user_permissions_api import UserPermissionsAPIView, RequestActionsStatusAPIView,StageActionsStatusAPIView

from d_services.apis.PortalTargetMapping import PortalTargetMappingMVS
from d_services.apis.portal_export import PortalExportView, PortalMarkSyncedView
from d_services.utils.portal_sync import PortalPullSyncView


from d_services.apis.portal_service_server import TriggerServiceSyncView
from d_services.apis.portal_service_receive import PortalServiceReceiveView
from d_services.apis.service_sync_log_api import ServiceSyncLogView


router = DefaultRouter()


router.register(r'services', ServiceMVS, basename='service')
router.register(r'service-versions', ServiceVersionMVS)
router.register(r'service-installment-plans', ServiceInstallmentPlanMVS)
router.register(r'organization-service-config', OrganizationServiceConfigMVS)
router.register(r'service-prerequisites', ServicePrerequisiteMVS)
router.register(r'workflow-stages', WorkflowStageMVS, basename='workflow-stage')
router.register(r'service-workflow-steps', ServiceWorkflowStepMVS, basename='workflow-step')
router.register(r'workflow-step-checklist-templates', WorkflowStepChecklistTemplateMVS, basename='checklist-template')
router.register(r'grant-sources', GrantSourceMVS, basename='grant-source')
router.register(r'service-erp-all_settings', ServiceERPSettingsMVS, basename='service-erp-all_settings')
router.register(r'group-service-permissions', GroupServicePermissionMVS)
router.register(r'stage-permissions', StagePermissionMVS)
router.register(r'service-permissions', ServicePermissionMVS,basename='service-permissions')
router.register(r'request-notes', RequestNoteMVS)
router.register(r'request-attachments', RequestAttachmentMVS)


router.register(r'service-requests', ServiceRequestMVS, basename='service-request')
router.register(r'service-call-func', ServiceCallResultMVS, basename='service-call-func')

router.register(r'request-actions', RequestActionMVS, basename='request-action')


router.register(r'service-logs', ServiceLogsMVS, basename='service-logs')

router.register(r'request-logs', RequestLogsMVS, basename='request-logs')

router.register(r'workflow-logs', WorkflowLogsMVS, basename='workflow-logs')
router.register(r'workflow-step-print-report-all_settings', WorkflowStepPrintReportSettingMVS, basename='workflow-step-print-report-setting')

router.register(r'portal-target-mapping', PortalTargetMappingMVS, basename='portal-target-mapping')



urlpatterns = [
    path('', include(router.urls)),
    path('service-schema/<int:pk>/', ServiceSchemaAPIView.as_view(), name='service-schema'),
    path('available-functions/', AvailableFunctionsView.as_view(), name='available-functions'),
    path('user-permissions/', UserPermissionsAPIView.as_view(), name='user-permissions'),
    path('request-actions-status/<int:pk>/', RequestActionsStatusAPIView.as_view(), name='request-actions-status'),
    path('stage-actions-status/<int:pk>/', StageActionsStatusAPIView.as_view(), name='request-actions-status'),
    # Portal request sync
    path('portal/export-requests/', PortalExportView.as_view(), name='portal-export'),
    path('portal/mark-synced/', PortalMarkSyncedView.as_view(), name='portal-mark-synced'),
    path('portal/sync/', PortalPullSyncView.as_view(), name='portal-sync'),
    # Portal service sync — مزامنة الخدمات
    path('trigger-service-sync/', TriggerServiceSyncView.as_view(), name='portal-trigger-service-sync'),
    path('receive-services/', PortalServiceReceiveView.as_view(), name='portal-receive-services'),
    path('service-sync-log/', ServiceSyncLogView.as_view(), name='portal-service-sync-log'),
]

