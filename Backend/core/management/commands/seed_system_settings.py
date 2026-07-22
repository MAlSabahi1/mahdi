"""
seed_system_settings.py
═══════════════════════════════════════
تلقيم جميع إعدادات النظام الحيوية — يعمل مرة واحدة أو لتحديث الإعدادات المفقودة.
لا يُعدّل القيم الحالية إذا كان الإعداد موجوداً (آمن للتشغيل المتكرر).
"""
from django.core.management.base import BaseCommand
from core.models.settings import SystemSetting


# ── إعدادات شاملة للنظام ════════════════════════════════════════════════════
SETTINGS = [
    # ═══════════════════════════════════════════════════════════════════════
    #  1. إعدادات التقاعد (retirement)
    # ═══════════════════════════════════════════════════════════════════════
    {
        'key': 'retirement_age_general',
        'category': 'retirement',
        'title': 'السن القانوني للتقاعد (العام)',
        'description': 'السن الذي يُعتبر عنده الفرد قد بلغ سن التقاعد. يُستخدم في المحرك الاستباقي وشاشة الإنذارات المبكرة.',
        'value_type': 'int',
        'value': '60',
    },
    {
        'key': 'retirement_age_officers',
        'category': 'retirement',
        'title': 'السن القانوني لتقاعد الضباط',
        'description': 'قد يختلف سن تقاعد الضباط عن الأفراد في بعض الأنظمة. اتركه مساوياً للعام إذا لم يكن هناك فرق.',
        'value_type': 'int',
        'value': '60',
    },
    {
        'key': 'min_service_years',
        'category': 'retirement',
        'title': 'الحد الأدنى لسنوات الخدمة للتقاعد',
        'description': 'عدد سنوات الخدمة التي بعد إكمالها يحق للفرد التقاعد بغض النظر عن عمره.',
        'value_type': 'int',
        'value': '35',
    },
    {
        'key': 'min_join_age',
        'category': 'retirement',
        'title': 'الحد الأدنى لسن الالتحاق',
        'description': 'أقل سن مسموح للالتحاق بالخدمة. يستخدمه النظام للتحقق من صحة البيانات.',
        'value_type': 'int',
        'value': '18',
    },
    {
        'key': 'max_service_extension_years',
        'category': 'retirement',
        'title': 'أقصى مدة لتمديد الخدمة (سنوات)',
        'description': 'الحد الأقصى لعدد سنوات التمديد بعد بلوغ سن التقاعد.',
        'value_type': 'int',
        'value': '5',
    },
    {
        'key': 'allow_service_extension',
        'category': 'retirement',
        'title': 'السماح بتمديد الخدمة',
        'description': 'هل يُسمح للأفراد بتمديد خدمتهم بعد بلوغ السن القانوني أو إكمال المدة؟',
        'value_type': 'bool',
        'value': 'True',
    },
    {
        'key': 'retirement_referral_auto',
        'category': 'retirement',
        'title': 'الإحالة التلقائية للتقاعد',
        'description': 'هل يقوم النظام بإحالة الأفراد تلقائياً عند بلوغ السن/المدة أم ينتظر إجراء يدوي؟',
        'value_type': 'bool',
        'value': 'False',
    },

    # ═══════════════════════════════════════════════════════════════════════
    #  2. إعدادات الترقيات (promotions)
    # ═══════════════════════════════════════════════════════════════════════
    {
        'key': 'promotion_min_years',
        'category': 'promotions',
        'title': 'سنوات البقاء الدنيا في الرتبة',
        'description': 'الحد الأدنى لسنوات البقاء في الرتبة الحالية قبل أن يكون الفرد مؤهلاً للترقية.',
        'value_type': 'int',
        'value': '4',
    },
    {
        'key': 'promotion_requires_clean_record',
        'category': 'promotions',
        'title': 'الترقية تتطلب سجلاً نظيفاً',
        'description': 'هل يشترط عدم وجود جزاءات أو إجراءات تأديبية سارية المفعول للترقية؟',
        'value_type': 'bool',
        'value': 'True',
    },
    {
        'key': 'promotion_requires_qualification',
        'category': 'promotions',
        'title': 'الترقية تتطلب مؤهلاً',
        'description': 'هل يشترط وجود مؤهل علمي مناسب للرتبة التالية؟',
        'value_type': 'bool',
        'value': 'False',
    },
    {
        'key': 'promotion_batch_enabled',
        'category': 'promotions',
        'title': 'تفعيل الترقيات الجماعية',
        'description': 'السماح بتنفيذ ترقيات دفعة واحدة لمجموعة أفراد.',
        'value_type': 'bool',
        'value': 'True',
    },
    {
        'key': 'promotion_auto_detect',
        'category': 'promotions',
        'title': 'الكشف التلقائي عن المستحقين',
        'description': 'هل يقوم المحرك الاستباقي بالبحث تلقائياً عن من استحقوا الترقية؟',
        'value_type': 'bool',
        'value': 'True',
    },

    # ═══════════════════════════════════════════════════════════════════════
    #  3. إعدادات الخدمات (services)
    # ═══════════════════════════════════════════════════════════════════════
    {
        'key': 'form_sla_days',
        'category': 'services',
        'title': 'المهلة القصوى لإنجاز الاستمارة (بالأيام)',
        'description': 'عدد الأيام المسموح بها لإنجاز استمارة إثبات حالة من تاريخ التقديم قبل أن تُعتبر متأخرة.',
        'value_type': 'int',
        'value': '7',
    },
    {
        'key': 'monthly_submission_deadline_day',
        'category': 'services',
        'title': 'يوم الموعد النهائي للرفع الشهري',
        'description': 'اليوم من كل شهر الذي يجب أن ترفع فيه الإدارات كشوفاتها الشهرية (مثلاً: 20 يعني يوم 20 من كل شهر).',
        'value_type': 'int',
        'value': '20',
    },
    {
        'key': 'max_attachment_size_mb',
        'category': 'services',
        'title': 'الحد الأقصى لحجم المرفق (ميجابايت)',
        'description': 'أقصى حجم مسموح به لملف مرفق واحد عند رفع المستندات.',
        'value_type': 'int',
        'value': '5',
    },
    {
        'key': 'allowed_attachment_formats',
        'category': 'services',
        'title': 'صيغ المرفقات المسموحة',
        'description': 'أنواع الملفات المسموح رفعها مفصولة بفواصل.',
        'value_type': 'str',
        'value': 'pdf,jpg,jpeg,png',
    },
    {
        'key': 'form_approval_workflow_enabled',
        'category': 'services',
        'title': 'تفعيل سلسلة الاعتماد',
        'description': 'هل تمر الاستمارات بدورة اعتماد متعددة المراحل أم يتم اعتمادها مباشرة؟',
        'value_type': 'bool',
        'value': 'True',
    },
    {
        'key': 'bulk_form_creation_enabled',
        'category': 'services',
        'title': 'السماح بإنشاء استمارات جماعية',
        'description': 'السماح بإنشاء استمارات لعدة أفراد دفعة واحدة (مثل إحالة 100 فرد للتقاعد).',
        'value_type': 'bool',
        'value': 'True',
    },
    {
        'key': 'overdue_form_alert_days',
        'category': 'services',
        'title': 'عدد أيام التنبيه قبل انتهاء المهلة',
        'description': 'قبل كم يوم من انتهاء مهلة الاستمارة يتم إرسال تنبيه بالتأخير؟',
        'value_type': 'int',
        'value': '2',
    },
    {
        'key': 'study_leave_max_years_diploma',
        'category': 'services',
        'title': 'التفرغ الدراسي (دبلوم) - أقصى مدة بالسنوات',
        'description': 'الحد الأقصى للتفرغ لدراسة الدبلوم أو الدورة التخصصية.',
        'value_type': 'int',
        'value': '2',
    },
    {
        'key': 'study_leave_max_years_bachelor',
        'category': 'services',
        'title': 'التفرغ الدراسي (بكالوريوس) - أقصى مدة',
        'description': 'الحد الأقصى لسنوات التفرغ لدراسة البكالوريوس.',
        'value_type': 'int',
        'value': '6',
    },
    {
        'key': 'study_leave_max_years_master',
        'category': 'services',
        'title': 'التفرغ الدراسي (ماجستير) - أقصى مدة',
        'description': 'الحد الأقصى لسنوات التفرغ لدراسة الماجستير.',
        'value_type': 'int',
        'value': '3',
    },
    {
        'key': 'study_leave_max_years_phd',
        'category': 'services',
        'title': 'التفرغ الدراسي (دكتوراه) - أقصى مدة',
        'description': 'الحد الأقصى لسنوات التفرغ لدراسة الدكتوراه.',
        'value_type': 'int',
        'value': '5',
    },
    {
        'key': 'study_leave_max_age_bachelor',
        'category': 'services',
        'title': 'أقصى عمر لطلب تفريغ بكالوريوس',
        'description': 'الحد الأقصى لعمر الفرد للموافقة على دراسة البكالوريوس.',
        'value_type': 'int',
        'value': '35',
    },
    {
        'key': 'study_leave_max_age_master',
        'category': 'services',
        'title': 'أقصى عمر لطلب تفريغ ماجستير',
        'description': 'الحد الأقصى لعمر الفرد للموافقة على دراسة الماجستير.',
        'value_type': 'int',
        'value': '40',
    },
    {
        'key': 'study_leave_max_age_phd',
        'category': 'services',
        'title': 'أقصى عمر لطلب تفريغ دكتوراه',
        'description': 'الحد الأقصى لعمر الفرد للموافقة على دراسة الدكتوراه.',
        'value_type': 'int',
        'value': '45',
    },

    # ═══════════════════════════════════════════════════════════════════════
    #  4. إعدادات الإجازات (holidays)
    # ═══════════════════════════════════════════════════════════════════════
    {
        'key': 'annual_leave_days',
        'category': 'holidays',
        'title': 'عدد أيام الإجازة السنوية',
        'description': 'الحد الأقصى لأيام الإجازة الاعتيادية السنوية للفرد.',
        'value_type': 'int',
        'value': '30',
    },
    {
        'key': 'sick_leave_days',
        'category': 'holidays',
        'title': 'عدد أيام الإجازة المرضية',
        'description': 'الحد الأقصى لأيام الإجازة المرضية المسموحة سنوياً.',
        'value_type': 'int',
        'value': '30',
    },
    {
        'key': 'emergency_leave_days',
        'category': 'holidays',
        'title': 'عدد أيام الإجازة الطارئة',
        'description': 'الحد الأقصى لأيام الإجازة الاضطرارية في السنة.',
        'value_type': 'int',
        'value': '7',
    },
    {
        'key': 'maternity_leave_days',
        'category': 'holidays',
        'title': 'عدد أيام إجازة الأمومة',
        'description': 'مدة إجازة الأمومة/الوضع بالأيام.',
        'value_type': 'int',
        'value': '90',
    },
    {
        'key': 'hajj_leave_days',
        'category': 'holidays',
        'title': 'عدد أيام إجازة الحج',
        'description': 'مدة إجازة الحج المسموحة (تُمنح مرة واحدة).',
        'value_type': 'int',
        'value': '21',
    },
    {
        'key': 'leave_carryover_enabled',
        'category': 'holidays',
        'title': 'ترحيل رصيد الإجازات',
        'description': 'هل يُسمح بترحيل رصيد الإجازات غير المستخدمة للسنة القادمة؟',
        'value_type': 'bool',
        'value': 'True',
    },
    {
        'key': 'max_leave_carryover_days',
        'category': 'holidays',
        'title': 'أقصى أيام ترحيل إجازة',
        'description': 'الحد الأقصى لعدد الأيام التي يمكن ترحيلها من السنة الحالية.',
        'value_type': 'int',
        'value': '15',
    },
    {
        'key': 'max_absence_days_before_penalty',
        'category': 'holidays',
        'title': 'أيام الغياب قبل الجزاء',
        'description': 'عدد أيام الغياب بدون إذن المسموحة قبل اتخاذ إجراء تأديبي.',
        'value_type': 'int',
        'value': '3',
    },

    # ═══════════════════════════════════════════════════════════════════════
    #  5. إعدادات عامة (system)
    # ═══════════════════════════════════════════════════════════════════════
    {
        'key': 'early_warning_months',
        'category': 'system',
        'title': 'فترة الإنذار المبكر (بالأشهر)',
        'description': 'عدد الأشهر المتبقية قبل التقاعد التي يبدأ عندها النظام بإرسال إنذارات مبكرة.',
        'value_type': 'int',
        'value': '6',
    },
    {
        'key': 'temp_status_warning_days',
        'category': 'system',
        'title': 'أيام التنبيه لانتهاء الحالة المؤقتة',
        'description': 'قبل كم يوم من انتهاء فترة الحالة المؤقتة (دراسة/سجن/انتداب/مرافقة) يتم إرسال تنبيه.',
        'value_type': 'int',
        'value': '30',
    },
    {
        'key': 'enable_proactive_engine',
        'category': 'system',
        'title': 'تفعيل المحرك الاستباقي',
        'description': 'تشغيل/إيقاف المحرك الاستباقي الذي يفحص البيانات ويُصدر التنبيهات تلقائياً.',
        'value_type': 'bool',
        'value': 'True',
    },
    {
        'key': 'notification_retention_days',
        'category': 'system',
        'title': 'مدة الاحتفاظ بالإشعارات (بالأيام)',
        'description': 'عدد الأيام التي يحتفظ بها النظام بالإشعارات المقروءة قبل حذفها تلقائياً.',
        'value_type': 'int',
        'value': '90',
    },
    {
        'key': 'default_page_size',
        'category': 'system',
        'title': 'عدد السجلات الافتراضي في الصفحة',
        'description': 'عدد العناصر المعروضة في كل صفحة في الجداول.',
        'value_type': 'int',
        'value': '50',
    },
    {
        'key': 'system_language',
        'category': 'system',
        'title': 'لغة النظام الافتراضية',
        'description': 'اللغة المبدئية لواجهة النظام (ar = عربي، en = إنجليزي).',
        'value_type': 'str',
        'value': 'ar',
    },
    {
        'key': 'print_header_org_name',
        'category': 'system',
        'title': 'اسم الجهة في رأس الطباعة',
        'description': 'اسم الجهة الذي يظهر في أعلى المطبوعات والتقارير الرسمية.',
        'value_type': 'str',
        'value': 'وزارة الداخلية — الإدارة العامة للشؤون المالية والإدارية',
    },
    {
        'key': 'print_footer_text',
        'category': 'system',
        'title': 'نص تذييل الطباعة',
        'description': 'النص الذي يظهر في أسفل كل صفحة مطبوعة.',
        'value_type': 'str',
        'value': 'سري — للاستخدام الداخلي فقط',
    },
    {
        'key': 'audit_log_enabled',
        'category': 'system',
        'title': 'تفعيل سجل التدقيق',
        'description': 'هل يقوم النظام بتسجيل جميع العمليات الحساسة في سجل التدقيق؟',
        'value_type': 'bool',
        'value': 'True',
    },
    {
        'key': 'session_timeout_minutes',
        'category': 'system',
        'title': 'مهلة انتهاء الجلسة (بالدقائق)',
        'description': 'عدد الدقائق التي ينتظرها النظام بعد عدم النشاط قبل تسجيل الخروج تلقائياً.',
        'value_type': 'int',
        'value': '60',
    },
]


class Command(BaseCommand):
    help = 'Seed all system settings. Safe to run multiple times — only adds missing settings.'

    def handle(self, *args, **options):
        created_count = 0
        skipped_count = 0

        for setting_data in SETTINGS:
            obj, created = SystemSetting.objects.get_or_create(
                key=setting_data['key'],
                defaults={
                    'category': setting_data['category'],
                    'title': setting_data['title'],
                    'description': setting_data.get('description', ''),
                    'value_type': setting_data['value_type'],
                    'value': setting_data['value'],
                }
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"  ✅ أُنشئ: [{setting_data['category']}] {setting_data['title']}"))
            else:
                skipped_count += 1

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(f"تم بنجاح! أُنشئ {created_count} إعداد جديد • تخطّي {skipped_count} إعداد (موجود مسبقاً)."))
        self.stdout.write(self.style.NOTICE(f"إجمالي الإعدادات في النظام: {SystemSetting.objects.count()}"))
