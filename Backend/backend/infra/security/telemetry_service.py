"""
Telemetry Service - خدمة المراقبة الأمنية

تجميع إحصائيات أمنية لعرضها في لوحة المراقبة:
- محاولات دخول فاشلة
- جلسات نشطة
- طلبات تفويض معلقة
- أحجام جداول الظل
- سلامة سجل التدقيق
"""
from django.db import connection
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta


class TelemetryService:
    """خدمة تجميع وعرض البيانات الأمنية"""
    
    def collect_all_metrics(self) -> dict:
        """تجميع جميع المقاييس وحفظها"""
        from infra.security.models import MetricsSnapshot
        
        metrics = {
            'login_failures': self._collect_login_failures(),
            'active_sessions': self._collect_active_sessions(),
            'pending_dual_auth': self._collect_pending_dual_auth(),
            'shadow_table_sizes': self._collect_shadow_table_sizes(),
            'system_health': self._collect_system_health(),
        }
        
        # حفظ كل مقياس
        for metric_type, data in metrics.items():
            MetricsSnapshot.objects.create(
                metric_type=metric_type,
                data=data,
            )
        
        return metrics
    
    def get_dashboard_data(self) -> dict:
        """
        جلب أحدث بيانات لوحة المراقبة
        """
        from infra.security.models import MetricsSnapshot
        
        dashboard = {}
        metric_types = [
            'login_failures', 'active_sessions', 'pending_dual_auth',
            'shadow_table_sizes', 'system_health',
        ]
        
        for mt in metric_types:
            latest = MetricsSnapshot.objects.filter(
                metric_type=mt
            ).first()
            dashboard[mt] = latest.data if latest else {}
        
        return dashboard
    
    def _collect_login_failures(self) -> dict:
        """تجميع محاولات الدخول الفاشلة (آخر 24 ساعة)"""
        from infra.audit.models import AuditLog
        
        since = timezone.now() - timedelta(hours=24)
        
        failures = AuditLog.objects.filter(
            action='LOGIN_FAILED',
            timestamp__gte=since
        )
        
        # تجميع حسب الساعة
        hourly = {}
        for f in failures:
            hour = f.timestamp.strftime('%H:00')
            hourly[hour] = hourly.get(hour, 0) + 1
        
        # تجميع حسب IP
        by_ip = {}
        for f in failures:
            ip = f.ip_address or 'unknown'
            by_ip[ip] = by_ip.get(ip, 0) + 1
        
        return {
            'total_24h': failures.count(),
            'by_hour': hourly,
            'by_ip': by_ip,
            'collected_at': timezone.now().isoformat(),
        }
    
    def _collect_active_sessions(self) -> dict:
        """تجميع الجلسات النشطة"""
        from infra.accounts.models import UserSession
        
        cutoff = timezone.now() - timedelta(minutes=30)
        active = UserSession.objects.filter(
            is_active=True,
            last_activity__gte=cutoff
        )
        
        return {
            'active_count': active.count(),
            'users': list(
                active.values_list('user__username', flat=True).distinct()
            ),
            'collected_at': timezone.now().isoformat(),
        }
    
    def _collect_pending_dual_auth(self) -> dict:
        """طلبات التفويض المزدوج المعلقة"""
        from infra.security.models import DualAuthorizationRequest
        
        pending = DualAuthorizationRequest.objects.filter(
            status='pending',
            expires_at__gt=timezone.now()
        )
        
        return {
            'pending_count': pending.count(),
            'by_type': dict(
                pending.values_list('action_type').annotate(
                    count=Count('id')
                ).values_list('action_type', 'count')
            ),
            'collected_at': timezone.now().isoformat(),
        }
    
    def _collect_shadow_table_sizes(self) -> dict:
        """أحجام جداول الظل"""
        sizes = {}
        shadow_tables = [
            'personnel_master_history',
            'service_event_log_history',
        ]
        
        for table in shadow_tables:
            try:
                with connection.cursor() as cursor:
                    cursor.execute(
                        f"SELECT COUNT(*) FROM {table}"
                    )
                    row = cursor.fetchone()
                    sizes[table] = row[0] if row else 0
            except Exception:
                sizes[table] = -1  # جدول غير موجود بعد
        
        return {
            'tables': sizes,
            'collected_at': timezone.now().isoformat(),
        }
    
    def _collect_system_health(self) -> dict:
        """صحة النظام العامة"""
        from infra.audit.models import AuditLog
        from systems.personnel.models import PersonnelMaster
        
        now = timezone.now()
        last_24h = now - timedelta(hours=24)
        
        return {
            'total_personnel': PersonnelMaster.objects.count(),
            'total_audit_logs': AuditLog.objects.count(),
            'audit_logs_24h': AuditLog.objects.filter(
                timestamp__gte=last_24h
            ).count(),
            'db_size': self._get_db_size(),
            'collected_at': now.isoformat(),
        }
    
    def _get_db_size(self) -> str:
        """حجم قاعدة البيانات"""
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT pg_size_pretty(pg_database_size(current_database()))"
                )
                row = cursor.fetchone()
                return row[0] if row else 'unknown'
        except Exception:
            return 'unknown'
