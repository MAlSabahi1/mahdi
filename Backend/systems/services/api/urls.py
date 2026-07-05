"""
Services URL Configuration — مسارات دورة الكشوفات
══════════════════════════════════════════════════
المرحلة 4: Export, Import, Staging, Reconciliation, Reports, Rejections, Webhooks
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from systems.services.api.views import main_views as views
from systems.services.api.views.main_views import (
    ExportView, ImportView, BatchExportView, StatusCascadeView,
    TaskStatusView, StagingViewSet, RejectionViewSet,
    ReconciliationViewSet, ReportViewSet, WebhookConfigViewSet,
    ComplianceViewSet, SnapshotViewSet,
)
from systems.services.api.views.import_views import ImportAPIViewSet
from systems.services.api.views.raw_data_views import RawDataStandardizedViewSet
from systems.services.api.views.status_change_views import StatusChangeFormViewSet
from systems.services.api.views.admin_views import CustomFormTemplateViewSet, CustomReportTemplateViewSet
from systems.services.api.views.initial_seed_views import InitialSeedViewSet
from systems.services.api.views.disciplinary_views import (
    DisciplinaryActionViewSet,
    AbsenceRecordViewSet,
    DisciplinaryCouncilVerdictViewSet,
)

router = DefaultRouter()
router.register(r'staging', views.StagingViewSet, basename='staging')
router.register(r'rejections', views.RejectionViewSet, basename='rejections')
router.register(r'compliance', views.ComplianceViewSet, basename='compliance')
router.register(r'snapshots', views.SnapshotViewSet, basename='snapshots')
router.register(r'webhooks', views.WebhookConfigViewSet, basename='webhooks')
router.register(r'raw-data-standardized', RawDataStandardizedViewSet, basename='raw-data-standardized')
router.register(r'forms', StatusChangeFormViewSet, basename='status-change-forms')
router.register(r'initial-seed', InitialSeedViewSet, basename='initial-seed')
router.register(r'disciplinary/actions',  DisciplinaryActionViewSet,        basename='disciplinary-actions')
router.register(r'disciplinary/absences', AbsenceRecordViewSet,              basename='disciplinary-absences')
router.register(r'disciplinary/verdicts', DisciplinaryCouncilVerdictViewSet, basename='disciplinary-verdicts')

# Import API Router
import_router = DefaultRouter()
import_router.register(r'import', ImportAPIViewSet, basename='import-api')

# Admin Router — إدارة الاستمارات والنماذج المخصصة
admin_router = DefaultRouter()
admin_router.register(r'forms', CustomFormTemplateViewSet, basename='admin-forms')
admin_router.register(r'reports', CustomReportTemplateViewSet, basename='admin-reports')

urlpatterns = [

    # Export — تصدير قالب لإدارة واحدة (multi أو single)
    path('export/', ExportView.as_view({'get': 'list'}), name='export'),

    # Batch Export — تصدير كل الإدارات دفعة واحدة (ZIP)
    path('export/batch/', BatchExportView.as_view({'post': 'create'}), name='export-batch'),

    # Status Cascade — خريطة الحالات المتتالية للفرونت اند
    path('status-cascade/', StatusCascadeView.as_view({'get': 'list'}), name='status-cascade'),

    # Import — استيراد الكشوف المعدلة
    path('import/', ImportView.as_view({'post': 'create'}), name='import'),

    # Task Status (Celery)
    path('tasks/<str:pk>/', TaskStatusView.as_view({'get': 'retrieve'}), name='task-status'),

    # Import API (New - Task 5.4)
    path('', include(import_router.urls)),

    # Reconciliation
    path('reconciliation/', views.ReconciliationViewSet.as_view({
        'get': 'list', 'post': 'create'
    }), name='reconciliation-list'),
    path('reconciliation/<int:pk>/', views.ReconciliationViewSet.as_view({
        'get': 'retrieve'
    }), name='reconciliation-detail'),
    path('reconciliation/<int:pk>/resolve/', views.ReconciliationViewSet.as_view({
        'post': 'resolve'
    }), name='reconciliation-resolve'),

    # Reports
    path('reports/', views.ReportViewSet.as_view({
        'get': 'list'
    }), name='report-list'),
    path('reports/generate/', views.ReportViewSet.as_view({
        'post': 'generate'
    }), name='report-generate'),
    path('reports/download/<str:filename>/', views.ReportViewSet.as_view({
        'get': 'download'
    }), name='report-download'),

    # Admin — إدارة الاستمارات والنماذج المخصصة (مدير فقط)
    path('admin/', include(admin_router.urls)),

    # Router URLs (staging, rejections, compliance, snapshots, webhooks)
    path('', include(router.urls)),
]
