from datetime import date, datetime
from systems.services.service_rules.core import ServiceRule, ServiceValidationContext

class MedicalUnfitTemporalRule(ServiceRule):
    """
    [MU-001] قواعد التحقق الزمني لاستمارة عدم اللياقة.
    """
    name = 'التحقق من تاريخ الوقوع (عدم اللياقة)'
    description = 'يمنع إدخال تواريخ مستقبلية، ويتحقق من تاريخ الالتحاق إذا كان السبب "أثناء الواجب".'

    def check(self, ctx: ServiceValidationContext) -> None:
        today = date.today()
        injury_date_str = ctx.form_data.get('injury_date')
        injury_context = ctx.form_data.get('injury_context')
        personnel = ctx.personnel

        if not injury_date_str:
            return  # سيتم التقاطها كحقل ناقص في القواعد الأخرى

        try:
            injury_date = datetime.strptime(str(injury_date_str)[:10], '%Y-%m-%d').date()
        except ValueError:
            ctx.add_error(
                code='INVALID_DATE_FORMAT',
                field='injury_date',
                message='صيغة تاريخ الوقوع غير صحيحة.',
            )
            return

        if injury_date > today:
            ctx.add_error(
                code='FUTURE_INJURY_DATE',
                field='injury_date',
                message='لا يمكن أن يكون تاريخ الوقوع في المستقبل.',
            )
        
        if injury_context == 'أثناء الواجب' and personnel.join_date:
            if injury_date < personnel.join_date:
                ctx.add_error(
                    code='INJURY_BEFORE_JOIN_DATE',
                    field='injury_date',
                    message=f"لا يمكن أن يكون تاريخ الوقوع ({injury_date_str}) قبل تاريخ الالتحاق بالخدمة ({personnel.join_date.strftime('%Y-%m-%d')}) إذا كانت الإصابة 'أثناء الواجب'.",
                )

class MedicalUnfitFieldsRule(ServiceRule):
    """
    [MU-002] قواعد التحقق من الحقول الإجبارية الطبية.
    """
    name = 'التحقق من البيانات الطبية ونسبة العجز'
    description = 'يضمن إدخال نوع المرض، مصدر القرار، وأن نسبة العجز صحيحة (1-100).'

    def check(self, ctx: ServiceValidationContext) -> None:
        disease_type = ctx.form_data.get('disease_type')
        if not disease_type or len(str(disease_type).strip()) < 3:
            ctx.add_error(
                code='INVALID_DISEASE_TYPE',
                field='disease_type',
                message='يجب إدخال نوع المرض أو الإصابة بشكل واضح.',
            )

        medical_source = ctx.form_data.get('medical_source')
        if not medical_source or len(str(medical_source).strip()) < 3:
            ctx.add_error(
                code='INVALID_MEDICAL_SOURCE',
                field='medical_source',
                message='يجب تحديد مصدر القرار الطبي (اللجنة الطبية).',
            )

        disability_percentage = ctx.form_data.get('disability_percentage')
        if disability_percentage is not None and str(disability_percentage).strip() != '':
            try:
                perc = int(disability_percentage)
                if perc <= 0 or perc > 100:
                    ctx.add_error(
                        code='INVALID_DISABILITY_PERCENTAGE',
                        field='disability_percentage',
                        message=f'نسبة العجز يجب أن تكون رقماً بين 1 و 100 (تم إدخال: {perc}).',
                    )
            except ValueError:
                ctx.add_error(
                    code='INVALID_DISABILITY_PERCENTAGE_FORMAT',
                    field='disability_percentage',
                    message='نسبة العجز يجب أن تكون رقماً صحيحاً.',
                )

class MedicalUnfitAttachmentsRule(ServiceRule):
    """
    [MU-003] التحقق من اكتمال وتطابق المرفقات الخاصة بعدم اللياقة.
    """
    name = 'التحقق من المرفقات الإلزامية (عدم اللياقة)'
    description = 'يضمن رفع القرار الطبي، البطاقة، وكالة شرعية وبطاقة الوكيل.'

    # المرفقات الإلزامية لاستمارة عدم لياقة
    REQUIRED_ATTACHMENTS = {
        'medical_report': 'القرار الطبي الأصل',
        'national_id_front': 'صورة البطاقة العسكرية والشخصية',
        'power_of_attorney': 'الوكالة الشرعية',
        'attorney_id': 'صورة بطاقة الوكيل',
    }

    def check(self, ctx: ServiceValidationContext) -> None:
        if not ctx.uploaded_attachments:
            ctx.add_warning(
                code='NO_ATTACHMENTS_YET',
                field='attachments',
                message='لم يتم رفع أي مرفقات. يجب رفع القرار الطبي والوكالة الشرعية والبطائق قبل التقديم.',
            )
            return

        # فحص تطابق الوكيل
        has_poa = 'power_of_attorney' in ctx.uploaded_attachments
        has_attorney_id = 'attorney_id' in ctx.uploaded_attachments

        if has_poa and not has_attorney_id:
            ctx.add_error(
                code='MISSING_ATTORNEY_ID',
                field='attachments',
                message='يجب إرفاق صورة بطاقة الوكيل طالما أرفقت الوكالة الشرعية.',
            )
        if has_attorney_id and not has_poa:
            ctx.add_error(
                code='MISSING_POWER_OF_ATTORNEY',
                field='attachments',
                message='يجب إرفاق الوكالة الشرعية طالما أرفقت بطاقة الوكيل.',
            )

        # فحص النواقص
        missing = []
        for att_code, att_label in self.REQUIRED_ATTACHMENTS.items():
            if att_code not in ctx.uploaded_attachments:
                missing.append(att_label)

        if missing:
            missing_str = '، '.join(missing)
            ctx.add_error(
                code='INCOMPLETE_ATTACHMENTS',
                field='attachments',
                message=f'لا يمكن تقديم الطلب. المرفقات التالية ناقصة: {missing_str}.',
            )

# ── تصدير القواعد لاستخدامها في Dispatcher ──
MEDICAL_UNFIT_FORM_RULES = [
    MedicalUnfitTemporalRule(),
    MedicalUnfitFieldsRule(),
    MedicalUnfitAttachmentsRule(),
]
