"""
systems/services/service_rules/rules/study_leave.py
════════════════════════════════════════════════
قواعد التحقق الخاصة باستمارة مفرغ للدراسة (Study Leave Form Rules).

القواعد المتضمنة:
  [SL-001] ValidStudyLeaveStatusRule  : يمنع تفريغ من ليس على رأس العمل (عاملين).
  [SL-002] StudyLeaveTemporalRule     : فحص التواريخ والمدد حسب الدرجة العلمية (بكالوريوس، ماجستير، الخ).
  [SL-003] StudyLeaveAgeLimitRule     : فحص الحد الأقصى للعمر المسموح به للدراسة.
"""
from datetime import date, datetime
from typing import Optional
from systems.services.service_rules.core import ServiceRule, ServiceValidationContext
from core.models.settings import SystemSetting


class ValidStudyLeaveStatusRule(ServiceRule):
    """
    [SL-001] يمنع فتح استمارة تفريغ لأي فرد حالته ليست (1 - عاملين).
    """
    name = 'شرط الأهلية للتفرغ الدراسي'
    description = 'يمنع تفريغ فرد ليس على رأس العمل (يجب أن تكون حالته "عامل").'

    def check(self, ctx: ServiceValidationContext) -> None:
        p = ctx.personnel
        status_obj = getattr(p, 'current_status', None)
        
        if not status_obj or status_obj.id != 1:
            ctx.add_error(
                code='INVALID_SOURCE_STATUS_FOR_STUDY',
                field='personnel',
                message=(
                    f'رفض الطلب: الفرد "{p.full_name}" (رقم {p.military_number}) '
                    f'مسجل حالياً بحالة "{status_obj.name if status_obj else "غير معروف"}". '
                    f'التفرغ الدراسي مسموح فقط للأفراد العاملين.'
                ),
            )


class StudyLeaveTemporalRule(ServiceRule):
    """
    [SL-002] فحص المنطق الزمني لفترة الدراسة بناءً على الدرجة العلمية.
    """
    name = 'التحقق من المدة والتواريخ للدراسة'
    description = 'يتأكد من أن مدة الدراسة تتوافق مع السقف الأعلى للدرجة العلمية المحددة في الإعدادات.'

    def _parse_date(self, value) -> Optional[date]:
        if not value: return None
        if isinstance(value, date): return value
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
        study_type = ctx.form_data.get('study_type', '')
        
        start_date = self._parse_date(start_val)
        end_date = self._parse_date(end_val)

        if not start_date or not end_date:
            return  # سيتم التقاطها كحقول مفقودة من المخطط (Schema)

        if end_date <= start_date:
            ctx.add_error(
                code='INVALID_STUDY_DATES',
                field='end_date',
                message='تاريخ الانتهاء يجب أن يكون أكبر من تاريخ البدء.'
            )
            return

        # حساب المدة الفعلية بالسنوات
        actual_years = (end_date - start_date).days / 365.25

        # جلب الحد الأقصى للمدة حسب الدرجة من الإعدادات العامة (القيم الافتراضية كما طلب المستخدم)
        max_years_map = {
            'دبلوم': SystemSetting.get_setting('study_leave_max_years_diploma', 2),
            'بكالوريوس': SystemSetting.get_setting('study_leave_max_years_bachelor', 6),
            'ماجستير': SystemSetting.get_setting('study_leave_max_years_master', 3),
            'دكتوراه': SystemSetting.get_setting('study_leave_max_years_phd', 5),
            'دورة تخصصية': SystemSetting.get_setting('study_leave_max_years_diploma', 2),
        }

        max_allowed_years = max_years_map.get(study_type, 6) # افتراضي

        if actual_years > max_allowed_years:
            ctx.add_error(
                code='EXCEED_MAX_STUDY_DURATION',
                field='end_date',
                message=f'مدة التفرغ المطلوبة ({actual_years:.1f} سنة) تتجاوز الحد الأقصى المسموح به لدرجة {study_type} ({max_allowed_years} سنوات).'
            )

        # حساب وتخزين المدة تلقائياً بنص عربي واضح (سنة، شهر، يوم)
        total_days = (end_date - start_date).days
        years = total_days // 365
        months = (total_days % 365) // 30
        days = (total_days % 365) % 30
        
        duration_parts = []
        if years > 0: duration_parts.append(f"{years} سنة")
        if months > 0: duration_parts.append(f"{months} شهر")
        if days > 0: duration_parts.append(f"{days} يوم")
        
        ctx.form_data['duration'] = " و ".join(duration_parts) if duration_parts else "0 يوم"


class StudyLeaveAgeLimitRule(ServiceRule):
    """
    [SL-003] فحص الحد الأقصى للعمر المسموح به للتفرغ الدراسي حسب الدرجة العلمية.
    """
    name = 'التحقق من سن المفرغ للدراسة'
    description = 'يمنع تفريغ الأفراد الذين تتجاوز أعمارهم الحد الأقصى المسموح للدرجة العلمية المطلوبة.'

    def check(self, ctx: ServiceValidationContext) -> None:
        birth_date = ctx.personnel.birth_date
        if not birth_date:
            return # إذا لم يكن مسجلاً نتجاهل الشرط

        study_type = ctx.form_data.get('study_type', '')
        
        # حساب العمر الحالي
        current_age = (date.today() - birth_date).days / 365.25

        max_age_map = {
            'بكالوريوس': SystemSetting.get_setting('study_leave_max_age_bachelor', 35),
            'ماجستير': SystemSetting.get_setting('study_leave_max_age_master', 40),
            'دكتوراه': SystemSetting.get_setting('study_leave_max_age_phd', 45),
        }

        # الدبلوم والدورات قد لا يكون لها حد عمري صارم أو تتبع حد البكالوريوس
        max_allowed_age = max_age_map.get(study_type)

        if max_allowed_age and current_age > max_allowed_age:
            ctx.add_error(
                code='EXCEED_MAX_STUDY_AGE',
                field='personnel',
                message=f'عمر الفرد ({int(current_age)} سنة) يتجاوز الحد الأقصى المسموح به للتفرغ لدرجة {study_type} ({max_allowed_age} سنة).'
            )


# ── قائمة القواعد ──────────────────────────
STUDY_LEAVE_FORM_RULES = [
    ValidStudyLeaveStatusRule(),
    StudyLeaveTemporalRule(),
    StudyLeaveAgeLimitRule(),
]
