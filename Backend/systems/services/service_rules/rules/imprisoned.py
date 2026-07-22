"""
systems/services/service_rules/rules/imprisoned.py
═══════════════════════════════════════════════
قواعد التحقق الخاصة باستمارة المسجون (Imprisoned Form Rules).

هذه القواعد تُشغَّل بعد القواعد المشتركة (common.py) وتختص بالتحقق
من البيانات والشروط الخاصة باستمارة المساجين.

القواعد المتضمنة:
  [I-001] ImprisonmentTemporalRule : فحص التواريخ والمنطق الزمني (تاريخ التوقيف، الحكم).
  [I-002] ImprisonmentFieldsCompleteRule : فرض الحقول المطلوبة بحسب نوع الحكم (موقوف أم محكوم).
  [I-003] ImprisonmentAttachmentsRule : فرض المرفقات الشرطية بحسب حالة الفرد القانونية.
"""
from datetime import date, datetime
from typing import Optional
from systems.services.service_rules.core import ServiceRule, ServiceValidationContext

class ImprisonmentTemporalRule(ServiceRule):
    """
    [I-001] قاعدة فحص التواريخ والمنطق الزمني لبيانات السجن.
    """
    name = 'التحقق من المنطق الزمني لتاريخ التوقيف والحكم'
    description = 'يمنع إدخال تواريخ توقيف أو حكم في المستقبل ويتأكد من منطقية التواريخ.'

    def _parse_date(self, value) -> Optional[date]:
        if not value:
            return None
        if isinstance(value, date):
            return value
        if isinstance(value, datetime):
            return value.date()
        if isinstance(value, str):
            for fmt in ('%Y-%m-%d', '%d/%m/%Y', '%Y/%m/%d'):
                try:
                    return datetime.strptime(value, fmt).date()
                except ValueError:
                    continue
        return None

    def check(self, ctx: ServiceValidationContext) -> None:
        arrest_date = self._parse_date(ctx.form_data.get('arrest_date'))
        ruling_date = self._parse_date(ctx.form_data.get('ruling_date'))
        duration_from = self._parse_date(ctx.form_data.get('duration_from'))
        duration_to = self._parse_date(ctx.form_data.get('duration_to'))
        today = ctx.today

        if arrest_date and arrest_date > today:
            ctx.add_error(
                code='ARREST_DATE_IN_FUTURE',
                field='arrest_date',
                message=f'تاريخ التوقيف ({arrest_date}) لا يمكن أن يكون في المستقبل.',
                details=f'اليوم: {today}'
            )

        if ruling_date and ruling_date > today:
            ctx.add_error(
                code='RULING_DATE_IN_FUTURE',
                field='ruling_date',
                message=f'تاريخ الحكم ({ruling_date}) لا يمكن أن يكون في المستقبل.',
                details=f'اليوم: {today}'
            )

        if duration_from and duration_to and duration_to <= duration_from:
            ctx.add_error(
                code='INVALID_RULING_DURATION',
                field='duration_to',
                message='تاريخ نهاية الحكم يجب أن يكون بعد تاريخ البداية.',
                details=f'البداية: {duration_from} | النهاية: {duration_to}'
            )


class ImprisonmentFieldsCompleteRule(ServiceRule):
    """
    [I-002] التحقق من اكتمال الحقول.
    تم الاستغناء عن تفريع أنواع الحكم بناءً على رغبة المستخدم.
    """
    name = 'اكتمال الحقول'
    description = 'يضمن أن الحقول اختيارية ومكتملة.'

    def check(self, ctx: ServiceValidationContext) -> None:
        pass

class ImprisonmentAttachmentsRule(ServiceRule):
    """
    [I-003] قاعدة المرفقات.
    """
    name = 'اكتمال المرفقات الأساسية للمساجين'
    description = 'يفرض رفع المرفق المناسب.'

    def check(self, ctx: ServiceValidationContext) -> None:
        if not ctx.uploaded_attachments:
            ctx.add_warning(
                code='NO_ATTACHMENTS_YET',
                field='attachments',
                message='لم يتم رفع أي مرفقات حتى الآن. يفضل إرفاق المستندات الداعمة (مذكرة نيابة أو نسخة حكم) قبل التقديم.',
                details=''
            )
            return

# ── قائمة القواعد ──────────────────────────
IMPRISONED_FORM_RULES = [
    ImprisonmentTemporalRule(),
    ImprisonmentFieldsCompleteRule(),
    ImprisonmentAttachmentsRule(),
]
