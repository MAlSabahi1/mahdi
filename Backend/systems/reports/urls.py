from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api.views import CategoricalWorkforceReportView, NonWorkforceReportView, ExportRequestViewSet, ReportLayoutTemplateViewSet
from ..personnel.api.views.detailed_reports_views import (
    ActiveForceReportView,
    TempInactiveReportsView,
    PermInactiveReportsView,
    AuditMovementReportsView
)

app_name = 'reports'

router = DefaultRouter()
router.register(r'export-requests', ExportRequestViewSet, basename='export-request')
router.register(r'templates', ReportLayoutTemplateViewSet, basename='report-layout-template')

urlpatterns = [
    path('categorical-summary/', CategoricalWorkforceReportView.as_view(), name='categorical-summary'),
    path('non-workforce-summary/', NonWorkforceReportView.as_view(), name='non-workforce-summary'),
    
    path('detailed-reports/active-force/', ActiveForceReportView.as_view(), name='active_force_report'),
    path('detailed-reports/temp-inactive/', TempInactiveReportsView.as_view(), name='temp_inactive_reports'),
    path('detailed-reports/perm-inactive/', PermInactiveReportsView.as_view(), name='perm_inactive_reports'),
    path('detailed-reports/audit-movement/', AuditMovementReportsView.as_view(), name='audit_movement_reports'),
    
    path('', include(router.urls)),
]
