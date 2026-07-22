"""
systems/services/service_rules/rules/seconded.py
════════════════════════════════════════════════
قواعد التحقق الخاصة باستمارة الانتداب (Secondment Form Rules).

هذه القواعد تُشغَّل بعد القواعد المشتركة (common.py) وتختص بالتحقق
من البيانات والشروط الخاصة بهذه الاستمارة تحديداً.

القواعد المتضمنة:
  [S-001] ValidSourceStatusRule       : يمنع الانتداب لمن ليس على رأس العمل (عاملين).
  [S-002] SecondmentTemporalLogicRule : فحص التواريخ والحد الأقصى للمدة بناءً على إعدادات النظام.
  [S-003] SecondmentAttachmentsRule   : فرض إرفاق أمر الانتداب.
"""
from datetime import date, datetime
from typing import Optional
from systems.services.service_rules.core import ServiceRule, ServiceValidationContext
from core.models.settings import SystemSetting


class ValidSourceStatusRule(ServiceRule):
    """
    [S-001] يمنع فتح استمارة انتداب لأي فرد حالته ليست (1 - عاملين).
    """
    name = 'شرط الأهلية للانتداب'
    description = 'يمنع انتداب فرد ليس على رأس العمل (يجب أن تكون حالته "عامل").'

    def check(self, ctx: ServiceValidationContext) -> None:
        p = ctx.personnel
        status_obj = getattr(p, 'current_status', None)
        
        # 1 is the status code for Active (عاملين)
        if not status_obj or status_obj.id != 1:
            ctx.add_error(
                code='INVALID_SOURCE_STATUS_FOR_SECONDMENT',
                field='personnel',
                message=(
                    f'رفض الطلب: الفرد "{p.full_name}" (رقم {p.military_number}) '
                    f'مسجل حالياً بحالة "{status_obj.name if status_obj else "غير معروف"}". '
                    f'الانتداب مسموح فقط للأفراد العاملين على رأس العمل.'
                ),
            )


class SecondmentTemporalLogicRule(ServiceRule):
    """
    [S-002] فحص المنطق الزمني لفترة الانتداب.
    
    الشروط:
      - يجب أن يكون تاريخ الانتهاء أكبر من تاريخ البدء.
      - لا يجوز أن تتجاوز مدة الانتداب الحد الأقصى المحدد في الإعدادات العامة.
    """
    name = 'التحقق من التواريخ ومدة الانتداب'
    description = 'يتأكد من صحة التواريخ وعدم تجاوز المدة القصوى المسموحة.'

    def _parse_date(self, value) -> Optional[date]:
        if not value: return None
        if isinstance(value, date): return value
        if isinstance(value, datetime): return value.date()
        if isinstance(value, str):
            for fmt in ('%Y-%m-%d', '%d/%m/%Y', '%Y/%m/%d'):
                try: return datetime.strptime(value, fmt).date()
                except ValueError: continue
        return None

    def check(self, ctx: ServiceValidationContext) -> None:
        raw_start = ctx.form_data.get('start_date')
        raw_end = ctx.form_data.get('end_date')

        start_date = self._parse_date(raw_start)
        end_date = self._parse_date(raw_end)

        if not start_date:
            ctx.add_error(
                code='MISSING_START_DATE',
                field='start_date',
                message='تاريخ بدء الانتداب حقل إجباري.'
            )
        
        if not end_date:
            ctx.add_error(
                code='MISSING_END_DATE',
                field='end_date',
                message='تاريخ انتهاء الانتداب حقل إجباري.'
            )

        if not start_date or not end_date:
            return  # Stop if dates are missing or invalid

        if end_date <= start_date:
            ctx.add_error(
                code='END_DATE_BEFORE_START_DATE',
                field='end_date',
                message=(
                    f'خطأ منطقي: تاريخ الانتهاء ({end_date}) '
                    f'يسبق أو يساوي تاريخ البدء ({start_date}).'
                ),
            )
            return

        # Fetch max duration from system settings, default to 4 years (1460 days) if not set
        max_days = SystemSetting.get_setting('max_secondment_duration_days', default=1460)
        try:
            max_days = int(max_days)
        except (ValueError, TypeError):
            max_days = 1460

        duration_days = (end_date - start_date).days
        if duration_days > max_days:
            max_years = max_days / 365.25
            ctx.add_error(
                code='SECONDMENT_EXCEEDS_MAX_DURATION',
                field='end_date',
                message=(
                    f'خطأ: مدة الانتداب المدخلة تتجاوز الحد الأقصى المسموح به '
                    f'({max_years:.1f} سنة). يرجى مراجعة الإعدادات أو تعديل التاريخ.'
                ),
                details=f'المدة المطلوبة: {duration_days} يوم | الحد الأقصى: {max_days} يوم'
            )


class SecondmentAttachmentsRule(ServiceRule):
    """
    [S-003] فرض إرفاق أمر الانتداب.
    """
    name = 'التحقق من المرفقات الإلزامية'
    description = 'يفرض إرفاق أمر الانتداب قبل إتاحة تقديم الطلب.'

    REQUIRED_ATTACHMENTS = {
        'secondment_order': 'نسخة من أمر الانتداب',
    }

    def check(self, ctx: ServiceValidationContext) -> None:
        if not ctx.uploaded_attachments:
            ctx.add_warning(
                code='NO_ATTACHMENTS_YET',
                field='attachments',
                message='لم يتم رفع أي مرفقات حتى الآن. يجب إرفاق أمر الانتداب لتقديم الطلب.'
            )
            return

        valid_codes = {'secondment_order', 'secondment_order_copy'}
        has_order = any(code in ctx.uploaded_attachments for code in valid_codes)

        if not has_order:
            ctx.add_error(
                code='INCOMPLETE_SECONDMENT_ATTACHMENTS',
                field='attachments',
                message=(
                    f'المرفقات التالية ناقصة وإلزامية:\n'
                    f'  - نسخة من أمر الانتداب\n'
                ),
            )


# ── قائمة القواعد ──────────────────────────
SECONDED_FORM_RULES = [
    ValidSourceStatusRule(),
    SecondmentTemporalLogicRule(),
    SecondmentAttachmentsRule(),
]
