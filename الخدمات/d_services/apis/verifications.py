"""
Prerequisite Verification APIs
ViewSet for AudienceConditionVerification
"""
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db import transaction

from d_services.apis.base import OrganizationViewSet
from d_services.models.AudienceConditionVerification import AudienceConditionVerification
from d_services.models.ServiceRequest import ServiceRequest
from d_services.models.ServicePrerequisite import ServicePrerequisite
from d_services.serializers.verifications import (
    AudienceConditionVerificationSerializer,
    VerifyPrerequisitesSerializer,
)
from d_services.choices.choices import PrerequisiteStatusChoice, ServiceStatusChoice


class PrerequisiteVerificationViewSet(OrganizationViewSet):
    """ViewSet for Prerequisite Verifications"""
    queryset = AudienceConditionVerification.objects.filter(is_deleted=False)
    serializer_class = AudienceConditionVerificationSerializer
    organization_field = 'fk_organization'
    
    def get_queryset(self):
        request_id = self.kwargs.get('request_pk')
        return AudienceConditionVerification.objects.filter(
            fk_request_id=request_id,
            is_deleted=False
        ).order_by('fk_prerequisite__order')
    
    @action(detail=False, methods=['post'], url_path='verify')
    def verify_prerequisites(self, request, request_pk=None):
        """Verify all prerequisites for a request"""
        serializer = VerifyPrerequisitesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            service_request = ServiceRequest.objects.get(pk=request_pk)
        except ServiceRequest.DoesNotExist:
            return Response(
                {'error': _('Request not found')},
                status=status.HTTP_404_NOT_FOUND
            )
        
        force_recheck = serializer.validated_data.get('force_recheck', False)
        
        # Get all prerequisites for the service
        prerequisites = ServicePrerequisite.objects.filter(
            fk_service=service_request.fk_service,
            is_deleted=False
        ).order_by('order')
        
        results = []
        all_mandatory_satisfied = True
        
        with transaction.atomic():
            for prereq in prerequisites:
                # Check if already verified
                existing = AudienceConditionVerification.objects.filter(
                    fk_request=service_request,
                    fk_prerequisite=prereq,
                    is_deleted=False
                ).first()
                
                if existing and not force_recheck:
                    results.append({
                        'prerequisite': prereq.name,
                        'status': prereq.status,
                        'is_satisfied': existing.is_satisfied,
                        'message': _('Already verified')
                    })
                    
                    if prereq.status == PrerequisiteStatusChoice.MANDATORY and not existing.is_satisfied:
                        all_mandatory_satisfied = False
                    continue
                
                # Execute verification procedure
                is_satisfied = self._execute_verification(
                    prereq,
                    service_request,
                    request.user
                )
                
                # Create or update verification record
                if existing:
                    existing.is_satisfied = is_satisfied
                    existing.verified_at = timezone.now()
                    existing.fk_verified_by = request.user
                    existing.save()
                    verification = existing
                else:
                    verification = AudienceConditionVerification.objects.create(
                        fk_request=service_request,
                        fk_prerequisite=prereq,
                        fk_organization=service_request.fk_organization,
                        is_satisfied=is_satisfied,
                        fk_verified_by=request.user
                    )
                
                results.append({
                    'prerequisite': prereq.name,
                    'status': prereq.status,
                    'is_satisfied': is_satisfied,
                    'message': _('Verified')
                })
                
                if prereq.status == PrerequisiteStatusChoice.MANDATORY and not is_satisfied:
                    all_mandatory_satisfied = False
            
            # Update request status if mandatory prerequisites failed
            if not all_mandatory_satisfied:
                service_request.status = ServiceStatusChoice.REJECTED
                service_request.locked_reason = _('Mandatory prerequisites not satisfied')
                service_request.save()
        
        return Response({
            'all_mandatory_satisfied': all_mandatory_satisfied,
            'results': results,
            'message': _('All prerequisites satisfied') if all_mandatory_satisfied else _('Some mandatory prerequisites failed')
        })
    
    def _execute_verification(self, prerequisite, service_request, user):
        """Execute the verification procedure for a prerequisite"""
        # If validation_procedure_name is set, try to call it
        if prerequisite.validation_procedure_name:
            # In a real implementation, this would dynamically call the procedure
            # For now, return True as a placeholder
            try:
                # Dynamic procedure execution would go here
                # procedure = getattr(verification_procedures, prerequisite.validation_procedure_name)
                # return procedure(service_request, user)
                pass
            except Exception:
                pass
        
        # Default: return True (satisfied)
        return True
