"""
Domain Entity: StatusChangeForm
══════════════════════════════════
كيان استمارة إثبات الحالة — يحتوي كل قواعد الأعمال.
Python نقي — لا Django — مطابق لـ status_change_views.py الموجود.

دورة الحياة:
    draft
      ↓ submit()
    pending_services
      ↓ approve(SERVICES)
    pending_hr
      ↓ approve(HR)
    pending_director
      ↓ approve(DIRECTOR)
    approved
    
    أي مرحلة من pending_* → rejected بـ reject()
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional
from uuid import UUID

from ..value_objects.status_change import (
    FormStatus,
    FormType,
)


@dataclass
class StatusChangeFormEntity:
    """
    كيان الاستمارة — يعكس بالضبط منطق status_change_views.py الموجود.
    يُنشأ من الـ Repository عند جلب النموذج من قاعدة البيانات.
    """
    # ── بيانات أساسية ──
    personnel_id:      int
    security_admin_id: int
    form_type:         str
    submitted_by_id:   int

    # ── الحالتان ──
    from_status_id:    Optional[int]  = None   # الحالة الخدمية السابقة
    to_status_id:      Optional[int]  = None   # الحالة الخدمية الجديدة

    # ── بيانات الاستمارة ──
    form_data:         dict           = field(default_factory=dict)
    effective_date:    Optional[date] = None
    notes:             str            = ""

    # ── الحالة الحالية ──
    status:            FormStatus     = FormStatus.DRAFT

    # ── بيانات دورة الاعتماد ──
    submitted_at:             Optional[datetime] = None
    current_step_id:          Optional[int]      = None
    workflow_log:             list               = field(default_factory=list)

    # ── الرفض ──
    rejection_reason:  str           = ""
    rejected_by_id:    Optional[int] = None

    # ── المرفقات ──
    required_attachments: list       = field(default_factory=list)
    attachments_complete: bool       = False

    # ── المعرف (يُضاف بعد الحفظ) ──
    id: Optional[UUID] = None

    # ══════════════════════════════════════════════════════════════
    # State Machine — مطابق لـ status_change_views.py
    # ══════════════════════════════════════════════════════════════

    def can_be_submitted(self) -> bool:
        """يمكن تقديم المسودات فقط"""
        return self.status == FormStatus.DRAFT

    def submit(self, submitted_at: datetime, first_step_id: int) -> None:
        """تقديم الاستمارة وبدء المسار في الخطوة الأولى"""
        if not self.can_be_submitted():
            raise ValueError(f"يمكن تقديم المسودات فقط. الحالة الحالية: {self.status.value}")

        self.status       = FormStatus.IN_PROGRESS
        self.submitted_at = submitted_at
        self.current_step_id = first_step_id
        
        self.workflow_log.append({
            'action': 'submitted',
            'at': submitted_at.isoformat()
        })

    def approve_current_step(self, approved_by_id: int, approved_at: datetime, next_step_id: Optional[int]) -> None:
        """
        اعتماد المرحلة الحالية وتمريرها للمرحلة القادمة أو إنهاؤها
        """
        if self.status != FormStatus.IN_PROGRESS:
            raise ValueError(f"لا يمكن الاعتماد واستمارة بحالة '{self.status.value}'")

        # سجل الاعتماد
        self.workflow_log.append({
            'action': 'approved_step',
            'step_id': self.current_step_id,
            'approved_by': approved_by_id,
            'at': approved_at.isoformat()
        })

        if next_step_id:
            # الانتقال للمرحلة التالية
            self.current_step_id = next_step_id
        else:
            # تم الوصول للنهاية
            self.current_step_id = None
            self.status = FormStatus.APPROVED

    def can_be_rejected(self) -> bool:
        """يمكن الرفض في أي مرحلة قيد الإجراء (in_progress)"""
        return self.status == FormStatus.IN_PROGRESS

    def reject(self, reason: str, rejected_by_id: int) -> None:
        """
        رفض الاستمارة: in_progress → rejected
        مطابق لـ: form.status = 'rejected'
        """
        if not self.can_be_rejected():
            raise ValueError(
                f"لا يمكن الرفض في الحالة '{self.status.value}'. "
                f"مسموح فقط في حالة: '{FormStatus.IN_PROGRESS.value}'"
            )

        self.status           = FormStatus.REJECTED
        self.rejection_reason = reason
        self.rejected_by_id   = rejected_by_id

    def is_final(self) -> bool:
        """هل الاستمارة في حالة نهائية؟"""
        return self.status in (FormStatus.APPROVED, FormStatus.REJECTED)

    def is_approved(self) -> bool:
        """هل تمت الموافقة النهائية؟"""
        return self.status == FormStatus.APPROVED

    def __repr__(self) -> str:
        return (
            f"StatusChangeFormEntity("
            f"id={self.id}, type={self.form_type}, status={self.status.value})"
        )
