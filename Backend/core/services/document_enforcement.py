import os
import json
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class DocumentEnforcementService:
    """
    محرك تدقيق المرفقات المركزي
    يتولى التحقق من وجود المرفقات المطلوبة لأي عملية إدارية بناءً على القواعد المحددة.
    يميز بين المرفقات "المؤقتة/الجديدة" (Transactional) والمرفقات "الدائمة/الهوية" (Persistent).
    """

    def __init__(self):
        self.rules_file_path = os.path.join(
            settings.BASE_DIR, 'core', 'dictionaries', 'action_attachment_rules.json'
        )
        self.rules = self._load_rules()

    def _load_rules(self) -> dict:
        if not os.path.exists(self.rules_file_path):
            return {}
        with open(self.rules_file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def validate_action_documents(self, action_key: str, context_id: str, personnel_id: str = None):
        """
        يقوم بالتحقق من وجود جميع المرفقات المطلوبة لعملية معينة.
        
        :param action_key: مفتاح العملية (مثال: "SuggestedCorrection:name_correction")
        :param context_id: المعرف الخاص بالعملية الحالية (ID الطلب)
        :param personnel_id: معرف الفرد (للبحث عن المرفقات الدائمة كالصور الشخصية)
        :raises ValidationError: إذا كان هناك مرفقات مفقودة
        """
        if action_key not in self.rules:
            # إذا لم تكن هناك قواعد محددة لهذه العملية، نمررها بسلام (يمكن تغيير هذا السلوك ليكون أكثر صرامة)
            return

        # استيراد Document هنا لتجنب Circular Imports
        from infra.storage.models import Document

        rule_def = self.rules[action_key]
        required_docs = rule_def.get("required_documents", [])
        
        context_type = action_key.split(":")[0]  # الجزء الأول هو الموديل (مثل SuggestedCorrection)

        missing_documents = []

        for req in required_docs:
            doc_type = req.get("type")
            is_transactional = req.get("is_transactional", True)

            # 1. البحث في المستندات المرفوعة خصيصاً لهذه العملية (Transactional Search)
            has_transactional = Document.objects.filter(
                context_type=context_type,
                context_id=context_id,
                document_type=doc_type
            ).exists()

            if has_transactional:
                continue

            # 2. إذا لم يجد المرفق، وكان المرفق "دائماً" (Persistent)، نبحث في أرشيف الفرد
            if not is_transactional and personnel_id:
                has_persistent = Document.objects.filter(
                    context_type='PersonnelMaster',
                    context_id=personnel_id,
                    document_type=doc_type
                ).exists()

                if has_persistent:
                    continue

            # 3. إذا وصلنا هنا، يعني المرفق مفقود
            missing_documents.append(doc_type)

        if missing_documents:
            # يمكن جلب الأسماء المترجمة من storage.models للحصول على رسالة خطأ أوضح
            doc_choices = dict(Document.DOCUMENT_TYPE_CHOICES)
            missing_names = [str(doc_choices.get(d, d)) for d in missing_documents]
            
            error_msg = _("لا يمكن إتمام العملية. المرفقات التالية مفقودة: ") + "، ".join(missing_names)
            
            # إذا كانت بعض المرفقات transactional، يجب التوضيح أنها تتطلب رفعاً جديداً
            raise ValidationError({"documents": error_msg})

