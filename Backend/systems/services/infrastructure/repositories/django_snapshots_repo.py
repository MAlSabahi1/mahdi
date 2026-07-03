"""
Infrastructure Repositories: Snapshots (Django ORM)
════════════════════════════════════════════════════
تطبيق المستودعات باستخدام Django ORM.
"""
from typing import Optional

from ...domain.entities.snapshots import MonthlySnapshotEntity, DirectorateComplianceEntity
from ...domain.repositories.i_snapshots_repo import IMonthlySnapshotRepository, IDirectorateComplianceRepository
from ..models.snapshots import MonthlySnapshot, DirectorateCompliance


class DjangoMonthlySnapshotRepository(IMonthlySnapshotRepository):
    
    def _to_entity(self, model: MonthlySnapshot) -> MonthlySnapshotEntity:
        return MonthlySnapshotEntity(
            service_month=model.service_month,
            data=model.data,
            security_admin_id=model.security_admin_id,
            central_department_id=model.central_department_id,
            locked=model.locked,
        )

    def _to_model(self, entity: MonthlySnapshotEntity) -> MonthlySnapshot:
        # We handle get_or_create logic in save
        return MonthlySnapshot(
            service_month=entity.service_month,
            data=entity.data,
            security_admin_id=entity.security_admin_id,
            central_department_id=entity.central_department_id,
            locked=entity.locked,
        )

    def get_snapshot(self, service_month: str, security_admin_id: Optional[int], central_department_id: Optional[int]) -> Optional[MonthlySnapshotEntity]:
        try:
            model = MonthlySnapshot.objects.get(
                service_month=service_month,
                security_admin_id=security_admin_id,
                central_department_id=central_department_id
            )
            return self._to_entity(model)
        except MonthlySnapshot.DoesNotExist:
            return None

    def save(self, snapshot: MonthlySnapshotEntity) -> None:
        model, created = MonthlySnapshot.objects.update_or_create(
            service_month=snapshot.service_month,
            security_admin_id=snapshot.security_admin_id,
            central_department_id=snapshot.central_department_id,
            defaults={
                'data': snapshot.data,
                'locked': snapshot.locked,
            }
        )


class DjangoDirectorateComplianceRepository(IDirectorateComplianceRepository):
    
    def _to_entity(self, model: DirectorateCompliance) -> DirectorateComplianceEntity:
        return DirectorateComplianceEntity(
            service_month=model.service_month,
            security_admin_id=model.security_admin_id,
            central_department_id=model.central_department_id,
            submitted_at=model.submitted_at,
            error_count=model.error_count,
            rejected_changes_count=model.rejected_changes_count,
            late_days=model.late_days,
            quality_score=model.quality_score,
        )

    def get_compliance(self, service_month: str, security_admin_id: Optional[int], central_department_id: Optional[int]) -> Optional[DirectorateComplianceEntity]:
        try:
            model = DirectorateCompliance.objects.get(
                service_month=service_month,
                security_admin_id=security_admin_id,
                central_department_id=central_department_id
            )
            return self._to_entity(model)
        except DirectorateCompliance.DoesNotExist:
            return None

    def save(self, compliance: DirectorateComplianceEntity) -> None:
        model, created = DirectorateCompliance.objects.update_or_create(
            service_month=compliance.service_month,
            security_admin_id=compliance.security_admin_id,
            central_department_id=compliance.central_department_id,
            defaults={
                'submitted_at': compliance.submitted_at,
                'error_count': compliance.error_count,
                'rejected_changes_count': compliance.rejected_changes_count,
                'late_days': compliance.late_days,
                'quality_score': compliance.quality_score,
            }
        )
