"""
Service Logs API - API سجلات الخدمات
APIs متقدمة لعرض وإدارة سجلات الخدمات مع الملاحظات والتنبيهات والإحصائيات
"""
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from django.utils import timezone
from django.db.models import Count, Q
from django.utils.translation import gettext_lazy as _

from d_services.models.ServiceLog import ServiceLog
from d_services.choices.choices import LogActionChoice, LogSeverityChoice
from d_services.utils.exception_handler import handle_exceptions
from config.imports.viewmodel_core import AllMVS
from utils.BranchMixinQuerset import BranchViewSetMixin


class ServiceLogsMVS(BranchViewSetMixin, AllMVS):
    """
    ViewSet متقدم لسجلات الخدمات
    يوفر عرض السجلات مع فلاتر متقدمة، إضافة ملاحظات، تعليم، ومراجعة
    """
    from d_services.serializers.logs import EnhancedServiceLogSerializer
    queryset = ServiceLog.objects.select_related('fk_service', 'fk_user', 'reviewed_by', 'related_version')
    serializer_class = EnhancedServiceLogSerializer
    branch_field = 'fk_service__fk_organization'
    enable_actions = ['all','select','list','second_list','filter','filter_paginate',]
    filterset_fields = {
        'fk_service': ['exact'],
        'action': ['exact', 'in'],
        'fk_user': ['exact'],
        'severity': ['exact', 'in'],
        'is_flagged': ['exact'],
        'reviewed_at': ['isnull'],
        'timestamp': ['gte', 'lte', 'date'],
    }
    search_fields = ['notes', 'fk_service__code', 'fk_service__name_ar', 'fk_user__username']
    ordering_fields = ['timestamp', 'severity', 'action']
    ordering = ['-timestamp']

    def get_queryset(self):
        return ServiceLog.objects.filter(
            is_deleted=False
        ).select_related(
            'fk_service', 'fk_user', 'reviewed_by', 'related_version'
        )

    def get_serializer_class(self):
        """اختيار Serializer حسب الـ action"""
        from d_services.serializers.logs import (
            EnhancedServiceLogSerializer,
            ServiceLogDetailSerializer,
            ServiceLogStatisticsSerializer,
        )
        if self.action == 'retrieve':
            return ServiceLogDetailSerializer
        if self.action == 'statistics':
            return ServiceLogStatisticsSerializer
        return EnhancedServiceLogSerializer

    # ========================================
    # العمليات الأساسية - Core Operations
    # ========================================
    @handle_exceptions
    def list(self, request, *args, **kwargs):
        """قائمة السجلات مع فلاتر متقدمة"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset[:100], many=True)
        return Response({
            'success': True,
            'message': _('تم جلب السجلات بنجاح'),
            'data': serializer.data
        })

    @handle_exceptions
    def retrieve(self, request, pk=None, *args, **kwargs):
        """تفاصيل سجل معين"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'success': True,
            'message': _('تم جلب تفاصيل السجل بنجاح'),
            'data': serializer.data
        })

    # ========================================
    # العمليات المتقدمة - Advanced Operations
    # ========================================
    @action(detail=False, methods=['get'], url_path='by-service', url_name='by-service')
    @handle_exceptions
    def by_service(self, request):
        """
        جلب سجلات خدمة معينة
        Query params: service_id (required), limit (optional, default=50)
        """
        service_id = request.query_params.get('service_id')
        if not service_id:
            return Response({
                'success': False,
                'message': _('يجب تحديد معرف الخدمة (service_id)'),
            }, status=status.HTTP_400_BAD_REQUEST)
        
        limit = int(request.query_params.get('limit', 50))
        logs = ServiceLog.get_recent_by_service(service_id, limit)
        serializer = self.get_serializer(logs, many=True)
        
        return Response({
            'success': True,
            'message': _('تم جلب سجلات الخدمة بنجاح'),
            'data': serializer.data,
            'count': logs.count()
        })

    @action(detail=False, methods=['get'], url_path='timeline', url_name='timeline')
    @handle_exceptions
    def timeline(self, request):
        """
        عرض timeline للخدمة
        Query params: service_id (required)
        """
        service_id = request.query_params.get('service_id')
        if not service_id:
            return Response({
                'success': False,
                'message': _('يجب تحديد معرف الخدمة (service_id)'),
            }, status=status.HTTP_400_BAD_REQUEST)
        
        logs = self.get_queryset().filter(
            fk_service_id=service_id
        ).order_by('timestamp')
        
        # تجميع حسب التاريخ
        timeline_data = []
        current_date = None
        current_group = []
        
        for log in logs:
            log_date = log.timestamp.date()
            if current_date != log_date:
                if current_group:
                    timeline_data.append({
                        'date': str(current_date),
                        'events': current_group
                    })
                current_date = log_date
                current_group = []
            
            current_group.append({
                'id': log.id,
                'time': log.timestamp.strftime('%H:%M'),
                'action': log.action,
                'action_display': log.action_display,
                'user': log.fk_user.username if log.fk_user else None,
                'severity': log.severity,
                'notes': log.notes[:100] if log.notes else None,
                'is_flagged': log.is_flagged,
            })
        
        if current_group:
            timeline_data.append({
                'date': str(current_date),
                'events': current_group
            })
        
        return Response({
            'success': True,
            'message': _('تم جلب timeline الخدمة بنجاح'),
            'data': timeline_data
        })

    @action(detail=False, methods=['get'], url_path='statistics', url_name='statistics')
    @handle_exceptions
    def statistics(self, request):
        """
        إحصائيات السجلات
        Query params: service_id (optional), days (optional, default=30)
        """
        service_id = request.query_params.get('service_id')
        days = int(request.query_params.get('days', 30))
        
        date_from = timezone.now() - timezone.timedelta(days=days)
        qs = self.get_queryset().filter(timestamp__gte=date_from)
        
        if service_id:
            qs = qs.filter(fk_service_id=service_id)
        
        # إحصائيات عامة
        stats = {
            'total_count': qs.count(),
            'flagged_count': qs.filter(is_flagged=True).count(),
            'pending_review_count': qs.filter(is_flagged=True, reviewed_at__isnull=True).count(),
            'by_action': {},
            'by_severity': {},
            'by_day': [],
        }
        
        # تجميع حسب الإجراء
        action_stats = qs.values('action').annotate(count=Count('id'))
        for item in action_stats:
            action_display = dict(LogActionChoice.choices).get(item['action'], item['action'])
            stats['by_action'][item['action']] = {
                'count': item['count'],
                'display': str(action_display)
            }
        
        # تجميع حسب مستوى الأهمية
        severity_stats = qs.values('severity').annotate(count=Count('id'))
        for item in severity_stats:
            severity_display = dict(LogSeverityChoice.choices).get(item['severity'], item['severity'])
            stats['by_severity'][item['severity']] = {
                'count': item['count'],
                'display': str(severity_display)
            }
        
        # تجميع حسب اليوم (آخر 7 أيام)
        from django.db.models.functions import TruncDate
        daily_stats = qs.filter(
            timestamp__gte=timezone.now() - timezone.timedelta(days=7)
        ).annotate(
            date=TruncDate('timestamp')
        ).values('date').annotate(count=Count('id')).order_by('date')
        
        stats['by_day'] = list(daily_stats)
        
        return Response({
            'success': True,
            'message': _('تم جلب الإحصائيات بنجاح'),
            'data': stats
        })

    # ========================================
    # إدارة الملاحظات والتنبيهات - Notes & Alerts Management
    # ========================================
    @action(detail=True, methods=['post'], url_path='add-note', url_name='add-note')
    @handle_exceptions
    def add_note(self, request, pk=None):
        """
        إضافة ملاحظة للسجل
        Body: { "note": "نص الملاحظة", "append": true/false }
        """
        log = self.get_object()
        note = request.data.get('note')
        append = request.data.get('append', True)
        
        if not note:
            return Response({
                'success': False,
                'message': _('يجب تحديد نص الملاحظة'),
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # إضافة معلومات المستخدم والوقت
        formatted_note = f"[{timezone.now().strftime('%Y-%m-%d %H:%M')}] {request.user.username}: {note}"
        log.add_note(formatted_note, append)
        
        return Response({
            'success': True,
            'message': _('تمت إضافة الملاحظة بنجاح'),
            'data': {'notes': log.notes}
        })

    @action(detail=True, methods=['post'], url_path='flag', url_name='flag')
    @handle_exceptions
    def flag(self, request, pk=None):
        """
        تعليم السجل للانتباه
        Body: { "reason": "سبب التعليم (اختياري)" }
        """
        log = self.get_object()
        reason = request.data.get('reason')
        
        log.flag(reason)
        
        return Response({
            'success': True,
            'message': _('تم تعليم السجل بنجاح'),
            'data': {
                'is_flagged': log.is_flagged,
                'flag_reason': log.flag_reason
            }
        })

    @action(detail=True, methods=['post'], url_path='unflag', url_name='unflag')
    @handle_exceptions
    def unflag(self, request, pk=None):
        """إزالة تعليم السجل"""
        log = self.get_object()
        log.unflag()
        
        return Response({
            'success': True,
            'message': _('تمت إزالة تعليم السجل بنجاح'),
            'data': {'is_flagged': log.is_flagged}
        })

    @action(detail=True, methods=['post'], url_path='mark-reviewed', url_name='mark-reviewed')
    @handle_exceptions
    def mark_reviewed(self, request, pk=None):
        """
        تعليم السجل كمراجع
        Body: { "notes": "ملاحظات المراجعة (اختياري)" }
        """
        log = self.get_object()
        notes = request.data.get('notes')
        
        log.mark_reviewed(request.user, notes)
        
        return Response({
            'success': True,
            'message': _('تم تعليم السجل كمراجع بنجاح'),
            'data': {
                'reviewed_by': log.reviewed_by.username,
                'reviewed_at': log.reviewed_at,
                'review_notes': log.review_notes
            }
        })

    # ========================================
    # التنبيهات والمراجعات - Alerts & Reviews
    # ========================================
    @action(detail=False, methods=['get'], url_path='alerts', url_name='alerts')
    @handle_exceptions
    def alerts(self, request):
        """
        التنبيهات النشطة (السجلات المعلمة غير المراجعة)
        """
        service_id = request.query_params.get('service_id')
        
        logs = ServiceLog.get_unreviewed(service_id)
        serializer = self.get_serializer(logs[:50], many=True)
        
        return Response({
            'success': True,
            'message': _('تم جلب التنبيهات بنجاح'),
            'data': serializer.data,
            'count': logs.count()
        })

    @action(detail=False, methods=['get'], url_path='flagged', url_name='flagged')
    @handle_exceptions
    def flagged(self, request):
        """
        جميع السجلات المعلمة
        """
        service_id = request.query_params.get('service_id')
        
        logs = ServiceLog.get_flagged(service_id)
        serializer = self.get_serializer(logs[:100], many=True)
        
        return Response({
            'success': True,
            'message': _('تم جلب السجلات المعلمة بنجاح'),
            'data': serializer.data,
            'count': logs.count()
        })

    @action(detail=False, methods=['get'], url_path='critical', url_name='critical')
    @handle_exceptions
    def critical(self, request):
        """
        السجلات الحرجة (ERROR, CRITICAL)
        """
        service_id = request.query_params.get('service_id')
        days = int(request.query_params.get('days', 7))
        
        date_from = timezone.now() - timezone.timedelta(days=days)
        qs = self.get_queryset().filter(
            timestamp__gte=date_from,
            severity__in=[LogSeverityChoice.ERROR, LogSeverityChoice.CRITICAL]
        )
        
        if service_id:
            qs = qs.filter(fk_service_id=service_id)
        
        serializer = self.get_serializer(qs[:50], many=True)
        
        return Response({
            'success': True,
            'message': _('تم جلب السجلات الحرجة بنجاح'),
            'data': serializer.data,
            'count': qs.count()
        })

    # ========================================
    # تصدير البيانات - Export
    # ========================================
    @action(detail=False, methods=['get'], url_path='export', url_name='export')
    @handle_exceptions
    def export(self, request):
        """
        تصدير السجلات كـ JSON
        Query params: service_id (optional), days (optional), format (json/csv)
        """
        service_id = request.query_params.get('service_id')
        days = int(request.query_params.get('days', 30))
        
        date_from = timezone.now() - timezone.timedelta(days=days)
        qs = self.get_queryset().filter(timestamp__gte=date_from)
        
        if service_id:
            qs = qs.filter(fk_service_id=service_id)
        
        # تحديد الحد الأقصى
        qs = qs[:1000]
        
        data = []
        for log in qs:
            data.append({
                'id': log.id,
                'service_code': log.fk_service.code,
                'action': log.action,
                'action_display': log.action_display,
                'user': log.fk_user.username if log.fk_user else None,
                'timestamp': log.timestamp.isoformat(),
                'severity': log.severity,
                'notes': log.notes,
                'is_flagged': log.is_flagged,
                'changes': log.changes,
            })
        
        return Response({
            'success': True,
            'message': _('تم تصدير السجلات بنجاح'),
            'data': data,
            'count': len(data)
        })
