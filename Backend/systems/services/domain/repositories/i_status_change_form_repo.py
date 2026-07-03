"""
Domain Repository Interface: StatusChangeForm
══════════════════════════════════════════════
واجهة مجردة — لا تعرف Django ولا قاعدة البيانات.
"""
from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID

from ..entities.status_change_form import StatusChangeFormEntity
from ..value_objects.status_change import FormStatus


class IStatusChangeFormRepository(ABC):

    @abstractmethod
    def get_by_id(self, form_id: UUID) -> Optional[StatusChangeFormEntity]:
        """جلب استمارة بالمعرف."""
        ...

    @abstractmethod
    def save(self, entity: StatusChangeFormEntity) -> StatusChangeFormEntity:
        """حفظ أو تحديث استمارة."""
        ...

    @abstractmethod
    def save_fields(self, entity: StatusChangeFormEntity, fields: List[str]) -> None:
        """
        تحديث حقول محددة فقط.
        مطابق لـ: form.save(update_fields=[...])
        """
        ...

    @abstractmethod
    def list_by_admin(
        self,
        security_admin_id: int,
        status: Optional[FormStatus] = None,
    ) -> List[StatusChangeFormEntity]:
        """قائمة الاستمارات لإدارة أمن مع فلترة اختيارية."""
        ...

    @abstractmethod
    def get_personnel_forms(
        self,
        personnel_id: int,
        status: Optional[FormStatus] = None,
    ) -> List[StatusChangeFormEntity]:
        """استمارات فرد محدد."""
        ...
