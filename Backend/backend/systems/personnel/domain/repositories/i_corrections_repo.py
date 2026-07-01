"""
Domain Repository Interfaces: Corrections & Rank Settlements
════════════════════════════════════════════════════════════
واجهات المستودعات للتصحيحات وتسويات الرتب.
"""
from typing import Protocol, Optional
from ..entities.corrections import SuggestedCorrectionEntity, RankSettlementEntity


class ISuggestedCorrectionRepository(Protocol):
    
    def get_by_id(self, correction_id: int) -> Optional[SuggestedCorrectionEntity]:
        """جلب طلب تصحيح بناءً على المعرف"""
        ...
        
    def save(self, correction: SuggestedCorrectionEntity) -> SuggestedCorrectionEntity:
        """حفظ أو تحديث طلب التصحيح"""
        ...


class IRankSettlementRepository(Protocol):
    
    def get_by_id(self, settlement_id: int) -> Optional[RankSettlementEntity]:
        """جلب تسوية رتبة بناءً على المعرف"""
        ...
        
    def save(self, settlement: RankSettlementEntity) -> RankSettlementEntity:
        """حفظ أو تحديث تسوية الرتبة"""
        ...
