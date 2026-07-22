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

    @decorators.action(detail=True, methods=['get'])
    def engine_rules(self, request, pk=None):
        """جلب قواعد محرك الخدمات المبرمجة بالخلفية"""
        service = self.get_object()
        
        # Load dispatcher and mappings
        import systems.services.service_rules
        from systems.services.service_rules.core import ServiceRulesDispatcher
        
        SERVICE_RULES_MAP = {
            'martyr': 'MARTYR_FORM',
            'seconded': 'SECONDED_FORM',
        }
        
        engine_code = SERVICE_RULES_MAP.get(service.form_type, service.code)
        rules = ServiceRulesDispatcher.get_rules(engine_code)
        
        rules_data = []
        disabled_rules = service.disabled_engine_rules or []
        for r in rules:
            rules_data.append({
                'id': r.rule_id,
                'name': getattr(r, 'name', r.rule_id),
                'description': getattr(r, 'description', ''),
                'is_active': r.rule_id not in disabled_rules
            })
            
        return Response(rules_data)

    @decorators.action(detail=True, methods=['post'])
    def toggle_engine_rule(self, request, pk=None):
        """تفعيل أو إيقاف قاعدة محرك مركزية للخدمة"""
        service = self.get_object()
        rule_id = request.data.get('rule_id')
        is_active = request.data.get('is_active')
        
        if not rule_id:
            return Response({'error': 'rule_id is required'}, status=status.HTTP_400_BAD_REQUEST)
            
        disabled_rules = list(service.disabled_engine_rules or [])
        
        if is_active:
            if rule_id in disabled_rules:
                disabled_rules.remove(rule_id)
        else:
            if rule_id not in disabled_rules:
                disabled_rules.append(rule_id)
                
        service.disabled_engine_rules = disabled_rules
        service.save(update_fields=['disabled_engine_rules'])
        
        return Response({'success': True, 'disabled_rules': disabled_rules})


class PrerequisitesValidationViewSet(viewsets.ViewSet):
    """
    التحقق من الشروط المسبقة لنموذج
    """
    permission_classes = [AllowAny]

    @decorators.action(detail=False, methods=['post'])
    def validate(self, request):
        """التحقق من الشروط المسبقة للفرد بناءً على الخدمة"""
        from systems.services.models import ServiceCatalog
        from systems.personnel.models import PersonnelMaster
        from datetime import date
        
        military_number = request.data.get('military_number')
        service_id = request.data.get('service_id')
        
        if not military_number or not service_id:
            return Response({'valid': False, 'errors': ['الرقم العسكري ومعرف الخدمة مطلوبان']}, status=status.HTTP_400_BAD_REQUEST)
            
        personnel = get_object_or_404(PersonnelMaster, military_number=military_number)
        service = get_object_or_404(ServiceCatalog, pk=service_id)
        
        prerequisites = service.prerequisites.filter(is_mandatory=True)
        errors = []
        today = date.today()
        
        for prereq in prerequisites:
            val = prereq.validation_value
            try:
                if prereq.validation_type == 'age_min':
                    if personnel.birth_date:
                        age = today.year - personnel.birth_date.year - ((today.month, today.day) < (personnel.birth_date.month, personnel.birth_date.day))
                        if age < int(val):
                            errors.append(f"{prereq.name_ar}: العمر الحالي {age} وهو أقل من الحد الأدنى {val}")
                    else:
                        errors.append(f"{prereq.name_ar}: تاريخ الميلاد غير متوفر للفرد")
                        
                elif prereq.validation_type == 'age_max':
                    if personnel.birth_date:
                        age = today.year - personnel.birth_date.year - ((today.month, today.day) < (personnel.birth_date.month, personnel.birth_date.day))
                        if age > int(val):
                            errors.append(f"{prereq.name_ar}: العمر الحالي {age} وهو أكبر من الحد الأقصى {val}")
                    else:
                        errors.append(f"{prereq.name_ar}: تاريخ الميلاد غير متوفر للفرد")
                        
                elif prereq.validation_type == 'service_years_min':
                    if personnel.join_date:
                        years = today.year - personnel.join_date.year - ((today.month, today.day) < (personnel.join_date.month, personnel.join_date.day))
                        if years < int(val):
                            errors.append(f"{prereq.name_ar}: سنوات الخدمة {years} أقل من المطلوب {val}")
                    else:
                        errors.append(f"{prereq.name_ar}: تاريخ الالتحاق غير متوفر")
                        
                elif prereq.validation_type == 'status_check':
                    if personnel.current_status and personnel.current_status.name != val and personnel.current_status.classification != val:
                        errors.append(f"{prereq.name_ar}: الحالة الحالية ({personnel.current_status.name}) غير مطابقة للمطلوب")
            except (ValueError, TypeError):
                errors.append(f"خطأ في إعداد شرط: {prereq.name_ar}")
                
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
