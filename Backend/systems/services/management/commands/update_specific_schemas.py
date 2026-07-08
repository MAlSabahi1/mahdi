import json
from django.core.management.base import BaseCommand
from systems.services.models import ServiceCatalog

class Command(BaseCommand):
    def handle(self, *args, **options):
        schemas = {
            'name_correction': {
                "label": "طلب تصحيح الاسم",
                "sections": [{
                    "title": "بيانات التصحيح",
                    "source": "user_input",
                    "fields": [
                        {"key": "old_value", "label": "الاسم الحالي (الخاطئ)", "type": "text", "required": False},
                        {"key": "new_value", "label": "الاسم الجديد الصحيح", "type": "text", "required": True},
                        {"key": "reason", "label": "ملاحظات", "type": "textarea", "required": False}
                    ]
                }],
                "attachments": [
                    {"doc_type": "form_23", "label": "نموذج 23", "required": True},
                    {"doc_type": "national_id", "label": "صورة البطاقة الشخصية", "required": True}
                ]
            },
            'national_id_correction': {
                "label": "طلب تصحيح الرقم الوطني",
                "sections": [{
                    "title": "بيانات التصحيح",
                    "source": "user_input",
                    "fields": [
                        {"key": "old_value", "label": "الرقم الوطني الحالي (إن وجد)", "type": "text", "required": False},
                        {"key": "new_value", "label": "الرقم الوطني الجديد (11 رقم)", "type": "text", "required": True},
                        {"key": "reason", "label": "ملاحظات", "type": "textarea", "required": False}
                    ]
                }],
                "attachments": [
                    {"doc_type": "national_id", "label": "صورة البطاقة الوطنية (أمام + خلف)", "required": True}
                ]
            },
            'military_number_correction': {
                "label": "طلب تصحيح الرقم العسكري",
                "sections": [{
                    "title": "بيانات التصحيح",
                    "source": "user_input",
                    "fields": [
                        {"key": "old_value", "label": "الرقم العسكري الحالي (الخاطئ)", "type": "text", "required": False},
                        {"key": "new_value", "label": "الرقم العسكري الجديد الصحيح", "type": "text", "required": True},
                        {"key": "reason", "label": "ملاحظات", "type": "textarea", "required": False}
                    ]
                }],
                "attachments": [
                    {"doc_type": "ministerial_decree", "label": "قرار وزاري رسمي", "required": True}
                ]
            },
            'linked_military_swap': {
                "label": "طلب التبديل المترابط للأرقام العسكرية",
                "sections": [{
                    "title": "بيانات التبديل",
                    "source": "user_input",
                    "fields": [
                        {"key": "new_value", "label": "الرقم العسكري للطرف الثاني", "type": "text", "required": True},
                        {"key": "reason", "label": "سبب التبديل", "type": "textarea", "required": True}
                    ]
                }],
                "attachments": [
                    {"doc_type": "official_decree", "label": "قرار رسمي يثبت التبديل", "required": True}
                ]
            },
            'rank_promotion': {
                "label": "ترقية ضمن نفس الصنف",
                "sections": [{
                    "title": "بيانات القرار",
                    "source": "user_input",
                    "fields": [
                        {"key": "to_rank", "label": "الرتبة المستهدفة", "type": "text", "required": True},
                        {"key": "decision_number", "label": "رقم القرار", "type": "text", "required": True},
                        {"key": "decision_date", "label": "تاريخ القرار", "type": "date", "required": True},
                        {"key": "notes", "label": "ملاحظات", "type": "textarea", "required": False}
                    ]
                }],
                "attachments": [
                    {"doc_type": "promotion_decree", "label": "صورة قرار الترقية", "required": True}
                ]
            },
            'personnel_to_officer': {
                "label": "تسوية فرد إلى ضابط",
                "sections": [{
                    "title": "بيانات قرار التسوية",
                    "source": "user_input",
                    "fields": [
                        {"key": "to_rank", "label": "الرتبة المستهدفة (ضابط)", "type": "text", "required": True},
                        {"key": "new_military_number", "label": "الرقم العسكري الجديد (يجب أن يبدأ بـ 60)", "type": "text", "required": True},
                        {"key": "decision_number", "label": "رقم القرار", "type": "text", "required": True},
                        {"key": "decision_date", "label": "تاريخ القرار", "type": "date", "required": True},
                        {"key": "notes", "label": "ملاحظات", "type": "textarea", "required": False}
                    ]
                }],
                "attachments": [
                    {"doc_type": "settlement_decree", "label": "صورة قرار التسوية", "required": True}
                ]
            },
            'disciplinary': {
                "label": "طلب جزاء / إجراء تأديبي",
                "sections": [{
                    "title": "بيانات الجزاء",
                    "source": "user_input",
                    "fields": [
                        {"key": "action_type", "label": "نوع الجزاء", "type": "select", "options": ["توقيف", "خصم", "إنذار", "توبيخ", "عزل"], "required": True},
                        {"key": "decision_ref", "label": "رقم القرار التأديبي", "type": "text", "required": True},
                        {"key": "issued_date", "label": "تاريخ الإصدار", "type": "date", "required": True},
                        {"key": "effective_date", "label": "تاريخ السريان", "type": "date", "required": True},
                        {"key": "duration_days", "label": "مدة الجزاء بالأيام (إن وجد)", "type": "number", "required": False},
                        {"key": "description", "label": "وصف المخالفة", "type": "textarea", "required": True}
                    ]
                }],
                "attachments": [
                    {"doc_type": "disciplinary_decree", "label": "صورة قرار الجزاء", "required": True}
                ]
            },
            'retirement_age': {
                "label": "إثبات حالة (بلوغ السن القانوني)",
                "sections": [{
                    "title": "بيانات الحالة",
                    "source": "user_input",
                    "fields": [
                        {"key": "category", "label": "الفئة", "type": "text", "required": True, "disabled": True, "value": "كبار سن"},
                        {"key": "age", "label": "العمر", "type": "number", "required": True},
                        {"key": "gender", "label": "الجنس", "type": "select", "options": [{"value": "M", "label": "ذكر"}, {"value": "F", "label": "أنثى"}], "required": True}
                    ]
                }],
                "attachments": [
                    {"doc_type": "personal_request", "label": "الطلب الشخصي المقدم من المذكور", "required": True},
                    {"doc_type": "certified_id", "label": "نسخة من البطاقة العسكرية والشخصية معمدة", "required": True}
                ]
            },
            'death': {
                "label": "إثبات حالة (متوفى)",
                "sections": [{
                    "title": "بيانات الوفاة",
                    "source": "user_input",
                    "fields": [
                        {"key": "category", "label": "الفئة", "type": "text", "required": True, "disabled": True, "value": "وفيات"},
                        {"key": "status_type", "label": "نوع الحالة", "type": "text", "required": True},
                        {"key": "incident_status", "label": "حالة الوقوع", "type": "text", "required": False},
                        {"key": "death_date", "label": "تاريخ الوفاة", "type": "date", "required": True},
                        {"key": "death_reason", "label": "سبب الوفاة", "type": "text", "required": True},
                        {"key": "death_place", "label": "مكان الوفاة", "type": "text", "required": True},
                        {"key": "notes", "label": "ملاحظات", "type": "textarea", "required": False}
                    ]
                }],
                "attachments": [
                    {"doc_type": "death_certificate", "label": "شهادة الوفاة", "required": True},
                    {"doc_type": "heirs_certificate", "label": "حكم انحصار الورثة", "required": True},
                    {"doc_type": "legal_power_of_attorney", "label": "وكالة شرعية", "required": True},
                    {"doc_type": "deceased_id", "label": "صورة البطاقة الشخصية/العسكرية", "required": True},
                    {"doc_type": "agent_id", "label": "صورة البطاقة الشخصية للوكيل", "required": True},
                    {"doc_type": "guardianship_ruling", "label": "حكم التنصيب", "required": True}
                ]
            },
            'missing': {
                "label": "إثبات حالة (مفقود)",
                "sections": [{
                    "title": "تفاصيل الفقدان",
                    "source": "user_input",
                    "fields": [
                        {"key": "category", "label": "الفئة", "type": "text", "required": True, "disabled": True, "value": "مفقودين"},
                        {"key": "procedure_status", "label": "حالة الإجراءات", "type": "select", "options": ["مستكمل", "غير مستكمل"], "required": True},
                        {"key": "missing_place", "label": "محل الفقدان", "type": "text", "required": True},
                        {"key": "missing_date", "label": "تاريخ الفقدان", "type": "date", "required": True},
                        {"key": "ruling_date", "label": "تاريخ الحكم (إن وجد)", "type": "date", "required": False},
                        {"key": "notes", "label": "ملاحظات", "type": "textarea", "required": False}
                    ]
                }],
                "attachments": [
                    {"doc_type": "missing_report", "label": "بلاغ الفقدان", "required": True},
                    {"doc_type": "heirs_certificate", "label": "حكم انحصار الورثة", "required": True},
                    {"doc_type": "legal_power_of_attorney", "label": "وكالة شرعية", "required": True},
                    {"doc_type": "personnel_id", "label": "صورة البطاقة الشخصية/العسكرية", "required": True},
                    {"doc_type": "agent_id", "label": "صورة البطاقة الشخصية للوكيل", "required": True},
                    {"doc_type": "newspaper_ad", "label": "إعلان الجريدة", "required": True},
                    {"doc_type": "legal_ruling", "label": "حكم شرعي بالفقدان", "required": True}
                ]
            },
            'medical_unfit': {
                "label": "إثبات حالة (عدم اللياقة الصحية)",
                "sections": [{
                    "title": "بيانات الحالة الصحية",
                    "source": "user_input",
                    "fields": [
                        {"key": "category", "label": "الفئة", "type": "text", "required": True, "disabled": True, "value": "عدم اللياقة الصحية"},
                        {"key": "disease_type", "label": "نوع المرض أو الإصابة", "type": "text", "required": True},
                        {"key": "decision_source", "label": "مصدر القرار", "type": "text", "required": True},
                        {"key": "disability_percentage", "label": "نسبة العجز", "type": "number", "required": True},
                        {"key": "reason", "label": "سبب الحالة", "type": "text", "required": True},
                        {"key": "notes", "label": "ملاحظات", "type": "textarea", "required": False}
                    ]
                }],
                "attachments": [
                    {"doc_type": "original_medical_decision", "label": "القرار الطبي الأصل", "required": True},
                    {"doc_type": "personnel_id", "label": "صورة البطاقة الشخصية/العسكرية", "required": True},
                    {"doc_type": "recent_photo", "label": "صورة حديثة للمريض", "required": True},
                    {"doc_type": "legal_power_of_attorney", "label": "وكالة شرعية", "required": True},
                    {"doc_type": "agent_id", "label": "صورة البطاقة الشخصية للوكيل", "required": True}
                ]
            },
            'end_of_service': {
                "label": "إثبات حالة (إنهاء مدة)",
                "sections": [{
                    "title": "بيانات إنهاء المدة",
                    "source": "user_input",
                    "fields": [
                        {"key": "category", "label": "الفئة", "type": "text", "required": True, "disabled": True, "value": "إنهاء مدة"},
                        {"key": "birth_date", "label": "تاريخ الميلاد", "type": "date", "required": True},
                        {"key": "join_date", "label": "تاريخ الالتحاق", "type": "date", "required": True},
                        {"key": "age", "label": "العمر", "type": "number", "required": True},
                        {"key": "gender", "label": "الجنس", "type": "select", "options": [{"value": "M", "label": "ذكر"}, {"value": "F", "label": "أنثى"}], "required": True},
                        {"key": "notes", "label": "ملاحظات", "type": "textarea", "required": False}
                    ]
                }],
                "attachments": [
                    {"doc_type": "personal_request", "label": "الطلب الشخصي المقدم من المذكور", "required": True},
                    {"doc_type": "certified_id", "label": "نسخة من البطاقة العسكرية والشخصية معمدة", "required": True}
                ]
            },
            'retired': {
                "label": "إثبات حالة (محال للتقاعد)",
                "sections": [{
                    "title": "بيانات الإحالة",
                    "source": "user_input",
                    "fields": [
                        {"key": "category", "label": "الفئة", "type": "text", "required": True, "disabled": True, "value": "محال للتقاعد"},
                        {"key": "decision_number", "label": "رقم قرار الإحالة", "type": "text", "required": True},
                        {"key": "decision_date", "label": "تاريخ قرار الإحالة", "type": "date", "required": True},
                        {"key": "retirement_date", "label": "تاريخ الإحالة (الفعلي)", "type": "date", "required": True},
                        {"key": "notes", "label": "ملاحظات", "type": "textarea", "required": False}
                    ]
                }],
                "attachments": [
                    {"doc_type": "personal_request", "label": "الطلب الشخصي المقدم من المذكور", "required": False},
                    {"doc_type": "certified_id", "label": "نسخة معمدة من البطاقة العسكرية والبطاقة الشخصية", "required": True}
                ]
            },
            'imprisoned': {
                "label": "إثبات حالة (مسجون)",
                "sections": [{
                    "title": "البيانات القانونية",
                    "source": "user_input",
                    "fields": [
                        {"key": "category", "label": "الفئة", "type": "text", "required": True, "disabled": True, "value": "سجناء"},
                        {"key": "case_type", "label": "نوع القضية", "type": "text", "required": True},
                        {"key": "ruling_date", "label": "تاريخ الحكم", "type": "date", "required": False},
                        {"key": "ruling_duration", "label": "مدة الحكم", "type": "text", "required": False},
                        {"key": "arrest_date", "label": "تاريخ التوقيف", "type": "date", "required": True},
                        {"key": "arrest_authority", "label": "جهة التوقيف", "type": "text", "required": True},
                        {"key": "notes", "label": "ملاحظات", "type": "textarea", "required": False}
                    ]
                }],
                "attachments": [
                    {"doc_type": "ruling_copy", "label": "نسخة من الحكم (إن وجد)", "required": False},
                    {"doc_type": "prosecution_memo", "label": "مذكرة من النيابة", "required": False},
                    {"doc_type": "personnel_id", "label": "صورة البطاقة الشخصية/العسكرية", "required": True},
                    {"doc_type": "legal_power_of_attorney", "label": "وكالة شرعية", "required": True},
                    {"doc_type": "agent_id", "label": "صورة البطاقة الشخصية للوكيل", "required": True}
                ]
            },
            'escort': {
                "label": "إثبات حالة (مرافق)",
                "sections": [{
                    "title": "بيانات المرافقة",
                    "source": "user_input",
                    "fields": [
                        {"key": "category", "label": "الفئة", "type": "text", "required": True, "disabled": True, "value": "المعيات"},
                        {"key": "vip_name", "label": "اسم الشخصية", "type": "text", "required": True},
                        {"key": "vip_position", "label": "منصب الشخصية", "type": "text", "required": True},
                        {"key": "order_source", "label": "مصدر الأمر", "type": "text", "required": True},
                        {"key": "start_date", "label": "تاريخ البدء", "type": "date", "required": True},
                        {"key": "end_date", "label": "تاريخ الانتهاء", "type": "date", "required": True}
                    ]
                }],
                "attachments": [
                    {"doc_type": "order_copy", "label": "نسخة من الأمر الصادر بالتكليف", "required": True},
                    {"doc_type": "certified_id", "label": "نسخة من البطاقة العسكرية والشخصية معمدة", "required": True}
                ]
            },
            'martyr': {
                "label": "إثبات حالة (شهيد)",
                "sections": [{
                    "title": "تفاصيل الاستشهاد",
                    "source": "user_input",
                    "fields": [
                        {"key": "category", "label": "الفئة", "type": "text", "required": True, "disabled": True, "value": "الشهداء"},
                        {"key": "martyrdom_date", "label": "تاريخ الاستشهاد", "type": "date", "required": True},
                        {"key": "martyrdom_reason", "label": "سبب الاستشهاد", "type": "text", "required": True},
                        {"key": "martyrdom_place", "label": "مكان الاستشهاد", "type": "text", "required": True},
                        {"key": "notes", "label": "ملاحظات", "type": "textarea", "required": False}
                    ]
                }],
                "attachments": [
                    {"doc_type": "death_certificate", "label": "شهادة الوفاة", "required": True},
                    {"doc_type": "heirs_certificate", "label": "حكم انحصار الورثة", "required": True},
                    {"doc_type": "legal_power_of_attorney", "label": "وكالة شرعية", "required": True},
                    {"doc_type": "deceased_id", "label": "صورة البطاقة الشخصية/العسكرية للشهيد", "required": True},
                    {"doc_type": "agent_id", "label": "صورة البطاقة الشخصية للوكيل", "required": True},
                    {"doc_type": "guardianship_ruling", "label": "حكم التنصيب", "required": True},
                    {"doc_type": "operations_report", "label": "بلاغ العمليات", "required": True},
                    {"doc_type": "mission_order", "label": "أمر التكليف بالمهمة", "required": True}
                ]
            },
            'study_leave': {
                "label": "إثبات حالة (مفرغ للدراسة)",
                "sections": [{
                    "title": "المسار الأكاديمي",
                    "source": "user_input",
                    "fields": [
                        {"key": "category", "label": "الفئة", "type": "text", "required": True, "disabled": True, "value": "مفرغين للدراسة"},
                        {"key": "study_type", "label": "نوع الدراسة", "type": "text", "required": True},
                        {"key": "study_place", "label": "مكان الدراسة", "type": "text", "required": True},
                        {"key": "order_source", "label": "مصدر الأمر", "type": "text", "required": True},
                        {"key": "duration", "label": "مدة الدراسة", "type": "text", "required": True},
                        {"key": "start_date", "label": "تاريخ البدء", "type": "date", "required": True},
                        {"key": "end_date", "label": "تاريخ الانتهاء", "type": "date", "required": True}
                    ]
                }],
                "attachments": [
                    {"doc_type": "study_order_copy", "label": "نسخة من الأمر الصادر بالتفرغ الدراسي", "required": True},
                    {"doc_type": "certified_id", "label": "نسخة معمدة من البطاقة العسكرية والشخصية", "required": True}
                ]
            },
            'seconded': {
                "label": "إثبات حالة (منتدب)",
                "sections": [{
                    "title": "تفاصيل الانتداب",
                    "source": "user_input",
                    "fields": [
                        {"key": "category", "label": "الفئة", "type": "text", "required": True, "disabled": True, "value": "المنتدبين"},
                        {"key": "secondment_place", "label": "جهة الانتداب", "type": "text", "required": True},
                        {"key": "reason", "label": "سبب الانتداب", "type": "text", "required": True},
                        {"key": "order_source", "label": "مصدر الأمر", "type": "text", "required": True},
                        {"key": "start_date", "label": "تاريخ البدء", "type": "date", "required": True},
                        {"key": "end_date", "label": "تاريخ الانتهاء", "type": "date", "required": True}
                    ]
                }],
                "attachments": [
                    {"doc_type": "secondment_order_copy", "label": "نسخة من الأمر الصادر بالانتداب", "required": True},
                    {"doc_type": "certified_id", "label": "نسخة معمدة من البطاقة العسكرية والشخصية", "required": True}
                ]
            }
        }
        
        for ftype, schema in schemas.items():
            ServiceCatalog.objects.filter(form_type=ftype).update(fields_schema=schema)
            ServiceCatalog.objects.filter(code=ftype).update(fields_schema=schema) # Just in case

        print("Specific schemas updated successfully!")
