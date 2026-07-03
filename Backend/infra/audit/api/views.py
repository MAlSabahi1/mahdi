"""
Audit API Views — واجهة برمجة التدقيق
═══════════════════════════════════════════
عرض + بحث + تصدير + تحقق من سلامة السجلات.

Endpoints:
    GET  /audit/logs/              → قائمة سجلات التدقيق (مع بحث وفلترة)
    GET  /audit/logs/<id>/         → تفاصيل سجل تدقيق
    GET  /audit/logs/stats/        → إحصائيات
    GET  /audit/logs/object-history/ → تاريخ كائن محدد
    POST /audit/logs/<id>/verify/  → تحقق من سلامة السجل (HMAC)
    GET  /audit/logins/            → سجلات الدخول
"""
import logging
from datetime import timedelta

from django.db.models import Count, Q
from django.utils import timezone
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from infra.audit.models.audit_log import AuditLog
from infra.audit.models.login_audit import LoginAuditLog
from infra.audit.serializers.serializers import (
    AuditLogSerializer,
    AuditLogListSerializer,
    LoginAuditLogSerializer,
)

logger = logging.getLogger('audit.views')


class AuditLogViewSet(ReadOnlyModelViewSet):
    """
    سجلات التدقيق — عرض فقط (Immutable).
    يدعم بحث وفلترة متقدمة.
    """
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    serializer_class = AuditLogListSerializer
    queryset = AuditLog.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AuditLogSerializer
        return AuditLogListSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        params = self.request.query_params

        # فلترة حسب الأكشن
        if action_filter := params.get('action'):
            qs = qs.filter(action=action_filter)

        # فلترة حسب النظام الفرعي
        if module := params.get('module'):
            qs = qs.filter(module=module)

        # فلترة حسب النموذج
        if model := params.get('model_name'):
            qs = qs.filter(model_name=model)

        # فلترة حسب المستخدم
        if user_id := params.get('user_id'):
            qs = qs.filter(user_id=user_id)

        # فلترة حسب الحساسية
        if severity := params.get('severity'):
            qs = qs.filter(severity=severity)

        # فلترة حسب التاريخ
        if date_from := params.get('date_from'):
            qs = qs.filter(timestamp__date__gte=date_from)
        if date_to := params.get('date_to'):
            qs = qs.filter(timestamp__date__lte=date_to)

        # بحث نصي
        if search := params.get('search'):
            qs = qs.filter(
                Q(username__icontains=search) |
                Q(model_name__icontains=search) |
                Q(object_id__icontains=search) |
                Q(change_reason__icontains=search)
            )

        return qs

    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None) -> Response:
        """التحقق من سلامة سجل تدقيق (HMAC)."""
        audit_log = self.get_object()
        is_valid = audit_log.verify()
        return Response({
            'success': True,
            'data': {
                'id': audit_log.pk,
                'is_verified': is_valid,
                'signature': audit_log.signature,
                'message': 'السجل سليم' if is_valid else '⚠️ تم اكتشاف تلاعب!',
            },
        })

    @action(detail=False, methods=['get'])
    def stats(self, request) -> Response:
        """إحصائيات التدقيق."""
        today = timezone.now().date()
        qs = AuditLog.objects.all()

        by_action = dict(
            qs.values_list('action').annotate(c=Count('id')).order_by('-c')
        )
        by_severity = dict(
            qs.values_list('severity').annotate(c=Count('id')).order_by('-c')
        )
        by_module = dict(
            qs.filter(module__gt='').values_list('module')
            .annotate(c=Count('id')).order_by('-c')
        )

        return Response({
            'success': True,
            'data': {
                'total_records': qs.count(),
                'today_count': qs.filter(timestamp__date=today).count(),
                'by_action': by_action,
                'by_severity': by_severity,
                'by_module': by_module,
            },
        })

    @action(detail=False, methods=['get'], url_path='object-history')
    def object_history(self, request) -> Response:
        """تاريخ تغييرات كائن محدد — Timeline."""
        model_name = request.query_params.get('model_name')
        object_id = request.query_params.get('object_id')

        if not model_name or not object_id:
            return Response(
                {'success': False, 'error': 'model_name و object_id مطلوبان'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        logs = AuditLog.objects.filter(
            model_name=model_name, object_id=str(object_id)
        ).order_by('-timestamp')[:100]

        serializer = AuditLogSerializer(logs, many=True)
        return Response({
            'success': True,
            'count': len(serializer.data),
            'results': serializer.data,
        })

    @action(detail=False, methods=['get'])
    def export(self, request) -> Response:
        """
        تصدير سجلات التدقيق بصيغة CSV.

        ⚠️ Frontend ملاحظات:
            GET /api/v1/audit/logs/export/?format=csv
            GET /api/v1/audit/logs/export/?format=csv&action=UPDATE&date_from=2026-01-01
            يدعم كل الفلاتر الموجودة في list (action, module, severity, date_from, date_to, etc.)
            الحد الأقصى: 50,000 سجل
        """
        import csv
        from django.http import HttpResponse

        # استخدام نفس الفلترة
        qs = self.get_queryset()
        max_export = 50000
        total = qs.count()

        if total > max_export:
            return Response(
                {
                    'success': False,
                    'error': f'عدد السجلات ({total:,}) يتجاوز الحد الأقصى ({max_export:,}). '
                             f'يرجى تضييق نطاق البحث.',
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # إنشاء CSV
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="audit_logs.csv"'
        # BOM for Excel Arabic support
        response.write('\ufeff')

        writer = csv.writer(response)
        writer.writerow([
            'ID', 'التوقيت', 'المستخدم', 'العملية', 'النموذج',
            'معرف الكائن', 'الحساسية', 'النظام الفرعي',
            'سبب التغيير', 'IP', 'البيانات القديمة', 'البيانات الجديدة',
        ])

        for log in qs.iterator(chunk_size=2000):
            writer.writerow([
                log.id,
                log.timestamp.strftime('%Y-%m-%d %H:%M:%S') if log.timestamp else '',
                log.username,
                log.action,
                log.model_name,
                log.object_id,
                log.severity,
                log.module,
                log.change_reason,
                log.ip_address or '',
                str(log.old_data) if log.old_data else '',
                str(log.new_data) if log.new_data else '',
            ])

        # تسجيل عملية التصدير
        from infra.audit.services.audit_service import AuditService
        AuditService.log_export(
            user=request.user,
            model_name='AuditLog',
            record_count=total,
            export_format='csv',
        )

        logger.info(
            f"[Audit Export] {request.user.username} exported {total} records"
        )
        return response


class LoginAuditViewSet(ReadOnlyModelViewSet):
    """سجلات تسجيل الدخول — عرض فقط."""
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    serializer_class = LoginAuditLogSerializer
    queryset = LoginAuditLog.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        params = self.request.query_params

        if action_filter := params.get('action'):
            qs = qs.filter(action=action_filter)
        if username := params.get('username'):
            qs = qs.filter(username_attempted__icontains=username)
        if ip := params.get('ip_address'):
            qs = qs.filter(ip_address=ip)
        if date_from := params.get('date_from'):
            qs = qs.filter(timestamp__date__gte=date_from)
        if date_to := params.get('date_to'):
            qs = qs.filter(timestamp__date__lte=date_to)

        return qs

    @action(detail=False, methods=['get'])
    def failed_attempts(self, request) -> Response:
        """محاولات الدخول الفاشلة في آخر 24 ساعة."""
        cutoff = timezone.now() - timedelta(hours=24)
        logs = LoginAuditLog.objects.filter(
            action='LOGIN_FAILED', timestamp__gte=cutoff,
        ).order_by('-timestamp')[:200]

        serializer = self.get_serializer(logs, many=True)
        return Response({
            'success': True,
            'count': len(serializer.data),
            'results': serializer.data,
        })

    @action(detail=False, methods=['get'])
    def export(self, request) -> Response:
        """
        تصدير سجلات الدخول بصيغة CSV.

        ⚠️ Frontend:
            GET /api/v1/audit/logins/export/
            GET /api/v1/audit/logins/export/?action=LOGIN_FAILED&date_from=2026-01-01
        """
        import csv
        from django.http import HttpResponse

        qs = self.get_queryset()
        max_export = 50000
        total = qs.count()

        if total > max_export:
            return Response(
                {'success': False, 'error': f'عدد السجلات يتجاوز {max_export:,}'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="login_audit.csv"'
        response.write('\ufeff')

        writer = csv.writer(response)
        writer.writerow([
            'ID', 'التوقيت', 'المستخدم', 'الحدث', 'IP',
            'سبب الفشل', 'User Agent', 'الموقع الجغرافي',
        ])

        for log in qs.iterator(chunk_size=2000):
            writer.writerow([
                log.id,
                log.timestamp.strftime('%Y-%m-%d %H:%M:%S') if log.timestamp else '',
                log.username_attempted,
                log.action,
                log.ip_address or '',
                log.failure_reason,
                log.user_agent[:100] if log.user_agent else '',
                log.geo_location,
            ])

        from infra.audit.services.audit_service import AuditService
        AuditService.log_export(
            user=request.user,
            model_name='LoginAuditLog',
            record_count=total,
            export_format='csv',
        )
        return response
