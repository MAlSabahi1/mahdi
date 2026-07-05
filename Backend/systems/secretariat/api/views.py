from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from ..models import (
    Correspondence, Task, Circular, CorrespondenceAttachment,
    MeetingMinutes, DocumentWorkRequest, InventoryItem, InventoryRequest,
    Custody, AttendanceLog, FinancialAllocation, Expense
)
from .serializers import (
    CorrespondenceSerializer, TaskSerializer, CircularSerializer,
    CorrespondenceAttachmentSerializer, MeetingMinutesSerializer,
    DocumentWorkRequestSerializer, InventoryItemSerializer,
    InventoryRequestSerializer, CustodySerializer, AttendanceLogSerializer,
    FinancialAllocationSerializer, ExpenseSerializer
)
from infra.security.permissions import ABACPermission, filter_by_department_scope, get_user_profile

class BaseSecretariatViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, ABACPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    def get_queryset(self):
        return filter_by_department_scope(
            self.request.user, 
            self.queryset, 
            'security_admin'
        )
        
    def perform_create(self, serializer):
        profile = get_user_profile(self.request.user)
        security_admin = getattr(profile, 'security_admin', None) if profile else None
        serializer.save(
            created_by=self.request.user,
            security_admin=security_admin
        )

class CorrespondenceViewSet(BaseSecretariatViewSet):
    queryset = Correspondence.objects.all()
    serializer_class = CorrespondenceSerializer
    filterset_fields = ['type', 'status', 'date']
    search_fields = ['reference_number', 'subject', 'sender', 'receiver']
    ordering_fields = ['date', 'created_at']

class CorrespondenceAttachmentViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, ABACPermission]
    queryset = CorrespondenceAttachment.objects.all()
    serializer_class = CorrespondenceAttachmentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['correspondence']

    def get_queryset(self):
        profile = get_user_profile(self.request.user)
        user_sec_admin = getattr(profile, 'security_admin', None) if profile else None
        if user_sec_admin:
            return self.queryset.filter(correspondence__security_admin=user_sec_admin)
        return self.queryset.none()

class TaskViewSet(BaseSecretariatViewSet):
    queryset = Task.objects.select_related('assigned_to').all()
    serializer_class = TaskSerializer
    filterset_fields = ['status', 'priority', 'due_date', 'assigned_to', 'related_correspondence']
    search_fields = ['title', 'description']
    ordering_fields = ['due_date', 'created_at', 'priority']

class CircularViewSet(BaseSecretariatViewSet):
    queryset = Circular.objects.all()
    serializer_class = CircularSerializer
    filterset_fields = ['is_active', 'date_issued']
    search_fields = ['title', 'content']
    ordering_fields = ['date_issued', 'created_at']

class MeetingMinutesViewSet(BaseSecretariatViewSet):
    queryset = MeetingMinutes.objects.prefetch_related('attendees').all()
    serializer_class = MeetingMinutesSerializer
    filterset_fields = ['date']
    search_fields = ['title', 'content', 'decisions', 'external_attendees']
    ordering_fields = ['date', 'created_at']

class DocumentWorkRequestViewSet(BaseSecretariatViewSet):
    queryset = DocumentWorkRequest.objects.select_related('requested_by').all()
    serializer_class = DocumentWorkRequestSerializer
    filterset_fields = ['type', 'status', 'requested_by']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'completed_at']

class InventoryItemViewSet(BaseSecretariatViewSet):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    filterset_fields = ['type']
    search_fields = ['name', 'code']
    ordering_fields = ['name', 'quantity_in_stock']

    def perform_create(self, serializer):
        # override since it does not have created_by
        profile = get_user_profile(self.request.user)
        security_admin = getattr(profile, 'security_admin', None) if profile else None
        serializer.save(security_admin=security_admin)

class InventoryRequestViewSet(BaseSecretariatViewSet):
    queryset = InventoryRequest.objects.select_related('item', 'requested_by').all()
    serializer_class = InventoryRequestSerializer
    filterset_fields = ['status', 'item', 'requested_by']
    search_fields = ['notes']
    ordering_fields = ['created_at']

class CustodyViewSet(BaseSecretariatViewSet):
    queryset = Custody.objects.select_related('item', 'assigned_to').all()
    serializer_class = CustodySerializer
    filterset_fields = ['status', 'item', 'assigned_to']
    search_fields = ['notes']
    ordering_fields = ['date_assigned', 'date_returned']

class AttendanceLogViewSet(BaseSecretariatViewSet):
    queryset = AttendanceLog.objects.select_related('employee').all()
    serializer_class = AttendanceLogSerializer
    filterset_fields = ['date', 'status', 'employee']
    search_fields = ['notes', 'employee__full_name', 'employee__military_number']
    ordering_fields = ['date']

class FinancialAllocationViewSet(BaseSecretariatViewSet):
    queryset = FinancialAllocation.objects.all()
    serializer_class = FinancialAllocationSerializer
    filterset_fields = ['month']
    ordering_fields = ['month']

class ExpenseViewSet(BaseSecretariatViewSet):
    queryset = Expense.objects.select_related('allocation').all()
    serializer_class = ExpenseSerializer
    filterset_fields = ['allocation', 'date', 'category']
    search_fields = ['description', 'receipt_number', 'category']
    ordering_fields = ['date', 'amount']
