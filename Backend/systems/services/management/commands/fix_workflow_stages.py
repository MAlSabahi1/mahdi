"""
fix_workflow_stages.py
═══════════════════════════════════════════════════════
أمر Django لتصحيح أسماء وأكواد مراحل سير العمل.

الهيكل الصحيح للمحافظة:
  1. رئيس قسم الخدمات     (code: services_dept)
  2. مدير إدارة القوى البشرية (code: hr_director)
  3. المدير العام للمحافظة  (code: governor_general)

الاستخدام:
  python manage.py fix_workflow_stages
  python manage.py fix_workflow_stages --dry-run   ← للمعاينة فقط
"""
from django.core.management.base import BaseCommand
from django.db import transaction


# الخريطة: الكود القديم/الاسم القديم → (كود جديد، اسم جديد)
STAGE_FIXES = [
    # مراحل قد تكون مُدخَلة بأسماء خاطئة
    {
        'match_codes': ['hr', 'resources', 'moarad'],
        'match_names': ['الموارد البشرية', 'مراجعة الموارد البشرية', 'مدير الموارد البشرية',
                        'قسم الموارد', 'مدير الموارد'],
        'new_code': 'hr_director',
        'new_name': 'مدير إدارة القوى البشرية',
    },
    {
        'match_codes': ['services', 'khidmat', 'service'],
        'match_names': ['قسم الخدمات', 'رئيس الخدمات', 'قسم الخدمات الامنيه',
                        'مراجعة الخدمات', 'موظف الخدمات'],
        'new_code': 'services_dept',
        'new_name': 'رئيس قسم الخدمات',
    },
    {
        'match_codes': ['director', 'general', 'mudeer'],
        'match_names': ['المدير العام', 'اعتماد مدير', 'مدير عام',
                        'اعتماد المدير العام', 'المدير العام للمحافظة/الوحدة'],
        'new_code': 'governor_general',
        'new_name': 'المدير العام للمحافظة',
    },
]


class Command(BaseCommand):
    help = 'تصحيح أسماء وأكواد مراحل سير العمل لتتطابق مع هيكل المحافظة'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run', action='store_true',
            help='معاينة التغييرات فقط بدون تطبيقها'
        )

    def handle(self, *args, **options):
        from systems.services.models import WorkflowStage

        dry_run = options['dry_run']
        if dry_run:
            self.stdout.write(self.style.WARNING('وضع المعاينة فقط — لا تُطبَّق أي تغييرات\n'))

        all_stages = list(WorkflowStage.objects.all())
        self.stdout.write(f'\nعدد المراحل الموجودة: {len(all_stages)}\n')
        self.stdout.write('─' * 60)

        changed = 0
        for stage in all_stages:
            self.stdout.write(f'\n  الكود: {stage.code!r:30} الاسم: {stage.name_ar!r}')

            for fix in STAGE_FIXES:
                code_match = stage.code in fix['match_codes']
                name_match = any(n in stage.name_ar for n in fix['match_names'])

                if code_match or name_match:
                    self.stdout.write(
                        self.style.WARNING(
                            f'\n    → يتطابق! سيصبح: code={fix["new_code"]!r}, name={fix["new_name"]!r}'
                        )
                    )
                    if not dry_run:
                        with transaction.atomic():
                            existing = WorkflowStage.objects.filter(code=fix['new_code']).first()
                            if existing and existing.id != stage.id:
                                # دمج: تحديث الخطوات المرتبطة لتشير إلى المرحلة الموجودة
                                from systems.services.models import ServiceWorkflowStep
                                steps_updated = ServiceWorkflowStep.objects.filter(stage=stage).update(stage=existing)
                                self.stdout.write(self.style.WARNING(f'      [Merge] تم دمج {steps_updated} خطوة للمرحلة الموجودة مسبقاً. سيتم حذف المرحلة المكررة.'))
                                stage.delete()
                            else:
                                stage.code = fix['new_code']
                                stage.name_ar = fix['new_name']
                                stage.save(update_fields=['code', 'name_ar'])
                    changed += 1
                    break
            else:
                self.stdout.write(self.style.SUCCESS('  ✓ لا يحتاج تعديل'))

        self.stdout.write('\n' + '═' * 60)
        if dry_run:
            self.stdout.write(
                self.style.WARNING(f'\n[معاينة] سيتم تعديل {changed} مرحلة. شغّل بدون --dry-run للتطبيق.')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'\n✅ تم تعديل {changed} مرحلة بنجاح.')
            )

        # عرض الحالة النهائية
        self.stdout.write('\n--- الحالة النهائية ---')
        for stage in WorkflowStage.objects.all():
            self.stdout.write(f'  {stage.code:25} → {stage.name_ar}')
