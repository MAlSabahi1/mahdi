"""
Application Use Cases: Snapshots
════════════════════════════════
حالات الاستخدام الخاصة باللقطات الشهرية والالتزام.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, Optional

from ...domain.entities.snapshots import MonthlySnapshotEntity, DirectorateComplianceEntity
from ...domain.repositories.i_snapshots_repo import IMonthlySnapshotRepository, IDirectorateComplianceRepository


@dataclass
class SaveSnapshotCommand:
    service_month: str
    data: Dict[str, Any]
    security_admin_id: Optional[int] = None
    central_department_id: Optional[int] = None


class SaveSnapshotUseCase:
    """حفظ لقطة شهرية جديدة أو تحديثها"""
    def __init__(self, repo: IMonthlySnapshotRepository):
        self._repo = repo

    def execute(self, cmd: SaveSnapshotCommand) -> MonthlySnapshotEntity:
        snapshot = self._repo.get_snapshot(
            service_month=cmd.service_month,
            security_admin_id=cmd.security_admin_id,
            central_department_id=cmd.central_department_id
        )

        if snapshot and snapshot.locked:
            raise ValueError(f"اللقطة الشهرية لشهر {cmd.service_month} مقفلة ولا يمكن تحديثها.")

        if not snapshot:
            snapshot = MonthlySnapshotEntity(
                service_month=cmd.service_month,
                data=cmd.data,
                security_admin_id=cmd.security_admin_id,
                central_department_id=cmd.central_department_id
            )
        else:
            snapshot.data = cmd.data

        self._repo.save(snapshot)
        return snapshot


@dataclass
class LockSnapshotCommand:
    service_month: str
    security_admin_id: Optional[int] = None
    central_department_id: Optional[int] = None


class LockSnapshotUseCase:
    """قفل لقطة شهرية لمنع التعديل المستقبلي عليها"""
    def __init__(self, repo: IMonthlySnapshotRepository):
        self._repo = repo

    def execute(self, cmd: LockSnapshotCommand) -> MonthlySnapshotEntity:
        snapshot = self._repo.get_snapshot(
            service_month=cmd.service_month,
            security_admin_id=cmd.security_admin_id,
            central_department_id=cmd.central_department_id
        )

        if not snapshot:
            raise ValueError(f"لا توجد لقطة لشهر {cmd.service_month} لقفلها.")

        snapshot.lock()
        self._repo.save(snapshot)
        return snapshot


@dataclass
class EvaluateComplianceCommand:
    service_month: str
    submission_date: datetime
    deadline_date: datetime
    error_count: int = 0
    rejected_changes_count: int = 0
    security_admin_id: Optional[int] = None
    central_department_id: Optional[int] = None


class EvaluateComplianceUseCase:
    """تقييم التزام إدارة بناءً على موعد التسليم والأخطاء"""
    def __init__(self, repo: IDirectorateComplianceRepository):
        self._repo = repo

    def execute(self, cmd: EvaluateComplianceCommand) -> DirectorateComplianceEntity:
        compliance = self._repo.get_compliance(
            service_month=cmd.service_month,
            security_admin_id=cmd.security_admin_id,
            central_department_id=cmd.central_department_id
        )

        if not compliance:
            compliance = DirectorateComplianceEntity(
                service_month=cmd.service_month,
                security_admin_id=cmd.security_admin_id,
                central_department_id=cmd.central_department_id
            )

        compliance.error_count = cmd.error_count
        compliance.rejected_changes_count = cmd.rejected_changes_count
        compliance.mark_submitted(cmd.submission_date, cmd.deadline_date)

        self._repo.save(compliance)
        return compliance
