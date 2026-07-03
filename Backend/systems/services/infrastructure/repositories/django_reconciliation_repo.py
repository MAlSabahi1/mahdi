"""
Django ORM Repository — تطبيق مستودع المطابقة
════════════════════════════════════════════════
هنا فقط يُسمح باستخدام Django ORM.
يحول بين Django Models وـ Domain Entities.
"""
from __future__ import annotations
from typing import Optional, List
from uuid import UUID

from ...domain.entities.reconciliation_task import ReconciliationTaskEntity
from ...domain.repositories.i_reconciliation_repo import IReconciliationRepository
from ...domain.value_objects.reconciliation import (
    ReconciliationStatus,
    ReconciliationResult,
)
# الاستيراد من نموذج Django الموجود في نفس infrastructure
from ..models.reconciliation import ReconciliationTask as ReconciliationTaskModel


class DjangoReconciliationRepository(IReconciliationRepository):
    """
    التطبيق الفعلي للـ Repository.
    يُعطى للـ Use Cases عبر Dependency Injection في الـ View.
    """

    def get_by_id(self, task_id: UUID) -> Optional[ReconciliationTaskEntity]:
        try:
            model = ReconciliationTaskModel.objects.get(id=task_id)
            return self._to_entity(model)
        except ReconciliationTaskModel.DoesNotExist:
            return None

    def save(self, entity: ReconciliationTaskEntity) -> ReconciliationTaskEntity:
        result_data = entity.result.to_dict() if entity.result else None

        model, _ = ReconciliationTaskModel.objects.update_or_create(
            id=entity.id,
            defaults={
                "name":              entity.name,
                "task_type":         entity.task_type.value,
                "security_admin_id": entity.security_admin_id,
                "created_by_id":     entity.created_by_id,
                "key_field":         entity.key_field,
                "status":            entity.status.value,
                "result":            result_data,
                "source_file":       entity.source_file_path or "",
            },
        )
        return self._to_entity(model)

    def list_by_admin(
        self,
        security_admin_id: int,
        status: Optional[ReconciliationStatus] = None,
    ) -> List[ReconciliationTaskEntity]:
        qs = ReconciliationTaskModel.objects.filter(
            security_admin_id=security_admin_id
        )
        if status:
            qs = qs.filter(status=status.value)
        return [self._to_entity(m) for m in qs.order_by("-created_at")]

    def exists_pending_for_admin(self, security_admin_id: int) -> bool:
        return ReconciliationTaskModel.objects.filter(
            security_admin_id=security_admin_id,
            status=ReconciliationStatus.PENDING.value,
        ).exists()

    # ──────────────────────────────────────────────
    # Private: تحويل Model → Entity
    # ──────────────────────────────────────────────

    def _to_entity(self, model: ReconciliationTaskModel) -> ReconciliationTaskEntity:
        result = None
        if model.result:
            result = ReconciliationResult(
                matched=model.result.get("matched", 0),
                unmatched=model.result.get("unmatched", 0),
                errors=model.result.get("errors", []),
            )

        return ReconciliationTaskEntity(
            id=model.id,
            name=model.name,
            task_type=model.task_type,
            security_admin_id=model.security_admin_id,
            created_by_id=model.created_by_id,
            key_field=model.key_field,
            status=ReconciliationStatus(model.status),
            result=result,
            source_file_path=str(model.source_file) if model.source_file else None,
        )
