from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Correspondence, Task, Circular
from .serializers import CorrespondenceSerializer, TaskSerializer, CircularSerializer
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

class TaskViewSet(BaseSecretariatViewSet):
    queryset = Task.objects.select_related('assigned_to').all()
    serializer_class = TaskSerializer
    filterset_fields = ['status', 'priority', 'due_date', 'assigned_to']
    search_fields = ['title', 'description']
    ordering_fields = ['due_date', 'created_at', 'priority']

class CircularViewSet(BaseSecretariatViewSet):
    queryset = Circular.objects.all()
    serializer_class = CircularSerializer
    filterset_fields = ['is_active', 'date_issued']
    search_fields = ['title', 'content']
    ordering_fields = ['date_issued', 'created_at']
