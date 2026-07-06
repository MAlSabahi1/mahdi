
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from django.utils import timezone
from django.db.models import Count, Avg, Max, Q
from django.utils.translation import gettext_lazy as _

from d_services.models.RequestLog import RequestLog
from d_services.models.WorkflowLog import WorkflowLog
from d_services.choices.choices import LogActionChoice, LogSeverityChoice, SLAStatusChoice
from d_services.utils.exception_handler import handle_exceptions
from utils.BranchMixinQuerset import BranchViewSetMixin
from config.imports.viewmodel_core import AllMVS
from d_services.serializers.logs import EnhancedRequestLogSerializer


class RequestLogsMVS(BranchViewSetMixin, AllMVS):
    queryset = RequestLog.objects.select_related('fk_request', 'fk_request__fk_service', 'fk_user', 'reviewed_by', 'related_stage')
    serializer_class = EnhancedRequestLogSerializer
    branch_field = 'fk_request__fk_organization'
    enable_actions = ['all','select','list','second_list','filter','filter_paginate',]

    def get_queryset(self):
        qs = RequestLog.objects.filter(
            is_deleted=False
        ).select_related(
            'fk_request', 'fk_request__fk_service', 'fk_user', 
            'reviewed_by', 'related_stage'
        )
        
        user = self.request.user
        if hasattr(user, 'fk_organization') and user.fk_organization and not user.is_superuser:
            qs = qs.filter(fk_request__fk_organization=user.fk_organization)
        
        return qs
    def _parse_notes_to_chat(self, notes_text):
        """
        تحويل نص الملاحظات إلى قائمة رسائل
        Format: [YYYY-MM-DD HH:MM] username: message_text
        """
        import re
        
        if not notes_text:
            return []
        
        chat_messages = []
        # Pattern to match: [2026-01-02 15:30] username: message text
        pattern = r'\[(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2})\]\s+([^:]+):\s*(.+?)(?=\[(\d{4}-\d{2}-\d{2})|$)'
        
        matches = re.findall(pattern, notes_text, re.DOTALL)
        
        if matches:
            for match in matches:
                datetime_str = match[0].strip()
                username = match[1].strip()
                message_text = match[2].strip()
                
                chat_messages.append({
                    'time': datetime_str,
                    'user': username,
                    'text': message_text,
                })
        else:
            # If no pattern matches, return the entire notes as a single message
            if notes_text.strip():
                chat_messages.append({
                    'time': None,
                    'user': None,
                    'text': notes_text.strip(),
                })
        
        return chat_messages



    @handle_exceptions
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset[:100], many=True)
        return Response({
            'success': True,
            'message': _('تم جلب سجلات الطلبات بنجاح'),
            'data': serializer.data
        })

    @action(detail=False, methods=['get'], url_path='by-request', url_name='by-request')
    @handle_exceptions
    def by_request(self, request):
        """
        جلب سجلات طلب معين
        Query params: request_id (required), limit (optional)
        """
        request_id = request.query_params.get('request_id')
        if not request_id:
            return Response({
                'success': False,
                'message': _('يجب تحديد معرف الطلب (request_id)'),
            }, status=status.HTTP_400_BAD_REQUEST)
        
        limit = int(request.query_params.get('limit', 50))
        logs = RequestLog.get_recent_by_request(request_id, limit)
        serializer = self.get_serializer(logs, many=True)
        
        return Response({
            'success': True,
            'message': _('تم جلب سجلات الطلب بنجاح'),
            'data': serializer.data
        })

    @action(detail=False, methods=['get'], url_path='timeline', url_name='timeline')
    @handle_exceptions
    def timeline(self, request):

        request_id = request.query_params.get('request_id')
        if not request_id:
            return Response({
                'success': False,
                'message': _('يجب تحديد معرف الطلب (request_id)'),
            }, status=status.HTTP_400_BAD_REQUEST)
        
        request_logs = RequestLog.get_timeline(request_id)
        
        workflow_logs = WorkflowLog.get_timeline(request_id)
        
        timeline = []
        
        for log in request_logs:
            timeline.append({
                'type': 'request',
                'id': log.id,
                'timestamp': log.timestamp,
                'action': log.action,
                'action_display': log.action_display,
                'user': log.fk_user.username if log.fk_user else None,
                'severity': log.severity,
                'old_status': log.old_status,
                'new_status': log.new_status,
                'notes': log.notes[:200] if log.notes else None,
                'is_flagged': log.is_flagged,
            })
        
        for log in workflow_logs:
            timeline.append({
                'type': 'workflow',
                'id': log.id,
                'timestamp': log.timestamp,
                'action': log.action,
                'action_display': log.action_display,
                'user': log.fk_user.username if log.fk_user else None,
                'from_stage': log.from_stage_name,
                'to_stage': log.to_stage_name,
                'action_taken': log.action_taken,
                'severity': log.severity,
                'sla_status': log.sla_status,
                'is_overdue': log.is_overdue,
                'notes': log.notes[:200] if log.notes else None,
            })
        
        timeline.sort(key=lambda x: x['timestamp'])
        
        grouped_timeline = []
        current_date = None
        current_group = []
        
        for event in timeline:
            event_date = event['timestamp'].date()
            if current_date != event_date:
                if current_group:
                    grouped_timeline.append({
                        'date': str(current_date),
                        'events': current_group
                    })
                current_date = event_date
                current_group = []
            
            event['time'] = event['timestamp'].strftime('%H:%M')
            del event['timestamp']
            current_group.append(event)
        
        if current_group:
            grouped_timeline.append({
                'date': str(current_date),
                'events': current_group
            })
        
        return Response({
            'success': True,
            'message': _('تم جلب timeline الطلب بنجاح'),
            'data': grouped_timeline
        })

    @action(detail=False, methods=['get'], url_path='status-changes', url_name='status-changes')
    @handle_exceptions
    def status_changes(self, request):
        from d_services.choices.choices import ServiceStatusChoice
        
        request_id = request.query_params.get('request_id')
        if not request_id:
            return Response({
                'success': False,
                'message': _('يجب تحديد معرف الطلب (request_id)'),
            }, status=status.HTTP_400_BAD_REQUEST)
        
        logs = RequestLog.get_status_changes(request_id)
        
        # قاموس لتحويل الحالات إلى العربية
        status_display = dict(ServiceStatusChoice.choices)
        
        status_flow = []
        for log in logs:
            status_flow.append({
                'id': log.id,
                'date': log.timestamp.strftime('%Y-%m-%d') if log.timestamp else None,
                'time': log.timestamp.strftime('%H:%M') if log.timestamp else None,
                'datetime': log.timestamp.strftime('%Y-%m-%d - %H:%M') if log.timestamp else None,
                'old_status': log.old_status,
                'old_status_display': str(status_display.get(log.old_status, log.old_status or '')),
                'new_status': log.new_status,
                'new_status_display': str(status_display.get(log.new_status, log.new_status or '')),
                'user': log.fk_user.username if log.fk_user else None,
                'notes': self._parse_notes_to_chat(log.notes),
            })
        
        return Response({
            'success': True,
            'message': _('تم جلب تغييرات الحالة بنجاح'),
            'data': status_flow
        })

    @action(detail=False, methods=['get'], url_path='statistics', url_name='statistics')
    @handle_exceptions
    def statistics(self, request):
        days = int(request.query_params.get('days', 30))
        date_from = timezone.now() - timezone.timedelta(days=days)
        
        qs = self.get_queryset().filter(timestamp__gte=date_from)
        
        stats = {
            'total_count': qs.count(),
            'flagged_count': qs.filter(is_flagged=True).count(),
            'by_action': {},
            'by_status_change': [],
        }
        action_stats = qs.values('action').annotate(count=Count('id'))
        for item in action_stats:
            stats['by_action'][item['action']] = item['count']
        
        status_changes = qs.exclude(
            new_status__isnull=True
        ).values('old_status', 'new_status').annotate(
            count=Count('id')
        ).order_by('-count')[:10]
        
        stats['by_status_change'] = list(status_changes)
        
        return Response({
            'success': True,
            'message': _('تم جلب الإحصائيات بنجاح'),
            'data': stats
        })

    @action(detail=True, methods=['post'],url_path="add-note",url_name="add-note")
    @handle_exceptions
    def add_note(self, request, pk=None):
        """إضافة ملاحظة للسجل"""
        log = self.get_object()
        note = request.data.get('note')
        
        if not note:
            return Response({
                'success': False,
                'message': _('يجب تحديد نص الملاحظة'),
            }, status=status.HTTP_400_BAD_REQUEST)
        
        formatted_note = f"[{timezone.now().strftime('%Y-%m-%d %H:%M')}] {request.user.username}: {note}"
        log.add_note(formatted_note)
        
        return Response({
            'success': True,
            'message': _('تمت إضافة الملاحظة بنجاح'),
        })

    @action(detail=True, methods=['post'], url_path='flag', url_name='flag')
    @handle_exceptions
    def flag(self, request, pk=None):
        log = self.get_object()
        reason = request.data.get('reason')
        log.flag(reason)
        
        return Response({
            'success': True,
            'message': _('تم تعليم السجل بنجاح'),
        })

    @action(detail=False, methods=['get'], url_path='alerts', url_name='alerts')
    @handle_exceptions
    def alerts(self, request):
        request_id = request.query_params.get('request_id')
        logs = RequestLog.get_flagged(request_id)
        serializer = self.get_serializer(logs[:50], many=True)
        
        return Response({
            'success': True,
            'message': _('تم جلب التنبيهات بنجاح'),
            'data': serializer.data
        })


class WorkflowLogsMVS(BranchViewSetMixin, AllMVS):
    """
    ViewSet متقدم لسجلات سير العمل
    يوفر عرض السجلات مع تقارير SLA والأداء
    """
    from d_services.serializers.logs import EnhancedWorkflowLogSerializer
    queryset = WorkflowLog.objects.select_related('fk_request', 'fk_request__fk_service', 'fk_user', 'fk_from_stage', 'fk_to_stage', 'fk_request_action')
    serializer_class = EnhancedWorkflowLogSerializer
    branch_field = 'fk_request__fk_organization'
    enable_actions = ['all','select','list','second_list','filter','filter_paginate',]
    filterset_fields = {
        'fk_request': ['exact'],
        'fk_user': ['exact'],
        'action': ['exact', 'in'],
        'sla_status': ['exact', 'in'],
        'is_overdue': ['exact'],
        'is_flagged': ['exact'],
        'timestamp': ['gte', 'lte', 'date'],
    }
    search_fields = ['notes', 'decision_notes', 'fk_request__request_number']
    ordering_fields = ['timestamp', 'actual_duration_hours', 'sla_status']
    ordering = ['-timestamp']

    def get_queryset(self):
        qs = WorkflowLog.objects.filter(
            is_deleted=False
        ).select_related(
            'fk_request', 'fk_request__fk_service', 'fk_user',
            'fk_from_stage', 'fk_to_stage', 'fk_request_action'
        )
        
        user = self.request.user
        if hasattr(user, 'fk_organization') and user.fk_organization and not user.is_superuser:
            qs = qs.filter(fk_request__fk_organization=user.fk_organization)
        
        return qs

    def get_serializer_class(self):
        from d_services.serializers.logs import (
            EnhancedWorkflowLogSerializer,
            WorkflowLogDetailSerializer,
        )
        if self.action == 'retrieve':
            return WorkflowLogDetailSerializer
        return EnhancedWorkflowLogSerializer

    # ========================================
    # العمليات الأساسية
    # ========================================
    @handle_exceptions
    def list(self, request, *args, **kwargs):
        """قائمة سجلات سير العمل"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset[:100], many=True)
        return Response({
            'success': True,
            'message': _('تم جلب سجلات سير العمل بنجاح'),
            'data': serializer.data
        })

    # ========================================
    # تقارير SLA والأداء
    # ========================================
    @action(detail=False, methods=['get'], url_path='by-request', url_name='by-request')
    @handle_exceptions 
    def by_request(self, request):
        """جلب سجلات طلب معين"""
        request_id = request.query_params.get('request_id')
        if not request_id:
            return Response({
                'success': False,
                'message': _('يجب تحديد معرف الطلب'),
            }, status=status.HTTP_400_BAD_REQUEST)
        
        logs = WorkflowLog.get_timeline(request_id)
        serializer = self.get_serializer(logs, many=True)
        
        return Response({
            'success': True,
            'message': _('تم جلب سجلات سير العمل بنجاح'),
            'data': serializer.data
        })

    @action(detail=False, methods=['get'], url_path='transitions', url_name='transitions')
    @handle_exceptions
    def transitions(self, request):
        """
        الانتقالات بين المراحل لطلب معين
        Query params: request_id (required)
        """
        request_id = request.query_params.get('request_id')
        if not request_id:
            return Response({
                'success': False,
                'message': _('يجب تحديد معرف الطلب'),
            }, status=status.HTTP_400_BAD_REQUEST)
        
        logs = self.get_queryset().filter(
            fk_request_id=request_id
        ).exclude(
            fk_from_stage__isnull=True,
            fk_to_stage__isnull=True
        ).order_by('timestamp')
        
        transitions = []
        for log in logs:
            transitions.append({
                'id': log.id,
                'timestamp': log.timestamp,
                'from_stage': log.from_stage_name,
                'to_stage': log.to_stage_name,
                'action': log.action,
                'action_taken': log.action_taken,
                'user': log.fk_user.username if log.fk_user else None,
                'duration_hours': float(log.actual_duration_hours) if log.actual_duration_hours else None,
                'sla_status': log.sla_status,
                'is_overdue': log.is_overdue,
            })
        
        return Response({
            'success': True,
            'message': _('تم جلب الانتقالات بنجاح'),
            'data': transitions
        })

    @action(detail=False, methods=['get'], url_path='sla-report', url_name='sla-report')
    @handle_exceptions
    def sla_report(self, request):
        """
        تقرير SLA
        Query params: days (optional, default=30), service_id (optional)
        """
        days = int(request.query_params.get('days', 30))
        service_id = request.query_params.get('service_id')
        
        date_from = timezone.now() - timezone.timedelta(days=days)
        qs = self.get_queryset().filter(
            timestamp__gte=date_from,
            sla_status__in=[SLAStatusChoice.ON_TIME, SLAStatusChoice.AT_RISK, SLAStatusChoice.OVERDUE]
        )
        
        if service_id:
            qs = qs.filter(fk_request__fk_service_id=service_id)
        
        stats = {
            'total': qs.count(),
            'on_time': qs.filter(sla_status=SLAStatusChoice.ON_TIME).count(),
            'at_risk': qs.filter(sla_status=SLAStatusChoice.AT_RISK).count(),
            'overdue': qs.filter(sla_status=SLAStatusChoice.OVERDUE).count(),
            'on_time_percentage': 0,
            'avg_duration_hours': None,
            'avg_overdue_hours': None,
        }
        
        if stats['total'] > 0:
            stats['on_time_percentage'] = round(
                (stats['on_time'] / stats['total']) * 100, 2
            )
        
        avg_duration = qs.filter(
            actual_duration_hours__isnull=False
        ).aggregate(avg=Avg('actual_duration_hours'))
        stats['avg_duration_hours'] = float(avg_duration['avg']) if avg_duration['avg'] else None
        
        avg_overdue = qs.filter(
            overdue_hours__isnull=False
        ).aggregate(avg=Avg('overdue_hours'))
        stats['avg_overdue_hours'] = float(avg_overdue['avg']) if avg_overdue['avg'] else None
        
        return Response({
            'success': True,
            'message': _('تم جلب تقرير SLA بنجاح'),
            'data': stats
        })

    @action(detail=False, methods=['get'], url_path='overdue', url_name='overdue')
    @handle_exceptions
    def overdue(self, request):
        """المراحل المتأخرة"""
        request_id = request.query_params.get('request_id')
        logs = WorkflowLog.get_overdue(request_id)
        serializer = self.get_serializer(logs[:50], many=True)
        
        return Response({
            'success': True,
            'message': _('تم جلب المراحل المتأخرة بنجاح'),
            'data': serializer.data,
            'count': logs.count()
        })

    @action(detail=False, methods=['get'], url_path='performance', url_name='performance')
    @handle_exceptions
    def performance(self, request):
        """
        تقرير الأداء لطلب معين
        Query params: request_id (required)
        """
        request_id = request.query_params.get('request_id')
        if not request_id:
            return Response({
                'success': False,
                'message': _('يجب تحديد معرف الطلب'),
            }, status=status.HTTP_400_BAD_REQUEST)
        
        performance = WorkflowLog.get_performance_summary(request_id)
        
        return Response({
            'success': True,
            'message': _('تم جلب تقرير الأداء بنجاح'),
            'data': performance
        })

    @action(detail=False, methods=['get'], url_path='stage-stats', url_name='stage-stats')
    @handle_exceptions
    def stage_stats(self, request):
        """
        إحصائيات حسب المرحلة
        Query params: stage_id (required)
        """
        stage_id = request.query_params.get('stage_id')
        if not stage_id:
            return Response({
                'success': False,
                'message': _('يجب تحديد معرف المرحلة'),
            }, status=status.HTTP_400_BAD_REQUEST)
        
        logs = WorkflowLog.get_by_stage(stage_id)
        
        stats = {
            'total': logs.count(),
            'avg_duration': None,
            'max_duration': None,
            'overdue_count': 0,
            'by_action': {},
        }
        
        agg = logs.aggregate(
            avg=Avg('actual_duration_hours'),
            max=Max('actual_duration_hours'),
            overdue=Count('id', filter=Q(is_overdue=True))
        )
        
        stats['avg_duration'] = float(agg['avg']) if agg['avg'] else None
        stats['max_duration'] = float(agg['max']) if agg['max'] else None
        stats['overdue_count'] = agg['overdue']
        
        action_stats = logs.values('action').annotate(count=Count('id'))
        for item in action_stats:
            stats['by_action'][item['action']] = item['count']
        
        return Response({
            'success': True,
            'message': _('تم جلب إحصائيات المرحلة بنجاح'),
            'data': stats
        })

    # ========================================
    # الملاحظات والتنبيهات
    # ========================================
    @action(detail=True, methods=['post'], url_path='add-note', url_name='add-note')
    @handle_exceptions
    def add_note(self, request, pk=None):
        """إضافة ملاحظة"""
        log = self.get_object()
        note = request.data.get('note')
        
        if not note:
            return Response({
                'success': False,
                'message': _('يجب تحديد نص الملاحظة'),
            }, status=status.HTTP_400_BAD_REQUEST)
        
        formatted_note = f"[{timezone.now().strftime('%Y-%m-%d %H:%M')}] {request.user.username}: {note}"
        log.add_note(formatted_note)
        
        return Response({
            'success': True,
            'message': _('تمت إضافة الملاحظة بنجاح'),
        })

    @action(detail=True, methods=['post'], url_path='flag', url_name='flag')
    @handle_exceptions
    def flag(self, request, pk=None):
        """تعليم السجل"""
        log = self.get_object()
        reason = request.data.get('reason')
        log.flag(reason)
        
        return Response({
            'success': True,
            'message': _('تم تعليم السجل بنجاح'),
        })
