"""
systems/services/service_rules/__init__.py
═══════════════════════════════════════════
نقطة التسجيل المركزية (Central Registry).

كل خدمة تُسجَّل هنا بكودها وقواعدها.
لإضافة خدمة جديدة:
  1. أنشئ ملف قواعد في rules/new_service.py
  2. أضف سطر تسجيل واحداً هنا:
     ServiceRulesDispatcher.register('NEW_SERVICE_CODE', new_service.NEW_SERVICE_RULES)
"""
from systems.services.service_rules.core import ServiceRulesDispatcher
from systems.services.service_rules.rules import common, martyr, seconded, study_leave, escort, imprisoned, end_of_service, medical_unfit

# ── تسجيل الخدمات ──────────────────────────────────────────────────────────

# استمارة الشهيد
# القواعد المشتركة تأتي أولاً دائماً، ثم القواعد الخاصة بالخدمة
ServiceRulesDispatcher.register(
    service_code='MARTYR_FORM',
    rules=[
        *common.COMMON_RULES,     # [C-001] إلى [C-004]: القواعد المشتركة
        *martyr.MARTYR_FORM_RULES, # [M-001] إلى [M-005]: قواعد الشهيد
    ]
)

# استمارة الانتداب
ServiceRulesDispatcher.register(
    service_code='SECONDED_FORM',
    rules=[
        *common.COMMON_RULES,
        *seconded.SECONDED_FORM_RULES,
    ]
)

# استمارة التفريغ الدراسي
ServiceRulesDispatcher.register(
    service_code='STUDY_LEAVE_FORM',
    rules=[
        *common.COMMON_RULES,
        *study_leave.STUDY_LEAVE_FORM_RULES,
    ]
)

# استمارة مرافق / معيات
ServiceRulesDispatcher.register(
    service_code='ESCORT_FORM',
    rules=[
        *common.COMMON_RULES,
        *escort.ESCORT_FORM_RULES,
    ]
)

# استمارة السجناء
ServiceRulesDispatcher.register(
    service_code='IMPRISONED_FORM',
    rules=[
        *common.COMMON_RULES,
        *imprisoned.IMPRISONED_FORM_RULES,
    ]
)

# ── الخدمات القادمة (جاهزة للتوسع) ─────────────────────────────────────────
# ServiceRulesDispatcher.register('DEATH_FORM', [...])
# ServiceRulesDispatcher.register('PROMOTION_FORM', [...])
# ServiceRulesDispatcher.register('RETIREMENT_FORM', [...])
# ServiceRulesDispatcher.register('CORRECTION', [...])

# استمارة إنهاء المدة
ServiceRulesDispatcher.register(
    service_code='END_OF_SERVICE_FORM',
    rules=[
        *common.COMMON_RULES,
        *end_of_service.END_OF_SERVICE_FORM_RULES,
    ]
)

# استمارة عدم اللياقة الصحية
ServiceRulesDispatcher.register(
    service_code='MEDICAL_UNFIT_FORM',
    rules=[
        *common.COMMON_RULES,
        *medical_unfit.MEDICAL_UNFIT_FORM_RULES,
    ]
)
