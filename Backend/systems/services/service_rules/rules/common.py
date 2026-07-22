"""
systems/services/service_rules/rules/common.py
═══════════════════════════════════════════════
القواعد المشتركة بين جميع الخدمات (Common Rules).

هذه القواعد يجب تشغيلها أولاً قبل قواعد الخدمة الخاصة.
تُعتبر "بوابة التفتيش العامة" التي يمر منها أي طلب أياً كان نوعه.

القواعد المتضمنة:
  [C-001] PersonnelExistsRule          : التحقق من وجود الفرد في النظام وصحة بيانات الهوية.
  [C-002] NoTerminalStatusRule         : منع تقديم أي خدمة لفرد في حالة "خروج نهائي".
  [C-003] MinimumDataQualityRule       : التحقق من أن جودة بيانات الفرد كافية للخدمة.
  [C-004] NoConflictingPendingFormRule : منع تضارب الطلبات المعلقة من نفس النوع.
"""
from systems.services.service_rules.core import ServiceRule, ServiceValidationContext


class PersonnelExistsRule(ServiceRule):
    """
    [C-001] قاعدة التحقق من صحة وجود الفرد.

    الشروط:
      - يجب أن يمتلك الفرد رقماً عسكرياً صالحاً (7 أرقام).
      - يجب أن يمتلك الفرد رقماً وطنياً مسجلاً (11 رقم).

    سبب الأهمية: لا يمكن إجراء أي خدمة رسمية لفرد لا هوية له في النظام.
    """
    name = 'التحقق من صحة هوية الفرد'
    description = 'يتأكد من وجود رقم عسكري ووطني صالح قبل قبول أي طلب خدمة.'

    def check(self, ctx: ServiceValidationContext) -> None:
        p = ctx.personnel

        # التحقق من الرقم العسكري
        if not p.military_number or len(str(p.military_number)) != 7:
            ctx.add_error(
                code='INVALID_MILITARY_NUMBER',
                field='military_number',
                message='لا يمكن تقديم هذه الخدمة. الرقم العسكري للفرد غير مكتمل أو غير صالح (يجب أن يكون 7 أرقام).',
                details=f'القيمة الحالية: "{p.military_number}". يتطلب إصلاح هذا من قِبَل مدير النظام عبر شاشة تصحيح الرقم العسكري.',
            )

        # التحقق من الرقم الوطني
        if not p.national_id or not str(p.national_id).isdigit() or len(str(p.national_id)) != 11:
            ctx.add_error(
                code='INVALID_NATIONAL_ID',
                field='national_id',
                message='لا يمكن تقديم هذه الخدمة. الرقم الوطني للفرد غير مسجل أو غير صالح (يجب أن يكون 11 رقماً).',
                details=f'القيمة الحالية: "{p.national_id}". يجب تصحيح الرقم الوطني أولاً عبر مسار "طلب تصحيح بيانات".',
            )


class NoTerminalStatusRule(ServiceRule):
    """
    [C-002] قاعدة منع تقديم خدمات لفرد في حالة خروج نهائي.

    الحالات النهائية (is_permanent_deactivation=True):
      - شهيد | متوفي | مسجون تأبيدي | متقاعد | مفصول | منهي خدمته

    الاستثناء: خدمة تعديل البيانات الأرشيفية (ARCHIVE_EDIT) مسموحة.
    """
    name = 'منع الخدمات للحالات النهائية'
    description = 'يمنع تقديم أي طلب خدمة لفرد صدر بحقه قرار خروج نهائي من الخدمة.'

    # الخدمات المستثناة من هذه القاعدة
    EXEMPT_SERVICE_CODES = {'ARCHIVE_EDIT', 'DATA_QUALITY_FIX'}

    def check(self, ctx: ServiceValidationContext) -> None:
        if ctx.service_code in self.EXEMPT_SERVICE_CODES:
            return  # هذه الخدمات مسموحة حتى للحالات النهائية

        p = ctx.personnel
        status_obj = getattr(p, 'current_status', None)

        if status_obj and status_obj.is_permanent_deactivation:
            status_name = status_obj.name
            ctx.add_error(
                code='PERSONNEL_TERMINAL_STATUS',
                field='personnel',
                message=f'رفض الطلب: لا يمكن تقديم هذه الخدمة للفرد "{p.full_name}" لأن حالته الحالية هي "{status_name}" وهي حالة خروج نهائي من الخدمة.',
                details=f'الفرد: {p.military_number} | الحالة: {status_name} | التصنيف: inactive_perm. يجب الرجوع للأرشيف للاطلاع على سجله التاريخي.',
            )


class MinimumDataQualityRule(ServiceRule):
    """
    [C-003] قاعدة الحد الأدنى لجودة البيانات.

    لا يمكن تقديم أي خدمة رسمية لفرد جودة بياناته أقل من عتبة معينة،
    لأن الخدمة قد تحتاج إلى بيانات أساسية مفقودة.

    العتبة الافتراضية: 50%
    (خدمة تصحيح البيانات مستثناة بالكامل من هذه القاعدة)
    """
    name = 'الحد الأدنى لجودة بيانات الفرد'
    description = 'يمنع تقديم الخدمات الرسمية لفرد جودة بياناته أقل من 50%.'

    MINIMUM_QUALITY = 50
    EXEMPT_SERVICE_CODES = {'CORRECTION', 'DATA_QUALITY_FIX'}

    def check(self, ctx: ServiceValidationContext) -> None:
        if ctx.service_code in self.EXEMPT_SERVICE_CODES:
            return

        p = ctx.personnel
        score = getattr(p, 'data_quality_score', 100) or 100

        if score < self.MINIMUM_QUALITY:
            ctx.add_error(
                code='LOW_DATA_QUALITY',
                field='personnel',
                message=(
                    f'رفض الطلب: جودة بيانات الفرد "{p.full_name}" منخفضة جداً ({score}%) '
                    f'ولا تسمح بتقديم الخدمات الرسمية. الحد الأدنى المطلوب: {self.MINIMUM_QUALITY}%.'
                ),
                details=f'الرقم العسكري: {p.military_number} | نسبة الجودة: {score}%. يجب استكمال الملف الشخصي أولاً عبر شاشة تصحيح البيانات.',
            )
        elif score < 70:
            # تحذير غير مانع: البيانات كافية لكن يُنصح باستكمالها
            ctx.add_warning(
                code='MODERATE_DATA_QUALITY',
                field='personnel',
                message=f'تحذير: جودة بيانات الفرد ({score}%) متدنية. يُوصى باستكمال الملف الشخصي لضمان صحة الخدمة.',
                details=f'الرقم العسكري: {p.military_number} | نسبة الجودة: {score}%.',
            )


class NoConflictingPendingFormRule(ServiceRule):
    """
    [C-004] قاعدة منع تضارب الطلبات المعلقة.

    يمنع تقديم استمارة من نفس النوع إذا كانت هناك استمارة معلقة مسبقاً
    لم يُبَتّ فيها بعد.

    مثال: لا يمكن تقديم استمارة (شهيد) إذا كانت هناك استمارة (شهيد) أخرى
    قيد المراجعة لنفس الفرد.

    الحقل المطلوب في form_data: 'form_type' (مثال: 'martyr')
    """
    name = 'منع تضارب الطلبات المعلقة'
    description = 'يمنع تقديم استمارة جديدة إذا كانت هناك استمارة معلقة من نفس النوع للفرد.'

    PENDING_STATUSES = ('draft', 'in_progress', 'returned')

    def check(self, ctx: ServiceValidationContext) -> None:
        form_type = ctx.form_data.get('form_type', '')
        if not form_type:
            return  # لا يمكن التحقق بدون معرفة نوع الاستمارة

        from systems.services.infrastructure.models.status_change import StatusChangeForm

        existing = StatusChangeForm.objects.filter(
            personnel=ctx.personnel,
            form_type=form_type,
            status__in=self.PENDING_STATUSES,
        ).first()

        if existing:
            ctx.add_error(
                code='CONFLICTING_PENDING_FORM',
                field='form_type',
                message=(
                    f'رفض الطلب: يوجد بالفعل طلب ({existing.get_form_type_display()}) معلق '
                    f'للفرد "{ctx.personnel.full_name}" وهو حالياً في مرحلة "{existing.get_status_display()}". '
                    f'يجب انتظار البتّ في الطلب السابق أو إلغاؤه قبل تقديم طلب جديد.'
                ),
                details=f'معرف الطلب المعلق: {existing.id} | النوع: {form_type} | الحالة: {existing.status}',
            )


# ── قائمة القواعد المشتركة مرتبة حسب الأولوية ──────────────────────────────
# تُستخدم هذه القائمة في التسجيل النهائي في __init__.py
COMMON_RULES = [
    PersonnelExistsRule(),
    NoTerminalStatusRule(),
    MinimumDataQualityRule(),
    NoConflictingPendingFormRule(),
]
