from django.core.management.base import BaseCommand
from systems.services.models import ServiceCatalog

class Command(BaseCommand):
    def handle(self, *args, **options):
        # 1. Corrections
        c_schema = {
            "label": "طلب تصحيح بيانات",
            "sections": [
                {
                    "title": "بيانات التصحيح",
                    "source": "user_input",
                    "fields": [
                        {"key": "correction_type", "label": "نوع التصحيح", "type": "select", "required": True, "options": [
                            {"value": "name_correction", "label": "تصحيح الاسم"},
                            {"value": "national_id_correction", "label": "تصحيح الرقم الوطني"},
                            {"value": "military_number_correction", "label": "تصحيح الرقم العسكري"}
                        ]},
                        {"key": "field_name", "label": "اسم الحقل المراد تصحيحه", "type": "select", "required": True, "options": [
                            {"value": "full_name", "label": "الاسم الكامل"},
                            {"value": "national_id", "label": "الرقم الوطني"},
                            {"value": "military_number", "label": "الرقم العسكري"},
                            {"value": "birth_date", "label": "تاريخ الميلاد"},
                            {"value": "join_date", "label": "تاريخ الانتساب"},
                            {"value": "phone_number", "label": "رقم الهاتف"}
                        ]},
                        {"key": "old_value", "label": "القيمة الحالية (تُملأ تلقائياً)", "type": "text", "required": False, "disabled": True},
                        {"key": "new_value", "label": "القيمة الجديدة الصحيحة", "type": "text", "required": True},
                        {"key": "notes", "label": "ملاحظات إضافية", "type": "textarea", "required": False}
                    ]
                }
            ],
            "attachments": [
                {"doc_type": "official_doc", "label": "الوثيقة الرسمية المثبتة", "required": True}
            ]
        }
        ServiceCatalog.objects.filter(service_type='correction').update(fields_schema=c_schema)

        # 2. Rank Settlements
        r_schema = {
            "label": "طلب ترقية / تسوية",
            "sections": [
                {
                    "title": "بيانات القرار",
                    "source": "user_input",
                    "fields": [
                        {"key": "settlement_type", "label": "نوع التسوية", "type": "select", "required": True, "options": [
                            {"value": "same_class_promotion", "label": "ترقية ضمن نفس الصنف"},
                            {"value": "personnel_to_officer", "label": "تسوية فرد إلى ضابط"},
                            {"value": "demotion", "label": "تخفيض رتبة (عقوبة/قرار قرار قضائي)"}
                        ]},
                        {"key": "to_rank", "label": "الرتبة المستهدفة", "type": "select", "required": True},
                        {"key": "decision_number", "label": "رقم القرار/المذكرة", "type": "text", "required": True},
                        {"key": "decision_date", "label": "تاريخ القرار", "type": "date", "required": True},
                        {"key": "due_date", "label": "تاريخ الاستحقاق", "type": "date", "required": True},
                        {"key": "new_military_number", "label": "الرقم العسكري الجديد (في حال التسوية للضباط)", "type": "text", "required": False},
                        {"key": "notes", "label": "ملاحظات", "type": "textarea", "required": False}
                    ]
                }
            ],
            "attachments": [
                {"doc_type": "decision_copy", "label": "صورة القرار الوزاري/الإداري", "required": True}
            ]
        }
        ServiceCatalog.objects.filter(service_type='rank_settlement').update(fields_schema=r_schema)

        # 3. Disciplinary
        d_schema = {
            "label": "إجراء تأديبي / جزاء",
            "sections": [
                {
                    "title": "بيانات الجزاء",
                    "source": "user_input",
                    "fields": [
                        {"key": "decision_ref", "label": "رقم/مرجع القرار", "type": "text", "required": True},
                        {"key": "issued_date", "label": "تاريخ الإصدار", "type": "date", "required": True},
                        {"key": "duration_days", "label": "المدة بالأيام (إن وجدت)", "type": "number", "required": False},
                        {"key": "description", "label": "وصف المخالفة/الجزاء", "type": "textarea", "required": True}
                    ]
                }
            ],
            "attachments": [
                {"doc_type": "punishment_doc", "label": "صورة قرار الجزاء", "required": True}
            ]
        }
        ServiceCatalog.objects.filter(service_type='disciplinary').update(fields_schema=d_schema)
        
        # 4. Security & Others
        s_schema = {
            "label": "طلب خدمة",
            "sections": [
                {
                    "title": "تفاصيل الطلب",
                    "source": "user_input",
                    "fields": [
                        {"key": "notes", "label": "التفاصيل", "type": "textarea", "required": True}
                    ]
                }
            ],
            "attachments": []
        }
        ServiceCatalog.objects.filter(service_type__in=['security', 'other']).update(fields_schema=s_schema)

        print("Schemas updated successfully!")
