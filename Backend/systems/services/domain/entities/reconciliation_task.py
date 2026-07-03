"""
Reconciliation Entity — كيان مهمة المطابقة
════════════════════════════════════════════
Python نقي — لا يوجد أي استيراد من Django هنا.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID, uuid4

from ..value_objects.reconciliation import (
    ReconciliationTaskType,
    ReconciliationStatus,
    ReconciliationResult,
)


@dataclass
class ReconciliationTaskEntity:
    """
    كيان مهمة المطابقة.
    يحتوي على قواعد الأعمال فقط، لا يعرف قاعدة البيانات.
    """
    name:              str
    task_type:         ReconciliationTaskType
    security_admin_id: int                          # Reference by ID فقط
    created_by_id:     int                          # Reference by ID فقط
    key_field:         str                          # حقل الربط (military_number)
    id:                UUID                  = field(default_factory=uuid4)
    status:            ReconciliationStatus  = ReconciliationStatus.PENDING
    result:            Optional[ReconciliationResult] = None
    source_file_path:  Optional[str]         = None  # المسار يُحدد من الـ Infrastructure

    # ──────────────────────────────────────────────
    # Business Rules
    # ──────────────────────────────────────────────

    def can_be_executed(self) -> bool:
        """المطابقة تُنفذ فقط إذا كانت في حالة pending."""
        return self.status == ReconciliationStatus.PENDING

    def mark_completed(self, result: ReconciliationResult) -> None:
        """
        قاعدة أعمال: إنهاء المطابقة بنجاح.
        يتحقق من الحالة قبل التغيير.
        """
        if self.status != ReconciliationStatus.PENDING:
            raise ValueError(
                f"لا يمكن إنهاء مهمة بحالة '{self.status.value}'"
            )
        self.result = result
        self.status = ReconciliationStatus.COMPLETED

    def mark_failed(self, reason: str) -> None:
        """
        قاعدة أعمال: تسجيل فشل المطابقة.
        """
        if self.status != ReconciliationStatus.PENDING:
            raise ValueError(
                f"لا يمكن تسجيل فشل مهمة بحالة '{self.status.value}'"
            )
        error_result = ReconciliationResult(
            matched=0,
            unmatched=0,
            errors=[reason],
        )
        self.result = error_result
        self.status = ReconciliationStatus.FAILED

    def get_result_summary(self) -> str:
        if self.result is None:
            return "لا توجد نتائج بعد"
        return self.result.summary
