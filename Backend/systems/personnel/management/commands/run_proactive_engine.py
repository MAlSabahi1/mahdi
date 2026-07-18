"""
run_proactive_engine.py
═══════════════════════════════════════
Management Command: يستدعي الخدمة المركزية ويحوّل النتائج إلى إشعارات في قاعدة البيانات.
يُشغَّل عبر: python manage.py run_proactive_engine
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from core.models.notification import NotificationRecord
from systems.personnel.engines.proactive_engine import run_engine_scan

User = get_user_model()

# ── تعيين نوع الإشعار حسب الخطورة ────────────────────────────────────────────
URGENCY_TO_NOTIF_TYPE = {
    'exceeded': 'WARNING',
    'critical': 'WARNING',
    'high':     'WARNING',
    'medium':   'SYSTEM',
    'low':      'SYSTEM',
    'info':     'SYSTEM',
}

URGENCY_TO_PRIORITY = {
    'exceeded': 'urgent',
    'critical': 'urgent',
    'high':     'high',
    'medium':   'normal',
    'low':      'normal',
    'info':     'normal',
}


class Command(BaseCommand):
    help = 'Run the Proactive Engine — scans personnel and creates notification records for admins.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('══════════════════════════════════'))
        self.stdout.write(self.style.NOTICE('   المحرك الاستباقي — بدء الفحص'))
        self.stdout.write(self.style.NOTICE('══════════════════════════════════'))

        # ── 1. تشغيل المحرك المركزي ───────────────────────────────────────
        warnings, stats, settings_used = run_engine_scan()

        self.stdout.write(f'الإعدادات: سن التقاعد={settings_used["retirement_age"]}, '
                          f'مدة الخدمة={settings_used["min_service_years"]}, '
                          f'نافذة الإنذار={settings_used["warning_months"]} أشهر')
        self.stdout.write(f'عدد الإنذارات المكتشفة: {stats["total"]}')

        if stats['total'] == 0:
            self.stdout.write(self.style.SUCCESS('لا توجد إنذارات — كل شيء على ما يرام.'))
            return

        # ── 2. جلب المستخدمين المسؤولين ────────────────────────────────────
        admins = User.objects.filter(is_superuser=True)
        if not admins.exists():
            self.stdout.write(self.style.WARNING('لا يوجد مستخدمين مسؤولين (superuser) لإرسال الإشعارات لهم!'))
            return

        # ── 3. تحويل الإنذارات إلى إشعارات ─────────────────────────────────
        created_count = 0
        skipped_count = 0

        for warning in warnings:
            notif_type = URGENCY_TO_NOTIF_TYPE.get(warning.get('urgency', 'info'), 'SYSTEM')
            priority = URGENCY_TO_PRIORITY.get(warning.get('urgency', 'info'), 'normal')
            mil_num = warning.get('military_number', '')

            for admin in admins:
                # منع التكرار: لا تُنشئ إشعاراً إذا وُجد إشعار مطابق غير مقروء
                already_exists = NotificationRecord.objects.filter(
                    notification_type=notif_type,
                    related_object_id=mil_num,
                    related_object_type='PersonnelMaster',
                    target_user=admin,
                    is_read=False,
                ).exists()

                if already_exists:
                    skipped_count += 1
                    continue

                NotificationRecord.objects.create(
                    notification_type=notif_type,
                    title=f'{warning.get("full_name", "")} — {warning.get("message", "")[:60]}',
                    message=warning.get('message', ''),
                    priority=priority,
                    target_user=admin,
                    related_object_type='PersonnelMaster',
                    related_object_id=mil_num,
                )
                created_count += 1

        # ── 4. الخلاصة ────────────────────────────────────────────────────
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(f'✅ تم بنجاح!'))
        self.stdout.write(f'   أُنشئ: {created_count} إشعار جديد')
        self.stdout.write(f'   تُخطّي: {skipped_count} (موجود مسبقاً)')
        self.stdout.write(f'   الإحصائيات: بلغوا السن={stats["exceeded_age"]}, '
                          f'أكملوا المدة={stats["exceeded_service"]}, '
                          f'مقتربون={stats["approaching"]}, '
                          f'بيانات ناقصة={stats["missing_data"]}, '
                          f'حالات مؤقتة={stats["temp_status_ending"]}')
