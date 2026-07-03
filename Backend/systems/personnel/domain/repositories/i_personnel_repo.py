"""
Domain Repository Interface: Personnel
══════════════════════════════════════
واجهة المستودع لكيان الفرد.
"""
from typing import Protocol, Optional
from uuid import UUID

from ..entities.personnel import PersonnelEntity


class IPersonnelRepository(Protocol):
    
    def get_by_military_number(self, military_number: str) -> Optional[PersonnelEntity]:
        """استرجاع الفرد بناءً على الرقم العسكري."""
        ...
        
    def get_by_national_id(self, national_id: str) -> Optional[PersonnelEntity]:
        """استرجاع الفرد بناءً على الرقم الوطني."""
        ...
        
    def save(self, personnel: PersonnelEntity) -> None:
        """حفظ أو تحديث بيانات الفرد."""
        ...
        
    def soft_delete(self, military_number: str) -> None:
        """الحذف المنطقي للفرد."""
        ...
