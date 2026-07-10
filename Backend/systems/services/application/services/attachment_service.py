"""
Attachment Service — خدمة المرفقات المركزية
═══════════════════════════════════════════════════
خدمة داخلية موحدة تُستخدم من أي جزء في النظام:
- تعريف المرفقات المطلوبة لكل عملية
- التحقق من اكتمال المرفقات قبل التنفيذ
- ربط المرفقات بالسياق الصحيح
- تثبيت المرفقات عند الموافقة

الاستخدام:
    from systems.services.attachment_service import AttachmentService

    # 1. فحص المرفقات قبل تنفيذ عملية
    result = AttachmentService.validate_requirements(
        context_type='NationalIdUpdate',
        personnel=personnel_obj,
        document_ids=[5, 6],
    )
    if not result['valid']:
        return error(result['missing'])

    # 2. تثبيت المرفقات بعد الموافقة
    AttachmentService.commit_documents([5, 6])

    # 3. ربط المرفقات بعملية محددة
    AttachmentService.link_to_context(
        document_ids=[5, 6],
        context_type='SuggestedCorrection',
        context_id=42,
        related_field='national_id',
    )
"""
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


# ═══════════════════════════════════════════════════════════
# سجل المتطلبات — ما هي المرفقات المطلوبة لكل عملية؟
# ═══════════════════════════════════════════════════════════

ATTACHMENT_REQUIREMENTS = {
    # ── تعديل الرقم الوطني ──
    'NationalIdUpdate': {
        'label': 'تعديل الرقم الوطني',
        'required_types': [
            {
                'type': 'national_id_front',
                'label': 'صورة البطاقة الوطنية — الوجه الأمامي',
                'required': True,
            },
            {
                'type': 'national_id_back',
                'label': 'صورة البطاقة الوطنية — الوجه الخلفي',
                'required': True,
            },
        ],
        'min_documents': 2,
        'max_documents': 3,  # يسمح بماسح ضوئي إضافي
    },

    # ── تسوية رتبة (ترقية عادية) ──
    'RankPromotion': {
        'label': 'ترقية رتبة',
        'required_types': [
            {
                'type': 'rank_decision',
                'label': 'صورة قرار الترقية الرسمي',
                'required': True,
            },
        ],
        'min_documents': 1,
        'max_documents': 5,
    },

    # ── تسوية فرد → ضابط ──
    'PersonnelToOfficer': {
        'label': 'تسوية فرد إلى ضابط',
        'required_types': [
            {
                'type': 'settlement_decision',
                'label': 'قرار التسوية الرسمي',
                'required': True,
            },
            {
                'type': 'military_id_front',
                'label': 'البطاقة العسكرية الجديدة',
                'required': False,  # قد لا تكون متاحة وقت التسوية
            },
        ],
        'min_documents': 1,
        'max_documents': 5,
    },

    # ── تصحيح الاسم ──
    'NameCorrection': {
        'label': 'تصحيح الاسم',
        'required_types': [
            {
                'type': 'national_id_front',
                'label': 'صورة البطاقة الوطنية تحمل الاسم الصحيح',
                'required': True,
            },
        ],
        'min_documents': 1,
        'max_documents': 3,
    },

    # ── تغيير الحالة الخدمية — مصنّف حسب نوع الحالة ──
    'StatusChange_Martyr': {
        'label': 'إثبات حالة شهيد',
        'required_types': [
            {'type': 'status_change_order', 'label': 'قرار إثبات الحالة', 'required': True},
            {'type': 'medical_report', 'label': 'شهادة وفاة / تقرير طبي', 'required': True},
            {'type': 'memo', 'label': 'بلاغ عمليات', 'required': True},
        ],
        'min_documents': 3,
        'max_documents': 10,
    },
    'StatusChange_Missing': {
        'label': 'إثبات حالة مفقود',
        'required_types': [
            {'type': 'status_change_order', 'label': 'قرار إثبات الحالة', 'required': True},
            {'type': 'memo', 'label': 'بلاغ عمليات / محضر', 'required': True},
        ],
        'min_documents': 2,
        'max_documents': 10,
    },
    'StatusChange_Death': {
        'label': 'إثبات حالة وفاة طبيعية',
        'required_types': [
            {'type': 'status_change_order', 'label': 'قرار تغيير الحالة', 'required': True},
            {'type': 'medical_report', 'label': 'شهادة وفاة', 'required': True},
        ],
        'min_documents': 2,
        'max_documents': 8,
    },
    'StatusChange_Desertion': {
        'label': 'إثبات حالة فرار / هروب',
        'required_types': [
            {'type': 'status_change_order', 'label': 'قرار إثبات الحالة', 'required': True},
            {'type': 'memo', 'label': 'محضر / بلاغ', 'required': True},
        ],
        'min_documents': 2,
        'max_documents': 8,
    },
    'StatusChange_Retirement': {
        'label': 'إحالة على التقاعد',
        'required_types': [
            {'type': 'status_change_order', 'label': 'أمر الإحالة على التقاعد', 'required': True},
            {'type': 'personal_request', 'label': 'الطلب الشخصي', 'required': False},
            {'type': 'national_id_front', 'label': 'صورة البطاقة الشخصية/العسكرية', 'required': True},
        ],
        'min_documents': 2,
        'max_documents': 5,
    },

    # ─── الأنواع التالية مُعرّفة في FormRegistry (المصدر الموحد) ───
    # StatusChange_Imprisoned, StatusChange_MedicalUnfit, StatusChange_Escort,
    # StatusChange_StudyLeave, StatusChange_Seconded, StatusChange_EndOfService,
    # StatusChange_RetirementAge
    # → يتم جلبها تلقائياً عبر get_requirements() → FormRegistry.attachment_requirements_dict()


    # Fallback — أي تغيير حالة لم يُصنّف أعلاه
    'StatusChange': {
        'label': 'تغيير حالة خدمية (عام)',
        'required_types': [
            {'type': 'status_change_order', 'label': 'قرار تغيير الحالة', 'required': True},
        ],
        'min_documents': 1,
        'max_documents': 10,
    },

    # ── أمر نقل ──
    'Transfer': {
        'label': 'أمر نقل',
        'required_types': [
            {
                'type': 'transfer_order',
                'label': 'صورة أمر النقل الرسمي',
                'required': True,
            },
        ],
        'min_documents': 1,
        'max_documents': 3,
    },

    # ── مرفقات عامة (لا يوجد متطلبات محددة) ──
    'General': {
        'label': 'مرفقات عامة',
        'required_types': [],
        'min_documents': 0,
        'max_documents': 20,
    },
}


class AttachmentService:
    """
    خدمة المرفقات المركزية — تُستخدم من أي مكان في النظام.
    
    المسؤوليات:
    1. تعريف ما هو مطلوب (ATTACHMENT_REQUIREMENTS)
    2. التحقق من اكتمال المرفقات
    3. ربط المرفقات بالسياق
    4. تثبيت / أرشفة المرفقات
    5. جلب المرفقات حسب الحقل أو السياق
    """

    @staticmethod
    def get_requirements(context_type):
        """
        جلب قائمة المرفقات المطلوبة لعملية محددة.

        يدعم نوعين:
        1. عمليات غير الاستمارات (NationalIdUpdate, Transfer...) → ATTACHMENT_REQUIREMENTS
        2. استمارات إثبات الحالة (StatusChange_*) → FormRegistry (المصدر الموحد)
        """
        # ── أولاً: تحقق من القاموس الثابت ──
        reqs = ATTACHMENT_REQUIREMENTS.get(context_type)
        if reqs:
            return reqs

        # ── ثانياً: حاول عبر FormRegistry ──
        from systems.services.application.registries.form_registry import FormRegistry
        # تحويل StatusChange_Escort → escort
        form_key = context_type.replace('StatusChange_', '').lower()
        # تحويل أسماء خاصة
        _KEY_MAP = {
            'retirementage': 'retirement_age',
            'medicalunfit': 'medical_unfit',
            'endofservice': 'end_of_service',
            'studyleave': 'study_leave',
        }
        form_key = _KEY_MAP.get(form_key, form_key)

        if FormRegistry.exists(form_key):
            return FormRegistry.attachment_requirements_dict(form_key)

        return ATTACHMENT_REQUIREMENTS['General']

    @staticmethod
    def validate_requirements(context_type, document_ids=None, documents=None):
        """
        التحقق من أن المرفقات المرفوعة تلبي المتطلبات.
        
        Args:
            context_type: نوع العملية (NationalIdUpdate, RankPromotion, إلخ)
            document_ids: قائمة IDs المرفقات (يتم جلبها من DB)
            documents: أو queryset من Document objects مباشرة
            
        Returns:
            {
                'valid': True/False,
                'missing': [...],  # المرفقات الناقصة
                'errors': [...],   # أخطاء أخرى
                'documents': [...], # المرفقات المتحققة
            }
        """
        from infra.storage.models import Document

        reqs = ATTACHMENT_REQUIREMENTS.get(context_type)
        if not reqs:
            return {'valid': True, 'missing': [], 'errors': [], 'documents': []}

        # جلب المرفقات
        if documents is None and document_ids:
            documents = Document.objects.filter(id__in=document_ids)
        elif documents is None:
            documents = Document.objects.none()

        doc_list = list(documents)
        doc_types = {d.document_type for d in doc_list}

        result = {
            'valid': True,
            'missing': [],
            'errors': [],
            'documents': doc_list,
        }

        # ── فحص الحد الأدنى ──
        if len(doc_list) < reqs['min_documents']:
            result['valid'] = False
            result['errors'].append(
                f"يجب رفع {reqs['min_documents']} مرفق على الأقل. "
                f"تم رفع {len(doc_list)} فقط."
            )

        # ── فحص الحد الأقصى ──
        if len(doc_list) > reqs['max_documents']:
            result['valid'] = False
            result['errors'].append(
                f"الحد الأقصى للمرفقات هو {reqs['max_documents']}. "
                f"تم رفع {len(doc_list)}."
            )

        # ── فحص الأنواع المطلوبة ──
        for req_type in reqs['required_types']:
            if req_type['required'] and req_type['type'] not in doc_types:
                result['valid'] = False
                result['missing'].append({
                    'type': req_type['type'],
                    'label': req_type['label'],
                })

        return result

    @staticmethod
    def link_to_context(document_ids, context_type, context_id,
                        related_field=None, personnel=None):
        """
        ربط مجموعة مرفقات بسياق محدد.
        
        يُستدعى بعد إنشاء عملية (SuggestedCorrection, RankSettlement, إلخ)
        لربط المرفقات المؤقتة بها.
        """
        from infra.storage.models import Document

        docs = Document.objects.filter(id__in=document_ids)
        update_fields = ['context_type', 'context_id']

        for doc in docs:
            doc.context_type = context_type
            doc.context_id = str(context_id)
            if related_field:
                doc.related_field = related_field
                update_fields.append('related_field')
            if personnel and not doc.personnel_id:
                doc.personnel = personnel
                update_fields.append('personnel_id')

        Document.objects.bulk_update(docs, list(set(update_fields)))
        return docs.count()

    @staticmethod
    def commit_documents(document_ids):
        """
        تثبيت مرفقات (من temp → committed).
        يُستدعى عند الموافقة على عملية.
        """
        from infra.storage.models import Document

        count = Document.objects.filter(
            id__in=document_ids,
            status='temp',
        ).update(status='committed')
        
        # أرشفة تلقائية للنسخ القديمة بناءً على نوع المرفق والفرد
        AttachmentService._auto_archive_old_versions(document_ids)
        
        return count

    @staticmethod
    def _auto_archive_old_versions(new_document_ids):
        """
        أرشفة المرفقات القديمة التي تشارك نفس الحقل (related_field)
        ونفس النوع لنفس الفرد، لكي لا تتراكم وتختلط في أرشيف الفرد.
        """
        from infra.storage.models import Document
        
        new_docs = Document.objects.filter(id__in=new_document_ids, status='committed')
        for doc in new_docs:
            if not doc.personnel_id or not doc.related_field:
                continue
                
            # جلب كل المرفقات القديمة لنفس الفرد ونفس الحقل
            # ما عدا المرفق الجديد نفسه
            old_docs = Document.objects.filter(
                personnel_id=doc.personnel_id,
                related_field=doc.related_field,
                document_type=doc.document_type,
                status='committed'
            ).exclude(id=doc.id)
            
            if old_docs.exists():
                old_docs.update(status='archived')

    @staticmethod
    def archive_documents(document_ids):
        """
        أرشفة مرفقات (committed → archived).
        يُستدعى عند استبدال مرفق.
        """
        from infra.storage.models import Document

        count = Document.objects.filter(
            id__in=document_ids,
        ).exclude(status='archived').update(status='archived')
        return count

    @staticmethod
    def get_by_field(personnel, field_name, status='committed'):
        """
        جلب مرفقات فرد حسب الحقل المرتبط.
        
        مثال: AttachmentService.get_by_field(personnel, 'national_id')
        → يرجع صور البطاقة الوطنية فقط
        """
        from infra.storage.models import Document

        return Document.objects.filter(
            personnel=personnel,
            related_field=field_name,
            status=status,
        ).order_by('-version', '-created_at')

    @staticmethod
    def get_by_context(context_type, context_id, status='committed'):
        """
        جلب مرفقات حسب السياق.
        
        مثال: AttachmentService.get_by_context('RankSettlement', 5)
        → يرجع مرفقات طلب التسوية رقم 5
        """
        from infra.storage.models import Document

        return Document.objects.filter(
            context_type=context_type,
            context_id=str(context_id),
            status=status,
        ).order_by('-created_at')

    @staticmethod
    def get_latest_by_type(personnel, document_type):
        """
        جلب آخر نسخة من مرفق بنوع محدد.
        
        مثال: AttachmentService.get_latest_by_type(personnel, 'national_id_front')
        → يرجع آخر نسخة مثبتة من صورة البطاقة الأمامية
        """
        from infra.storage.models import Document

        return Document.objects.filter(
            personnel=personnel,
            document_type=document_type,
            status='committed',
        ).order_by('-version').first()
