"""
═══════════════════════════════════════════════════════════════
سجل الاستمارات المركزي — Form Registry (Single Source of Truth)
═══════════════════════════════════════════════════════════════

كل ما يتعلق بالاستمارات الـ 11 موجود هنا فقط:
- الأعمدة المطلوبة (form_data schema)
- المرفقات الإلزامية
- قواعد التحقق (validation)
- الحالة المستهدفة
- بيانات العرض (labels)

الاستخدام:
    from systems.services.registries.form_registry import FormRegistry

    schema = FormRegistry.get('martyr')
    all_types = FormRegistry.choices()
    requirements = FormRegistry.attachments('martyr')
"""
from dataclasses import dataclass, field
from typing import Optional


# ─────────────────────────────────────────────
# تعريف حقل في form_data
# ─────────────────────────────────────────────
@dataclass(frozen=True)
class FormField:
    """حقل واحد في بيانات الاستمارة"""
    key: str                    # المفتاح البرمجي
    label: str                  # التسمية العربية
    field_type: str = 'text'    # text, date, number, select, textarea
    required: bool = True       # إلزامي أم اختياري
    options: tuple = ()         # خيارات (للـ select)
    help_text: str = ''         # توضيح إضافي
    disabled: bool = False      # هل الحقل معطل
    default: str = ''           # قيمة افتراضية


# ─────────────────────────────────────────────
# تعريف مرفق مطلوب
# ─────────────────────────────────────────────
@dataclass(frozen=True)
class AttachmentSpec:
    """مواصفات مرفق واحد مطلوب"""
    doc_type: str               # نوع المرفق (مفتاح برمجي)
    label: str                  # التسمية العربية
    required: bool = True       # إلزامي أم اختياري


# ─────────────────────────────────────────────
# تعريف استمارة كاملة
# ─────────────────────────────────────────────
@dataclass(frozen=True)
class FormDefinition:
    """تعريف كامل لاستمارة واحدة"""
    form_type: str              # المفتاح البرمجي
    label: str                  # التسمية العربية
    target_status: str          # الحالة المستهدفة (اسم ServiceStatus)
    fields: tuple               # حقول form_data المطلوبة
    attachments: tuple          # المرفقات المطلوبة
    min_documents: int = 1      # الحد الأدنى من المرفقات
    max_documents: int = 10     # الحد الأقصى
    description: str = ''       # وصف الاستمارة


# ═══════════════════════════════════════════════════════════════
# أقسام مشتركة — تُسحب تلقائياً من الفرد (لا يدخلها المستخدم)
# ═══════════════════════════════════════════════════════════════

# أولاً: البيانات الشخصية (الأساسية) — تُسحب من PersonnelMaster
SECTION_PERSONAL = (
    FormField('rank', 'الرتبة', 'auto', required=False, help_text='personnel.current_rank'),
    FormField('military_number', 'الرقم العسكري', 'auto', required=False, help_text='personnel.military_number'),
    FormField('full_name', 'الاسم', 'auto', required=False, help_text='personnel.full_name'),
    FormField('unit', 'الوحدة', 'auto', required=False, help_text='personnel.directorate'),
    FormField('company', 'السرية', 'auto', required=False, help_text='personnel.company'),
)

# ثانياً: بيانات الميلاد والإقامة — تُسحب من PersonnelMaster
SECTION_IDENTITY = (
    FormField('national_id', 'الرقم الوطني', 'auto', required=False, help_text='personnel.national_id'),
    FormField('birth_place', 'محل الميلاد', 'auto', required=False, help_text='personnel.birth_place'),
    FormField('current_residence', 'محل الإقامة الحالية', 'auto', required=False, help_text='personnel.current_residence'),
    FormField('id_issuer', 'جهة الإصدار', 'auto', required=False, help_text='personnel.id_issuer'),
    FormField('id_issue_date', 'تاريخ الإصدار', 'auto', required=False, help_text='personnel.id_issue_date'),
)


# ═══════════════════════════════════════════════════════════════
# تعريفات الاستمارات الـ 11 — حسب الدليل الإرشادي بالضبط
# ═══════════════════════════════════════════════════════════════


_FORMS = {

    # ── استمارة 1: بلوغ السن القانوني ──
    'retirement_age': FormDefinition(
        form_type='retirement_age',
        label='استمارة إثبات حالة — بلوغ السن القانوني',
        target_status='كبار سن',
        description='الدليل: ص 33 — تُستخدم عند بلوغ الفرد السن القانوني للتقاعد',
        fields=(
            FormField('category', 'الفئة', 'text', required=True, disabled=True, default='كبار سن'),
            FormField('birth_date', 'تاريخ الميلاد', 'date'),
            FormField('join_date', 'تاريخ الالتحاق بالخدمة', 'date'),
            FormField('age', 'العمر', 'number'),
            FormField('gender', 'الجنس', 'select', options=('ذكر', 'أنثى')),
        ),
        attachments=(
            AttachmentSpec('personal_request', 'الطلب الشخصي'),
            AttachmentSpec('national_id_front', 'صورة البطاقة العسكرية والشخصية'),
        ),
        min_documents=2,
    ),

    # ── استمارة 2: وفاة ──
    'death': FormDefinition(
        form_type='death',
        label='استمارة إثبات حالة — وفاة',
        target_status='وفيات',
        description='الدليل: ص 34 — تُستخدم لتوثيق الوفاة الطبيعية',
        fields=(
            FormField('category', 'الفئة', 'text', required=True, disabled=True, default='وفيات'),
            FormField('death_date', 'تاريخ الوفاة', 'date'),
            FormField('death_cause', 'سبب الوفاة', 'textarea'),
            FormField('death_location', 'مكان الوفاة', 'location_cascade',
                      help_text='محافظة → مديرية → عزلة/قرية — يمكن الكتابة يدوياً'),
            FormField('occurrence_context', 'حالة الوقوع', 'select',
                      options=('أثناء الواجب', 'طبيعية')),
        ),
        attachments=(
            AttachmentSpec('death_certificate', 'شهادة الوفاة'),
            AttachmentSpec('heir_ruling', 'حكم انحصار الورثة'),
            AttachmentSpec('power_of_attorney', 'وكالة شرعية'),
            AttachmentSpec('national_id_front', 'صورة البطاقة الشخصية/العسكرية'),
            AttachmentSpec('attorney_id', 'صورة بطاقة الوكيل'),
            AttachmentSpec('appointment_ruling', 'حكم التنصيب'),
        ),
        min_documents=4,
    ),

    # ── استمارة 3: مفقود ──
    'missing': FormDefinition(
        form_type='missing',
        label='استمارة إثبات حالة — مفقود',
        target_status='مفقودين',
        description='الدليل: ص 35 — نموذج 11 — المفقودين (مؤقتاً)',
        fields=(
            FormField('category', 'الفئة', 'text', required=True, disabled=True, default='مفقودين'),
            FormField('missing_date', 'تاريخ الفقدان', 'date'),
            FormField('missing_location', 'مكان الفقدان', 'location_cascade',
                      help_text='محافظة → مديرية → عزلة/قرية — يمكن الكتابة يدوياً'),
            FormField('court_ruling_date', 'تاريخ الحكم الشرعي', 'date', required=False),
            FormField('legal_status', 'حالة الإجراءات', 'select',
                      options=('مستكمل', 'غير مستكمل')),
        ),
        attachments=(
            AttachmentSpec('status_change_order', 'بلاغ الفقدان'),
            AttachmentSpec('heir_ruling', 'حكم انحصار الورثة'),
            AttachmentSpec('power_of_attorney', 'الوكالة الشرعية'),
            AttachmentSpec('national_id_front', 'صورة البطاقة الشخصية/العسكرية'),
            AttachmentSpec('attorney_id', 'صورة بطاقة الوكيل'),
            AttachmentSpec('newspaper_notice', 'إعلان الجريدة', required=False),
            AttachmentSpec('court_ruling', 'حكم شرعي بالفقدان', required=False),
        ),
        min_documents=3,
    ),

    # ── استمارة 4: عدم لياقة صحية ──
    'medical_unfit': FormDefinition(
        form_type='medical_unfit',
        label='استمارة إثبات حالة — عدم لياقة صحية',
        target_status='عدم لياقة',
        description='الدليل: ص 36 — نموذج 15 — أمراض ومشوهين',
        fields=(
            FormField('category', 'الفئة', 'text', required=True, disabled=True, default='عدم اللياقة الصحية'),
            FormField('disease_type', 'نوع المرض', 'text'),
            FormField('disability_percentage', 'نسبة العجز', 'number'),
            FormField('medical_source', 'مصدر القرار الطبي', 'text'),
            FormField('injury_context', 'حالة الوقوع', 'select',
                      options=('أثناء الواجب', 'طبيعية')),
            FormField('injury_date', 'تاريخ الوقوع', 'date'),
        ),
        attachments=(
            AttachmentSpec('medical_report', 'القرار الطبي الأصل (اللجنة الطبية)'),
            AttachmentSpec('national_id_front', 'صورة البطاقة الشخصية/العسكرية'),
            AttachmentSpec('photo', 'صورة حديثة للمريض', required=False),
            AttachmentSpec('power_of_attorney', 'وكالة شرعية'),
            AttachmentSpec('attorney_id', 'صورة بطاقة الوكيل'),
        ),
        min_documents=4,
    ),

    # ── استمارة 5: إنهاء مدة ──
    'end_of_service': FormDefinition(
        form_type='end_of_service',
        label='استمارة إثبات حالة — إنهاء مدة',
        target_status='إنهاء مدة',
        description='الدليل: ص 37 — نموذج 13 — شرط 20 سنة خدمة',
        fields=(
            FormField('category', 'الفئة', 'text', required=True, disabled=True, default='إنهاء مدة'),
            FormField('birth_date', 'تاريخ الميلاد', 'date'),
            FormField('join_date', 'تاريخ الالتحاق بالخدمة', 'date'),
            FormField('service_years', 'سنوات الخدمة', 'number'),
            FormField('gender', 'الجنس', 'select', options=('ذكر', 'أنثى')),
        ),
        attachments=(
            AttachmentSpec('personal_request', 'الطلب الشخصي من الفرد'),
            AttachmentSpec('national_id_front', 'صورة البطاقة العسكرية والشخصية'),
        ),
        min_documents=2,
    ),

    # ── استمارة 6: تقاعد ──
    'retired': FormDefinition(
        form_type='retired',
        label='استمارة إثبات حالة — محال للتقاعد',
        target_status='متقاعدين',
        description='الدليل: ص 38 — نموذج 17',
        fields=(
            FormField('category', 'الفئة', 'text', required=True, disabled=True, default='محال للتقاعد'),
            FormField('birth_date', 'تاريخ الميلاد', 'date'),
            FormField('join_date', 'تاريخ الالتحاق', 'date'),
            FormField('decision_number', 'رقم قرار الإحالة', 'text'),
            FormField('decision_date', 'تاريخ قرار الإحالة', 'date'),
            FormField('referral_date', 'تاريخ الإحالة الفعلي', 'date'),
        ),
        attachments=(
            AttachmentSpec('status_change_order', 'أمر الإحالة على التقاعد'),
            AttachmentSpec('personal_request', 'الطلب الشخصي', required=False),
            AttachmentSpec('national_id_front', 'صورة البطاقة الشخصية/العسكرية'),
        ),
        min_documents=2,
    ),

    # ── استمارة 7: مسجون ──
    'imprisoned': FormDefinition(
        form_type='imprisoned',
        label='استمارة إثبات حالة — مسجون',
        target_status='سجناء',
        description='الدليل: ص 37 — استمارة 7 — أحكام قضائية',
        fields=(
            FormField('category', 'الفئة', 'text', required=True, disabled=True, default='سجناء'),
            FormField('case_type', 'نوع القضية', 'text'),
            FormField('ruling_date', 'تاريخ الحكم', 'date'),
            FormField('sentence_duration', 'مدة الحكم', 'text'),
            FormField('arrest_date', 'تاريخ التوقيف', 'date'),
            FormField('detention_location', 'جهة التوقيف', 'text'),
        ),
        attachments=(
            AttachmentSpec('court_ruling', 'نسخة من الحكم القضائي'),
            AttachmentSpec('memo', 'مذكرة النيابة (رهن التحقيق)', required=False),
            AttachmentSpec('national_id_front', 'صورة البطاقة الشخصية/العسكرية'),
            AttachmentSpec('power_of_attorney', 'وكالة شرعية'),
            AttachmentSpec('attorney_id', 'صورة بطاقة الوكيل'),
        ),
        min_documents=4,
    ),

    # ── استمارة 8: مرافق / معيات ──
    'escort': FormDefinition(
        form_type='escort',
        label='استمارة إثبات حالة — مرافق',
        target_status='مفرغين للمرافقة',
        description='الدليل: ص 41 — نموذج 6',
        fields=(
            FormField('category', 'الفئة', 'text', required=True, disabled=True, default='المعيات'),
            FormField('dignitary_name', 'اسم الشخصية', 'text'),
            FormField('dignitary_position', 'منصب الشخصية', 'text'),
            FormField('order_source', 'مصدر الأمر', 'text',
                      help_text='وزير الداخلية / نائب الوزير / الوكيل / المدير العام'),
            FormField('start_date', 'تاريخ البدء', 'date'),
            FormField('end_date', 'تاريخ الانتهاء', 'date'),
        ),
        attachments=(
            AttachmentSpec('assignment_order', 'نسخة من أمر التكليف بالمرافقة'),
            AttachmentSpec('national_id_front', 'صورة البطاقة العسكرية والشخصية'),
        ),
        min_documents=2,
    ),

    # ── استمارة 9: شهيد ──
    'martyr': FormDefinition(
        form_type='martyr',
        label='استمارة إثبات حالة — شهيد',
        target_status='شهداء',
        description='الدليل: ص 40 — أكبر عدد مرفقات',
        fields=(
            FormField('category', 'الفئة', 'text', required=True, disabled=True, default='الشهداء'),
            FormField('martyrdom_date', 'تاريخ الاستشهاد', 'date'),
            FormField('martyrdom_cause', 'سبب الاستشهاد', 'textarea'),
            FormField('martyrdom_location', 'مكان الاستشهاد', 'location_cascade',
                      help_text='محافظة → مديرية → عزلة/قرية — يمكن الكتابة يدوياً'),
            FormField('occurrence_context', 'حالة الوقوع', 'select',
                      options=('أثناء الواجب',)),
        ),
        attachments=(
            AttachmentSpec('death_certificate', 'شهادة الوفاة'),
            AttachmentSpec('heir_ruling', 'حكم انحصار الورثة'),
            AttachmentSpec('power_of_attorney', 'الوكالة الشرعية'),
            AttachmentSpec('national_id_front', 'صورة البطاقة الشخصية/العسكرية'),
            AttachmentSpec('attorney_id', 'صورة بطاقة الوكيل'),
            AttachmentSpec('appointment_ruling', 'حكم التنصيب'),
            AttachmentSpec('operations_report', 'بلاغ العمليات'),
            AttachmentSpec('assignment_order', 'أمر التكليف بالمهمة'),
        ),
        min_documents=5,
        max_documents=12,
    ),

    # ── استمارة 10: مفرغ للدراسة ──
    'study_leave': FormDefinition(
        form_type='study_leave',
        label='استمارة إثبات حالة — مفرغ للدراسة',
        target_status='مفرغين للدراسة',
        description='الدليل: ص 42 — نموذج 8',
        fields=(
            FormField('category', 'الفئة', 'text', required=True, disabled=True, default='مفرغين للدراسة'),
            FormField('study_type', 'نوع الدراسة', 'select',
                      options=('دبلوم', 'بكالوريوس', 'ماجستير', 'دكتوراه', 'دورة تخصصية')),
            FormField('institution', 'جهة الدراسة', 'text'),
            FormField('order_source', 'مصدر الأمر / رقم قرار الإيفاد', 'text'),
            FormField('duration', 'مدة الدراسة', 'text'),
            FormField('start_date', 'تاريخ البدء', 'date'),
            FormField('end_date', 'تاريخ الانتهاء', 'date'),
        ),
        attachments=(
            AttachmentSpec('study_order', 'نسخة من أمر التفرغ الدراسي'),
            AttachmentSpec('national_id_front', 'صورة البطاقة العسكرية والشخصية'),
        ),
        min_documents=2,
    ),

    # ── استمارة 11: منتدب ──
    'seconded': FormDefinition(
        form_type='seconded',
        label='استمارة إثبات حالة — منتدب',
        target_status='منتدبين لدى جهات',
        description='الدليل: ص 42 — نموذج 7',
        fields=(
            FormField('category', 'الفئة', 'text', required=True, disabled=True, default='المنتدبين'),
            FormField('destination', 'جهة الانتداب', 'text'),
            FormField('reason', 'سبب الانتداب', 'textarea'),
            FormField('order_source', 'مصدر الأمر', 'text'),
            FormField('start_date', 'تاريخ البدء', 'date'),
            FormField('end_date', 'تاريخ الانتهاء', 'date'),
        ),
        attachments=(
            AttachmentSpec('secondment_order', 'نسخة من أمر الانتداب'),
            AttachmentSpec('national_id_front', 'صورة البطاقة العسكرية والشخصية'),
        ),
        min_documents=2,
    ),
    # ── استمارة 12: تنزيل الرتبة ──
    'rank_demotion': FormDefinition(
        form_type='rank_demotion',
        label='طلب تنزيل الرتبة',
        target_status='تنزيل رتبة',
        description='تنزيل رتبة الفرد نتيجة عقوبة عسكرية أو إدارية أو حكم قضائي',
        fields=(
            FormField('category', 'الفئة', 'text', required=True, disabled=True, default='الترقيات وتسويات الرتب'),
            FormField('settlement_type', 'نوع التسوية', 'text', required=True, disabled=True, default='تنزيل رتبة'),
            FormField('to_rank', 'الرتبة المستهدفة', 'select', required=True),
            FormField('demotion_reason', 'سبب التنزيل (بناءً على القرار)', 'textarea', required=True),
            FormField('decision_number', 'رقم قرار التنزيل', 'text', required=True),
            FormField('decision_date', 'تاريخ القرار', 'date', required=True),
        ),
        attachments=(
            AttachmentSpec('demotion_decision', 'نسخة من قرار التنزيل'),
            AttachmentSpec('national_id_front', 'صورة البطاقة العسكرية والشخصية'),
        ),
        min_documents=2,
    ),

    # ── استمارة 13: ترقية / تسوية رتبة ──
    'rank_promotion': FormDefinition(
        form_type='rank_promotion',
        label='طلب ترقية اعتيادية / استثنائية',
        target_status='ترقية رتبة',
        description='ترقية الفرد إلى الرتبة العسكرية التالية',
        fields=(
            FormField('category', 'الفئة', 'text', required=True, disabled=True, default='الترقيات وتسويات الرتب'),
            FormField('settlement_type', 'نوع الترقية', 'select', required=True, options=('ترقية اعتيادية', 'ترقية استثنائية', 'ترقية استثنائية (شهيد)', 'ترقية (متقاعد)')),
            FormField('to_rank', 'الرتبة المستهدفة', 'select', required=True),
            FormField('due_date', 'تاريخ الاستحقاق', 'date', required=True),
            FormField('decision_number', 'رقم قرار الترقية', 'text', required=True),
            FormField('decision_date', 'تاريخ القرار', 'date', required=True),
        ),
        attachments=(
            AttachmentSpec('promotion_decision', 'نسخة من قرار الترقية'),
            AttachmentSpec('national_id_front', 'صورة البطاقة العسكرية والشخصية'),
        ),
        min_documents=2,
    ),

    # ── استمارة 14: تسوية من كادر الأفراد إلى كادر الضباط ──
    'personnel_to_officer': FormDefinition(
        form_type='personnel_to_officer',
        label='طلب تسوية من كادر الأفراد إلى كادر الضباط',
        target_status='ضباط (تسوية جامعيين)',
        description='تسوية وضع فرد حاصل على مؤهل جامعي وتحويله إلى كادر الضباط مع رقم عسكري جديد يبدأ بـ (60)',
        fields=(
            FormField('category', 'الفئة', 'text', required=True, disabled=True, default='التسويات لجامعيين'),
            FormField('settlement_type', 'نوع التسوية', 'text', required=True, disabled=True, default='تسوية وضع (من فرد إلى ضابط)'),
            FormField('to_rank', 'الرتبة المستهدفة', 'select', required=True, help_text='عادة ما تكون ملازم'),
            FormField('new_military_number', 'الرقم العسكري الجديد (للضابط)', 'text', required=True, help_text='يجب أن يبدأ بـ 60 ويتكون من 7 أرقام'),
            FormField('university_degree_type', 'نوع المؤهل الجامعي', 'select', required=True, options=('بكالوريوس', 'ماجستير', 'دكتوراه', 'أخرى')),
            FormField('decision_number', 'رقم قرار التسوية', 'text', required=True),
            FormField('decision_date', 'تاريخ القرار', 'date', required=True),
        ),
        attachments=(
            AttachmentSpec('university_degree', 'صورة المؤهل الجامعي مصدقة'),
            AttachmentSpec('settlement_decision', 'نسخة من قرار التسوية'),
            AttachmentSpec('national_id_front', 'صورة البطاقة العسكرية والشخصية'),
        ),
        min_documents=3,
    ),
}


# ═══════════════════════════════════════════════════════════════
# FormRegistry — الواجهة الموحدة (API)
# ═══════════════════════════════════════════════════════════════

class FormRegistry:
    """
    سجل الاستمارات المركزي — نقطة الوصول الوحيدة.
    
    الاستخدام:
        FormRegistry.get('martyr')          → FormDefinition
        FormRegistry.choices()              → [('martyr', 'شهيد'), ...]
        FormRegistry.fields('martyr')       → [FormField(...), ...]
        FormRegistry.attachments('martyr')  → [AttachmentSpec(...), ...]
        FormRegistry.validate('martyr', data) → (valid, errors)
        FormRegistry.schema('martyr')       → dict (للفرونت اند)
        FormRegistry.all_schemas()          → dict (كل الأنواع)
    """
    
    @staticmethod
    def get(form_type: str) -> Optional[FormDefinition]:
        """جلب تعريف استمارة بالنوع"""
        return _FORMS.get(form_type)
    
    @staticmethod
    def exists(form_type: str) -> bool:
        return form_type in _FORMS
    
    @staticmethod
    def all() -> dict:
        """كل التعريفات"""
        return dict(_FORMS)
    
    @staticmethod
    def _get_custom(form_type: str):
        """جلب استمارة مخصصة من DB"""
        try:
            from systems.services.models import CustomFormTemplate
            return CustomFormTemplate.objects.get(form_type=form_type, is_active=True)
        except Exception:
            return None

    @staticmethod
    def _all_custom():
        """كل الاستمارات المخصصة من DB"""
        try:
            from systems.services.models import CustomFormTemplate
            return list(CustomFormTemplate.objects.filter(is_active=True))
        except Exception:
            return []

    @staticmethod
    def types() -> list:
        """كل أنواع الاستمارات المتاحة (ثابتة + مخصصة)"""
        built_in = list(_FORMS.keys())
        custom = [c.form_type for c in FormRegistry._all_custom()]
        return built_in + [c for c in custom if c not in built_in]
    
    @staticmethod
    def choices() -> list:
        """خيارات Django choices"""
        return [(k, v.label) for k, v in _FORMS.items()]
    
    @staticmethod
    def fields(form_type: str) -> tuple:
        """حقول form_data لنوع معين"""
        defn = _FORMS.get(form_type)
        return defn.fields if defn else ()
    
    @staticmethod
    def field_keys(form_type: str) -> list:
        """مفاتيح الحقول فقط (للتحقق السريع)"""
        return [f.key for f in FormRegistry.fields(form_type)]
    
    @staticmethod
    def required_field_keys(form_type: str) -> list:
        """مفاتيح الحقول الإلزامية فقط"""
        return [f.key for f in FormRegistry.fields(form_type) if f.required]
    
    @staticmethod
    def attachments(form_type: str) -> tuple:
        """مرفقات مطلوبة لنوع معين"""
        defn = _FORMS.get(form_type)
        if defn:
            return defn.attachments
        custom = FormRegistry._get_custom(form_type)
        if custom and custom.attachments:
            return tuple(
                AttachmentSpec(a['doc_type'], a['label'], a.get('required', True))
                for a in custom.attachments
            )
        return ()
    
    @staticmethod
    def required_attachments(form_type: str) -> list:
        """المرفقات الإلزامية فقط"""
        return [a for a in FormRegistry.attachments(form_type) if a.required]
    
    @staticmethod
    def attachment_labels(form_type: str) -> list:
        """تسميات المرفقات (لعرضها في الفرونت)"""
        return [a.label for a in FormRegistry.attachments(form_type)]
    
    @staticmethod
    def validate(form_type: str, form_data: dict) -> tuple:
        """
        التحقق من بيانات الاستمارة.
        
        Returns: (is_valid: bool, errors: list[str])
        """
        defn = _FORMS.get(form_type)
        if not defn:
            return False, [f'نوع استمارة غير صالح: {form_type}']
        
        errors = []
        for f in defn.fields:
            if f.required and not form_data.get(f.key):
                errors.append(f'الحقل "{f.label}" ({f.key}) مطلوب')
        
        return len(errors) == 0, errors
    
    @staticmethod
    def schema(form_type: str) -> dict:
        """
        هيكل الاستمارة كـ JSON (للفرونت اند).
        يبحث أولاً في الثابتة ثم في المخصصة.
        """
        _APPROVAL = [
            {'level': 1, 'label': 'قسم الخدمات', 'role': 'services'},
            {'level': 2, 'label': 'مدير إدارة الموارد', 'role': 'hr'},
            {'level': 3, 'label': 'مدير عام شرطة المحافظة/الوحدة', 'role': 'director'},
        ]

        def _field_dict(f):
            return {
                'key': f.key, 'label': f.label, 'type': f.field_type,
                'required': f.required,
                'options': list(f.options) if f.options else None,
                'help_text': f.help_text or None,
                'disabled': getattr(f, 'disabled', False),
                'default': getattr(f, 'default', ''),
            }

        def _auto_sections():
            return [
                {'title': 'أولاً: البيانات الشخصية الأساسية', 'source': 'auto',
                 'fields': [_field_dict(f) for f in SECTION_PERSONAL]},
                {'title': 'ثانياً: بيانات الميلاد والإقامة', 'source': 'auto',
                 'fields': [_field_dict(f) for f in SECTION_IDENTITY]},
            ]

        # ── 1. بحث في الثابتة ──
        defn = _FORMS.get(form_type)
        if defn:
            return {
                'form_type': defn.form_type, 'label': defn.label,
                'description': defn.description, 'target_status': defn.target_status,
                'is_custom': False,
                'sections': _auto_sections() + [{
                    'title': 'ثالثاً: بيانات الحالة', 'source': 'user_input',
                    'fields': [_field_dict(f) for f in defn.fields],
                }],
                'attachments': [
                    {'doc_type': a.doc_type, 'label': a.label, 'required': a.required}
                    for a in defn.attachments
                ],
                'min_documents': defn.min_documents,
                'max_documents': defn.max_documents,
                'approval_workflow': _APPROVAL,
            }

        # ── 2. بحث في المخصصة (DB) ──
        custom = FormRegistry._get_custom(form_type)
        if not custom:
            return {}

        user_fields = [{
            'key': f['key'], 'label': f['label'], 'type': f.get('type', 'text'),
            'required': f.get('required', True),
            'options': f.get('options'), 'help_text': f.get('help_text'),
            'disabled': f.get('disabled', False),
            'default': f.get('default', ''),
            'source': f.get('source', 'user_input'),
            'options_source': f.get('options_source', ''),
        } for f in (custom.fields or [])]

        return {
            'form_type': custom.form_type, 'label': custom.label,
            'description': custom.description, 'target_status': custom.target_status,
            'is_custom': True,
            'sections': _auto_sections() + [{
                'title': 'ثالثاً: بيانات الحالة', 'source': 'user_input',
                'fields': user_fields,
            }],
            'attachments': custom.attachments or [],
            'min_documents': custom.min_documents,
            'max_documents': custom.max_documents,
            'approval_workflow': _APPROVAL,
        }

    @staticmethod
    def all_schemas() -> dict:
        """كل الاستمارات كـ JSON (ثابتة + مخصصة)"""
        return {ft: FormRegistry.schema(ft) for ft in FormRegistry.types()}
    
    @staticmethod
    def attachment_requirements_dict(form_type: str) -> dict:
        """
        تحويل المرفقات لصيغة ATTACHMENT_REQUIREMENTS المتوافقة.
        لتوحيد الصيغة مع AttachmentService.
        """
        defn = _FORMS.get(form_type)
        if not defn:
            return {}
        
        return {
            'label': defn.label,
            'required_types': [
                {
                    'type': a.doc_type,
                    'label': a.label,
                    'required': a.required,
                }
                for a in defn.attachments
            ],
            'min_documents': defn.min_documents,
            'max_documents': defn.max_documents,
        }
