"""
Application Use Cases: Status Change Form
══════════════════════════════════════════
حالات الاستخدام لاستمارة إثبات الحالة.
تنسق بين الـ Domain والـ Infrastructure.

مطابقة للمنطق الموجود في:
    api/views/status_change_views.py
    → submit(), _advance(), approve_director(), reject()
"""
from __future__ import annotations
import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol, Optional
from uuid import UUID

from ...domain.entities.status_change_form import StatusChangeFormEntity
from ...domain.repositories.i_status_change_form_repo import IStatusChangeFormRepository
from ...domain.value_objects.status_change import ApprovalLevel, FormType, FormStatus

logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────────────────────────
# Protocols (Dependency Injection بطريقة Python)
# ──────────────────────────────────────────────────────────────────

class IPersonnelUpdater(Protocol):
    """تحديث الحالة الخدمية للفرد عند الاعتماد النهائي."""
    def update_status(self, personnel_id: int, to_status_id: int) -> None: ...


class IAttachmentCommitter(Protocol):
    """تثبيت مرفقات الاستمارة عند الاعتماد النهائي."""
    def commit_form_attachments(self, form_id: UUID) -> None: ...


class IEventPublisher(Protocol):
    """نشر الأحداث بعد commit قاعدة البيانات."""
    def publish_approved(self, form: StatusChangeFormEntity, approved_by_id: int) -> None: ...
    def publish_rejected(self, form: StatusChangeFormEntity, reason: str) -> None: ...


# ──────────────────────────────────────────────────────────────────
# Commands (CQRS)
# ──────────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class SubmitFormCommand:
    form_id:       UUID
    submitted_by:  int
    submitted_at:  datetime
    first_step_id: Optional[int] = None


@dataclass(frozen=True)
class ApproveFormCommand:
    form_id:      UUID
    approved_by:  int
    approved_at:  datetime
    next_step_id: Optional[int] = None


@dataclass(frozen=True)
class RejectFormCommand:
    form_id:     UUID
    reason:      str
    rejected_by: int


# ──────────────────────────────────────────────────────────────────
# Use Case 1: تقديم الاستمارة (draft → pending_services)
# ──────────────────────────────────────────────────────────────────

class SubmitStatusFormUseCase:
    """
    مطابق لـ: StatusChangeFormViewSet.submit()
    draft → pending_services
    """
    def __init__(self, repo: IStatusChangeFormRepository):
        self._repo = repo

    def execute(self, cmd: SubmitFormCommand) -> StatusChangeFormEntity:
        form = self._repo.get_by_id(cmd.form_id)
        if not form:
            raise ValueError(f"الاستمارة {cmd.form_id} غير موجودة")

        # قاعدة الأعمال في الـ Entity
        form.submit(submitted_at=cmd.submitted_at, first_step_id=cmd.first_step_id)

        # حفظ الحقول المعدّلة فقط
        self._repo.save_fields(form, ['status', 'submitted_at', 'current_step_id', 'workflow_log'])
        logger.info(f"Form {form.id} submitted by user {cmd.submitted_by}")
        return form


# ──────────────────────────────────────────────────────────────────
# Use Case 2: اعتماد الاستمارة (3 مستويات)
# ──────────────────────────────────────────────────────────────────

class ApproveStatusFormUseCase:
    """
    مطابق لـ:
        StatusChangeFormViewSet._advance()     → مستويات 1 و 2
        StatusChangeFormViewSet.approve_director() → المستوى 3 (الأهم)

    المستوى 3 (DIRECTOR) فقط ينفذ:
        - تحديث حالة الفرد الخدمية
        - تثبيت المرفقات
        - نشر الأحداث
    """
    def __init__(
        self,
        repo:                IStatusChangeFormRepository,
        personnel_updater:   IPersonnelUpdater,
        attachment_committer: IAttachmentCommitter,
        event_publisher:     IEventPublisher,
    ):
        self._repo                 = repo
        self._personnel_updater    = personnel_updater
        self._attachment_committer = attachment_committer
        self._event_publisher      = event_publisher

    def execute(self, cmd: ApproveFormCommand) -> StatusChangeFormEntity:
        form = self._repo.get_by_id(cmd.form_id)
        if not form:
            raise ValueError(f"الاستمارة {cmd.form_id} غير موجودة")

        # قاعدة الأعمال في الـ Entity
        form.approve_current_step(
            approved_by_id=cmd.approved_by,
            approved_at=cmd.approved_at,
            next_step_id=cmd.next_step_id,
        )

        # تحديث قاعدة البيانات
        self._repo.save_fields(form, ['status', 'current_step_id', 'workflow_log'])

        # المستوى النهائي
        if form.is_approved() and form.to_status_id:
            # تحديث حالة الفرد
            self._personnel_updater.update_status(
                personnel_id=form.personnel_id,
                to_status_id=form.to_status_id,
            )
            # تثبيت المرفقات
            self._attachment_committer.commit_form_attachments(form.id)
            
            # نشر الأحداث
            self._event_publisher.publish_approved(form, cmd.approved_by)

        logger.info(
            f"Form {form.id} approved "
            f"by user {cmd.approved_by} → new status: {form.status.value}"
        )
        return form


# ──────────────────────────────────────────────────────────────────
# Use Case 3: رفض الاستمارة
# ──────────────────────────────────────────────────────────────────

class RejectStatusFormUseCase:
    """
    مطابق لـ: StatusChangeFormViewSet.reject()
    أي pending_* → rejected
    """
    def __init__(
        self,
        repo:           IStatusChangeFormRepository,
        event_publisher: IEventPublisher,
    ):
        self._repo            = repo
        self._event_publisher = event_publisher

    def execute(self, cmd: RejectFormCommand) -> StatusChangeFormEntity:
        form = self._repo.get_by_id(cmd.form_id)
        if not form:
            raise ValueError(f"الاستمارة {cmd.form_id} غير موجودة")

        # قاعدة الأعمال في الـ Entity
        form.reject(reason=cmd.reason, rejected_by_id=cmd.rejected_by)

        self._repo.save_fields(form, ['status', 'rejection_reason', 'rejected_by'])

        # نشر الأحداث
        self._event_publisher.publish_rejected(form, cmd.reason)

        logger.info(f"Form {form.id} rejected by user {cmd.rejected_by}. Reason: {cmd.reason}")
        return form
