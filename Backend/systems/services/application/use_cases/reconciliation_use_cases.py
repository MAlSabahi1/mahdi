"""
Reconciliation Use Cases — حالات الاستخدام للمطابقة
══════════════════════════════════════════════════════
تنسق بين الـ Domain والـ Infrastructure.
لا تعرف Django. لا تعرف قاعدة البيانات مباشرة.
"""
from __future__ import annotations
import logging
from typing import Protocol

from ...domain.entities.reconciliation_task import ReconciliationTaskEntity
from ...domain.repositories.i_reconciliation_repo import IReconciliationRepository
from ...domain.value_objects.reconciliation import (
    ReconciliationTaskType,
    ReconciliationResult,
)
from ..commands.reconciliation_commands import (
    CreateReconciliationCommand,
    ExecuteReconciliationCommand,
)

logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────────────────────────
# Protocol (Dependency Injection بطريقة Python)
# ──────────────────────────────────────────────────────────────────

class IReconciliationProcessor(Protocol):
    """
    واجهة محرك المطابقة الفعلي.
    التطبيق يكون في Infrastructure (مثل ExcelReconciliationProcessor).
    """
    def process(
        self,
        file_path: str,
        key_field: str,
        task_type: str,
    ) -> ReconciliationResult:
        ...


# ──────────────────────────────────────────────────────────────────
# Use Case 1: إنشاء مهمة مطابقة
# ──────────────────────────────────────────────────────────────────

class CreateReconciliationUseCase:
    """
    إنشاء مهمة مطابقة جديدة.
    يتحقق من عدم وجود مطابقة قيد التنفيذ لنفس الإدارة.
    """

    def __init__(self, repo: IReconciliationRepository):
        self._repo = repo

    def execute(self, command: CreateReconciliationCommand) -> ReconciliationTaskEntity:
        # قاعدة أعمال: منع تشغيل مطابقتين متزامنتين لنفس الإدارة
        if self._repo.exists_pending_for_admin(command.security_admin_id):
            raise ValueError(
                "توجد مطابقة قيد التنفيذ لهذه الإدارة. انتظر اكتمالها قبل إنشاء مهمة جديدة."
            )

        task = ReconciliationTaskEntity(
            name=command.name,
            task_type=ReconciliationTaskType(command.task_type),
            security_admin_id=command.security_admin_id,
            created_by_id=command.created_by_id,
            key_field=command.key_field,
            source_file_path=command.source_file_path,
        )

        saved = self._repo.save(task)
        logger.info(f"ReconciliationTask created: {saved.id} | type={saved.task_type}")
        return saved


# ──────────────────────────────────────────────────────────────────
# Use Case 2: تشغيل المطابقة
# ──────────────────────────────────────────────────────────────────

class ExecuteReconciliationUseCase:
    """
    تشغيل مطابقة موجودة.
    يجلب المهمة، يشغّل المحرك، يحفظ النتيجة.
    """

    def __init__(
        self,
        repo:      IReconciliationRepository,
        processor: IReconciliationProcessor,
    ):
        self._repo      = repo
        self._processor = processor

    def execute(self, command: ExecuteReconciliationCommand) -> ReconciliationTaskEntity:
        # 1. جلب المهمة
        task = self._repo.get_by_id(command.task_id)
        if not task:
            raise ValueError(f"مهمة المطابقة {command.task_id} غير موجودة")

        # 2. تحقق من قاعدة الأعمال (في الـ Entity)
        if not task.can_be_executed():
            raise ValueError(
                f"لا يمكن تشغيل مهمة بحالة '{task.status.value}'"
            )

        # 3. تشغيل المحرك (في الـ Infrastructure)
        try:
            result = self._processor.process(
                file_path=task.source_file_path,
                key_field=task.key_field,
                task_type=task.task_type.value,
            )
            task.mark_completed(result)
            logger.info(f"Reconciliation {task.id} completed. {result.summary}")
        except Exception as exc:
            task.mark_failed(str(exc))
            logger.error(f"Reconciliation {task.id} failed: {exc}")

        # 4. حفظ النتيجة
        return self._repo.save(task)
