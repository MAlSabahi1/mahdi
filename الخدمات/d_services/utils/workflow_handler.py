from django.utils.translation import gettext_lazy as _


class WorkflowHandler:
    
    @staticmethod
    def get_workflow_snapshot(service) -> list:

        steps = service.workflow_steps.filter(is_deleted=False).order_by('order').values(
            'id', 'order', 'fk_stage_id', 'is_final_step', 'is_execution_step',
            'has_custom_output', 'custom_output_template', 'custom_input_template'
        )
        return list(steps)
    
    @staticmethod
    def get_prerequisites_snapshot(service) -> list:

        prereqs = service.prerequisites.filter(is_deleted=False).order_by('order').values(
            'id', 'name_ar', 'name_en', 'status', 'validation_procedure_name', 'order'
        )
        return list(prereqs)
    
    @staticmethod
    def validate_prerequisites(service, user, data, service_request=None) -> dict:
        from d_services.models.ServicePrerequisite import ServicePrerequisite
        from d_services.models.AudienceConditionVerification import AudienceConditionVerification
        from d_services.choices.choices import PrerequisiteStatusChoice
        from d_services.apis.external_methods import ExternalMethodHandler, FunctionType
        
        prerequisites = ServicePrerequisite.objects.filter(
            fk_service=service,
            is_deleted=False,
            status=PrerequisiteStatusChoice.MANDATORY
        ).order_by('order')
        
        if not prerequisites.exists():
            return None
        
        validation_errors = []
        validation_results = []
        
        for prereq in prerequisites:
            result = {
                'prerequisite_id': prereq.id,
                'name_ar': prereq.name_ar,
                'name_en': prereq.name_en,
                'is_valid': False,
                'message': None
            }
            
            if not prereq.validation_procedure_name:
                result['is_valid'] = True
                result['message'] = _('لا توجد دالة تحقق محددة')
                validation_results.append(result)
                
                if service_request:
                    AudienceConditionVerification.objects.create(
                        fk_request=service_request,
                        fk_prerequisite=prereq,
                        is_satisfied=True,
                        verification_result={'message': str(result['message']), 'auto_passed': True},
                        fk_verified_by=user,
                        notes=_('تم التجاوز - لا توجد دالة تحقق')
                    )
                continue
            
            try:
                # استخدام ExternalMethodHandler للأمان
                function_name = prereq.validation_procedure_name
                
                if ExternalMethodHandler.function_exists(function_name, FunctionType.VALIDATOR):
                    success, validation_result = ExternalMethodHandler.call_function(
                        function_name,
                        user=user,
                        service=service,
                        data=data,
                        function_type=FunctionType.VALIDATOR
                    )
                    
                    if success and isinstance(validation_result, dict):
                        result['is_valid'] = validation_result.get('is_valid', False)
                        result['message'] = validation_result.get('message', '')
                    elif success and isinstance(validation_result, bool):
                        result['is_valid'] = validation_result
                        result['message'] = _('تم التحقق بنجاح') if validation_result else _('فشل التحقق')
                    elif success and validation_result is None:
                        result['is_valid'] = True
                        result['message'] = _('تم التحقق بنجاح')
                    else:
                        result['is_valid'] = False
                        result['message'] = str(validation_result) if validation_result else _('فشل التحقق')
                else:
                    result['is_valid'] = False
                    result['message'] = _('دالة التحقق غير موجودة: %s') % function_name
                    
            except Exception as e:
                result['is_valid'] = False
                result['message'] = _('خطأ غير متوقع: %s') % str(e)
            
            validation_results.append(result)
            
            # Save verification record to AudienceConditionVerification
            if service_request:
                AudienceConditionVerification.objects.create(
                    fk_request=service_request,
                    fk_prerequisite=prereq,
                    is_satisfied=result['is_valid'],
                    verification_result={
                        'message': str(result['message']),
                        'validation_procedure': prereq.validation_procedure_name
                    },
                    fk_verified_by=user,
                    notes=result['message']
                )
            
            if not result['is_valid']:
                validation_errors.append({
                    'prerequisite': prereq.name_ar,
                    'message': result['message']
                })
        
        if validation_errors:
            return {
                'has_errors': True,
                'errors': validation_errors,
                'all_results': validation_results
            }
        
        return None
    
    @staticmethod
    def save_prerequisites_verification(service, user, data, service_request) -> None:
        """
        Save prerequisite verification records to AudienceConditionVerification.
        Called after service request is created to record all verification results.
        """
        from d_services.models.ServicePrerequisite import ServicePrerequisite
        from d_services.models.AudienceConditionVerification import AudienceConditionVerification
        from d_services.choices.choices import PrerequisiteStatusChoice
        import importlib
        
        prerequisites = ServicePrerequisite.objects.filter(
            fk_service=service,
            is_deleted=False
        ).order_by('order')
        
        for prereq in prerequisites:
            is_valid = False
            message = ''
            validation_result_data = {}
            
            if not prereq.validation_procedure_name:
                is_valid = True
                message = _('لا توجد دالة تحقق محددة')
                validation_result_data = {'auto_passed': True, 'message': str(message)}
            else:
                try:
                    procedure_path = prereq.validation_procedure_name
                    
                    if '.' in procedure_path:
                        module_path, function_name = procedure_path.rsplit('.', 1)
                        module = importlib.import_module(module_path)
                        validation_function = getattr(module, function_name)
                        
                        result = validation_function(user=user, service=service, data=data)
                        
                        if isinstance(result, dict):
                            is_valid = result.get('is_valid', False)
                            message = result.get('message', '')
                        elif isinstance(result, bool):
                            is_valid = result
                            message = _('تم التحقق بنجاح') if result else _('فشل التحقق')
                        elif result is None:
                            is_valid = True
                            message = _('تم التحقق بنجاح')
                        else:
                            is_valid = False
                            message = str(result)
                        
                        validation_result_data = {
                            'validation_procedure': prereq.validation_procedure_name,
                            'message': str(message)
                        }
                    else:
                        is_valid = False
                        message = _('صيغة اسم دالة التحقق غير صحيحة')
                        validation_result_data = {'error': 'invalid_procedure_format'}
                        
                except Exception as e:
                    is_valid = False
                    message = _('خطأ في التحقق: %s') % str(e)
                    validation_result_data = {'error': str(e)}
            
            # Create verification record
            AudienceConditionVerification.objects.create(
                fk_request=service_request,
                fk_prerequisite=prereq,
                is_satisfied=is_valid,
                verification_result=validation_result_data,
                fk_verified_by=user,
                notes=str(message)
            )


def example_execution_procedure(action_instance, request):
    return {
        'success': True,
        'message': _('تم التنفيذ بنجاح'),
        'data': {}
    }


def example_input_template_data(action_instance, request):

    service_request = action_instance.fk_request
    
    return {
        'request_number': service_request.request_number,
        'requester_name': service_request.fk_requester.get_full_name() if service_request.fk_requester else '',
        'service_name': service_request.fk_service.name_ar if service_request.fk_service else '',
        'requested_at': service_request.requested_at.strftime('%Y-%m-%d') if service_request.requested_at else '',
        'target_audience_data': service_request.target_audience_data or {},
        'version_data': service_request.version_data or {},
    }


def example_output_template_data(action_instance, request):

    service_request = action_instance.fk_request
    
    return {
        'request_number': service_request.request_number,
        'requester_name': service_request.fk_requester.get_full_name() if service_request.fk_requester else '',
        'organization_name': service_request.fk_organization.name_ar if service_request.fk_organization else '',
        'service_name': service_request.fk_service.name_ar if service_request.fk_service else '',
        'completion_date': action_instance.delivery_time.strftime('%Y-%m-%d') if action_instance.delivery_time else '',
        'stage_name': action_instance.fk_workflow_step.fk_stage.name_ar,
    }
