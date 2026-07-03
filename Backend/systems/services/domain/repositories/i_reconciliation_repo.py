"""
Repository Interface — مستودع المطابقة
══════════════════════════════════════════
واجهة مجردة فقط — لا تعرف Django ولا ORM.
الـ Infrastructure هي من ستطبق هذه الواجهة.
"""
from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID

from ..entities.reconciliation_task import ReconciliationTaskEntity
from ..value_objects.reconciliation import ReconciliationStatus


class IReconciliationRepository(ABC):
    """
    عقد (Contract) بين الـ Application وقاعدة البيانات.
    الـ Application تعرف هذه الواجهة فقط، لا تعرف Django.
    """

    @abstractmethod
    def get_by_id(self, task_id: UUID) -> Optional[ReconciliationTaskEntity]:
        """جلب مهمة بالمعرف."""
        ...

    @abstractmethod
    def save(self, entity: ReconciliationTaskEntity) -> ReconciliationTaskEntity:
        """حفظ أو تحديث مهمة."""
        ...

    @abstractmethod
    def list_by_admin(
        self,
        security_admin_id: int,
        status: Optional[ReconciliationStatus] = None,
    ) -> List[ReconciliationTaskEntity]:
        """قائمة المهام لإدارة أمن معينة مع فلترة اختيارية بالحالة."""
        ...

    @abstractmethod
    def exists_pending_for_admin(self, security_admin_id: int) -> bool:
        """هل توجد مطابقة قيد التنفيذ لهذه الإدارة؟"""
        ...
