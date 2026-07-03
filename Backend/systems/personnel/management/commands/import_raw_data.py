"""
import_raw_data.py
══════════════════════════════════════════════════════════
استيراد البيانات من ملف Excel إلى النظام (محرك ذكي محدّث)

الأعمدة المدعومة:
  الرقم العسكري / الرقم العسكري القديم / الرقم الوطني
  الرتبة / الاسم / تصحيح الاسم من واقع البطاقة
  الوحدة / الإدارة_السرية / القسم_فرع السرية
  المنصب / نوع العمل / الفئة / الحالة / نوع الحالة
  تصنيف القوة / المؤهل / رقم التليفون
  حالة النفقات / التعيينات / الملاحظات
  تاريخ الميلاد / تاريخ الألتحاق / تاريخ صدور القرار / تاريخ التصدور الينا
  أي عمود يبدأ بـ "متغير" → يُحفظ تلقائياً في HistoricalMonthlyVariables

استراتيجية ربط الهيكل التنظيمي (Soft Mapping):
  1. يُحاول مطابقة دقيقة أو جزئية مع CentralDepartment / Branch / DistrictPolice / Division
  2. إذا لم يجد تطابقاً → يترك الحقل NULL
     ويُضيف "[RAW_DEPT]: <القيمة الخام>" في حقل notes للمراجعة اليدوية
══════════════════════════════════════════════════════════
"""
import uuid
from datetime import datetime
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
import openpyxl

from core.models import (
    Rank, ServiceStatus, SecurityAdministration,
    CentralDepartment, Branch, DistrictPolice,
    Division, Unit, ForceType, Qualification,
    JobCategory, JobTitle, Position,
)
from systems.personnel.models import (
    PersonnelMaster, RawDataImport, SuggestedCorrection,
    HistoricalMonthlyVariables,
)

# ── جداول تصحيح الرتب ──
RANK_MAP = {
    'لواء': 'لواء', 'عميد': 'عميد', 'عقيد': 'عقيد',
    'مقدم': 'مقدم', 'رائد': 'رائد', 'نقيب': 'نقيب',
    'ملازم أول': 'ملازم أول', 'ملازم ثاني': 'ملازم ثاني',
    'مساعد1': 'مساعد 1', 'مساعد 1': 'مساعد 1', 'مساعد': 'مساعد 1',
    'مساعد2': 'مساعد 2', 'مساعد 2': 'مساعد 2',
    'رقيب1': 'رقيب 1', 'رقيب 1': 'رقيب 1',
    'رقيب2': 'رقيب 2', 'رقيب 2': 'رقيب 2',
    'عريف': 'عريف', 'جندي': 'جندي', 'مجند': 'جندي',
    'حارس': 'حارس', 'مدني': 'مدني', 'متعاقد': 'متعاقد',
}

# ── جداول تصحيح الحالات ──
STATUS_MAP = {
    'عاملين': 'عاملين', 'عامل': 'عاملين',
    'قوة عاملة فعلية': 'عاملين', 'قوة عاملة/فعلية': 'عاملين',
    'قوة احتياط': 'قوة احتياطية', 'قوة احتياطية': 'قوة احتياطية',
    'بدون عمل': 'بدون عمل', 'قوة غير فعلية': 'بدون عمل',
    'دارسين': 'دارسين', 'دراسة': 'دارسين',
    'منتدب': 'منتدبين لدى جهات', 'منتدبين': 'منتدبين لدى جهات',
    'مصدر': 'مصدرين إلى الوزارة', 'مصدرين': 'مصدرين إلى الوزارة',
    'منزل': 'مصدرين إلى الوزارة',
    'معيات': 'معارين', 'معارين': 'معارين',
    'غياب': 'غياب', 'غياب مستمر': 'غياب',
    'كبير سن': 'كبار سن', 'كبار سن': 'كبار سن',
    'جريح': 'جرحى', 'جرحى': 'جرحى',
    'أسير': 'أسرى', 'سجين': 'سجناء',
    'إجازة': 'إجازات', 'إجازات': 'إجازات',
    'شهيد': 'شهداء', 'شهداء': 'شهداء',
    'متوفى': 'وفيات', 'وفاة': 'وفيات',
    'متقاعد': 'متقاعدين', 'تقاعد': 'متقاعدين',
    'مفصول': 'مفصولين', 'مفصولين': 'مفصولين',
    'فرار': 'منقطعين - فرار', 'منقطع': 'منقطعين - فرار',
    'ملتحق بالعدوان': 'ملتحقين بالعدوان',
    'مهام أمنية': 'عاملين', 'خدمة أمنية': 'عاملين',
}

# ── تصنيف القوة ──
FORCE_TYPE_MAP = {
    'القوة الأساسي- أفراد': 'القوة الأساسي - أفراد',
    'القوة الأساسي - أفراد': 'القوة الأساسي - أفراد',
    'لجان أمنية- أفراد': 'لجان أمنية - أفراد',
    'لجان أمنية - أفراد': 'لجان أمنية - أفراد',
    'قوة- مستجدين جديد': 'قوة - مستجدين جديد',
    'قوة إداريا فقط': 'إداريا فقط',
    'إداريا فقط': 'إداريا فقط',
    'قوة منزلة- خارج الصرف': 'قوة منزلة - خارج الصرف',
    'عاملين': 'القوة الأساسي - أفراد',
}

# ── حالة النفقات ──
EXPENSE_MAP = {
    'لديه نفقات': 'has_expenses',
    'نفقات': 'expenses',
    'بدون نفقات': 'no_expenses',
}


class Command(BaseCommand):
    help = 'استيراد البيانات من ملف Excel مع دعم المتغيرات الديناميكية والهيكل الهرمي'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str)
        parser.add_argument('--dry-run', action='store_true')
        parser.add_argument('--sheet', type=str, default=None)

    def handle(self, *args, **options):
        file_path = options['file_path']
        dry_run = options['dry_run']
        sheet_name = options['sheet']

        self.stdout.write(f'📂 قراءة الملف: {file_path}')
        self._load_lookups()

        wb = openpyxl.load_workbook(file_path, data_only=True)
        ws = wb[sheet_name] if sheet_name else wb.active
        rows = list(ws.iter_rows(values_only=True))

        if not rows:
            self.stdout.write(self.style.ERROR('الملف فارغ!'))
            return

        headers = [str(h).strip() if h else '' for h in rows[0]]
        data_rows = rows[1:]
        batch_id = uuid.uuid4()

        # كشف أعمدة المتغيرات الديناميكية
        monthly_cols = [h for h in headers if h.startswith('متغير')]
        self.stdout.write(f'📊 الصفوف: {len(data_rows)} | الأعمدة: {len(headers)}')
        self.stdout.write(f'📅 أعمدة المتغيرات الشهرية ({len(monthly_cols)}): {monthly_cols}')
        self.stdout.write(f'🔑 Batch ID: {batch_id}')

        if dry_run:
            self.stdout.write(self.style.WARNING('🔄 DRY-RUN — لن يتم حفظ أي شيء'))

        stats = {
            'total': len(data_rows), 'created': 0, 'updated': 0,
            'skipped': 0, 'corrections': 0, 'monthly_vars': 0,
            'unmatched_dept': [], 'unknown_rank': [], 'unknown_status': [],
        }

        for row_idx, row in enumerate(data_rows):
            row_dict = dict(zip(headers, row))
            try:
                if not dry_run:
                    with transaction.atomic():
                        self._process_row(
                            row_idx + 2, row_dict, batch_id,
                            stats, monthly_cols, dry_run=False
                        )
                else:
                    self._process_row(
                        row_idx + 2, row_dict, batch_id,
                        stats, monthly_cols, dry_run=True
                    )
            except Exception as e:
                stats['skipped'] += 1
                self.stdout.write(self.style.ERROR(f'❌ صف {row_idx + 2}: {e}'))

        self._print_report(stats)

    # ══════════════════════════════════════════════
    def _load_lookups(self):
        """تحميل القواميس في الذاكرة مرة واحدة"""
        self.ranks = {r.name: r for r in Rank.objects.all()}
        self.statuses = {s.name: s for s in ServiceStatus.objects.all()}
        self.force_types = {f.name: f for f in ForceType.objects.all()}
        self.qualifications = {q.name: q for q in Qualification.objects.all()}
        self.categories = {c.name: c for c in JobCategory.objects.all()}
        self.job_titles = {j.name: j for j in JobTitle.objects.all()}
        self.positions = {p.name: p for p in Position.objects.all()}
        # الهيكل التنظيمي
        self.security_admins = {s.name: s for s in SecurityAdministration.objects.all()}
        self.central_depts = {d.name: d for d in CentralDepartment.objects.all()}
        self.branches = {b.name: b for b in Branch.objects.all()}
        self.district_police = {d.name: d for d in DistrictPolice.objects.all()}
        self.divisions = {d.name: d for d in Division.objects.all()}
        self.units = {u.name: u for u in Unit.objects.all()}

    def _clean(self, val):
        if val is None:
            return ''
        return str(val).strip()

    def _parse_date(self, val):
        if not val:
            return None
        if isinstance(val, datetime):
            return val.date()
        val = str(val).strip()
        for fmt in ('%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y', '%Y/%m/%d'):
            try:
                return datetime.strptime(val, fmt).date()
            except (ValueError, TypeError):
                continue
        return None

    def _resolve_rank(self, raw, stats, row_idx):
        if not raw:
            return None
        mapped = RANK_MAP.get(raw, raw)
        obj = self.ranks.get(mapped)
        if not obj:
            stats['unknown_rank'].append(f'صف {row_idx}: {raw}')
            obj = self.ranks.get('جندي')
        return obj

    def _resolve_status(self, row_dict, stats, row_idx):
        candidates = [
            self._clean(row_dict.get('نوع الحالة', '')),
            self._clean(row_dict.get('الحالة', '')),
            self._clean(row_dict.get('نوع العمل', '')),
        ]
        for c in candidates:
            if not c:
                continue
            mapped = STATUS_MAP.get(c, c)
            obj = self.statuses.get(mapped)
            if obj:
                return obj
        stats['unknown_status'].append(f'صف {row_idx}: {candidates}')
        return self.statuses.get('بدون عمل')

    def _soft_map_org(self, raw_val, lookup_dict):
        """
        Soft Mapping: مطابقة دقيقة أولاً، ثم جزئية.
        إذا لم يجد → يُعيد None (لا يُخمّن ولا يرمي في قسم وهمي).
        """
        if not raw_val:
            return None
        # مطابقة دقيقة
        obj = lookup_dict.get(raw_val)
        if obj:
            return obj
        # مطابقة جزئية
        for name, obj in lookup_dict.items():
            if raw_val in name or name in raw_val:
                return obj
        return None

    def _resolve_force_type(self, raw, mil_number):
        mapped = FORCE_TYPE_MAP.get(raw, raw)
        obj = self.force_types.get(mapped)
        if obj:
            return obj
        # استنتاج من الرقم العسكري
        if mil_number:
            p = str(mil_number)
            if p[:2] == '50':
                return self.force_types.get('لجان أمنية - أفراد')
            elif p[:2] == '60':
                return self.force_types.get('القوة الأساسي - ضباط')
            elif p[:1] == '7':
                return self.force_types.get('القوة الأساسي - أفراد')
        return None

    def _process_row(self, row_idx, row_dict, batch_id, stats,
                     monthly_cols, dry_run=False):
        """معالجة صف واحد من الإكسل"""

        # 1. حفظ النسخة الخام
        raw_data = {k: str(v) if v is not None else '' for k, v in row_dict.items()}
        if not dry_run:
            RawDataImport.objects.create(
                row_index=row_idx,
                raw_data=raw_data,
                import_batch_id=batch_id,
                status='processed',
            )

        # 2. الرقم العسكري
        mil_correct = self._clean(row_dict.get('الرقم العسكري الصحيح', ''))
        mil_normal = self._clean(row_dict.get('الرقم العسكري', ''))
        mil_old = self._clean(row_dict.get('الرقم العسكري القديم', ''))
        military_number = mil_correct or mil_normal

        if not military_number:
            stats['skipped'] += 1
            self.stdout.write(self.style.WARNING(f'⚠️ صف {row_idx}: لا يوجد رقم عسكري'))
            return

        # 3. الاسم
        full_name = self._clean(row_dict.get('الاسم', '') or row_dict.get('الأسم', ''))
        if not full_name:
            stats['skipped'] += 1
            return

        # 4. بقية الحقول الأساسية
        national_id = self._clean(row_dict.get('الرقم الوطني', '')) or None
        rank = self._resolve_rank(self._clean(row_dict.get('الرتبة', '')), stats, row_idx)
        status = self._resolve_status(row_dict, stats, row_idx)
        raw_force = self._clean(row_dict.get('تصنيف القوة', ''))
        force_type = self._resolve_force_type(raw_force, military_number)
        qualification = self.qualifications.get(self._clean(row_dict.get('المؤهل', '')))
        category = self.categories.get(self._clean(row_dict.get('الفئة', '')))
        job_title = self.job_titles.get(self._clean(row_dict.get('نوع العمل', '')))
        position = self.positions.get(self._clean(row_dict.get('المنصب', '')))

        # 5. الهيكل التنظيمي (Soft Mapping)
        # "الوحدة" في الإكسل = إدارة أمن المحافظة
        raw_sa = self._clean(row_dict.get('الوحدة', ''))
        security_admin = self._soft_map_org(raw_sa, self.security_admins)

        # "الإدارة_السرية" = إدارة مركزية
        raw_dept = self._clean(row_dict.get('الإدارة_السرية', ''))
        central_dept = self._soft_map_org(raw_dept, self.central_depts)

        # "القسم_فرع السرية" = فرع / شرطة مديرية / قسم
        raw_div = self._clean(row_dict.get('القسم_فرع السرية', ''))
        branch = self._soft_map_org(raw_div, self.branches)
        district_p = None if branch else self._soft_map_org(raw_div, self.district_police)
        division = None if (branch or district_p) else self._soft_map_org(raw_div, self.divisions)

        # جمع القيم التي لم تُطابَق → في حقل notes لمراجعة يدوية
        unmatched_notes_parts = []
        if raw_sa and not security_admin:
            unmatched_notes_parts.append(f'[RAW_UNIT]: {raw_sa}')
            stats['unmatched_dept'].append(f'صف {row_idx} (الوحدة): {raw_sa}')
        if raw_dept and not central_dept:
            unmatched_notes_parts.append(f'[RAW_DEPT]: {raw_dept}')
            stats['unmatched_dept'].append(f'صف {row_idx} (الإدارة): {raw_dept}')
        if raw_div and not (branch or district_p or division):
            unmatched_notes_parts.append(f'[RAW_DIV]: {raw_div}')
            stats['unmatched_dept'].append(f'صف {row_idx} (القسم): {raw_div}')

        # 6. التواريخ والحقول الإضافية
        birth_date = self._parse_date(row_dict.get('تاريخ الميلاد'))
        join_date = self._parse_date(row_dict.get('تاريخ الألتحاق'))
        decision_date = self._parse_date(row_dict.get('تاريخ صدور القرار'))
        transfer_date = self._parse_date(row_dict.get('تاريخ التصدور الينا'))

        raw_expense = self._clean(row_dict.get('حالة النفقات', ''))
        expense_val = None
        for k, v in EXPENSE_MAP.items():
            if k in raw_expense:
                expense_val = v
                break

        notes_base = self._clean(row_dict.get('الملاحظات', ''))
        notes = '\n'.join(filter(None, [notes_base] + unmatched_notes_parts))

        appointment_info = self._clean(row_dict.get('التعيينات', '')) or None

        if dry_run:
            stats['created'] += 1
            return

        # 7. إنشاء / تحديث PersonnelMaster
        person, created = PersonnelMaster.objects.update_or_create(
            military_number=military_number,
            defaults={
                'full_name': full_name,
                'national_id': national_id,
                'old_military_number': mil_old or (
                    mil_normal if (mil_correct and mil_correct != mil_normal) else None
                ),
                'current_rank': rank,
                'current_status': status,
                'force_classification': force_type,
                'qualification': qualification,
                'category': category,
                'job_title': job_title,
                'position': position,
                'security_admin': security_admin,
                'central_department': central_dept,
                'branch': branch,
                'district_police': district_p,
                'division': division,
                'birth_date': birth_date,
                'join_date': join_date,
                'decision_date': decision_date,
                'transfer_date': transfer_date,
                'phone_number': self._clean(row_dict.get('رقم التليفون', '')) or None,
                'expense_status': expense_val,
                'appointment_info': appointment_info,
                'notes': notes,
                'is_data_clean': False,
                'data_quality_score': 0,
            }
        )

        if created:
            stats['created'] += 1
        else:
            stats['updated'] += 1

        # 8. تصحيح الاسم → SuggestedCorrection فقط (لا corrected_name)
        name_correction = self._clean(
            row_dict.get('تصحيح الاسم من واقع البطاقة', '')
        )
        if name_correction and name_correction != full_name:
            # تجنب تكرار الطلب
            already_pending = SuggestedCorrection.objects.filter(
                personnel=person,
                correction_type='name_correction',
                status='pending',
            ).exists()
            if not already_pending:
                SuggestedCorrection.objects.create(
                    personnel=person,
                    security_admin=person.security_admin,
                    correction_type='name_correction',
                    field_name='full_name',
                    old_value=full_name,
                    new_value=name_correction,
                    status='pending',
                    requested_at=timezone.now(),
                )
                stats['corrections'] += 1

        # 9. المتغيرات الشهرية — ديناميكية بالكامل
        for col_name in monthly_cols:
            val = self._clean(row_dict.get(col_name, ''))
            if val:
                HistoricalMonthlyVariables.objects.create(
                    personnel=person,
                    month=col_name,          # اسم العمود كاملاً = مرجع الشهر
                    variable_value=val,
                    source_column=col_name,
                )
                stats['monthly_vars'] += 1

    def _print_report(self, stats):
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write(self.style.SUCCESS('📋 تقرير الاستيراد'))
        self.stdout.write('=' * 60)
        self.stdout.write(f'  إجمالي الصفوف  : {stats["total"]}')
        self.stdout.write(self.style.SUCCESS(f'  ✅ تم إنشاء     : {stats["created"]}'))
        self.stdout.write(f'  🔄 تم تحديث    : {stats["updated"]}')
        self.stdout.write(f'  ❌ تم تخطي     : {stats["skipped"]}')
        self.stdout.write(f'  📝 طلبات تصحيح : {stats["corrections"]}')
        self.stdout.write(f'  📅 متغيرات شهرية: {stats["monthly_vars"]}')

        if stats['unmatched_dept']:
            self.stdout.write(self.style.WARNING(
                f'\n  ⚠️ إدارات/أقسام لم تُطابَق ({len(stats["unmatched_dept"])})'
                ' — محفوظة في حقل notes للمراجعة اليدوية:'
            ))
            for d in stats['unmatched_dept'][:15]:
                self.stdout.write(f'     {d}')

        if stats['unknown_rank']:
            self.stdout.write(self.style.WARNING(
                f'\n  ⚠️ رتب غير معروفة: {len(stats["unknown_rank"])}'
            ))
            for r in stats['unknown_rank'][:10]:
                self.stdout.write(f'     {r}')

        if stats['unknown_status']:
            self.stdout.write(self.style.WARNING(
                f'\n  ⚠️ حالات غير معروفة: {len(stats["unknown_status"])}'
            ))
            for s in stats['unknown_status'][:10]:
                self.stdout.write(f'     {s}')

        self.stdout.write('=' * 60)
