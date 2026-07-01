"""
بذر البيانات الجغرافية والتنظيمية
══════════════════════════════════════
يقرأ من:
  1. yemen-info.json    → الجغرافيا
  2. org_structure.json  → الإدارات والفروع المعيارية

الاستخدام:
  python manage.py seed_geography --clear
"""
import json
import os
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.conf import settings

from core.models import (
    GeoGovernorate, GeoDistrict, GeoSubDistrict, GeoVillage,
    SecurityAdministration, CentralDepartment, Branch, DistrictPolice,
)


class Command(BaseCommand):
    help = 'بذر البيانات الجغرافية والهيكل الأمني'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear', action='store_true',
            help='حذف البيانات القديمة قبل البذر',
        )
        parser.add_argument(
            '--json-path', type=str, default=None,
            help='مسار yemen-info.json',
        )
        parser.add_argument(
            '--skip-villages', action='store_true',
            help='تخطي القرى (41K+ سجل)',
        )

    def handle(self, *args, **options):
        # ── 1. تحميل الملفات ──
        json_path = self._find_file(options['json_path'], 'yemen-info.json')
        org_path = self._find_file(None, 'org_structure.json', extra_paths=[
            Path(settings.BASE_DIR) / 'core' / 'fixtures' / 'org_structure.json',
        ])

        with open(json_path, 'r', encoding='utf-8') as f:
            geo_data = json.load(f)
        with open(org_path, 'r', encoding='utf-8') as f:
            org_data = json.load(f)

        governorates = geo_data.get('governorates', [])
        departments = org_data.get('central_departments', [])
        branches = org_data.get('branches', [])

        if not governorates:
            raise CommandError('لا توجد بيانات محافظات.')

        self.stdout.write(f'📂 جغرافيا: {json_path}')
        self.stdout.write(f'📂 هيكل:    {org_path}')
        self.stdout.write(f'   {len(departments)} إدارة مركزية × {len(governorates)} محافظة')
        self.stdout.write(f'   {len(branches)} فرع × {len(governorates)} محافظة')

        # ── 2. حذف القديم ──
        if options['clear']:
            self.stdout.write(self.style.WARNING('🗑️  حذف البيانات القديمة...'))
            self._clear_all()

        # ── 3. بذر ──
        with transaction.atomic():
            stats = self._seed(governorates, departments, branches, options['skip_villages'])

        # ── 4. ملخص ──
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('✅ اكتمل البذر!'))
        self.stdout.write(self.style.SUCCESS('─' * 50))
        for label, key in [
            ('📍 محافظات',        'geo_govs'),
            ('📍 مديريات',        'geo_districts'),
            ('📍 عزل',            'geo_sub_districts'),
            ('📍 قرى',            'geo_villages'),
            ('🛡️ إدارات أمن',     'security_admins'),
            ('🛡️ إدارات مركزية',  'central_departments'),
            ('🛡️ فروع',           'branches'),
            ('🛡️ شرطة مديريات',   'district_police'),
        ]:
            self.stdout.write(f'  {label:20s} {stats[key]}')
        self.stdout.write(self.style.SUCCESS('─' * 50))

    # ══════════════════════════════════════════════════════
    # Helpers
    # ══════════════════════════════════════════════════════

    def _find_file(self, explicit_path, filename, extra_paths=None):
        """البحث عن ملف في المسارات المحتملة"""
        if explicit_path and os.path.exists(explicit_path):
            return explicit_path
        candidates = [
            Path(settings.BASE_DIR).parent / filename,
            Path(settings.BASE_DIR) / filename,
            Path('/app') / filename,
        ]
        if extra_paths:
            candidates = extra_paths + candidates
        for p in candidates:
            if p.exists():
                return str(p)
        raise CommandError(f'لم يتم العثور على {filename}')

    def _clear_all(self):
        dp = DistrictPolice.objects.all().delete()[0]
        br = Branch.objects.all().delete()[0]
        cd = CentralDepartment.objects.all().delete()[0]
        sa = SecurityAdministration.objects.all().delete()[0]
        v = GeoVillage.objects.all().delete()[0]
        sd = GeoSubDistrict.objects.all().delete()[0]
        d = GeoDistrict.objects.all().delete()[0]
        g = GeoGovernorate.objects.all().delete()[0]
        self.stdout.write(
            f'  حُذف: {g} محافظة, {d} مديرية, {sd} عزلة, {v} قرية, '
            f'{sa} إدارة أمن, {cd} إدارة, {br} فرع, {dp} شرطة مديرية'
        )

    def _seed(self, governorates, departments, branches, skip_villages):
        stats = dict.fromkeys([
            'geo_govs', 'geo_districts', 'geo_sub_districts', 'geo_villages',
            'security_admins', 'central_departments', 'branches', 'district_police',
        ], 0)

        total = len(governorates)
        for idx, gov in enumerate(governorates, 1):
            self.stdout.write(f'  [{idx}/{total}] 🏛️  {gov["name_ar"]}')

            # ── محافظة جغرافية ──
            geo_gov, created = GeoGovernorate.objects.update_or_create(
                name_ar=gov['name_ar'],
                defaults={
                    'name_en': gov.get('name_en', ''),
                    'name_ar_normalized': gov.get('name_ar_normalized', ''),
                    'name_en_normalized': gov.get('name_en_normalized', ''),
                    'phone_numbering_plan': gov.get('phone_numbering_plan', ''),
                    'capital_name_ar': gov.get('capital_name_ar', ''),
                    'capital_name_en': gov.get('capital_name_en', ''),
                }
            )
            if created:
                stats['geo_govs'] += 1

            # ── إدارة أمن المحافظة ──
            sa, sa_created = SecurityAdministration.objects.update_or_create(
                geo_governorate=geo_gov,
                defaults={
                    'name': f'إدارة أمن {gov["name_ar"]}',
                    'code': f'SA-{str(gov.get("id", idx)).zfill(2)}',
                }
            )
            if sa_created:
                stats['security_admins'] += 1

            # ── إدارات مركزية (من org_structure.json) ──
            for order, dept_name in enumerate(departments, 1):
                _, c = CentralDepartment.objects.get_or_create(
                    security_admin=sa, name=dept_name,
                    defaults={'order': order}
                )
                if c:
                    stats['central_departments'] += 1

            # ── فروع (من org_structure.json) ──
            for order, br_name in enumerate(branches, 1):
                _, c = Branch.objects.get_or_create(
                    security_admin=sa, name=br_name,
                    defaults={'order': order}
                )
                if c:
                    stats['branches'] += 1

            # ── مديريات + شرطة مديريات ──
            for d_data in gov.get('districts', []):
                geo_dist, d_created = GeoDistrict.objects.update_or_create(
                    governorate=geo_gov, name_ar=d_data['name_ar'],
                    defaults={
                        'name_en': d_data.get('name_en', ''),
                        'name_ar_normalized': d_data.get('name_ar_normalized', ''),
                        'name_en_normalized': d_data.get('name_en_normalized', ''),
                    }
                )
                if d_created:
                    stats['geo_districts'] += 1

                _, dp_created = DistrictPolice.objects.update_or_create(
                    security_admin=sa, geo_district=geo_dist,
                    defaults={'name': f'شرطة مديرية {d_data["name_ar"]}'}
                )
                if dp_created:
                    stats['district_police'] += 1

                # ── عزل ──
                for u in d_data.get('uzaal', []):
                    geo_sub, u_created = GeoSubDistrict.objects.update_or_create(
                        district=geo_dist, name_ar=u['name_ar'],
                        defaults={
                            'name_en': u.get('name_en', ''),
                            'name_ar_normalized': u.get('name_ar_normalized', ''),
                            'name_en_normalized': u.get('name_en_normalized', ''),
                        }
                    )
                    if u_created:
                        stats['geo_sub_districts'] += 1

                    # ── قرى ──
                    if not skip_villages:
                        existing = set(
                            GeoVillage.objects.filter(sub_district=geo_sub)
                            .values_list('name_ar', flat=True)
                        )
                        bulk = [
                            GeoVillage(
                                sub_district=geo_sub,
                                name_ar=v['name_ar'],
                                name_en=v.get('name_en', ''),
                                name_ar_normalized=v.get('name_ar_normalized', ''),
                                name_en_normalized=v.get('name_en_normalized', ''),
                            )
                            for v in u.get('villages', [])
                            if v['name_ar'] not in existing
                        ]
                        if bulk:
                            GeoVillage.objects.bulk_create(bulk, batch_size=500)
                            stats['geo_villages'] += len(bulk)

        return stats
