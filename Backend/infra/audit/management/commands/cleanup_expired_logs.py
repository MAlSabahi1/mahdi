"""
cleanup_expired_logs — حذف سجلات التدقيق المنتهية
═══════════════════════════════════════════════════════
يحذف السجلات المؤرشفة الأقدم من 10 سنوات (افتراضياً).
يحذف أيضاً سجلات Idempotency المنتهية الصلاحية.

الاستخدام:
    python manage.py cleanup_expired_logs                  # 10 سنوات (افتراضي)
    python manage.py cleanup_expired_logs --days=3650      # 10 سنوات
    python manage.py cleanup_expired_logs --dry-run        # معاينة فقط
    python manage.py cleanup_expired_logs --include-login  # يشمل سجلات الدخول

⚠️ تحذير:
    - يحذف السجلات نهائياً — لا يمكن استرجاعها!
    - يُشغّل أسبوعياً عبر Cron أو Celery Beat
    - يحذف فقط السجلات المؤرشفة (is_archived=True)
"""
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone


class Command(BaseCommand):
    help = 'حذف سجلات التدقيق المؤرشفة الأقدم من 10 سنوات + تنظيف Idempotency'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=3650,  # 10 سنوات
            help='حذف السجلات المؤرشفة الأقدم من هذا العدد من الأيام (افتراضي: 3650 = 10 سنوات)',
        )
        parser.add_argument(
            '--batch-size',
            type=int,
            default=5000,
            help='حجم الدفعة (افتراضي: 5000)',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='معاينة فقط — لا تنفيذ فعلي',
        )
        parser.add_argument(
            '--include-login',
            action='store_true',
            help='يشمل سجلات الدخول القديمة أيضاً',
        )

    def handle(self, *args, **options):
        from infra.audit.models.audit_log import AuditLog
        from infra.audit.models.login_audit import LoginAuditLog

        days = options['days']
        batch_size = options['batch_size']
        dry_run = options['dry_run']
        include_login = options['include_login']
        cutoff_date = timezone.now() - timedelta(days=days)

        self.stdout.write(f'🗑️  تنظيف السجلات الأقدم من {cutoff_date.date()} ({days} يوم)')
        self.stdout.write('─' * 50)

        # ══════════════════════════════════════════════════
        # 1. حذف AuditLog المؤرشفة
        # ══════════════════════════════════════════════════
        audit_qs = AuditLog.objects.filter(
            timestamp__lt=cutoff_date,
            is_archived=True,  # فقط المؤرشفة — حماية إضافية
        )
        audit_count = audit_qs.count()

        self.stdout.write(f'  📋 AuditLog مؤرشفة للحذف: {audit_count:,}')

        if audit_count > 0 and not dry_run:
            deleted_total = 0
            while True:
                batch_ids = list(
                    AuditLog.objects.filter(
                        timestamp__lt=cutoff_date,
                        is_archived=True,
                    ).values_list('id', flat=True)[:batch_size]
                )
                if not batch_ids:
                    break
                deleted, _ = AuditLog.objects.filter(id__in=batch_ids).delete()
                deleted_total += deleted
                self.stdout.write(f'    ← حُذف {deleted:,} (المجموع: {deleted_total:,})')
            audit_count = deleted_total

        # ══════════════════════════════════════════════════
        # 2. حذف LoginAuditLog القديمة (اختياري)
        # ══════════════════════════════════════════════════
        login_count = 0
        if include_login:
            login_qs = LoginAuditLog.objects.filter(timestamp__lt=cutoff_date)
            login_count = login_qs.count()
            self.stdout.write(f'  🔑 LoginAuditLog للحذف: {login_count:,}')

            if login_count > 0 and not dry_run:
                deleted_total = 0
                while True:
                    batch_ids = list(
                        LoginAuditLog.objects.filter(
                            timestamp__lt=cutoff_date,
                        ).values_list('id', flat=True)[:batch_size]
                    )
                    if not batch_ids:
                        break
                    deleted, _ = LoginAuditLog.objects.filter(id__in=batch_ids).delete()
                    deleted_total += deleted
                login_count = deleted_total

        # ══════════════════════════════════════════════════
        # 3. تنظيف IdempotencyRecord المنتهية
        # ══════════════════════════════════════════════════
        idempotency_count = 0
        try:
            from infra.security.idempotency import IdempotencyRecord
            idempotency_qs = IdempotencyRecord.objects.filter(
                expires_at__lt=timezone.now()
            )
            idempotency_count = idempotency_qs.count()
            self.stdout.write(f'  🔄 IdempotencyRecord منتهية: {idempotency_count:,}')

            if idempotency_count > 0 and not dry_run:
                deleted, _ = idempotency_qs.delete()
                idempotency_count = deleted
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'  ⚠️ IdempotencyRecord: {e}'))

        # ══════════════════════════════════════════════════
        # النتيجة
        # ══════════════════════════════════════════════════
        self.stdout.write('─' * 50)

        if dry_run:
            self.stdout.write(self.style.WARNING(
                '⚠️ وضع المعاينة — لم يُحذف شيء.'
            ))
        else:
            # تسجيل العملية
            from infra.audit.services.audit_service import AuditService
            AuditService.log_action(
                user=None,
                action='SYSTEM_CLEANUP',
                model_name='AuditLog',
                object_id='bulk',
                new_data={
                    'audit_deleted': audit_count,
                    'login_deleted': login_count,
                    'idempotency_deleted': idempotency_count,
                    'cutoff_date': str(cutoff_date.date()),
                    'days': days,
                },
                severity='medium',
                module='system',
            )

            self.stdout.write(self.style.SUCCESS(
                f'✅ تم التنظيف: '
                f'Audit={audit_count:,} | '
                f'Login={login_count:,} | '
                f'Idempotency={idempotency_count:,}'
            ))
