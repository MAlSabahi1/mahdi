
import uuid
import time
from typing import Optional, Dict, Any, List, Type
from django.db import transaction
from django.utils import timezone
from django.http import HttpRequest

from d_services.choices.choices import LogActionChoice, LogSeverityChoice, SLAStatusChoice


class LoggingManager:

    @staticmethod
    def get_request_metadata(request: HttpRequest) -> Dict[str, Any]:

        if not request:
            return {}
        
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0].strip()
        else:
            ip_address = request.META.get('REMOTE_ADDR')
        
        return {
            'ip_address': ip_address,
            'user_agent': request.META.get('HTTP_USER_AGENT', '')[:500] if request.META.get('HTTP_USER_AGENT') else None,
            'request_path': request.path[:500] if hasattr(request, 'path') else None,
            'request_method': request.method if hasattr(request, 'method') else None,
            'session_id': getattr(request, 'session_id', None) or str(uuid.uuid4()),
        }
    
    @staticmethod
    def calculate_changes(old_data: Dict, new_data: Dict) -> tuple:
        changes = {}
        old_values = {}
        new_values = {}
        affected_fields = []
        
        all_keys = set(old_data.keys()) | set(new_data.keys())
        
        for key in all_keys:
            old_val = old_data.get(key)
            new_val = new_data.get(key)
            
            if old_val != new_val:
                changes[key] = {'from': old_val, 'to': new_val}
                old_values[key] = old_val
                new_values[key] = new_val
                affected_fields.append(key)
        
        return changes, old_values, new_values, affected_fields


    @classmethod
    def log_service_action(
        cls,
        service,
        action: str,
        user=None,
        request: HttpRequest = None,
        old_data: Dict = None,
        new_data: Dict = None,
        notes: str = None,
        severity: str = LogSeverityChoice.INFO,
        related_version=None,
        extra_data: Dict = None,
        start_time: float = None
    ):

        from d_services.models.ServiceLog import ServiceLog
        
        changes, old_values, new_values, affected_fields = {}, {}, {}, []
        if old_data and new_data:
            changes, old_values, new_values, affected_fields = cls.calculate_changes(old_data, new_data)
        
        metadata = cls.get_request_metadata(request) if request else {}
        
        duration_ms = None
        if start_time:
            duration_ms = int((time.time() - start_time) * 1000)
        
        return ServiceLog.objects.create(
            fk_service=service,
            action=action,
            fk_user=user,
            changes=changes,
            old_values=old_values,
            new_values=new_values,
            affected_fields=affected_fields,
            notes=notes,
            severity=severity,
            related_version=related_version,
            extra_data=extra_data or {},
            duration_ms=duration_ms,
            **metadata
        )

    @classmethod
    def log_request_action(
        cls,
        service_request,
        action: str,
        user=None,
        request: HttpRequest = None,
        old_data: Dict = None,
        new_data: Dict = None,
        old_status: str = None,
        new_status: str = None,
        old_payment_status: str = None,
        new_payment_status: str = None,
        notes: str = None,
        severity: str = LogSeverityChoice.INFO,
        related_stage=None,
        rollback_data: Dict = None,
        extra_data: Dict = None,
        start_time: float = None
    ):

        from d_services.models.RequestLog import RequestLog
        
        changes, old_values, new_values, affected_fields = {}, {}, {}, []
        if old_data and new_data:
            changes, old_values, new_values, affected_fields = cls.calculate_changes(old_data, new_data)
        
        metadata = cls.get_request_metadata(request) if request else {}
        
        duration_ms = None
        if start_time:
            duration_ms = int((time.time() - start_time) * 1000)
        
        return RequestLog.objects.create(
            fk_request=service_request,
            action=action,
            fk_user=user,
            changes=changes,
            old_values=old_values,
            new_values=new_values,
            affected_fields=affected_fields,
            old_status=old_status,
            new_status=new_status,
            old_payment_status=old_payment_status,
            new_payment_status=new_payment_status,
            notes=notes,
            severity=severity,
            related_stage=related_stage,
            rollback_data=rollback_data or {},
            extra_data=extra_data or {},
            duration_ms=duration_ms,
            **metadata
        )

    @classmethod
    def log_workflow_transition(
        cls,
        service_request,
        action: str = LogActionChoice.MOVE,
        from_stage=None,
        to_stage=None,
        request_action=None,
        user=None,
        request: HttpRequest = None,
        action_taken: str = None,
        notes: str = None,
        decision_notes: str = None,
        severity: str = LogSeverityChoice.INFO,
        started_at=None,
        completed_at=None,
        expected_duration_hours: int = None,
        input_data: Dict = None,
        output_data: Dict = None,
        extra_data: Dict = None,
        start_time: float = None
    ):

        from d_services.models.WorkflowLog import WorkflowLog
        
        metadata = cls.get_request_metadata(request) if request else {}
        session_id = metadata.pop('session_id', None)
        
        duration_ms = None
        if start_time:
            duration_ms = int((time.time() - start_time) * 1000)
        
        actual_duration_hours = None
        if started_at and completed_at:
            delta = completed_at - started_at
            actual_duration_hours = round(delta.total_seconds() / 3600, 2)
        
        sla_status = SLAStatusChoice.NOT_APPLICABLE
        is_overdue = False
        overdue_hours = None
        
        if expected_duration_hours and actual_duration_hours:
            if actual_duration_hours <= expected_duration_hours:
                sla_status = SLAStatusChoice.ON_TIME
            elif actual_duration_hours <= expected_duration_hours * 1.25:
                sla_status = SLAStatusChoice.AT_RISK
            else:
                sla_status = SLAStatusChoice.OVERDUE
                is_overdue = True
                overdue_hours = round(actual_duration_hours - expected_duration_hours, 2)
        
        return WorkflowLog.objects.create(
            fk_request=service_request,
            action=action,
            fk_from_stage=from_stage,
            fk_to_stage=to_stage,
            fk_request_action=request_action,
            fk_user=user,
            action_taken=action_taken,
            notes=notes,
            decision_notes=decision_notes,
            severity=severity,
            session_id=session_id,
            started_at=started_at,
            completed_at=completed_at,
            expected_duration_hours=expected_duration_hours,
            actual_duration_hours=actual_duration_hours,
            sla_status=sla_status,
            is_overdue=is_overdue,
            overdue_hours=overdue_hours,
            input_data=input_data or {},
            output_data=output_data or {},
            extra_data=extra_data or {},
            duration_ms=duration_ms,
        )

    @classmethod
    def bulk_log_service_actions(cls, entries: List[Dict]) -> List:

        from d_services.models.ServiceLog import ServiceLog
        
        logs = []
        for entry in entries:
            logs.append(ServiceLog(
                fk_service=entry.get('service'),
                action=entry.get('action'),
                fk_user=entry.get('user'),
                changes=entry.get('changes', {}),
                old_values=entry.get('old_values', {}),
                new_values=entry.get('new_values', {}),
                affected_fields=entry.get('affected_fields', []),
                notes=entry.get('notes'),
                severity=entry.get('severity', LogSeverityChoice.INFO),
                extra_data=entry.get('extra_data', {}),
            ))
        
        return ServiceLog.objects.bulk_create(logs)
    
    @classmethod
    def bulk_log_request_actions(cls, entries: List[Dict]) -> List:
        from d_services.models.RequestLog import RequestLog
        
        logs = []
        for entry in entries:
            logs.append(RequestLog(
                fk_request=entry.get('service_request'),
                action=entry.get('action'),
                fk_user=entry.get('user'),
                changes=entry.get('changes', {}),
                old_values=entry.get('old_values', {}),
                new_values=entry.get('new_values', {}),
                affected_fields=entry.get('affected_fields', []),
                old_status=entry.get('old_status'),
                new_status=entry.get('new_status'),
                notes=entry.get('notes'),
                severity=entry.get('severity', LogSeverityChoice.INFO),
                extra_data=entry.get('extra_data', {}),
            ))
        
        return RequestLog.objects.bulk_create(logs)


    @classmethod
    def log_service_create(cls, service, user=None, request=None, **kwargs):
        return cls.log_service_action(
            service=service,
            action=LogActionChoice.CREATE,
            user=user,
            request=request,
            **kwargs
        )
    
    @classmethod
    def log_service_update(cls, service, user=None, request=None, old_data=None, new_data=None, **kwargs):
        return cls.log_service_action(
            service=service,
            action=LogActionChoice.UPDATE,
            user=user,
            request=request,
            old_data=old_data,
            new_data=new_data,
            **kwargs
        )
    
    @classmethod
    def log_request_create(cls, service_request, user=None, request=None, **kwargs):
        return cls.log_request_action(
            service_request=service_request,
            action=LogActionChoice.CREATE,
            user=user,
            request=request,
            **kwargs
        )
    
    @classmethod
    def log_request_status_change(cls, service_request, old_status, new_status, user=None, request=None, **kwargs):
        return cls.log_request_action(
            service_request=service_request,
            action=LogActionChoice.UPDATE,
            user=user,
            request=request,
            old_status=old_status,
            new_status=new_status,
            **kwargs
        )
    
    @classmethod
    def log_stage_start(cls, service_request, stage, user=None, request=None, request_action=None, **kwargs):
        return cls.log_workflow_transition(
            service_request=service_request,
            action=LogActionChoice.START,
            to_stage=stage,
            request_action=request_action,
            user=user,
            request=request,
            started_at=timezone.now(),
            **kwargs
        )
    
    @classmethod
    def log_stage_complete(cls, service_request, from_stage, to_stage=None, user=None, request=None, **kwargs):
        return cls.log_workflow_transition(
            service_request=service_request,
            action=LogActionChoice.COMPLETE,
            from_stage=from_stage,
            to_stage=to_stage,
            user=user,
            request=request,
            completed_at=timezone.now(),
            **kwargs
        )
    
    @classmethod
    def log_stage_reject(cls, service_request, stage, user=None, request=None, reason=None, **kwargs):
        return cls.log_workflow_transition(
            service_request=service_request,
            action=LogActionChoice.REJECT,
            from_stage=stage,
            user=user,
            request=request,
            decision_notes=reason,
            severity=LogSeverityChoice.WARNING,
            **kwargs
        )
    
    @classmethod
    def log_stage_return(cls, service_request, from_stage, to_stage, user=None, request=None, reason=None, **kwargs):
        return cls.log_workflow_transition(
            service_request=service_request,
            action=LogActionChoice.RETURN,
            from_stage=from_stage,
            to_stage=to_stage,
            user=user,
            request=request,
            decision_notes=reason,
            **kwargs
        )


    @classmethod
    def log_permission_change(cls, service, user=None, request=None, permission_type=None, 
                               affected_groups=None, affected_users=None, **kwargs):
        extra_data = {
            'permission_type': permission_type,
            'affected_groups': affected_groups or [],
            'affected_users': affected_users or [],
        }
        return cls.log_service_action(
            service=service,
            action=LogActionChoice.PERMISSION_CHANGE,
            user=user,
            request=request,
            extra_data=extra_data,
            **kwargs
        )
