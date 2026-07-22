"""
systems/services/service_rules/core.py
═══════════════════════════════════════
الكلاسات الأساسية لمحرك قواعد الخدمات.

التصميم:
  - ServiceValidationContext  : يحمل سياق كامل لعملية التحقق (الفرد، نوع الخدمة، البيانات المرسلة).
  - ServiceRule               : الواجهة الأساسية (Interface) لأي قاعدة خدمة.
  - ServiceRulesDispatcher    : الموزع الذي يربط كل نوع خدمة بقواعدها، ويشغّلها بالتسلسل.

المبادئ المتبعة:
  [1] Single Responsibility : كل قاعدة مستقلة ومسؤولة عن شرط واحد فقط.
  [2] Open/Closed Principle : لإضافة خدمة جديدة، نضيف قواعدها فقط دون تعديل الكود الأساسي.
  [3] رسائل خطأ واضحة ومفصلة: كل خطأ يحتوي على كود، سبب، وتوجيه للمستخدم والمبرمج.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, TYPE_CHECKING
from datetime import date

if TYPE_CHECKING:
    from systems.personnel.models import PersonnelMaster


# ══════════════════════════════════════════════════════════════════════════════
# 1. ServiceError — بنية خطأ منظّمة
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class ServiceError:
    """
    خطأ تحقق منظّم يُرجعه المحرك.

    الحقول:
      code     : كود فريد للخطأ (للاستخدام البرمجي والـ Frontend).
                 مثال: 'ALREADY_MARTYR' | 'CONFLICTING_PENDING_FORM'
      field    : اسم الحقل المرتبط بالخطأ (إن وُجد) لتلوين الحقل باللون الأحمر في الواجهة.
                 مثال: 'martyrdom_date' | 'attachments'
      message  : رسالة مفهومة للمستخدم العادي (باللغة العربية).
      details  : تفاصيل تقنية للمبرمج أو لتسجيل الأحداث (AuditLog).
      blocking : هل هذا خطأ مانع (يمنع الحفظ)، أم تحذير فقط (يسمح بالمتابعة مع تنبيه)؟
    """
    code: str
    message: str
    field: Optional[str] = None
    details: Optional[str] = None
    blocking: bool = True  # الافتراضي: خطأ مانع

    def to_dict(self) -> dict:
        """تحويل الخطأ إلى قاموس جاهز للإرسال عبر API."""
        return {
            'code': self.code,
            'field': self.field,
            'message': self.message,
            'details': self.details,
            'blocking': self.blocking,
        }


# ══════════════════════════════════════════════════════════════════════════════
# 2. ServiceValidationContext — حامل السياق الكامل
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class ServiceValidationContext:
    """
    سياق عملية التحقق الكاملة.

    يتم إنشاؤه مرة واحدة لكل طلب خدمة، ويتم تمريره لجميع القواعد (Rules).
    كل قاعدة تقرأ منه وتكتب أخطاءها فيه.

    الحقول:
      personnel     : كائن PersonnelMaster للفرد المعني بالطلب.
      service_code  : كود الخدمة المطلوبة (مثال: 'MARTYR_FORM').
      form_data     : البيانات المرسلة من الواجهة (JSON).
      uploaded_attachments: قائمة بأنواع المرفقات التي قام المستخدم برفعها فعلاً.
      errors        : قائمة الأخطاء المتراكمة من القواعد (يُملأ تلقائياً).
      warnings      : قائمة التحذيرات غير المانعة.
      today         : تاريخ اليوم (قابل للاستبدال في الاختبارات).
    """
    personnel: "PersonnelMaster"
    service_code: str
    form_data: Dict[str, Any] = field(default_factory=dict)
    uploaded_attachments: List[str] = field(default_factory=list)
    errors: List[ServiceError] = field(default_factory=list)
    warnings: List[ServiceError] = field(default_factory=list)
    today: date = field(default_factory=date.today)
    disabled_rules: List[str] = field(default_factory=list)

    # ── دوال مساعدة ────────────────────────────────────────────────────────────

    def add_error(self, code: str, message: str,
                  field: Optional[str] = None, details: Optional[str] = None) -> None:
        """إضافة خطأ مانع (Blocking Error)."""
        self.errors.append(ServiceError(
            code=code, message=message, field=field, details=details, blocking=True
        ))

    def add_warning(self, code: str, message: str,
                    field: Optional[str] = None, details: Optional[str] = None) -> None:
        """إضافة تحذير غير مانع (Warning). يسمح بالمتابعة لكنه يُعرض للمستخدم."""
        self.warnings.append(ServiceError(
            code=code, message=message, field=field, details=details, blocking=False
        ))

    def has_blocking_errors(self) -> bool:
        """هل يوجد أخطاء مانعة؟"""
        return len(self.errors) > 0

    def to_response_dict(self) -> dict:
        """تحويل السياق كاملاً إلى استجابة API منظّمة."""
        return {
            'valid': not self.has_blocking_errors(),
            'errors': [e.to_dict() for e in self.errors],
            'warnings': [w.to_dict() for w in self.warnings],
        }


# ══════════════════════════════════════════════════════════════════════════════
# 3. ServiceRule — الواجهة الأساسية لكل قاعدة
# ══════════════════════════════════════════════════════════════════════════════

class ServiceRule(ABC):
    """
    الواجهة الأساسية (Abstract Base Class) لأي قاعدة خدمة.

    كيفية إنشاء قاعدة جديدة:
    ─────────────────────────
    class MyCustomRule(ServiceRule):
        name = 'اسم القاعدة'
        description = 'وصف ما تفعله'

        def check(self, ctx: ServiceValidationContext) -> None:
            # اقرأ من ctx.personnel، ctx.form_data، ctx.uploaded_attachments
            # في حال الخطأ: ctx.add_error(code=..., message=..., field=...)
            # في حال التحذير: ctx.add_warning(...)
            pass
    """
    # هوية القاعدة (تُستخدم في الـ Logs والـ Admin)
    name: str = ''
    description: str = ''

    @abstractmethod
    def check(self, ctx: ServiceValidationContext) -> None:
        """
        تنفيذ منطق التحقق.
        إذا كان الشرط مكسوراً → استدعِ ctx.add_error(...)
        إذا كان مجرد تحذير     → استدعِ ctx.add_warning(...)
        إذا كان كل شيء صحيحاً → لا تفعل شيئاً
        """
        pass

    @property
    def rule_id(self) -> str:
        """معرّف برمجي فريد للقاعدة (اسم الكلاس بالإنجليزية)."""
        return self.__class__.__name__


# ══════════════════════════════════════════════════════════════════════════════
# 4. ServiceRulesDispatcher — الموزع والمنسّق الرئيسي
# ══════════════════════════════════════════════════════════════════════════════

class ServiceRulesDispatcher:
    """
    المحرك الرئيسي: يربط كل كود خدمة بقائمة قواعده، ويشغّلها بالتسلسل.

    كيفية الاستخدام من API View:
    ──────────────────────────────
    ctx = ServiceRulesDispatcher.validate(
        personnel=personnel_instance,
        service_code='MARTYR_FORM',
        form_data=request.data,
        uploaded_attachments=['death_certificate', 'field_report'],
    )
    if ctx.has_blocking_errors():
        return Response(ctx.to_response_dict(), status=400)
    # المتابعة في حال نجاح التحقق...

    إضافة خدمة جديدة:
    ───────────────────
    from systems.services.service_rules.rules import my_new_rules
    ServiceRulesDispatcher.register('MY_NEW_SERVICE', my_new_rules.RULES)
    """

    # سجل القواعد: { service_code: [Rule1, Rule2, ...] }
    _registry: Dict[str, List[ServiceRule]] = {}

    @classmethod
    def register(cls, service_code: str, rules: List[ServiceRule]) -> None:
        """تسجيل قواعد خدمة جديدة. يُستدعى من __init__.py للحزمة."""
        cls._registry[service_code] = rules

    @classmethod
    def get_rules(cls, service_code: str) -> List[ServiceRule]:
        """استرداد قواعد خدمة معينة."""
        return cls._registry.get(service_code, [])

    @classmethod
    def validate(
        cls,
        personnel: "PersonnelMaster",
        service_code: str,
        form_data: Optional[Dict[str, Any]] = None,
        uploaded_attachments: Optional[List[str]] = None,
        disabled_rules: Optional[List[str]] = None,
    ) -> ServiceValidationContext:
        """
        نقطة الدخول الرئيسية لتشغيل التحقق.

        يقوم بـ:
        1. إنشاء سياق (Context) للعملية.
        2. تشغيل كل قاعدة مسجلة لهذه الخدمة بالتسلسل.
        3. إذا كانت قاعدة ما مانعة (blocking)، يتوقف عن تشغيل القواعد التالية التي تعتمد عليها.
        4. يُرجع السياق كاملاً للمتصل.

        ملاحظة: القواعد تُشغَّل جميعها ولا تتوقف عند أول خطأ بالافتراضي،
        لكي نجمع كل الأخطاء دفعة واحدة وعرضها للمستخدم (UX أفضل).
        """
        ctx = ServiceValidationContext(
            personnel=personnel,
            service_code=service_code,
            form_data=form_data or {},
            uploaded_attachments=uploaded_attachments or [],
            disabled_rules=disabled_rules or [],
        )

        rules = cls.get_rules(service_code)
        if not rules:
            # لا توجد قواعد مسجلة لهذه الخدمة — تحذير للمبرمج
            ctx.add_warning(
                code='NO_RULES_REGISTERED',
                message=f'لم يتم تسجيل أي قواعد للخدمة: {service_code}',
                details=f'تأكد من تسجيل قواعد الخدمة في ServiceRulesDispatcher._registry'
            )
            return ctx

        for rule in rules:
            if rule.rule_id in ctx.disabled_rules:
                continue
            rule.check(ctx)

        return ctx
