"""
Domain Repository Interfaces: Staging Records
═════════════════════════════════════════════
واجهات المستودعات لسجلات المراجعة المؤقتة.
"""
from typing import Protocol, Optional, List
from ..entities.staging import StagingRecordEntity


class IStagingRecordRepository(Protocol):
    
    def get_by_id(self, record_id: int) -> Optional[StagingRecordEntity]:
        """جلب سجل مؤقت بناءً على المعرف"""
        ...
        
    def get_pending_records(self, batch_id: Optional[str] = None) -> List[StagingRecordEntity]:
        """جلب السجلات المعلقة للمراجعة"""
        ...
        
    def save(self, record: StagingRecordEntity) -> StagingRecordEntity:
        """حفظ أو تحديث السجل"""
        ...
