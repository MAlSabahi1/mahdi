from django.core.management.base import BaseCommand
from systems.services.models import ServiceCatalog

class Command(BaseCommand):
    help = 'Seeds the database with initial service catalog items'

    def handle(self, *args, **options):
        services = [
            {'code': '01', 'name_ar': 'طلب تسوية رتبة', 'description': 'معالجة تسويات الوضع وتعديل الرتبة المستحقة للأفراد والضباط بناءً على قرارات تسوية الأوضاع القيادية.', 'category': 'military', 'icon': 'Award', 'form_type': None},
            {'code': '02', 'name_ar': 'طلب علاوة رتبة جديدة', 'description': 'تفعيل وصرف علاوة الرتبة الجديدة المترتبة على قرارات الترقية أو تسوية الوضع المالي للمنتسب.', 'category': 'financial', 'icon': 'TrendingUp', 'form_type': None},
            {'code': '03', 'name_ar': 'استمارة بلوغ السن القانوني', 'description': 'تُستخدم عند بلوغ الفرد السن القانوني للتقاعد حسب الدليل.', 'category': 'military', 'icon': 'LogOut', 'form_type': 'retirement_age'},
            {'code': '04', 'name_ar': 'طلب تجميد الراتب المؤقت', 'description': 'إيقاف المعالجة المالية للفرد لغيابه أو انقطاعه عن العمل لرفع كشوف الرد والتنزيلات.', 'category': 'financial', 'icon': 'PauseCircle', 'form_type': None},
            {'code': '05', 'name_ar': 'استمارة إنهاء مدة', 'description': 'تُستخدم للمطالبة بإنهاء مدة الخدمة حسب قانون 20 سنة.', 'category': 'military', 'icon': 'MapPin', 'form_type': 'end_of_service'},
            {'code': '06', 'name_ar': 'إجراء جزائي مالي (عقوبة)', 'description': 'حسم مبالغ محددة من البدلات أو الراتب الأساسي لقاء مخالفات انضباطية موثقة ومعتمدة.', 'category': 'disciplinary', 'icon': 'Percent', 'form_type': None},
            {'code': '07', 'name_ar': 'طلب بدل سكن وإقامة نائية', 'description': 'صرف بدلات إضافية مخصصة للمناطق ذات الظروف الميدانية الصعبة والنائية بالمحافظات.', 'category': 'financial', 'icon': 'Home', 'form_type': None},
            {'code': '08', 'name_ar': 'استمارة إثبات حالة مفقود', 'description': 'إصدار أمر للمفقودين وتوثيقه.', 'category': 'disciplinary', 'icon': 'AlertOctagon', 'form_type': 'missing'},
            {'code': '09', 'name_ar': 'استمارة إثبات حالة وفاة', 'description': 'معاملة عاجلة لتوثيق الوفاة لورثة المنتسب المتوفى.', 'category': 'financial', 'icon': 'HeartHandshake', 'form_type': 'death'},
            {'code': '10', 'name_ar': 'استمارة شهيد', 'description': 'إثبات حالة شهيد حسب قرار معتمد.', 'category': 'financial', 'icon': 'Binary', 'form_type': 'martyr'},
            {'code': '11', 'name_ar': 'استمارة مفرغ للدراسة', 'description': 'تحديث حالة منتسب ليكون مفرغاً للدراسة وتعديل الراتب.', 'category': 'military', 'icon': 'GraduationCap', 'form_type': 'study_leave'},
            {'code': '12', 'name_ar': 'إقرار عودة من إجازة طويلة', 'description': 'إعادة تفعيل صرف الراتب وإعادة الإدراج في الكشوف الجارية بعد الانقطاع المعتمد.', 'category': 'military', 'icon': 'CalendarCheck', 'form_type': None},
            {'code': '13', 'name_ar': 'طلب ضم سنوات خدمة سابقة', 'description': 'احتساب سنوات الخدمة السابقة في قطاع الخدمة الأمنية وتأثيرها على الأقدمية والراتب.', 'category': 'military', 'icon': 'History', 'form_type': None},
            {'code': '14', 'name_ar': 'طلب ترقية استثنائية للشهداء', 'description': 'ترقية الفرد للرتبة التالية مباشرة استثنائياً تقديراً للتضحيات أثناء الواجب الرسمي.', 'category': 'military', 'icon': 'ShieldCheck', 'form_type': None},
            {'code': '15', 'name_ar': 'طلب صرف بدل طبيعة عمل', 'description': 'صرف بدل مالي تخصصي للوظائف الفنية والتقنية التي تتطلب مهارات تخصصية خاصة.', 'category': 'financial', 'icon': 'Briefcase', 'form_type': None},
            {'code': '16', 'name_ar': 'استمارة عدم لياقة صحية', 'description': 'اعتماد الإجازات المرضية الطويلة أو عدم اللياقة بناءً على تقارير اللجنة الطبية المختصة.', 'category': 'military', 'icon': 'Activity', 'form_type': 'medical_unfit'},
            {'code': '17', 'name_ar': 'استمارة مرافق / معيات', 'description': 'إثبات حالة المرافق أو المعيات.', 'category': 'military', 'icon': 'ExternalLink', 'form_type': 'escort'},
            {'code': '18', 'name_ar': 'استمارة منتدب', 'description': 'إنهاء أو إثبات انتداب الفرد لجهته الأصلية وتحديث موقعه.', 'category': 'military', 'icon': 'Reply', 'form_type': 'seconded'},
            {'code': '19', 'name_ar': 'طلب صرف بدل تمثال خارجي', 'description': 'مخصص مالي للضباط الموفدين في مهام رسمية أو دورات تدريبية خارج الدولة.', 'category': 'financial', 'icon': 'Globe', 'form_type': None},
            {'code': '20', 'name_ar': 'طلب تعديل البدلات العائلية', 'description': 'تحديث بيانات الحالة الاجتماعية والتابعين لاحتساب البدلات العائلية المقرة باللوائح.', 'category': 'financial', 'icon': 'Users', 'form_type': None},
            {'code': '21', 'name_ar': 'تسوية فروقات مالية بأثر رجعي', 'description': 'صرف مستحقات مالية متأخرة ناتجة عن تأخر تطبيق قرار ترقية أو تسوية بالمديرية.', 'category': 'financial', 'icon': 'Coins', 'form_type': None},
            {'code': '22', 'name_ar': 'استمارة محال للتقاعد', 'description': 'إصدار استمارة الإحالة للتقاعد.', 'category': 'military', 'icon': 'FileText', 'form_type': 'retired'},
            {'code': '23', 'name_ar': 'استمارة فصل تأديبي', 'description': 'إنهاء خدمة الفرد كإجراء تأديبي بسبب مخالفة جسيمة لضوابط وشروط العمل.', 'category': 'disciplinary', 'icon': 'FileX', 'form_type': 'dismissed'},
            {'code': '24', 'name_ar': 'استمارة إعادة للخدمة', 'description': 'إعادة قيد الفرد المفصول أو المستقيل إلى سجلات القوة العاملة الرسمية.', 'category': 'military', 'icon': 'UserPlus', 'form_type': 'returned_to_service'},
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
                    'form_type': s['form_type'],
                    'is_active': True,
                    'requires_approval': True
                }
            )
            if created:
                count += 1
                
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {count} new service catalogs. Total services: {ServiceCatalog.objects.count()}'))
