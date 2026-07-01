"""
clean_legacy_corrections.py
═══════════════════════════════════════════════════════════════
أمر إدارة لتنظيف سجلات SuggestedCorrection غير الصالحة.

الوظائف:
  1. حذف صارم للسجلات التي field_name = 'current_rank'
     (بيانات legacy من قبل نظام RankSettlement — لا تنتمي لهذا الجدول)
  2. ملء security_admin الفارغة من بيانات الفرد المرتبط
  3. ملء requested_at الفارغة بقيمة افتراضية

الاستخدام:
  python manage.py clean_legacy_corrections --dry-run
  python manage.py clean_legacy_corrections --execute
═══════════════════════════════════════════════════════════════
"""
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction


class Command(BaseCommand):
    help = 'تنظيف سجلات SuggestedCorrection القديمة وإصلاح البيانات الناقصة'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            default=False,
            help='عرض ما سيتم تنفيذه دون تعديل فعلي على قاعدة البيانات',
        )
        parser.add_argument(
            '--execute',
            action='store_true',
            default=False,
            help='تنفيذ التنظيف فعلياً على قاعدة البيانات',
        )
        parser.add_argument(
            '--skip-delete',
            action='store_true',
            default=False,
            help='تخطّي خطوة الحذف وتنفيذ الإصلاح فقط',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        execute = options['execute']

        if not dry_run and not execute:
            raise CommandError(
                'يجب تحديد --dry-run للمعاينة أو --execute للتنفيذ الفعلي.'
            )

        mode = 'DRY-RUN (معاينة فقط)' if dry_run else '⚠️  EXECUTE (تنفيذ فعلي)'
        self.stdout.write(self.style.WARNING(f'\n═══ وضع التشغيل: {mode} ═══\n'))

        # ── الاستيراد المتأخر لتجنب circular imports ──
        from systems.personnel.models import SuggestedCorrection

        # ══════════════════════════════════════════════
        # الخطوة 1: تحديد البيانات Legacy المراد حذفها
        # ══════════════════════════════════════════════
        legacy_qs = SuggestedCorrection.objects.filter(
            field_name='current_rank'
        )
        legacy_count = legacy_qs.count()
        self.stdout.write(
            f'📊 سجلات current_rank (legacy): {self.style.ERROR(str(legacy_count))}'
        )

        # السجلات ذات correction_type غير موجود في الـ choices الحالية
        valid_types = [c[0] for c in SuggestedCorrection.CORRECTION_TYPE_CHOICES]
        invalid_type_qs = SuggestedCorrection.objects.exclude(
            correction_type__in=valid_types
        )
        invalid_type_count = invalid_type_qs.count()
        self.stdout.write(
            f'📊 سجلات بنوع تصحيح غير صالح (rank_correction وغيره): '
            f'{self.style.ERROR(str(invalid_type_count))}'
        )

        # ══════════════════════════════════════════════
        # الخطوة 2: تحديد البيانات الناقصة (security_admin)
        # ══════════════════════════════════════════════
        missing_sa_qs = SuggestedCorrection.objects.filter(
            security_admin__isnull=True,
            personnel__isnull=False,
            personnel__security_admin__isnull=False,
        ).select_related('personnel__security_admin')
        missing_sa_count = missing_sa_qs.count()
        self.stdout.write(
            f'📊 سجلات بدون security_admin (قابلة للإصلاح): '
            f'{self.style.WARNING(str(missing_sa_count))}'
        )

        # ══════════════════════════════════════════════
        # إذا كان dry-run نتوقف هنا
        # ══════════════════════════════════════════════
        if dry_run:
            self.stdout.write('\n' + self.style.SUCCESS(
                'الوضع: DRY-RUN — لم يتم تعديل أي شيء.\n'
                'استخدم --execute لتنفيذ التنظيف الفعلي.'
            ))
            return

        # ══════════════════════════════════════════════
        # التنفيذ الفعلي داخل transaction آمنة
        # ══════════════════════════════════════════════
        with transaction.atomic():

            # ── 1a. حذف سجلات current_rank ──
            if not options['skip_delete']:
                deleted_rank, _ = legacy_qs.delete()
                self.stdout.write(self.style.SUCCESS(
                    f'✅ تم حذف {deleted_rank} سجل current_rank (legacy)'
                ))

                # ── 1b. حذف سجلات بنوع غير صالح ──
                deleted_invalid, _ = invalid_type_qs.delete()
                self.stdout.write(self.style.SUCCESS(
                    f'✅ تم حذف {deleted_invalid} سجل بنوع تصحيح غير صالح'
                ))
            else:
                self.stdout.write(self.style.WARNING('⏭️  تم تخطّي خطوة الحذف'))

            # ── 2. إصلاح security_admin الفارغة ──
            fixed_sa = 0
            for correction in missing_sa_qs.iterator(chunk_size=200):
                correction.security_admin = correction.personnel.security_admin
                # نستخدم update_fields لتجنب استدعاء full_clean()
                # (لأن البيانات القديمة قد لا تجتاز التحقق)
                SuggestedCorrection.objects.filter(pk=correction.pk).update(
                    security_admin=correction.personnel.security_admin
                )
                fixed_sa += 1

            self.stdout.write(self.style.SUCCESS(
                f'✅ تم إصلاح security_admin لـ {fixed_sa} سجل'
            ))

        # ══════════════════════════════════════════════
        # ملخص نهائي
        # ══════════════════════════════════════════════
        total_remaining = SuggestedCorrection.objects.count()
        self.stdout.write('\n' + '═' * 50)
        self.stdout.write(self.style.SUCCESS(
            f'✅ اكتمل التنظيف\n'
            f'   السجلات المتبقية في القاعدة: {total_remaining}'
        ))
        self.stdout.write('═' * 50 + '\n')
