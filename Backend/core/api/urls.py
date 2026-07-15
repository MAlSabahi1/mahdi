"""Core URLs - مسارات API القواميس والهيكل التنظيمي"""
from rest_framework.routers import DefaultRouter
from . import views
from .settings_views import SystemSettingViewSet

router = DefaultRouter()

# Geographic (yemen-info.json)
router.register(r'geo/governorates', views.GeoGovernorateViewSet, basename='geo-governorate')
router.register(r'geo/districts', views.GeoDistrictViewSet, basename='geo-district')
router.register(r'geo/sub-districts', views.GeoSubDistrictViewSet, basename='geo-sub-district')
router.register(r'geo/villages', views.GeoVillageViewSet, basename='geo-village')

# Security Organization
router.register(r'security-admins', views.SecurityAdministrationViewSet, basename='security-admin')
router.register(r'central-departments', views.CentralDepartmentViewSet, basename='central-department')
router.register(r'branches', views.BranchViewSet, basename='branch')
router.register(r'district-police', views.DistrictPoliceViewSet, basename='district-police')
router.register(r'divisions', views.DivisionViewSet, basename='division')
router.register(r'units', views.UnitViewSet, basename='unit')

# Other dictionaries
router.register(r'positions', views.PositionViewSet, basename='position')
router.register(r'force-types', views.ForceTypeViewSet, basename='force-type')
router.register(r'ranks', views.RankViewSet, basename='rank')
router.register(r'statuses', views.ServiceStatusViewSet, basename='service-status')
router.register(r'job-categories', views.JobCategoryViewSet, basename='job-category')
router.register(r'job-titles', views.JobTitleViewSet, basename='job-title')
router.register(r'qualifications', views.QualificationViewSet, basename='qualification')
router.register(r'variable-types', views.VariableTypeViewSet, basename='variable-type')

# Workflow & Rules
router.register(r'transition-rules', views.StateTransitionRuleViewSet, basename='transition-rule')

# Notifications
router.register(r'notifications', views.NotificationRecordViewSet, basename='notification')

# System Settings
router.register(r'system-settings', SystemSettingViewSet, basename='system-setting')

from django.urls import path

urlpatterns = [
    path('attachment-rules/', views.DocumentDictionaryViewSet.as_view(), name='attachment-rules'),
] + router.urls
