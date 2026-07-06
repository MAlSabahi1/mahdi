from rest_framework import viewsets, status, decorators
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.shortcuts import get_object_or_404

from systems.services.models import ServiceCatalog, ServicePrerequisite, WorkflowStage, ServiceWorkflowStep
from systems.services.api.serializers.service_catalog_serializers import (
    ServiceCatalogSerializer,
    ServicePrerequisiteSerializer,
    WorkflowStageSerializer,
    ServiceWorkflowStepSerializer
)


class ServiceCatalogViewSet(viewsets.ModelViewSet):
    """
    إدارة دليل الخدمات
    """
    queryset = ServiceCatalog.objects.all()
    serializer_class = ServiceCatalogSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'prerequisites']:
            return [AllowAny()]
        return [AllowAny()]

    def get_queryset(self):
        queryset = super().get_queryset()
        # المستخدم العادي يرى المفعل فقط
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_active=True)
        return queryset

    @decorators.action(detail=True, methods=['get'])
    def prerequisites(self, request, pk=None):
        """جلب شروط الخدمة"""
        service = self.get_object()
        prerequisites = ServicePrerequisite.objects.filter(service=service).order_by('order')
        serializer = ServicePrerequisiteSerializer(prerequisites, many=True)
        return Response(serializer.data)


class PrerequisitesValidationViewSet(viewsets.ViewSet):
    """
    التحقق من الشروط المسبقة لنموذج
    """
    permission_classes = [AllowAny]

    @decorators.action(detail=True, methods=['post'])
    def validate(self, request, pk=None):
        """التحقق من الشروط المسبقة للفرد بناءً على الخدمة"""
        # (Simplified Mock Logic for now)
        from systems.services.models import StatusChangeForm
        from systems.personnel.models import PersonnelMaster
        
        form = get_object_or_404(StatusChangeForm, pk=pk)
        
        if not form.service_catalog:
            return Response({'valid': True, 'errors': []})
            
        prerequisites = form.service_catalog.prerequisites.all()
        errors = []
        
        for prereq in prerequisites:
            # Here we would implement real validation logic 
            # e.g., checking personnel age if prereq.validation_type == 'age_min'
            pass
            
        return Response({
            'valid': len(errors) == 0,
            'errors': errors
        })


class ServicePrerequisiteViewSet(viewsets.ModelViewSet):
    """
    إدارة الشروط المسبقة للخدمات
    """
    queryset = ServicePrerequisite.objects.all()
    serializer_class = ServicePrerequisiteSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        qs = super().get_queryset()
        service_id = self.request.query_params.get('service_id')
        if service_id:
            qs = qs.filter(service_id=service_id)
        return qs


class WorkflowStageViewSet(viewsets.ModelViewSet):
    """
    إدارة المراحل العامة
    """
    queryset = WorkflowStage.objects.all()
    serializer_class = WorkflowStageSerializer
    permission_classes = [AllowAny]


class ServiceWorkflowStepViewSet(viewsets.ModelViewSet):
    """
    إدارة خطوات سير العمل للخدمات
    """
    queryset = ServiceWorkflowStep.objects.all()
    serializer_class = ServiceWorkflowStepSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        qs = super().get_queryset()
        service_id = self.request.query_params.get('service_id')
        if service_id:
            qs = qs.filter(service_id=service_id)
        return qs

    @decorators.action(detail=False, methods=['post'], url_path='bulk-sync')
    def bulk_sync(self, request):
        service_id = request.data.get('service_id')
        steps_data = request.data.get('steps', [])
        if not service_id:
            return Response({'error': 'service_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Delete old steps
        ServiceWorkflowStep.objects.filter(service_id=service_id).delete()
        
        # Create new steps
        for step_data in steps_data:
            ServiceWorkflowStep.objects.create(
                service_id=service_id,
                stage_id=step_data.get('stage'),
                order=step_data.get('order'),
                description=step_data.get('description', ''),
                is_final_step=step_data.get('is_final_step', False),
                is_execution_step=step_data.get('is_execution_step', False),
                requires_approval=step_data.get('requires_approval', True)
            )
            
        return Response({'success': True, 'message': 'تم مزامنة سير العمل بنجاح'})
