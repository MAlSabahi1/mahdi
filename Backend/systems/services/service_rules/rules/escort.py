from datetime import datetime
from typing import Optional
from systems.services.service_rules.core import ServiceRule, ServiceValidationContext

class EscortTemporalRule(ServiceRule):
    """
    [ESC-001] قاعدة حساب مدة المرافقة
    تقوم بحساب المدة بين تاريخ البدء والانتهاء، وتقوم بتحديث حقل 'مدة المرافقة المحسوبة' 
    بصيغة نصية عربية واضحة.
    """
    name = 'حساب مدة المرافقة'
    description = 'حساب مدة تفريغ الفرد للمرافقة وتحويلها إلى نص مقروء'

    def _parse_date(self, value: any) -> Optional[datetime.date]:
        if not value: return None
        if isinstance(value, datetime): return value.date()
        if isinstance(value, str):
            for fmt in ('%Y-%m-%d', '%d/%m/%Y', '%Y/%m/%d'):
                try:
                    return datetime.strptime(value.split('T')[0], fmt).date()
                except ValueError:
                    continue
        return None

    def check(self, ctx: ServiceValidationContext) -> None:
        start_val = ctx.form_data.get('start_date')
        end_val = ctx.form_data.get('end_date')
        
        start_date = self._parse_date(start_val)
        end_date = self._parse_date(end_val)

        if not start_date or not end_date:
            return

        if start_date >= end_date:
            ctx.add_error(
                code='INVALID_DATE_RANGE',
                field='end_date',
                message='تاريخ الانتهاء يجب أن يكون بعد تاريخ البدء.'
            )
            return

        # حساب المدة بالكامل
        total_days = (end_date - start_date).days
        years = total_days // 365
        months = (total_days % 365) // 30
        days = (total_days % 365) % 30
        
        duration_parts = []
        if years > 0: duration_parts.append(f"{years} سنة")
        if months > 0: duration_parts.append(f"{months} شهر")
        if days > 0: duration_parts.append(f"{days} يوم")
        
        ctx.form_data['duration'] = " و ".join(duration_parts) if duration_parts else "0 يوم"


ESCORT_FORM_RULES = [
    EscortTemporalRule(),
]
