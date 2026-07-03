"""
Value Objects — المطابقة
═══════════════════════
قيم ثابتة لا تتغير، بدون أي استيراد من Django.
"""
from enum import Enum


class ReconciliationTaskType(str, Enum):
    """نوع المطابقة"""
    ATTENDANCE    = "attendance"    # مطابقة حضور
    PAYROLL       = "payroll"       # مطابقة راتب
    QUALIFICATION = "qualification" # مطابقة مؤهلات


class ReconciliationStatus(str, Enum):
    """حالة مهمة المطابقة"""
    PENDING   = "pending"
    COMPLETED = "completed"
    FAILED    = "failed"


class ReconciliationResult:
    """
    نتيجة المطابقة — Value Object
    لا يمكن تعديلها بعد الإنشاء
    """
    __slots__ = ("_matched", "_unmatched", "_errors", "_summary")

    def __init__(
        self,
        matched: int,
        unmatched: int,
        errors: list[str],
    ):
        self._matched   = matched
        self._unmatched = unmatched
        self._errors    = tuple(errors)  # immutable
        self._summary   = f"✅ {matched} مطابق | ❌ {unmatched} غير مطابق | ⚠️ {len(errors)} خطأ"

    @property
    def matched(self) -> int:
        return self._matched

    @property
    def unmatched(self) -> int:
        return self._unmatched

    @property
    def errors(self) -> tuple:
        return self._errors

    @property
    def summary(self) -> str:
        return self._summary

    @property
    def is_successful(self) -> bool:
        return len(self._errors) == 0

    def to_dict(self) -> dict:
        return {
            "matched":   self._matched,
            "unmatched": self._unmatched,
            "errors":    list(self._errors),
            "summary":   self._summary,
        }
