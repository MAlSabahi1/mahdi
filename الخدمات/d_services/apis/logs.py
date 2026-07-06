"""
Log APIs
ViewSets for ServiceLog, RequestLog, WorkflowLog, RequestReturnLog
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from d_services.models.ServiceLog import ServiceLog
from d_services.models.RequestLog import RequestLog
from d_services.models.WorkflowLog import WorkflowLog
from d_services.models.RequestReturnLog import RequestReturnLog
from d_services.serializers.logs import (
    ServiceLogSerializer,
    RequestLogSerializer,
    WorkflowLogSerializer,
    RequestReturnLogSerializer,
)


class ReadOnlyLogViewSet(viewsets.ReadOnlyModelViewSet):
    """Base read-only ViewSet for logs"""
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering = ['-timestamp']


class ServiceLogViewSet(ReadOnlyLogViewSet):
    """ViewSet for Service Logs"""
    queryset = ServiceLog.objects.filter(is_deleted=False)
    serializer_class = ServiceLogSerializer
    filterset_fields = ['fk_service', 'action', 'fk_user']
    ordering_fields = ['timestamp']


class RequestLogViewSet(ReadOnlyLogViewSet):
    """ViewSet for Request Logs"""
    queryset = RequestLog.objects.filter(is_deleted=False)
    serializer_class = RequestLogSerializer
    filterset_fields = ['fk_request', 'action', 'fk_user']
    ordering_fields = ['timestamp']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by organization through request
        user = self.request.user
        if hasattr(user, 'fk_organization') and user.fk_organization:
            queryset = queryset.filter(
                fk_request__fk_organization=user.fk_organization
            )
        
        return queryset


class WorkflowLogViewSet(ReadOnlyLogViewSet):
    """ViewSet for Workflow Logs"""
    queryset = WorkflowLog.objects.filter(is_deleted=False)
    serializer_class = WorkflowLogSerializer
    filterset_fields = ['fk_request', 'fk_user']
    ordering_fields = ['timestamp']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        user = self.request.user
        if hasattr(user, 'fk_organization') and user.fk_organization:
            queryset = queryset.filter(
                fk_request__fk_organization=user.fk_organization
            )
        
        return queryset


class RequestReturnLogViewSet(ReadOnlyLogViewSet):
    """ViewSet for Request Return Logs"""
    queryset = RequestReturnLog.objects.filter(is_deleted=False)
    serializer_class = RequestReturnLogSerializer
    filterset_fields = ['fk_request', 'return_reason', 'fk_returned_by', 'is_resolved']
    ordering_fields = ['returned_at']
    ordering = ['-returned_at']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        user = self.request.user
        if hasattr(user, 'fk_organization') and user.fk_organization:
            queryset = queryset.filter(
                fk_request__fk_organization=user.fk_organization
            )
        
        return queryset
