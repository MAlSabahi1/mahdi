from datetime import date
from dateutil.relativedelta import relativedelta
from systems.services.service_rules.core import ServiceRule, ServiceValidationContext

class EndOfServiceTemporalRule(ServiceRule):
    """
    [EOS-001] قواعد التحقق الزمني والمقاييس العمرية لإنهاء المدة.
    """
    name = 'التحقق من تواريخ الميلاد والالتحاق (إنهاء مدة)'
    description = 'يضمن ألا تكون التواريخ في المستقبل، وأن الخدمة 20 عاماً على الأقل.'

    def check(self, ctx: ServiceValidationContext) -> None:
        today = date.today()
        
        # استخراج التواريخ من النموذج إذا تم توفيرها، وإلا من ملف الفرد
        form_birth_str = ctx.form_data.get('birth_date')
        form_join_str = ctx.form_data.get('join_date')
        
        personnel = ctx.personnel
        
        birth_date = self._parse_date(form_birth_str) if form_birth_str else personnel.birth_date
        join_date = self._parse_date(form_join_str) if form_join_str else personnel.join_date

        if not birth_date:
            ctx.add_error(
                code='MISSING_BIRTH_DATE',
                field='birth_date',
                message='تاريخ الميلاد مفقود. يجب تحديد تاريخ الميلاد لحساب العمر.',
                details='يرجى إدخال تاريخ الميلاد في الاستمارة.'
            )
        
        if not join_date:
            ctx.add_error(
                code='MISSING_JOIN_DATE',
                field='join_date',
                message='تاريخ الالتحاق مفقود. يجب تحديده لحساب مدة الخدمة (شرط 20 سنة).',
                details='يرجى إدخال تاريخ الالتحاق بالخدمة.'
            )
            
        if not birth_date or not join_date:
            return

        # 1. منع التواريخ المستقبلية
        if birth_date > today:
            ctx.add_error('FUTURE_BIRTH_DATE', 'birth_date', 'تاريخ الميلاد لا يمكن أن يكون في المستقبل.')
        if join_date > today:
            ctx.add_error('FUTURE_JOIN_DATE', 'join_date', 'تاريخ الالتحاق لا يمكن أن يكون في المستقبل.')

        if birth_date > today or join_date > today:
            return

        # 2. التحقق من المنطق بين الميلاد والالتحاق (العمر عند التجنيد)
        age_at_join = relativedelta(join_date, birth_date).years
        if age_at_join < 15:
            ctx.add_error(
                code='INVALID_AGE_AT_JOIN',
                field='join_date',
                message=f'تاريخ الالتحاق غير منطقي مقارنة بتاريخ الميلاد. العمر عند الالتحاق كان ({age_at_join}) سنة.',
                details='يجب أن يكون العمر عند الالتحاق 15 سنة على الأقل ليكون التاريخ صحيحاً.'
            )

        # 3. التحقق من شرط 20 سنة خدمة
        service_duration = relativedelta(today, join_date)
        if service_duration.years < 20:
            ctx.add_error(
                code='INSUFFICIENT_SERVICE_DURATION',
                field='join_date',
                message=f'لا يمكن إنهاء المدة. الخدمة الفعلية للفرد هي ({service_duration.years} سنوات و {service_duration.months} أشهر).',
                details='الحد الأدنى لإنهاء المدة هو 20 سنة خدمة فعلية.'
            )

class EndOfServiceAttachmentsRule(ServiceRule):
    """
    [EOS-002] التحقق من المرفقات الإلزامية.
    """
    name = 'اكتمال المرفقات الأساسية (إنهاء مدة)'
    description = 'يفرض رفع المرفقات الأساسية.'

    def check(self, ctx: ServiceValidationContext) -> None:
        if not ctx.uploaded_attachments:
            ctx.add_warning(
                code='NO_ATTACHMENTS_YET',
                field='attachments',
                message='لم يتم رفع أي مرفقات حتى الآن. يفضل إرفاق الطلب الشخصي والبطاقة قبل التقديم النهائي.',
                details=''
            )
            return
            
        uploaded_types = [att.attachment_type for att in ctx.uploaded_attachments]
        
        required = [
            ('personal_request', 'الطلب الشخصي'),
            ('national_id_front', 'صورة البطاقة')
        ]
        
        missing = [lbl for key, lbl in required if key not in uploaded_types]
        if missing:
            ctx.add_warning(
                code='MISSING_REQUIRED_ATTACHMENT',
                field='attachments',
                message=f'بعض المرفقات الأساسية مفقودة: {", ".join(missing)}',
                details='سيتمكن النظام من حفظ الاستمارة، لكنها قد تتعرقل في دورة الاعتماد إذا استمر النقص.'
            )

# ── قائمة القواعد ──────────────────────────
END_OF_SERVICE_FORM_RULES = [
    EndOfServiceTemporalRule(),
    EndOfServiceAttachmentsRule(),
]
