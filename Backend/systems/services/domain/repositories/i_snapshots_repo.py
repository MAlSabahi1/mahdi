"""
Domain Repository Interfaces: Snapshots
════════════════════════════════════════
واجهات المستودعات للقطات الشهرية والالتزام.
"""
from typing import Protocol, Optional, List
from ..entities.snapshots import MonthlySnapshotEntity, DirectorateComplianceEntity


class IMonthlySnapshotRepository(Protocol):
    
    def get_snapshot(self, service_month: str, security_admin_id: Optional[int], central_department_id: Optional[int]) -> Optional[MonthlySnapshotEntity]:
        """جلب لقطة شهرية معينة بناءً على الشهر والجهة"""
        ...
        
    def save(self, snapshot: MonthlySnapshotEntity) -> None:
        """حفظ أو تحديث اللقطة الشهرية"""
        ...


class IDirectorateComplianceRepository(Protocol):
    
    def get_compliance(self, service_month: str, security_admin_id: Optional[int], central_department_id: Optional[int]) -> Optional[DirectorateComplianceEntity]:
        """جلب سجل الالتزام لشهر وجهة معينة"""
        ...
        
    def save(self, compliance: DirectorateComplianceEntity) -> None:
        """حفظ سجل الالتزام"""
        ...
