"""
═══════════════════════════════════════════════════════════════
سجل التقارير المركزي — Report Registry (25 نموذج)
═══════════════════════════════════════════════════════════════
كل نموذج من الـ 25 معرّف هنا بأعمدته الدقيقة حسب الدليل الإرشادي.

الاستخدام:
    from systems.services.registries import ReportRegistry
    schema = ReportRegistry.schema(4)
    all_models = ReportRegistry.available_models()
"""
from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class ReportColumn:
    """عمود واحد في تقرير"""
    key: str
    label: str
    source: str = ''  # مصدر البيانات: personnel.field أو form_data.field


@dataclass(frozen=True)
class ReportDefinition:
    """تعريف نموذج كامل"""
    model_number: int
    title: str
    report_type: str       # aggregation, detail, status_based
    columns: tuple
    category: str = ''     # أولاً/أ, أولاً/ب, ثانياً
    base_filter: dict = field(default_factory=dict)
    row_field: str = ''    # حقل الصفوف (للتجميع)
    col_field: str = ''    # حقل الأعمدة (للتجميع)
    sub_reports: tuple = ()
    description: str = ''
    parent_section: str = ''  # أولاً/ثانياً
    sub_section: str = ''     # أ/ب


# ═══════════════════════════════════════════════════════════════
# أعمدة مشتركة (DRY — لا تكرار)
# ═══════════════════════════════════════════════════════════════

_BASE = (
    ReportColumn('seq', 'م'),
    ReportColumn('current_rank', 'الرتبة', 'personnel.current_rank.name'),
    ReportColumn('military_number', 'الرقم العسكري', 'personnel.military_number'),
    ReportColumn('full_name', 'الاسم', 'personnel.full_name'),
)

_ID = (
    ReportColumn('national_id', 'الرقم الوطني', 'personnel.national_id'),
)

_QUAL = (
    ReportColumn('qualification', 'المؤهل', 'personnel.qualification'),
)

_NOTES = (
    ReportColumn('notes', 'ملاحظات'),
)

_BIRTH_JOIN = (
    ReportColumn('birth_date', 'تاريخ الميلاد', 'personnel.birth_date'),
    ReportColumn('join_date', 'تاريخ الالتحاق', 'personnel.join_date'),
)

_PROCEDURES = (
    ReportColumn('procedures_status', 'الإجراءات (مستكمل/غير مستكمل)'),
)


# ═══════════════════════════════════════════════════════════════
# الإدارات — القائمة الافتراضية (fallback إذا لم يتصل بـ DB)
# الفعلية تُسحب من DB عبر ReportRegistry.directorates()
# ═══════════════════════════════════════════════════════════════

_DEFAULT_DIRECTORATES = (
    'مكتب المدير العام', 'مكتب نائب المدير العام', 'مكتب المساعدين',
    'أمن الوحدة', 'إدارة الموارد', 'إدارة الشؤون المالية',
    'إدارة الأمن الوقائي', 'إدارة المشاريع', 'إدارة القيادة والسيطرة',
    'إدارة الاتصالات', 'إدارة التدريب والتوجيه', 'إدارة الإمداد والتموين',
    'فرع جهاز المفتش', 'فرع الأحوال المدنية', 'فرع الهجرة والجوازات',
    'فرع الإصلاح والتأهيل', 'فرع الدفاع المدني', 'فرع خفر السواحل',
    'إدارات المطارات والمنافذ', 'إدارة البحث الجنائي', 'إدارة الأدلة الجنائية',
    'إدارة مباحث الأموال', 'فرع القوات الخاصة', 'فرع النجدة',
    'إدارة المرور', 'إدارة مكافحة المخدرات', 'إدارة مكافحة الإرهاب',
    'التدخل السريع', 'إدارة المنشآت', 'الكادر الصحي',
    'شرطة المديريات',
)

# ═══════════════════════════════════════════════════════════════
# الـ 25 نموذج — حسب الدليل الإرشادي بالترتيب
# ═══════════════════════════════════════════════════════════════

_REPORTS = {

    # ════════════════════════════════════════
    # أولاً: القوة العاملة — الخلاصات (1-3)
    # ════════════════════════════════════════

    1: ReportDefinition(
        model_number=1,
        title='خلاصة عددية للقوة العاملة بحسب الرتبة',
        report_type='aggregation',
        category='أولاً', parent_section='أولاً: القوة العاملة', sub_section='خلاصات',
        row_field='directorate', col_field='current_rank',
        base_filter={'current_status__name': 'عاملين'},
        columns=(),
        description='نموذج 1 — الدليل ص 7 — صفوف: إدارات | أعمدة: رتب | القيمة: عدد',
    ),

    2: ReportDefinition(
        model_number=2,
        title='خلاصة فئوية للقوة العاملة',
        report_type='aggregation',
        category='أولاً', parent_section='أولاً: القوة العاملة', sub_section='خلاصات',
        row_field='directorate', col_field='job_category',
        base_filter={'current_status__name': 'عاملين'},
        columns=(),
        description='نموذج 2 — صفوف: إدارات | أعمدة: فئات (إداري/ميداني/فني/تخصصي/حرفي)',
    ),

    3: ReportDefinition(
        model_number=3,
        title='خلاصة عددية للقوة غير العاملة بحسب الرتبة',
        report_type='aggregation',
        category='أولاً', parent_section='أولاً: القوة العاملة', sub_section='خلاصات',
        row_field='current_status', col_field='current_rank',
        base_filter={'current_status__name__ne': 'عاملين'},
        columns=(),
        description='نموذج 3 — صفوف: حالات خدمية | أعمدة: رتب',
    ),

    # ════════════════════════════════════════
    # أولاً - أ: القوة العاملة فعلياً (4)
    # ════════════════════════════════════════

    # ── نموذج 4: القوة العاملة فعلياً ──
    4: ReportDefinition(
        model_number=4,
        title='كشف القوة العاملة فعلياً',
        report_type='detail',
        category='أولاً-أ', parent_section='أولاً: القوة العاملة',
        sub_section='أ - القوة العاملة فعلياً',
        base_filter={'current_status__name': 'عاملين'},
        sub_reports=_DEFAULT_DIRECTORATES,  # fallback — الفعلية من DB
        columns=_BASE + (
            ReportColumn('location', 'محل الخدمة', 'personnel.location'),
            ReportColumn('job_title', 'نوع الخدمة', 'personnel.job_title'),
        ) + _ID + _QUAL + _NOTES,
        description='نموذج 4 — الدليل ص 12 — أعمدة موحدة لكل الـ 31 إدارة',
    ),

    # ════════════════════════════════════════
    # أولاً - ب: القوة العاملة غير الفعلية (كشفان)
    # بدون عمل + احتياط — ليس لها رقم نموذج
    # يتم الوصول إليها عبر ReportRegistry.non_active_sheets()
    # ════════════════════════════════════════

    # ── نموذج 5: مصفوفة الفئات والمسميات الوظيفية ──
    5: ReportDefinition(
        model_number=5,
        title='مصفوفة الفئات والمسميات الوظيفية',
        report_type='taxonomy',
        category='أولاً', parent_section='أولاً: القوة العاملة',
        sub_section='مرجع المسميات',
        columns=(
            ReportColumn('category', 'الفئة'),
            ReportColumn('job_titles', 'المسميات الوظيفية'),
        ),
        sub_reports=('إدارية', 'ميدانية', 'فنية', 'تخصصية', 'حرفية'),
        description='نموذج 5 — الدليل ص 18 — قاموس 5 فئات × 100+ مسمى وظيفي',
    ),

    # ════════════════════════════════════════
    # ثانياً - أ: القوة غير العاملة مؤقتاً (6-11)
    # ════════════════════════════════════════

    # ── نموذج 6: المرافقون ──
    6: ReportDefinition(
        model_number=6,
        title='كشف القوة غير العاملة مؤقتاً — مرافقة',
        report_type='status_based',
        category='ثانياً-أ', parent_section='ثانياً: القوة غير العاملة',
        sub_section='أ - غير العاملة مؤقتاً',
        base_filter={'current_status__name': 'مفرغين للمرافقة'},
        columns=_BASE + (
            ReportColumn('order_source', 'مصدر الأمر', 'form_data.order_source'),
            ReportColumn('dignitary_name', 'اسم الشخصية', 'form_data.dignitary_name'),
            ReportColumn('dignitary_position', 'منصب الشخصية', 'form_data.dignitary_position'),
            ReportColumn('start_date', 'مدة التفريغ من', 'form_data.start_date'),
            ReportColumn('end_date', 'مدة التفريغ إلى', 'form_data.end_date'),
        ),
        description='نموذج 6 — الدليل ص 22',
    ),

    # ── نموذج 7: المنتدبون ──
    7: ReportDefinition(
        model_number=7,
        title='كشف المنتدبين لدى جهات',
        report_type='status_based',
        category='ثانياً-أ', parent_section='ثانياً: القوة غير العاملة',
        sub_section='أ - غير العاملة مؤقتاً',
        base_filter={'current_status__name': 'منتدبين لدى جهات'},
        columns=_BASE + (
            ReportColumn('destination', 'جهة الانتداب', 'form_data.destination'),
            ReportColumn('order_source', 'مصدر الأمر', 'form_data.order_source'),
            ReportColumn('reason', 'الغرض من الانتداب', 'form_data.reason'),
            ReportColumn('start_date', 'مدة الانتداب من', 'form_data.start_date'),
            ReportColumn('end_date', 'مدة الانتداب إلى', 'form_data.end_date'),
        ),
        description='نموذج 7 — الدليل ص 24',
    ),

    # ── نموذج 8: المفرغون للدراسة ──
    8: ReportDefinition(
        model_number=8,
        title='كشف المفرغين للدراسة',
        report_type='status_based',
        category='ثانياً-أ', parent_section='ثانياً: القوة غير العاملة',
        sub_section='أ - غير العاملة مؤقتاً',
        base_filter={'current_status__name': 'مفرغين للدراسة'},
        columns=_BASE + (
            ReportColumn('study_type', 'نوع الدراسة', 'form_data.study_type'),
            ReportColumn('institution', 'جهة الدراسة', 'form_data.institution'),
            ReportColumn('order_source', 'رقم قرار الإيفاد', 'form_data.order_source'),
            ReportColumn('start_date', 'مدة الدراسة من', 'form_data.start_date'),
            ReportColumn('end_date', 'مدة الدراسة إلى', 'form_data.end_date'),
        ),
        description='نموذج 8 — الدليل ص 24',
    ),

    # ── نموذج 9: السجناء ──
    9: ReportDefinition(
        model_number=9,
        title='كشف السجناء',
        report_type='status_based',
        category='ثانياً-أ', parent_section='ثانياً: القوة غير العاملة',
        sub_section='أ - غير العاملة مؤقتاً',
        base_filter={'current_status__name': 'سجناء'},
        columns=_BASE + (
            ReportColumn('case_type', 'نوع القضية', 'form_data.case_type'),
            ReportColumn('arrest_date', 'تاريخ التوقيف', 'form_data.arrest_date'),
            ReportColumn('ruling_type', 'نوع الحكم'),
            ReportColumn('ruling_date', 'تاريخ الحكم', 'form_data.ruling_date'),
            ReportColumn('sentence_start', 'مدة الحكم من', 'form_data.arrest_date'),
            ReportColumn('sentence_end', 'مدة الحكم إلى'),
        ),
        description='نموذج 9 — الدليل ص 25',
    ),

    # ── نموذج 10: الإجازات ──
    10: ReportDefinition(
        model_number=10,
        title='كشف الإجازات',
        report_type='status_based',
        category='ثانياً-أ', parent_section='ثانياً: القوة غير العاملة',
        sub_section='أ - غير العاملة مؤقتاً',
        base_filter={'current_status__name': 'إجازات'},
        columns=_BASE + (
            ReportColumn('leave_type', 'نوع الإجازة'),
            ReportColumn('order_source', 'مصدر الأمر'),
            ReportColumn('start_date', 'مدة الإجازة من'),
            ReportColumn('end_date', 'مدة الإجازة إلى'),
        ) + _NOTES,
        description='نموذج 10 — الدليل ص 25 — المادة 56 من قانون هيئة الشرطة',
    ),

    # ── نموذج 11: المفقودون (مؤقتاً) ──
    11: ReportDefinition(
        model_number=11,
        title='كشف القوة غير العاملة مؤقتاً — مفقودين',
        report_type='status_based',
        category='ثانياً-أ', parent_section='ثانياً: القوة غير العاملة',
        sub_section='أ - غير العاملة مؤقتاً',
        base_filter={'current_status__name': 'مفقودين'},
        columns=_BASE + (
            ReportColumn('location', 'محل الخدمة', 'personnel.location'),
            ReportColumn('missing_date', 'تاريخ الفقدان', 'form_data.missing_date'),
            ReportColumn('court_ruling_status', 'حكم شرعي بالفقدان (مستكمل/غير مستكمل)'),
            ReportColumn('power_of_attorney_status', 'وكالة شرعية (مستكمل/غير مستكمل)'),
            ReportColumn('heir_ruling_status', 'حكم انحصار ورثة (مستكمل/غير مستكمل)'),
        ),
        description='نموذج 11 — الدليل ص 26',
    ),

    # ════════════════════════════════════════
    # ثانياً - ب: القوة غير العاملة نهائياً (12-25)
    # ════════════════════════════════════════

    # ── نموذج 12: كبار السن ──
    12: ReportDefinition(
        model_number=12,
        title='كشف القوة غير العاملة نهائياً — كبار سن',
        report_type='status_based',
        category='ثانياً-ب', parent_section='ثانياً: القوة غير العاملة',
        sub_section='ب - غير العاملة نهائياً',
        base_filter={'current_status__name': 'كبار سن'},
        columns=_BASE + _BIRTH_JOIN + _PROCEDURES + _NOTES,
        description='نموذج 12 — الدليل ص 27 — بلوغ السن القانوني',
    ),

    # ── نموذج 13: نهاية المدة ──
    13: ReportDefinition(
        model_number=13,
        title='كشف القوة غير العاملة نهائياً — نهاية المدة',
        report_type='status_based',
        category='ثانياً-ب', parent_section='ثانياً: القوة غير العاملة',
        sub_section='ب - غير العاملة نهائياً',
        base_filter={'current_status__name': 'إنهاء مدة'},
        columns=_BASE + _BIRTH_JOIN + _PROCEDURES + _NOTES,
        description='نموذج 13 — الدليل ص 27 — شرط 20 سنة خدمة',
    ),

    # ── نموذج 14: مرشحين للتقاعد ──
    14: ReportDefinition(
        model_number=14,
        title='كشف القوة غير العاملة نهائياً — مرشحين للتقاعد',
        report_type='detail',
        category='ثانياً-ب', parent_section='ثانياً: القوة غير العاملة',
        sub_section='ب - غير العاملة نهائياً',
        columns=_BASE + (
            ReportColumn('status_type', 'نوع الحالة'),
        ) + _BIRTH_JOIN + _PROCEDURES + _NOTES,
        description='نموذج 14 — الدليل ص 28 — 50 سنة عمر أو 20 سنة خدمة',
    ),

    # ── نموذج 15: عدم لياقة / أمراض ومشوهين ──
    15: ReportDefinition(
        model_number=15,
        title='كشف القوة غير العاملة — عدم اللياقة (أمراض ومشوهين)',
        report_type='status_based',
        category='ثانياً-ب', parent_section='ثانياً: القوة غير العاملة',
        sub_section='ب - غير العاملة نهائياً',
        base_filter={'current_status__name': 'عدم لياقة'},
        columns=_BASE + (
            ReportColumn('disease_type', 'نوع المرض', 'form_data.disease_type'),
            ReportColumn('disability_percentage', 'نسبة العجز', 'form_data.disability_percentage'),
            ReportColumn('injury_date', 'تاريخ وقوعها', 'form_data.injury_date'),
            ReportColumn('medical_source', 'مصدر القرار', 'form_data.medical_source'),
            ReportColumn('during_duty', 'أثناء الواجب', 'form_data.injury_context'),
            ReportColumn('natural', 'طبيعية', 'form_data.injury_context'),
        ),
        description='نموذج 15 — الدليل ص 28',
    ),

    # ── نموذج 16: شهداء ووفيات ──
    16: ReportDefinition(
        model_number=16,
        title='كشف القوة غير العاملة — شهداء ووفيات',
        report_type='status_based',
        category='ثانياً-ب', parent_section='ثانياً: القوة غير العاملة',
        sub_section='ب - غير العاملة نهائياً',
        base_filter={'current_status__name__in': ['شهداء', 'وفيات']},
        columns=_BASE + (
            ReportColumn('status_type', 'نوع الحالة (شهيد/متوفى)'),
            ReportColumn('event_date', 'تاريخ وقوعها'),
            ReportColumn('during_duty', 'أثناء الواجب'),
            ReportColumn('natural', 'طبيعية'),
        ) + _NOTES,
        description='نموذج 16 — الدليل ص 29',
    ),

    # ── نموذج 17: متقاعدين ──
    17: ReportDefinition(
        model_number=17,
        title='كشف القوة غير العاملة — متقاعدين',
        report_type='status_based',
        category='ثانياً-ب', parent_section='ثانياً: القوة غير العاملة',
        sub_section='ب - غير العاملة نهائياً',
        base_filter={'current_status__name': 'متقاعدين'},
        columns=_BASE + _BIRTH_JOIN + (
            ReportColumn('decision_number', 'رقم القرار', 'form_data.decision_number'),
            ReportColumn('decision_date', 'تاريخ القرار', 'form_data.decision_date'),
        ) + _NOTES,
        description='نموذج 17 — الدليل ص 30',
    ),

    # ── نموذج 18: الواصلون من الوزارة ──
    18: ReportDefinition(
        model_number=18,
        title='كشف الواصلين من الوزارة',
        report_type='detail',
        category='ثانياً-ب', parent_section='ثانياً: القوة غير العاملة',
        sub_section='ب - غير العاملة نهائياً',
        columns=_BASE + (
            ReportColumn('location', 'محل الخدمة', 'personnel.location'),
            ReportColumn('source_unit', 'الجهة الواصل منها'),
            ReportColumn('start_date', 'تاريخ المباشرة'),
        ) + _NOTES,
        description='نموذج 18 — الدليل ص 30',
    ),

    # ── نموذج 19: العازمون إلى الوزارة ──
    19: ReportDefinition(
        model_number=19,
        title='كشف العازمين من الوحدة إلى الوزارة',
        report_type='detail',
        category='ثانياً-ب', parent_section='ثانياً: القوة غير العاملة',
        sub_section='ب - غير العاملة نهائياً',
        columns=_BASE + (
            ReportColumn('location', 'محل الخدمة', 'personnel.location'),
            ReportColumn('job_title', 'نوع الخدمة', 'personnel.job_title'),
            ReportColumn('transfer_date', 'تاريخ النقل'),
            ReportColumn('transfer_reason', 'سبب النقل'),
        ) + _NOTES,
        description='نموذج 19 — الدليل ص 28',
    ),

    # ── نموذج 20: العازمون (تفصيلي) ──
    20: ReportDefinition(
        model_number=20,
        title='كشف العازمين من الوحدة — تفصيلي',
        report_type='detail',
        category='ثانياً-ب', parent_section='ثانياً: القوة غير العاملة',
        sub_section='ب - غير العاملة نهائياً',
        columns=_BASE + (
            ReportColumn('prev_location', 'محل الخدمة السابق'),
            ReportColumn('prev_job_title', 'نوع الخدمة السابقة'),
            ReportColumn('new_location', 'محل الخدمة الحالي (الوجهة)'),
            ReportColumn('new_job_title', 'نوع الخدمة الجديدة'),
        ) + _NOTES,
        description='نموذج 20 — الدليل ص 28',
    ),

    # ── نموذج 21: عاملون لدينا ومرتباتهم في جهات أخرى ──
    21: ReportDefinition(
        model_number=21,
        title='كشف العاملين لدينا ومرتباتهم في جهات أخرى',
        report_type='detail',
        category='ثانياً-ب', parent_section='ثانياً: القوة غير العاملة',
        sub_section='ب - غير العاملة نهائياً',
        columns=_BASE + (
            ReportColumn('location', 'محل الخدمة', 'personnel.location'),
            ReportColumn('job_title', 'نوع الخدمة', 'personnel.job_title'),
            ReportColumn('salary_source', 'جهة المرتب'),
            ReportColumn('start_date', 'تاريخ المباشرة'),
        ) + _NOTES,
        description='نموذج 21 — الدليل ص 29 — المطابقة المالية',
    ),

    # ── نموذج 22: عاملون في جهات أخرى ومرتباتهم لدينا ──
    22: ReportDefinition(
        model_number=22,
        title='كشف العاملين في جهات أخرى ومرتباتهم لدينا',
        report_type='detail',
        category='ثانياً-ب', parent_section='ثانياً: القوة غير العاملة',
        sub_section='ب - غير العاملة نهائياً',
        columns=_BASE + (
            ReportColumn('prev_location', 'محل الخدمة السابق'),
            ReportColumn('job_title', 'نوع الخدمة', 'personnel.job_title'),
            ReportColumn('transfer_date', 'تاريخ النقل'),
        ) + _NOTES,
        description='نموذج 22 — الدليل ص 29',
    ),

    # ── نموذج 23: تصحيح الأسماء ──
    23: ReportDefinition(
        model_number=23,
        title='كشف المطلوب تصحيح أسماؤهم',
        report_type='detail',
        category='ثانياً-ب', parent_section='ثانياً: القوة غير العاملة',
        sub_section='ب - غير العاملة نهائياً',
        columns=_BASE + (
            ReportColumn('correct_name', 'الاسم الصحيح (من البطاقة الشخصية)'),
            ReportColumn('wrong_name', 'الاسم الخطأ (من كشف الراتب)'),
            ReportColumn('correction_target', 'المطلوب تصحيحه (أول/ثاني/ثالث/رابع/لقب)'),
        ) + _NOTES,
        description='نموذج 23 — الدليل ص 31',
    ),

    # ── نموذج 24: الغياب ──
    24: ReportDefinition(
        model_number=24,
        title='كشف الغياب',
        report_type='detail',
        category='ثانياً-ب', parent_section='ثانياً: القوة غير العاملة',
        sub_section='ب - غير العاملة نهائياً',
        base_filter={'current_status__name__in': ['غياب', 'منقطعين - فرار']},
        columns=_BASE + _ID + (
            ReportColumn('absence_reason', 'سبب التوقيف'),
            ReportColumn('absence_days', 'عدد أيام الغياب / مدة الغياب'),
        ) + _NOTES,
        description='نموذج 24 — الدليل ص 31 — قسم أ: توقيف مرتبات | قسم ب: غياب مستمر',
    ),

    # ── نموذج 25: الملتحقون بالعدوان ──
    25: ReportDefinition(
        model_number=25,
        title='كشف الملتحقين بالعدوان',
        report_type='detail',
        category='ثانياً-ب', parent_section='ثانياً: القوة غير العاملة',
        sub_section='ب - غير العاملة نهائياً',
        base_filter={'current_status__name': 'ملتحقين بالعدوان'},
        columns=_BASE + _ID + (
            ReportColumn('report_source', 'جهة البلاغ'),
            ReportColumn('actions_taken', 'الإجراءات المتخذة ضده'),
        ) + _NOTES,
        description='نموذج 25 — الدليل ص 32 — القائمة السوداء',
    ),
}


# ═══════════════════════════════════════════════════════════════
# ReportRegistry — الواجهة الموحدة
# ═══════════════════════════════════════════════════════════════

class ReportRegistry:
    """
    سجل التقارير المركزي — نقطة الوصول الوحيدة لكل الـ 25 نموذج.
    
    الاستخدام:
        ReportRegistry.get(4)              → ReportDefinition
        ReportRegistry.schema(4)           → dict (للفرونت)
        ReportRegistry.available_models()  → [1,2,...,25]
        ReportRegistry.by_category('ب')   → {12: ..., 13: ...}
    """

    @staticmethod
    def _get_custom(model_number: int):
        """جلب نموذج مخصص من DB"""
        try:
            from systems.services.models import CustomReportTemplate
            return CustomReportTemplate.objects.get(model_number=model_number, is_active=True)
        except Exception:
            return None

    @staticmethod
    def _all_custom():
        """كل النماذج المخصصة من DB"""
        try:
            from systems.services.models import CustomReportTemplate
            return list(CustomReportTemplate.objects.filter(is_active=True))
        except Exception:
            return []

    @staticmethod
    def get(model_number: int) -> Optional[ReportDefinition]:
        return _REPORTS.get(model_number)

    @staticmethod
    def exists(model_number: int) -> bool:
        return model_number in _REPORTS or ReportRegistry._get_custom(model_number) is not None

    @staticmethod
    def all() -> dict:
        return dict(_REPORTS)

    @staticmethod
    def available_models() -> list:
        """كل أرقام النماذج (ثابتة 1-25 + مخصصة 26+)"""
        built_in = sorted(_REPORTS.keys())
        custom = [c.model_number for c in ReportRegistry._all_custom()]
        return sorted(set(built_in + custom))

    @staticmethod
    def by_category(category: str) -> dict:
        """جلب نماذج حسب الفئة"""
        return {k: v for k, v in _REPORTS.items() if v.category == category}

    @staticmethod
    def schema(model_number: int) -> dict:
        """هيكل النموذج — يبحث أولاً في الثابتة ثم في المخصصة"""
        # 1. ثابتة (1-25)
        defn = _REPORTS.get(model_number)
        if defn:
            return {
                'model_number': defn.model_number,
                'title': defn.title,
                'type': defn.report_type,
                'category': defn.category,
                'is_custom': False,
                'columns': [
                    {'key': c.key, 'label': c.label, 'source': c.source}
                    for c in defn.columns
                ],
                'base_filter': defn.base_filter,
                'description': defn.description,
            }
        # 2. مخصصة (26+)
        custom = ReportRegistry._get_custom(model_number)
        if not custom:
            return {}
        return {
            'model_number': custom.model_number,
            'title': custom.title,
            'type': custom.report_type,
            'category': custom.category,
            'is_custom': True,
            'columns': custom.columns or [],
            'base_filter': custom.base_filter or {},
            'description': '',
        }

    @staticmethod
    def all_schemas() -> dict:
        return {k: ReportRegistry.schema(k) for k in _REPORTS}

    @staticmethod
    def directorates() -> list:
        """
        الإدارات من قاعدة البيانات (ديناميكي).
        عند إضافة إدارة جديدة → تظهر تلقائياً في نموذج 4.
        """
        try:
            from core.models import CentralDepartment
            names = list(
                CentralDepartment.objects.filter(is_active=True)
                .order_by('order', 'name')
                .values_list('name', flat=True)
            )
            return names if names else list(_DEFAULT_DIRECTORATES)
        except Exception:
            return list(_DEFAULT_DIRECTORATES)

    @staticmethod
    def non_active_sheets() -> list:
        """
        كشفا القوة العاملة غير الفعلية (أولاً-ب):
        1. كشف المتواجدين بدون عمل
        2. كشف قوة الاحتياط
        أعمدة موحدة مع نموذج 4 + محل الخدمة السابق
        """
        cols = _BASE + (
            ReportColumn('prev_location', 'محل الخدمة السابق', 'personnel.prev_location'),
            ReportColumn('prev_job_title', 'نوع الخدمة السابقة', 'personnel.prev_job_title'),
        ) + _ID + _QUAL + _NOTES
        return [
            {
                'key': 'no_work', 'title': 'كشف المتواجدين بدون عمل',
                'filter': {'current_status__name': 'بدون عمل'},
                'columns': [{'key': c.key, 'label': c.label, 'source': c.source} for c in cols],
                'parent_section': 'أولاً: القوة العاملة',
                'sub_section': 'ب - القوة العاملة غير الفعلية',
            },
            {
                'key': 'reserve', 'title': 'كشف قوة الاحتياط',
                'filter': {'current_status__name': 'قوة احتياطية'},
                'columns': [{'key': c.key, 'label': c.label, 'source': c.source} for c in cols],
                'parent_section': 'أولاً: القوة العاملة',
                'sub_section': 'ب - القوة العاملة غير الفعلية',
            },
        ]

    @staticmethod
    def tree() -> dict:
        """
        شجرة التنقل الكاملة — للفرونت اند.
        يعيد الهيكل الهرمي الكامل كما في الدليل الإرشادي.
        """
        return {
            'أولاً: القوة العاملة': {
                'خلاصات': [ReportRegistry.schema(n) for n in [1, 2, 3]],
                'أ - القوة العاملة فعلياً': {
                    'نموذج_4': ReportRegistry.schema(4),
                    'كشوفات': ReportRegistry.directorates(),
                },
                'ب - القوة العاملة غير الفعلية': ReportRegistry.non_active_sheets(),
                'نموذج_5': ReportRegistry.schema(5),
            },
            'ثانياً: القوة غير العاملة': {
                'أ - غير العاملة مؤقتاً': [ReportRegistry.schema(n) for n in range(6, 12)],
                'ب - غير العاملة نهائياً': [ReportRegistry.schema(n) for n in range(12, 26)],
            },
        }

