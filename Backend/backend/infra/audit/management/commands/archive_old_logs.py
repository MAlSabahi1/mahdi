"""
archive_old_logs — أرشفة سجلات التدقيق القديمة
═══════════════════════════════════════════════════════
يُعلّم السجلات القديمة (أقدم من 5 سنوات افتراضياً) كـ is_archived=True.
السجلات المؤرشفة تبقى قابلة للبحث لكن يمكن نقلها لتخزين بارد.

الاستخدام:
    python manage.py archive_old_logs                  # 5 سنوات (افتراضي)
    python manage.py archive_old_logs --days=1825      # 5 سنوات
    python manage.py archive_old_logs --days=365       # سنة واحدة
    python manage.py archive_old_logs --dry-run        # معاينة فقط

ملاحظة:
    - لا يحذف أي سجلات — فقط يعلّمها كمؤرشفة
    - يُشغّل يومياً عبر Cron أو Celery Beat
    - يستخدم batch update لتقليل الضغط على DB
"""
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone


class Command(BaseCommand):
    help = 'أرشفة سجلات التدقيق القديمة (تعليمها كـ is_archived=True)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=1825,  # 5 سنوات
            help='أرشفة السجلات الأقدم من هذا العدد من الأيام (افتراضي: 1825 = 5 سنوات)',
        )
        parser.add_argument(
            '--batch-size',
            type=int,
            default=5000,
            help='حجم الدفعة لتقليل الضغط على DB (افتراضي: 5000)',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='معاينة فقط — لا تنفيذ فعلي',
        )

    def handle(self, *args, **options):
        from infra.audit.models.audit_log import AuditLog

        days = options['days']
        batch_size = options['batch_size']
        dry_run = options['dry_run']
        cutoff_date = timezone.now() - timedelta(days=days)

        # عدد السجلات المرشحة للأرشفة
        qs = AuditLog.objects.filter(
            timestamp__lt=cutoff_date,
            is_archived=False,
        )
        total = qs.count()

        if total == 0:
            self.stdout.write(self.style.SUCCESS(
                f'✅ لا توجد سجلات للأرشفة (أقدم من {days} يوم).'
            ))
            return

        self.stdout.write(
            f'📦 عدد السجلات المرشحة للأرشفة: {total:,} '
            f'(أقدم من {cutoff_date.date()})'
        )

        if dry_run:
            self.stdout.write(self.style.WARNING(
                '⚠️ وضع المعاينة — لم يتم تعديل أي سجلات.'
            ))
            return

        # أرشفة على دفعات
        archived_total = 0
        while True:
            batch_ids = list(
                AuditLog.objects.filter(
                    timestamp__lt=cutoff_date,
                    is_archived=False,
                ).values_list('id', flat=True)[:batch_size]
            )

            if not batch_ids:
                break

            updated = AuditLog.objects.filter(id__in=batch_ids).update(
                is_archived=True,
            )
            archived_total += updated
            self.stdout.write(f'  ← أُرشف {updated:,} سجل (المجموع: {archived_total:,}/{total:,})')

        # تسجيل العملية في audit نفسه
        from infra.audit.services.audit_service import AuditService
        AuditService.log_action(
            user=None,
            action='SYSTEM_ARCHIVE',
            model_name='AuditLog',
            object_id='bulk',
            new_data={
                'archived_count': archived_total,
                'cutoff_date': str(cutoff_date.date()),
                'days': days,
            },
            severity='info',
            module='system',
        )

        self.stdout.write(self.style.SUCCESS(
            f'✅ تمت الأرشفة بنجاح: {archived_total:,} سجل.'
        ))
