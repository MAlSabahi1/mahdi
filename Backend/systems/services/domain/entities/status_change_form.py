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
    ApprovalLevel,
    APPROVAL_TRANSITIONS,
    REJECTABLE_STATUSES,
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
    form_type:         FormType
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
    services_approved_by_id:  Optional[int]      = None
    services_approved_at:     Optional[datetime] = None
    hr_approved_by_id:        Optional[int]      = None
    hr_approved_at:           Optional[datetime] = None
    director_approved_by_id:  Optional[int]      = None
    director_approved_at:     Optional[datetime] = None

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
        """يمكن تقديم المسودات فقط — من: view.submit()"""
        return self.status == FormStatus.DRAFT

    def submit(self, submitted_at: datetime) -> None:
        """
        تقديم الاستمارة: draft → pending_services
        مطابق لـ: form.status = 'pending_services'
        """
        if not self.can_be_submitted():
            raise ValueError(f"يمكن تقديم المسودات فقط. الحالة الحالية: {self.status.value}")

        self.status       = FormStatus.PENDING_SERVICES
        self.submitted_at = submitted_at

    def can_be_approved_by(self, level: ApprovalLevel) -> bool:
        """هل يمكن اعتماد الاستمارة من هذا المستوى؟"""
        return (self.status, level) in APPROVAL_TRANSITIONS

    def approve(self, level: ApprovalLevel, approved_by_id: int, approved_at: datetime) -> None:
        """
        اعتماد الاستمارة بمستوى محدد.
        مطابق لـ: view._advance() و view.approve_director()

        الانتقالات:
            SERVICES: pending_services → pending_hr
            HR:       pending_hr       → pending_director
            DIRECTOR: pending_director → approved  (النهائي)
        """
        if not self.can_be_approved_by(level):
            raise ValueError(
                f"لا يمكن اعتماد استمارة بحالة '{self.status.value}' "
                f"من مستوى '{level.name}'"
            )

        next_status = APPROVAL_TRANSITIONS[(self.status, level)]
        self.status = next_status

        if level == ApprovalLevel.SERVICES:
            self.services_approved_by_id = approved_by_id
            self.services_approved_at    = approved_at
        elif level == ApprovalLevel.HR:
            self.hr_approved_by_id = approved_by_id
            self.hr_approved_at    = approved_at
        elif level == ApprovalLevel.DIRECTOR:
            self.director_approved_by_id = approved_by_id
            self.director_approved_at    = approved_at

    def can_be_rejected(self) -> bool:
        """يمكن الرفض في أي مرحلة pending — مطابق لـ: view.reject()"""
        return self.status in REJECTABLE_STATUSES

    def reject(self, reason: str, rejected_by_id: int) -> None:
        """
        رفض الاستمارة: أي pending_* → rejected
        مطابق لـ: form.status = 'rejected'
        """
        if not self.can_be_rejected():
            raise ValueError(
                f"لا يمكن الرفض في الحالة '{self.status.value}'. "
                f"مسموح فقط من: {[s.value for s in REJECTABLE_STATUSES]}"
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

    def get_next_approver_level(self) -> Optional[ApprovalLevel]:
        """ما هو المستوى المطلوب لاعتماد هذه الاستمارة الآن؟"""
        _map = {
            FormStatus.PENDING_SERVICES: ApprovalLevel.SERVICES,
            FormStatus.PENDING_HR:       ApprovalLevel.HR,
            FormStatus.PENDING_DIRECTOR: ApprovalLevel.DIRECTOR,
        }
        return _map.get(self.status)

    def get_fields_to_update_on_approve(self, level: ApprovalLevel) -> list[str]:
        """
        يُعيد قائمة الحقول التي يجب تحديثها في DB بعد الاعتماد.
        مطابق لـ: form.save(update_fields=[...])
        """
        base = ['status']
        fields_map = {
            ApprovalLevel.SERVICES: ['services_approved_by', 'services_approved_at'],
            ApprovalLevel.HR:       ['hr_approved_by', 'hr_approved_at'],
            ApprovalLevel.DIRECTOR: ['director_approved_by', 'director_approved_at'],
        }
        return base + fields_map.get(level, [])

    def __repr__(self) -> str:
        return (
            f"StatusChangeFormEntity("
            f"id={self.id}, type={self.form_type.value}, status={self.status.value})"
        )
