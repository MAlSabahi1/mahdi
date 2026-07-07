from django.core.management.base import BaseCommand
from systems.services.models import ServiceCatalog

class Command(BaseCommand):
    help = 'Seeds the database with initial service catalog items matching m.md requirements'

    def handle(self, *args, **options):
        services = [
            # ═══════ تبويب 1: الاستمارات (forms) ═══════
            {'code': '03', 'name_ar': 'استمارة بلوغ السن القانوني', 'description': 'تُستخدم عند بلوغ الفرد السن القانوني للتقاعد حسب الدليل.', 'category': 'military', 'icon': 'LogOut', 'form_type': 'retirement_age', 'service_type': 'form', 'approval_type': 'internal'},
            {'code': '09', 'name_ar': 'استمارة إثبات حالة وفاة', 'description': 'معاملة عاجلة لتوثيق الوفاة الطبيعية أو نتيجة حادث.', 'category': 'military', 'icon': 'HeartHandshake', 'form_type': 'death', 'service_type': 'form', 'approval_type': 'internal'},
            {'code': '08', 'name_ar': 'استمارة إثبات حالة مفقود', 'description': 'إثبات فقدان الفرد وفقاً للوائح المعتمدة.', 'category': 'military', 'icon': 'AlertOctagon', 'form_type': 'missing', 'service_type': 'form', 'approval_type': 'internal'},
            {'code': '22', 'name_ar': 'استمارة محال للتقاعد', 'description': 'إحالة الفرد إلى التقاعد بناءً على طلبه أو وفقاً للقرارات المعتمدة.', 'category': 'military', 'icon': 'FileText', 'form_type': 'retired', 'service_type': 'form', 'approval_type': 'internal'},
            {'code': '16', 'name_ar': 'استمارة عدم لياقة صحية', 'description': 'إثبات عدم لياقة الفرد الصحية بناءً على التقارير الطبية.', 'category': 'military', 'icon': 'Activity', 'form_type': 'medical_unfit', 'service_type': 'form', 'approval_type': 'internal'},
            {'code': '05', 'name_ar': 'استمارة إنهاء مدة', 'description': 'إنهاء خدمة الأفراد المتعاقدين بعد انتهاء مدة تعاقدهم.', 'category': 'military', 'icon': 'MapPin', 'form_type': 'end_of_service', 'service_type': 'form', 'approval_type': 'internal'},
            {'code': '07', 'name_ar': 'استمارة مسجون', 'description': 'تغيير حالة الفرد عند صدور حكم قضائي أو قرار رسمي بالحبس.', 'category': 'disciplinary', 'icon': 'ShieldAlert', 'form_type': 'imprisoned', 'service_type': 'form', 'approval_type': 'internal'},
            {'code': '17', 'name_ar': 'استمارة مرافق / معيات', 'description': 'تفريغ الفرد لمرافقة مريض أو بعثة رسمية.', 'category': 'military', 'icon': 'ExternalLink', 'form_type': 'escort', 'service_type': 'form', 'approval_type': 'internal'},
            {'code': '11', 'name_ar': 'استمارة مفرغ للدراسة', 'description': 'إثبات تفريغ الفرد للدراسة في جهة تعليمية.', 'category': 'military', 'icon': 'GraduationCap', 'form_type': 'study_leave', 'service_type': 'form', 'approval_type': 'internal'},
            {'code': '18', 'name_ar': 'استمارة منتدب', 'description': 'توثيق انتداب الفرد للعمل لدى جهة أخرى.', 'category': 'military', 'icon': 'Reply', 'form_type': 'seconded', 'service_type': 'form', 'approval_type': 'internal'},
            {'code': '10', 'name_ar': 'استمارة شهيد', 'description': 'إثبات استشهاد الفرد وتحديث حالته في النظام.', 'category': 'military', 'icon': 'Binary', 'form_type': 'martyr', 'service_type': 'form', 'approval_type': 'internal'},

            # ═══════ تبويب 2: معاملات تصحيح البيانات الأساسية (corrections) ═══════
            {'code': 'C01', 'name_ar': 'طلب تصحيح الاسم', 'description': 'تصحيح اسم الفرد وفقاً للوثائق الرسمية. يتطلب رفع نموذج (23) الرسمي وصورة البطاقة الوطنية.', 'category': 'military', 'icon': 'FileText', 'form_type': 'name_correction', 'service_type': 'correction', 'approval_type': 'external', 'is_repeatable': False},
            {'code': 'C02', 'name_ar': 'طلب تصحيح الرقم الوطني', 'description': 'تعديل الرقم الوطني للفرد. يتطلب إرفاق صورة البطاقة الذكية أو الوطنية. تحقق فوري من عدم التكرار.', 'category': 'military', 'icon': 'Binary', 'form_type': 'national_id_correction', 'service_type': 'correction', 'approval_type': 'internal', 'is_repeatable': False},
            {'code': 'C03', 'name_ar': 'طلب تصحيح الرقم العسكري', 'description': 'تصحيح الرقم العسكري للفرد عند وجود خطأ في بياناته.', 'category': 'military', 'icon': 'ShieldCheck', 'form_type': 'military_number_correction', 'service_type': 'correction', 'approval_type': 'internal', 'is_repeatable': False},
            {'code': 'C04', 'name_ar': 'طلب التبديل المترابط للأرقام العسكرية', 'description': 'تصحيح تبديل الأرقام العسكرية بين شخصين بالخطأ. عملية ذرية واحدة.', 'category': 'military', 'icon': 'Users', 'form_type': 'linked_military_swap', 'service_type': 'correction', 'approval_type': 'external', 'is_repeatable': False},

            # ═══════ تبويب 3: الترقيات وتسويات الرتب (rank_settlement) ═══════
            {'code': 'R01', 'name_ar': 'طلب ترقية اعتيادية / استثنائية', 'description': 'ترقية الفرد إلى الرتبة العسكرية التالية. يدعم ترقية فرد واحد أو عدة أفراد.', 'category': 'military', 'icon': 'Award', 'form_type': 'rank_promotion', 'service_type': 'rank_settlement', 'approval_type': 'internal'},
            {'code': 'R02', 'name_ar': 'طلب تسوية من كادر الأفراد إلى كادر الضباط', 'description': 'تسوية وضع فرد حاصل على مؤهل جامعي وتحويله إلى كادر الضباط مع رقم عسكري جديد يبدأ بـ (60).', 'category': 'military', 'icon': 'TrendingUp', 'form_type': 'personnel_to_officer', 'service_type': 'rank_settlement', 'approval_type': 'internal'},
            {'code': 'R03', 'name_ar': 'طلب تنزيل الرتبة', 'description': 'تنزيل رتبة الفرد نتيجة عقوبة عسكرية أو إدارية أو حكم قضائي.', 'category': 'disciplinary', 'icon': 'ArrowDown', 'form_type': 'rank_demotion', 'service_type': 'rank_settlement', 'approval_type': 'internal'},

            # ═══════ تبويب 4: المزامنة والمطابقات والأمان (security) ═══════
            {'code': 'S01', 'name_ar': 'طلب تنزيل بيانات', 'description': 'طلب تصدير بيانات من النظام. التصدير ممنوع افتراضياً ويتطلب موافقة رسمية.', 'category': 'other', 'icon': 'Download', 'form_type': 'data_export_request', 'service_type': 'security', 'approval_type': 'internal'},
            {'code': 'S02', 'name_ar': 'طلب مطابقة بيانات', 'description': 'مطابقة البيانات بين مصادر مختلفة داخل النظام أو مع جهات خارجية.', 'category': 'other', 'icon': 'GitCompare', 'form_type': 'reconciliation_request', 'service_type': 'security', 'approval_type': 'internal'},
            {'code': 'S03', 'name_ar': 'طلب وصول لبيانات محظورة', 'description': 'طلب الوصول إلى بيانات حساسة أو عمليات مقيدة مع موافقات متعددة المراحل.', 'category': 'other', 'icon': 'Lock', 'form_type': 'security_access_request', 'service_type': 'security', 'approval_type': 'internal'},

            # ═══════ تبويب 5: الجزاءات والانضباط (disciplinary) ═══════
            {'code': 'D01', 'name_ar': 'طلب إنذار (شفهي / كتابي)', 'description': 'إجراء إداري يتم تسجيله في ملف الفرد دون تأثير مباشر على الراتب.', 'category': 'disciplinary', 'icon': 'AlertTriangle', 'form_type': 'warning', 'service_type': 'disciplinary', 'approval_type': 'internal'},
            {'code': 'D02', 'name_ar': 'طلب خصم من الراتب', 'description': 'إجراء مالي يتم تطبيقه ضمن مسير الرواتب الشهرية بعد الاعتماد.', 'category': 'disciplinary', 'icon': 'Percent', 'form_type': 'salary_deduction', 'service_type': 'disciplinary', 'approval_type': 'internal'},
            {'code': 'D03', 'name_ar': 'طلب إيقاف عن العمل وتوقيف النفقات', 'description': 'تغيير حالة الفرد إلى موقف مؤقتاً وإيقاف الراتب والنفقات تلقائياً.', 'category': 'disciplinary', 'icon': 'PauseCircle', 'form_type': 'suspension', 'service_type': 'disciplinary', 'approval_type': 'external'},
            {'code': 'D04', 'name_ar': 'طلب حبس عسكري', 'description': 'تحديد مدة الحبس وإرفاق القرار الرسمي.', 'category': 'disciplinary', 'icon': 'ShieldAlert', 'form_type': 'military_detention', 'service_type': 'disciplinary', 'approval_type': 'external'},
            {'code': 'D05', 'name_ar': 'طلب فصل من الخدمة', 'description': 'إجراء نهائي ينهي خدمة الفرد بشكل كامل بناءً على قرار معتمد.', 'category': 'disciplinary', 'icon': 'FileX', 'form_type': 'dismissal', 'service_type': 'disciplinary', 'approval_type': 'external'},
            {'code': 'D06', 'name_ar': 'بلاغ غياب / انقطاع', 'description': 'تسجيل بلاغ غياب بدون إذن أو انقطاع متواصل من الوحدة الميدانية.', 'category': 'disciplinary', 'icon': 'UserX', 'form_type': 'absence_report', 'service_type': 'disciplinary', 'approval_type': 'internal'},

            # ═══════ خدمات مالية وإدارية أخرى (تظهر في "الكل" فقط) ═══════
            {'code': '01', 'name_ar': 'طلب تسوية رتبة', 'description': 'معالجة تسويات الوضع وتعديل الرتبة المستحقة بناءً على قرارات تسوية الأوضاع.', 'category': 'military', 'icon': 'Award', 'form_type': None, 'service_type': 'other', 'approval_type': 'internal'},
            {'code': '02', 'name_ar': 'طلب علاوة رتبة جديدة', 'description': 'تفعيل وصرف علاوة الرتبة الجديدة المترتبة على قرارات الترقية.', 'category': 'financial', 'icon': 'TrendingUp', 'form_type': None, 'service_type': 'other', 'approval_type': 'internal'},
            {'code': '04', 'name_ar': 'طلب تجميد الراتب المؤقت', 'description': 'إيقاف المعالجة المالية للفرد لغيابه أو انقطاعه عن العمل.', 'category': 'financial', 'icon': 'PauseCircle', 'form_type': None, 'service_type': 'other', 'approval_type': 'internal'},
            {'code': '06', 'name_ar': 'إجراء جزائي مالي (عقوبة)', 'description': 'حسم مبالغ من البدلات أو الراتب لقاء مخالفات انضباطية.', 'category': 'financial', 'icon': 'Percent', 'form_type': None, 'service_type': 'other', 'approval_type': 'internal'},
            {'code': '12', 'name_ar': 'إقرار عودة من إجازة طويلة', 'description': 'إعادة تفعيل صرف الراتب وإعادة الإدراج في الكشوف بعد الانقطاع.', 'category': 'military', 'icon': 'CalendarCheck', 'form_type': None, 'service_type': 'other', 'approval_type': 'internal'},
            {'code': '13', 'name_ar': 'طلب ضم سنوات خدمة سابقة', 'description': 'احتساب سنوات الخدمة السابقة وتأثيرها على الأقدمية والراتب.', 'category': 'military', 'icon': 'History', 'form_type': None, 'service_type': 'other', 'approval_type': 'internal'},
            {'code': '14', 'name_ar': 'طلب ترقية استثنائية للشهداء', 'description': 'ترقية الفرد للرتبة التالية استثنائياً تقديراً للتضحيات.', 'category': 'military', 'icon': 'ShieldCheck', 'form_type': None, 'service_type': 'other', 'approval_type': 'external'},
            {'code': '24', 'name_ar': 'استمارة إعادة للخدمة', 'description': 'إعادة قيد الفرد المفصول أو المستقيل إلى سجلات القوة العاملة.', 'category': 'military', 'icon': 'UserPlus', 'form_type': 'returned_to_service', 'service_type': 'other', 'approval_type': 'external'},
        ]

        count = 0
        for s in services:
            obj, created = ServiceCatalog.objects.update_or_create(
                code=s['code'],
                defaults={
                    'name_ar': s['name_ar'],
                    'description': s['description'],
                    'category': s['category'],
                    'icon': s['icon'],
                    'form_type': s.get('form_type'),
                    'service_type': s.get('service_type', 'other'),
                    'approval_type': s.get('approval_type', 'internal'),
                    'is_active': True,
                    'requires_approval': True,
                    'is_repeatable': s.get('is_repeatable', True),
                }
            )
            if created:
                count += 1
                
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {count} new service catalogs. Total services: {ServiceCatalog.objects.count()}'))
