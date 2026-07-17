from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CorrespondenceViewSet, TaskViewSet, CircularViewSet,
    CorrespondenceAttachmentViewSet, MeetingMinutesViewSet,
    DocumentWorkRequestViewSet, InventoryItemViewSet,
    InventoryRequestViewSet, CustodyViewSet, AttendanceLogViewSet,
    FinancialAllocationViewSet, ExpenseViewSet, CorrespondenceReferralViewSet,
    OfficialMemoTemplateViewSet
)

router = DefaultRouter()
router.register(r'correspondences', CorrespondenceViewSet, basename='correspondence')
router.register(r'attachments', CorrespondenceAttachmentViewSet, basename='attachment')
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'circulars', CircularViewSet, basename='circular')
router.register(r'meetings', MeetingMinutesViewSet, basename='meeting')
router.register(r'document-requests', DocumentWorkRequestViewSet, basename='document-request')
router.register(r'inventory-items', InventoryItemViewSet, basename='inventory-item')
router.register(r'inventory-requests', InventoryRequestViewSet, basename='inventory-request')
router.register(r'custodies', CustodyViewSet, basename='custody')
router.register(r'attendance-logs', AttendanceLogViewSet, basename='attendance-log')
router.register(r'financial-allocations', FinancialAllocationViewSet, basename='financial-allocation')
router.register(r'expenses', ExpenseViewSet, basename='expense')
router.register(r'referrals', CorrespondenceReferralViewSet, basename='referral')
router.register(r'memo-templates', OfficialMemoTemplateViewSet, basename='memo-template')

app_name = 'secretariat'

urlpatterns = [
    path('', include(router.urls)),
]
