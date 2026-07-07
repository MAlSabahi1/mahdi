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
            }
        }
        
        for ftype, schema in schemas.items():
            ServiceCatalog.objects.filter(form_type=ftype).update(fields_schema=schema)
            ServiceCatalog.objects.filter(code=ftype).update(fields_schema=schema) # Just in case

        print("Specific schemas updated successfully!")
