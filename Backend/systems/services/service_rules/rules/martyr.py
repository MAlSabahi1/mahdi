"""
systems/services/service_rules/rules/martyr.py
═══════════════════════════════════════════════
قواعد التحقق الخاصة باستمارة الشهيد (Martyr Form Rules).

هذه القواعد تُشغَّل بعد القواعد المشتركة (common.py) وتختص بالتحقق
من البيانات والشروط الخاصة بهذه الاستمارة تحديداً.

القواعد المتضمنة (بالترتيب):
  [M-001] NotAlreadyMartyrRule          : منع إعلان استشهاد فرد هو شهيد أصلاً.
  [M-002] NoConflictingTerminalFormRule : منع تضارب استمارة الشهيد مع استمارات خروج نهائي أخرى معلقة.
  [M-003] MartyrdomDateTemporalRule     : فحص المنطق الزمني لتاريخ الاستشهاد (شامل وكامل).
  [M-004] MartyrdomFieldsCompleteRule   : فرض اكتمال الحقول الإجبارية في الاستمارة.
  [M-005] MartyrdomAttachmentsRule      : فرض اكتمال جميع المرفقات المطلوبة قبل الاعتماد.
"""
from datetime import date, datetime
from typing import Optional
from systems.services.service_rules.core import ServiceRule, ServiceValidationContext


class NotAlreadyMartyrRule(ServiceRule):
    """
    [M-001] منع إعلان فرد كشهيد إذا كانت حالته الحالية (شهيد) مسبقاً.

    هذا الفحص يختلف عن [C-002] الذي يمنع الخدمات للحالات النهائية عموماً.
    هذه القاعدة تُعطي رسالة خطأ دقيقة ومخصصة لحالة الشهيد تحديداً.
    """
    name = 'منع ازدواجية قيد الاستشهاد'
    description = 'يمنع تقديم استمارة شهيد لفرد سبق تسجيله شهيداً في النظام.'

    # أسماء الحالات الدالة على الاستشهاد المسبق (قد تتغير حسب بيانات النظام)
    MARTYR_STATUS_NAMES = {'شهيد', 'استشهد', 'شهداء'}

    def check(self, ctx: ServiceValidationContext) -> None:
        p = ctx.personnel
        status_obj = getattr(p, 'current_status', None)
        if not status_obj:
            return

        # الفحص 1: هل الحالة الحالية معلمة كـ "خروج نهائي" واسمها يدل على الاستشهاد؟
        is_already_martyr = (
            status_obj.is_permanent_deactivation and
            any(m in status_obj.name for m in self.MARTYR_STATUS_NAMES)
        )

        if is_already_martyr:
            ctx.add_error(
                code='ALREADY_MARTYR',
                field='personnel',
                message=(
                    f'رفض الطلب: الفرد "{p.full_name}" (رقم {p.military_number}) '
                    f'مسجل مسبقاً في النظام بحالة "{status_obj.name}". '
                    f'لا يمكن تقديم استمارة شهيد مكررة.'
                ),
                details=(
                    f'تاريخ التسجيل: {status_obj.updated_at.date() if hasattr(status_obj, "updated_at") else "غير معروف"} | '
                    f'معرف الحالة: {status_obj.id}'
                ),
            )


class NoConflictingTerminalFormRule(ServiceRule):
    """
    [M-002] منع تضارب استمارة الشهيد مع أي استمارة خروج نهائي معلقة أخرى.

    حالات التعارض:
      - استمارة وفاة (death) معلقة + استمارة شهيد جديدة → تعارض
      - استمارة تقاعد (retired) معلقة + استمارة شهيد جديدة → تعارض
      - استمارة إنهاء خدمة (end_of_service) معلقة → تعارض

    هذه القاعدة تختلف عن [C-004] لأنها تنظر في جميع استمارات الخروج النهائي
    وليس فقط استمارات الشهيد.
    """
    name = 'منع تضارب استمارة الشهيد مع خروج نهائي آخر'
    description = 'يمنع تقديم استمارة شهيد إذا كانت هناك استمارة خروج نهائي أخرى معلقة للفرد.'

    # أنواع الاستمارات التي تتعارض مع استمارة الشهيد
    CONFLICTING_FORM_TYPES = ('death', 'retirement_age', 'end_of_service', 'medical_unfit', 'missing')
    PENDING_STATUSES = ('draft', 'in_progress', 'returned')

    def check(self, ctx: ServiceValidationContext) -> None:
        from systems.services.infrastructure.models.status_change import StatusChangeForm

        conflicting = StatusChangeForm.objects.filter(
            personnel=ctx.personnel,
            form_type__in=self.CONFLICTING_FORM_TYPES,
            status__in=self.PENDING_STATUSES,
        ).first()

        if conflicting:
            ctx.add_error(
                code='CONFLICTING_TERMINAL_FORM',
                field='form_type',
                message=(
                    f'رفض الطلب: يوجد بالفعل طلب "{conflicting.get_form_type_display()}" '
                    f'معلق للفرد "{ctx.personnel.full_name}" وهو في مرحلة '
                    f'"{conflicting.get_status_display()}". '
                    f'لا يمكن تقديم استمارة شهيد مع وجود طلب خروج نهائي آخر. '
                    f'يجب إلغاء الطلب السابق أو البتّ فيه أولاً.'
                ),
                details=f'معرف الطلب المتعارض: {conflicting.id} | النوع: {conflicting.form_type}',
            )


class MartyrdomDateTemporalRule(ServiceRule):
    """
    [M-003] قاعدة المنطق الزمني الشامل لتاريخ الاستشهاد.

    الفحوصات (بالترتيب):
      A. لا يمكن أن يكون التاريخ في المستقبل.
      B. لا يمكن أن يكون التاريخ قبل تاريخ تجنيد الفرد.
         (استثناء: إذا لم يكن تاريخ التجنيد مسجلاً، يُعطى تحذير لا خطأ)
      C. لا يمكن أن يكون الفرد عمره أقل من 18 سنة عند الاستشهاد.
         (محسوب من تاريخ الميلاد إذا كان موجوداً)

    الحقل المطلوب في form_data: 'martyrdom_date' بصيغة ISO (YYYY-MM-DD)
    """
    name = 'التحقق من المنطق الزمني لتاريخ الاستشهاد'
    description = 'يتأكد أن تاريخ الاستشهاد منطقي وواقعي ومتوافق مع بيانات الفرد.'

    MIN_AGE_AT_MARTYRDOM = 18  # الحد الأدنى للعمر عند الاستشهاد

    def _parse_date(self, value) -> Optional[date]:
        """تحويل قيمة التاريخ إلى كائن date بشكل آمن."""
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
        raw_date = ctx.form_data.get('martyrdom_date')

        # الفحص الأساسي: هل التاريخ موجود؟
        if not raw_date:
            # سيتم التحقق منه في [M-004]، هنا لا نكرر الخطأ
            return

        martyrdom_date = self._parse_date(raw_date)
        if not martyrdom_date:
            ctx.add_error(
                code='INVALID_MARTYRDOM_DATE_FORMAT',
                field='martyrdom_date',
                message=f'تاريخ الاستشهاد "{raw_date}" غير صالح. يجب أن يكون بصيغة YYYY-MM-DD (مثال: 2024-03-15).',
                details=f'القيمة المستقبَلة: "{raw_date}"',
            )
            return  # لا جدوى من الفحوصات اللاحقة إذا كان التاريخ غير صالح

        p = ctx.personnel

        # [A] لا يمكن أن يكون في المستقبل
        if martyrdom_date > ctx.today:
            ctx.add_error(
                code='MARTYRDOM_DATE_IN_FUTURE',
                field='martyrdom_date',
                message=(
                    f'خطأ: تاريخ الاستشهاد ({martyrdom_date}) لا يمكن أن يكون في المستقبل. '
                    f'تاريخ اليوم هو {ctx.today}.'
                ),
                details=f'تاريخ الاستشهاد: {martyrdom_date} | اليوم: {ctx.today}',
            )

        # [B] لا يمكن أن يكون قبل تاريخ التجنيد
        if p.join_date:
            join_date = self._parse_date(p.join_date)
            if join_date and martyrdom_date < join_date:
                ctx.add_error(
                    code='MARTYRDOM_DATE_BEFORE_JOIN',
                    field='martyrdom_date',
                    message=(
                        f'خطأ منطقي: تاريخ الاستشهاد ({martyrdom_date}) '
                        f'يسبق تاريخ التجنيد ({join_date}). '
                        f'لا يمكن أن يستشهد الفرد قبل أن يلتحق بالخدمة.'
                    ),
                    details=(
                        f'تاريخ الاستشهاد: {martyrdom_date} | '
                        f'تاريخ التجنيد: {join_date} | '
                        f'الفارق: {(join_date - martyrdom_date).days} يوم'
                    ),
                )
        else:
            # تاريخ التجنيد غير مسجل: تحذير لا خطأ
            ctx.add_warning(
                code='MISSING_JOIN_DATE_FOR_VALIDATION',
                field='join_date',
                message='تحذير: تاريخ التجنيد للفرد غير مسجل، لم يتم التحقق من التسلسل الزمني. يُوصى بإضافة تاريخ التجنيد.',
                details=f'الفرد: {p.military_number} | تاريخ الاستشهاد المدخل: {martyrdom_date}',
            )

        # [C] لا يمكن أن يكون عمر الفرد عند الاستشهاد أقل من 18 سنة
        if p.birth_date:
            birth_date = self._parse_date(p.birth_date)
            if birth_date:
                age_at_martyrdom_days = (martyrdom_date - birth_date).days
                age_at_martyrdom_years = age_at_martyrdom_days / 365.25

                if age_at_martyrdom_years < self.MIN_AGE_AT_MARTYRDOM:
                    ctx.add_error(
                        code='MARTYRDOM_AGE_TOO_YOUNG',
                        field='martyrdom_date',
                        message=(
                            f'خطأ: وفق تاريخ الميلاد ({birth_date})، '
                            f'كان عمر الفرد {age_at_martyrdom_years:.1f} سنة '
                            f'عند تاريخ الاستشهاد ({martyrdom_date}). '
                            f'الحد الأدنى القانوني هو {self.MIN_AGE_AT_MARTYRDOM} سنة.'
                        ),
                        details=(
                            f'تاريخ الميلاد: {birth_date} | '
                            f'تاريخ الاستشهاد: {martyrdom_date} | '
                            f'العمر المحسوب: {age_at_martyrdom_years:.2f} سنة'
                        ),
                    )


class MartyrdomFieldsCompleteRule(ServiceRule):
    """
    [M-004] قاعدة اكتمال الحقول الإجبارية في استمارة الشهيد.

    الحقول الإجبارية:
      - martyrdom_date     : تاريخ الاستشهاد
      - martyrdom_location : مكان الاستشهاد
      - martyrdom_cause    : سبب الاستشهاد أو اسم العملية/الحادثة

    هذه الحقول يجب أن لا تكون فارغة قبل رفع الطلب.
    """
    name = 'اكتمال الحقول الإجبارية في استمارة الشهيد'
    description = 'يتأكد أن جميع الحقول الإجبارية في الاستمارة مملوءة قبل إتاحة الرفع.'

    REQUIRED_FIELDS = {
        'martyrdom_date': 'تاريخ الاستشهاد',
        'martyrdom_location': 'مكان الاستشهاد',
        'occurrence_context': 'سبب الاستشهاد / اسم العملية',
    }

    def check(self, ctx: ServiceValidationContext) -> None:
        for field_key, field_label in self.REQUIRED_FIELDS.items():
            value = ctx.form_data.get(field_key)
            is_empty = value is None or (isinstance(value, str) and not value.strip())
            if is_empty:
                ctx.add_error(
                    code=f'MISSING_FIELD_{field_key.upper()}',
                    field=field_key,
                    message=f'حقل "{field_label}" إجباري ولم يتم تعبئته. لا يمكن رفع الاستمارة قبل ملء هذا الحقل.',
                    details=f'اسم الحقل في الـ API: "{field_key}"',
                )


class MartyrdomAttachmentsRule(ServiceRule):
    """
    [M-005] قاعدة اكتمال المرفقات الإلزامية لاستمارة الشهيد.

    المرفقات الإلزامية (يجب رفع جميعها لكي يُسمح بتقديم الطلب):
      1. death_certificate  : شهادة الوفاة
      2. heirs_certificate  : حكم انحصار الورثة
      3. legal_power_of_attorney : وكالة شرعية
      4. deceased_id : صورة البطاقة الشخصية للشهيد
      5. agent_id : صورة البطاقة الشخصية للوكيل
      6. guardianship_ruling : حكم التنصيب
      7. operations_report : بلاغ العمليات
      8. mission_order : أمر التكليف بالمهمة
    """
    name = 'اكتمال المرفقات الإلزامية لاستمارة الشهيد'
    description = 'يفرض رفع جميع المرفقات المطلوبة قبل السماح بتقديم الطلب.'

    # المرفقات الإلزامية: { code: الاسم المعروض }
    REQUIRED_ATTACHMENTS = {
        'death_certificate': 'شهادة الوفاة',
        'heirs_certificate': 'حكم انحصار الورثة',
        'legal_power_of_attorney': 'وكالة شرعية',
        'deceased_id': 'صورة البطاقة الشخصية للشهيد',
        'agent_id': 'صورة البطاقة الشخصية للوكيل',
        'guardianship_ruling': 'حكم التنصيب',
        'operations_report': 'بلاغ العمليات',
        'mission_order': 'أمر التكليف بالمهمة',
    }

    def check(self, ctx: ServiceValidationContext) -> None:
        # إذا لم ترسل أي مرفقات بعد (مرحلة المسودة)، نعطي تحذيراً لا خطأً
        if not ctx.uploaded_attachments:
            ctx.add_warning(
                code='NO_ATTACHMENTS_YET',
                field='attachments',
                message='لم يتم رفع أي مرفقات حتى الآن. يجب رفع جميع المرفقات الإلزامية قبل تقديم الطلب الرسمي.',
                details=f'المرفقات المطلوبة: {", ".join(self.REQUIRED_ATTACHMENTS.values())}',
            )
            return

        missing = []
        for att_code, att_label in self.REQUIRED_ATTACHMENTS.items():
            if att_code not in ctx.uploaded_attachments:
                missing.append(att_label)

        if missing:
            missing_str = '\n  - '.join(missing)
            ctx.add_error(
                code='INCOMPLETE_ATTACHMENTS',
                field='attachments',
                message=(
                    f'لا يمكن تقديم الطلب. المرفقات التالية ناقصة وإلزامية:\n'
                    f'  - {missing_str}\n'
                    f'يجب رفع جميع المرفقات أعلاه قبل إتمام الطلب.'
                ),
                details=f'المرفقات المفقودة: {[a for a in self.REQUIRED_ATTACHMENTS if a not in ctx.uploaded_attachments]}',
            )


# ── قائمة قواعد استمارة الشهيد مرتبة حسب الأولوية ──────────────────────────
MARTYR_FORM_RULES = [
    NotAlreadyMartyrRule(),           # [M-001] أولاً: التحقق السريع من الحالة
    NoConflictingTerminalFormRule(),  # [M-002] ثانياً: منع تضارب الاستمارات
    MartyrdomDateTemporalRule(),      # [M-003] ثالثاً: فحص التواريخ بالكامل
    MartyrdomFieldsCompleteRule(),    # [M-004] رابعاً: اكتمال الحقول
    MartyrdomAttachmentsRule(),       # [M-005] خامساً: اكتمال المرفقات
]
