"""
أمر إدارة لإدخال جميع بيانات القواميس من الدليل الإرشادي
=====================================================
يُنشئ أو يحدّث:
  - 19 رتبة عسكرية
  - 26+ حالة خدمية
  - 5 فئات وظيفية و 117+ مسمى وظيفي
  - 8 مؤهلات دراسية
  - 15+ منصب إداري
  - 1 محافظة (المحافظة الأولى) + 33 إدارة عامة (Directorate)
"""

from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):
    help = 'إدخال جميع بيانات القواميس من الدليل الإرشادي لضبط الخدمات (تحديث آمن)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset', action='store_true', default=False,
            help='تحديث البيانات (مجرد تعبير متوافق)'
        )

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('\n🚀 بدء إدخال بيانات القواميس الكاملة بطريقة التحديث الآمن...\n'))

        count_ranks = self._seed_ranks()
        count_statuses = self._seed_service_statuses()
        count_quals = self._seed_qualifications()
        count_cats, count_titles = self._seed_job_categories_and_titles()
        count_positions = self._seed_positions()
        count_gov, count_dirs = self._seed_governorate_and_directorates()
        count_rules = self._seed_transition_rules()

        self.stdout.write(self.style.SUCCESS(f'\n{"="*60}'))
        self.stdout.write(self.style.SUCCESS(f'✅ تم إدخال/تحديث جميع البيانات بنجاح!'))
        self.stdout.write(self.style.SUCCESS(f'{"="*60}'))
        self.stdout.write(f'  📊 الرتب: {count_ranks}')
        self.stdout.write(f'  📊 الحالات الخدمية: {count_statuses}')
        self.stdout.write(f'  📊 المؤهلات الدراسية: {count_quals}')
        self.stdout.write(f'  📊 الفئات الوظيفية: {count_cats}')
        self.stdout.write(f'  📊 المسميات الوظيفية: {count_titles}')
        self.stdout.write(f'  📊 المناصب: {count_positions}')
        self.stdout.write(f'  📊 المحافظات: {count_gov}')
        self.stdout.write(f'  📊 الإدارات العامة: {count_dirs}')
        self.stdout.write(f'  📊 قواعد انتقال الحالات: {count_rules}')
        self.stdout.write(self.style.SUCCESS(f'{"="*60}\n'))

    def _seed_ranks(self):
        from core.models import Rank
        ranks_data = [
            ('لواء', 1, True), ('عميد', 2, True), ('عقيد', 3, True),
            ('مقدم', 4, True), ('رائد', 5, True), ('نقيب', 6, True),
            ('ملازم أول', 7, True), ('ملازم ثاني', 8, True), ('مساعد 1', 9, False),
            ('مساعد 2', 10, False), ('مساعد', 11, False), ('رقيب 1', 12, False),
            ('رقيب 2', 13, False), ('عريف', 14, False), ('جندي', 15, False),
            ('حارس', 16, False), ('مدني', 17, False), ('متعاقد', 18, False),
            ('مجند', 19, False),
        ]
        count = 0
        for name, order, is_officer in ranks_data:
            from django.db.utils import IntegrityError
            try:
                _, created = Rank.objects.update_or_create(
                    name=name, defaults={'order': order, 'is_officer': is_officer}
                )
                if created: count += 1
            except IntegrityError:
                pass
        return Rank.objects.count()

    def _seed_service_statuses(self):
        from core.models import ServiceStatus
        statuses_data = [
            # قوة عاملة فعلية
            ('تعمل في الميدان', 'active_full', True, False, False),
            
            # قوة عاملة غير فعلية
            ('قوة احتياطية', 'active_part', True, False, False),
            ('بدون عمل', 'active_part', True, False, False),
            
            # قوة غير عاملة مؤقتاً
            ('المفرغين للمرافقة', 'inactive_temp', True, True, False),
            ('المنتدبين لدى جهات', 'inactive_temp', True, True, False),
            ('المفرغين للدراسة', 'inactive_temp', True, True, False),
            ('المفرغين في الجبهات', 'inactive_temp', True, True, False),
            ('الأمراض والمصابين', 'inactive_temp', True, True, False),
            ('المفقودين', 'inactive_temp', True, True, False),
            ('الجرحى', 'inactive_temp', True, True, False),
            ('الأسرى', 'inactive_temp', True, True, False),
            ('السجناء', 'inactive_temp', False, True, False),
            ('الإجازات', 'inactive_temp', True, False, False),
            ('غياب', 'inactive_temp', False, False, False),
            
            # قوة غير عاملة نهائياً
            ('الشهداء', 'inactive_perm', False, True, True),
            ('الوفيات', 'inactive_perm', False, True, True),
            ('إنهاء المدة القانونية', 'inactive_perm', False, True, True),
            ('بلوغ السن القانوني', 'inactive_perm', False, True, True),
            ('عدم لياقة', 'inactive_perm', False, True, True),
            ('المفقودين (بصك شرعي)', 'inactive_perm', False, True, True),
            ('المتقاعدين', 'inactive_perm', False, True, True),
            ('المصدرين إلى الوزارة', 'inactive_perm', False, True, True),
            ('الغياب المستمر', 'inactive_perm', False, True, True),
            ('المنقطعين - فرار', 'inactive_perm', False, True, True),
            ('الملتحقين بالعدوان', 'inactive_perm', False, True, True),
        ]
        count = 0
        for name, classification, salary, doc, perm in statuses_data:
            _, created = ServiceStatus.objects.update_or_create(
                name=name, defaults={'classification': classification, 'receives_salary': salary, 'requires_document': doc, 'is_permanent_deactivation': perm}
            )
            if created: count += 1
        return ServiceStatus.objects.count()

    def _seed_qualifications(self):
        from core.models import Qualification
        quals_data = [('دكتوراه', 1), ('ماجستير', 2), ('جامعي', 3), ('دبلوم', 4), ('ثانوي', 5), ('إعدادي', 6), ('ابتدائي', 7), ('يقرأ ويكتب', 8), ('أمي', 9)]
        count = 0
        for name, order in quals_data:
            _, created = Qualification.objects.update_or_create(order=order, defaults={'name': name})
            if created: count += 1
        return Qualification.objects.count()

    def _seed_job_categories_and_titles(self):
        from core.models import JobCategory, JobTitle
        categories_data = {
            'إداري': [
                'إداري', 'كاتب', 'مؤرشف', 'أمين صندوق', 'خطاط', 'مغلف', 'مراسل', 'تسجيل جنائي', 'محاسب', 'مراجع', 
                'جامع بيانات شخصية', 'قيم جامع', 'موثق', 'مستلم بلاغات', 'معلم', 'مرشد توعوي', 'صحفي', 'مذيع', 
                'رئيس وحدة', 'إحصاء بيانات', 'مترجم', 'مدير مكتب', 'سكرتير', 'علاقات', 'جامع بيانات لاستخراج جواز', 'مندوب متابعات',
                # مناصب القيادة الإدارية
                'وزير', 'نائب وزير', 'مستشار', 'وكيل قطاع', 'مدير عام', 'مدير مصلحة', 'مدير إدارة', 'نائب مدير إدارة',
                'رئيس قسم', 'مسؤول شعبة', 'ضابط ارتباط', 'مساعد رئيس قسم'
            ],
            'ميداني': [
                'ميداني', 'حراسة', 'مفتش', 'محقق', 'مكافحة إرهاب', 'تحريات', 'مرافق', 'خدمة أمنية', 'ميداني مرور', 
                'فض شغب', 'رياضي', 'خيال', 'سجان', 'نجدة وإنقاذ', 'مدرب', 'مكافحة تهريب', 'حرس حدود', 'ش/راجلة', 
                'ش/محمولة', 'ش/تخدير', 'حارس ليل', 'حماية بيئة', 'ش/سياحة', 'ش/قضائية', 'ش/منطقة حرة', 'مهام أمنية', 'مشاة',
                # مناصب القيادة الميدانية
                'قائد فرع', 'قائد كتيبة', 'أركان حرب كتيبة', 'قائد سرية', 'قائد فصيلة', 'قائد نقطة'
            ],
            'فني': ['فني', 'فني كمبيوتر', 'فني طباعة', 'فني تصوير', 'فني إطفاء', 'فني اتصالات', 'فني عمليات', 'فني مرور', 'فني مسرح جريمة', 'فني مختبرات', 'فني تمريض', 'فني مخدرات', 'فني أسلحة', 'فني متفجرات', 'فني كهرباء', 'فني موسيقى', 'فني أدلة', 'أمين مستودع', 'فني تخدير', 'فني أشعة', 'تحويلة'],
            'تخصصي': ['متخصص', 'طبيب', 'مهندس معماري', 'مختبرات طبية', 'أدلة ومختبرات جنائية', 'محامي قانوني', 'محاسب', 'أخصائي اجتماعي', 'مدرس', 'صيدلي'],
            'حرفي': ['حرفي', 'طباخ', 'وراد ماء', 'خباز', 'عجان', 'ميكانيكي سيارات', 'جزار', 'ملحم', 'نجار', 'سائق', 'عامل وقود', 'مباشر', 'منظف', 'مرنج', 'سمكري', 'خراز', 'فراش', 'غسال', 'مكوجي', 'منقي بقوليات', 'مزارع', 'سائس خيل', 'كهربائي', 'مشحم', 'حداد', 'طحان', 'خراط', 'بناء', 'مسروس', 'سباك', 'حلاق', 'خضري']
        }
        for cat_name, titles in categories_data.items():
            category, _ = JobCategory.objects.get_or_create(name=cat_name)
            for title_name in titles:
                JobTitle.objects.update_or_create(name=title_name, defaults={'category': category})
        return JobCategory.objects.count(), JobTitle.objects.count()

    def _seed_positions(self):
        from core.models import Position
        positions_data = [
            # مناصب إدارية فقط
            ('الوزير', 1, ['إداري']),
            ('نائب الوزير', 2, ['إداري']),
            ('المستشار', 2, ['إداري']),
            ('وكيل القطاع', 3, ['إداري']),
            ('مدير العام', 4, ['إداري']),
            ('مدير المصلحة', 5, ['إداري']),
            ('مدير المكتب', 5, ['إداري']),
            ('مدير الإدارة', 6, ['إداري']),
            ('نائب مدير الإدارة', 7, ['إداري']),
            ('رئيس القسم', 8, ['إداري']),
            ('مساعد رئيس القسم', 10, ['إداري']),
            ('رئيس الوحدة', 9, ['إداري']),
            ('مسؤول الشعبة', 9, ['إداري']),
            ('ضابط الارتباط', 9, ['إداري']),
            
            # مناصب القيادة الميدانية (مسموحة للميدانيين فقط)
            ('قائد الفرع', 5, ['ميداني']),
            ('قائد الكتيبة', 6, ['ميداني']),
            ('أركان حرب الكتيبة', 7, ['ميداني']),
            ('قائد السرية', 8, ['ميداني']),
            ('قائد الفصيلة', 9, ['ميداني']),
            ('قائد النقطة', 10, ['ميداني']),
        ]
        for name, level, allowed_categories in positions_data:
            Position.objects.update_or_create(
                name=name, 
                defaults={
                    'level': level,
                    'allowed_categories': allowed_categories
                }
            )
        return Position.objects.count()

    def _seed_governorate_and_directorates(self):
        """
        ينشئ الهيكل الأمني الافتراضي لالمحافظة الأولى.
        البيانات الجغرافية يتم تحميلها من seed_geography.
        """
        from core.models import (
            GeoGovernorate, SecurityAdministration,
            CentralDepartment, Branch,
        )

        # تأكد من وجود المحافظة الجغرافية (تُنشأ بواسطة seed_geography)
        geo_gov, _ = GeoGovernorate.objects.get_or_create(
            name_ar='المحافظة الأولى',
            defaults={
                'name_en': 'Marib',
                'capital_name_ar': 'المحافظة الأولى',
            }
        )

        # إدارة أمن المحافظة
        sec_admin, _ = SecurityAdministration.objects.update_or_create(
            geo_governorate=geo_gov,
            defaults={
                'name': 'إدارة أمن المحافظة الأولى',
                'code': 'SA-MAR',
                'is_active': True,
            }
        )

        # الإدارات المركزية
        central_depts = [
            ('مكتب المدير العام', 'CD-01', 1),
            ('مكتب نائب المدير العام', 'CD-02', 2),
            ('مكتب المساعدين', 'CD-03', 3),
            ('أمن الوحدة', 'CD-04', 4),
            ('إدارة الموارد', 'CD-05', 5),
            ('إدارة الشؤون المالية', 'CD-06', 6),
            ('إدارة الأمن الوقائي', 'CD-07', 7),
            ('إدارة المشاريع', 'CD-08', 8),
            ('إدارة القيادة والسيطرة', 'CD-09', 9),
            ('إدارة الاتصالات', 'CD-10', 10),
            ('إدارة التدريب والتوجيه', 'CD-11', 11),
            ('إدارة الإمداد والتموين', 'CD-12', 12),
            ('إدارة المطارات والمنافذ', 'CD-19', 13),
            ('إدارة البحث الجنائي', 'CD-20', 14),
            ('إدارة الأدلة الجنائية', 'CD-21', 15),
            ('إدارة مباحث الأموال', 'CD-22', 16),
            ('إدارة المرور', 'CD-25', 17),
            ('إدارة مكافحة المخدرات', 'CD-26', 18),
            ('إدارة مكافحة الإرهاب', 'CD-27', 19),
            ('التدخل السريع', 'CD-28', 20),
            ('إدارة المنشآت وحماية الشخصيات', 'CD-29', 21),
            ('الكادر الصحي', 'CD-30', 22),
            ('إدارة الأمن والنظام', 'CD-31', 23),
            ('قوة غير عاملة', 'CD-NW', 24),
            ('التنزيلات', 'CD-TD', 25),
        ]
        for name, code, order in central_depts:
            CentralDepartment.objects.update_or_create(
                security_admin=sec_admin, code=code,
                defaults={'name': name, 'is_active': True, 'order': order}
            )

        # الفروع
        branches_data = [
            ('فرع جهاز المفتش', 'BR-13', 1),
            ('فرع الأحوال المدنية', 'BR-14', 2),
            ('فرع الهجرة والجوازات', 'BR-15', 3),
            ('فرع الإصلاح والتأهيل', 'BR-16', 4),
            ('فرع الدفاع المدني', 'BR-17', 5),
            ('فرع خفر السواحل', 'BR-18', 6),
            ('فرع القوات الخاصة', 'BR-23', 7),
            ('فرع النجدة', 'BR-24', 8),
        ]
        for name, code, order in branches_data:
            Branch.objects.update_or_create(
                security_admin=sec_admin, code=code,
                defaults={'name': name, 'is_active': True, 'order': order}
            )

        return SecurityAdministration.objects.count(), CentralDepartment.objects.count() + Branch.objects.count()

    def _seed_transition_rules(self):
        from core.models import ServiceStatus, StateTransitionRule
        
        # جلب الحالات الأساسية
        # جلب الحالات الأساسية
        statuses_to_fetch = {
            'active_full': 'تعمل في الميدان',
            'martyrs': 'الشهداء',
            'deceased': 'الوفيات',
            'missing': 'المفقودين',
            'retired': 'المتقاعدين',
            'study_leave': 'المفرغين للدراسة',
            'sick_leave': 'الجرحى',
            'prison': 'السجناء',
            'escort': 'المفرغين للمرافقة',
            'seconded': 'المنتدبين لدى جهات',
            'end_of_service': 'إنهاء المدة القانونية',
            'medical_unfit': 'عدم لياقة'
        }
        
        fetched_statuses = {}
        for key, name in statuses_to_fetch.items():
            try:
                fetched_statuses[key] = ServiceStatus.objects.get(name=name)
            except ServiceStatus.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"الخطأ: لم يتم العثور على الحالة: {name}"))
                return 0
                
        active_full = fetched_statuses['active_full']
        martyrs = fetched_statuses['martyrs']
        deceased = fetched_statuses['deceased']
        missing = fetched_statuses['missing']
        retired = fetched_statuses['retired']
        study_leave = fetched_statuses['study_leave']
        sick_leave = fetched_statuses['sick_leave']
        prison = fetched_statuses['prison']
        escort = fetched_statuses['escort']
        seconded = fetched_statuses['seconded']
        end_of_service = fetched_statuses['end_of_service']
        medical_unfit = fetched_statuses['medical_unfit']

        # تفصيل المرفقات الدقيقة من الدليل الإرشادي (صفحة 34 وما بعدها)
        rules_data = [
            # (من حالة، إلى حالة، يتطلب مستند، تفويض مزدوج، قائمة المستندات)
            
            # 1. الشهداء
            (active_full, martyrs, True, True, [
                'death_cert', 'inheritance_ruling', 'legal_power_of_attorney', 
                'national_id_front', 'agent_id_copy', 'installation_ruling', 
                'incident_report', 'assignment_order'
            ]),
            
            # 2. الوفيات
            (active_full, deceased, True, True, [
                'death_cert', 'inheritance_ruling', 'legal_power_of_attorney', 
                'national_id_front', 'agent_id_copy'
            ]),
            
            # 3. المفقودين
            (active_full, missing, True, True, [
                'missing_report', 'inheritance_ruling', 'legal_power_of_attorney', 
                'national_id_front', 'agent_id_copy', 'newspaper_announcement', 
                'court_ruling_missing'
            ]),
            
            # 4. الجرحى / عدم اللياقة الصحية
            (active_full, sick_leave, True, False, [
                'medical_report', 'national_id_front', 'patient_photo', 
                'legal_power_of_attorney', 'agent_id_copy'
            ]),
            (active_full, medical_unfit, True, True, [
                'medical_report', 'national_id_front', 'patient_photo', 
                'legal_power_of_attorney', 'agent_id_copy'
            ]),
            
            # 5. إنهاء المدة القانونية
            (active_full, end_of_service, True, True, [
                'personal_request', 'national_id_front'
            ]),
            
            # 6. المتقاعدين
            (active_full, retired, True, True, [
                'personal_request', 'national_id_front'
            ]),
            
            # 7. السجناء
            (active_full, prison, True, False, [
                'court_verdict', 'prison_memo', 'national_id_front', 
                'legal_power_of_attorney', 'agent_id_copy'
            ]),
            
            # 8. المفرغين للمرافقة
            (active_full, escort, True, False, [
                'assignment_order', 'national_id_front'
            ]),
            
            # 9. المفرغين للدراسة
            (active_full, study_leave, True, False, [
                'study_leave_order', 'national_id_front'
            ]),
            
            # 10. المنتدبين لدى جهات
            (active_full, seconded, True, False, [
                'secondment_order', 'national_id_front'
            ]),
        ]

        count = 0
        for from_status, to_status, req_doc, req_dual, docs in rules_data:
            _, created = StateTransitionRule.objects.update_or_create(
                from_status=from_status,
                to_status=to_status,
                defaults={
                    'requires_document': req_doc,
                    'requires_dual_auth': req_dual,
                    'required_document_types': docs,
                }
            )
            if created:
                count += 1
                
        return count

