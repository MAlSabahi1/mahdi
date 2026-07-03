"""
Infrastructure Repositories: Staging Records
════════════════════════════════════════════
تطبيق المستودعات باستخدام Django ORM.
"""
from typing import Optional, List
from ...domain.entities.staging import StagingRecordEntity
from ...domain.repositories.i_staging_repo import IStagingRecordRepository
from ..models.staging import StagingRecord


class DjangoStagingRecordRepository(IStagingRecordRepository):
    
    def _to_entity(self, model: StagingRecord) -> StagingRecordEntity:
        return StagingRecordEntity(
            import_batch_id=str(model.import_batch_id),
            row_index=model.row_index,
            military_number=model.military_number,
            action_type=model.action_type,
            status=model.status,
            changes=model.changes,
            validation_errors=model.validation_errors,
            security_admin_id=model.security_admin_id,
            central_department_id=model.central_department_id,
            rejection_reason=model.rejection_reason,
            reviewed_by_id=model.reviewed_by_id,
            reviewed_at=model.reviewed_at
        )

    def _to_model(self, entity: StagingRecordEntity, model: Optional[StagingRecord] = None) -> StagingRecord:
        if model is None:
            model = StagingRecord()
            
        model.import_batch_id = entity.import_batch_id
        model.row_index = entity.row_index
        model.military_number = entity.military_number
        model.action_type = entity.action_type
        model.status = entity.status
        model.changes = entity.changes
        model.validation_errors = entity.validation_errors
        model.security_admin_id = entity.security_admin_id
        model.central_department_id = entity.central_department_id
        model.rejection_reason = entity.rejection_reason
        model.reviewed_by_id = entity.reviewed_by_id
        model.reviewed_at = entity.reviewed_at
        return model

    def get_by_id(self, record_id: int) -> Optional[StagingRecordEntity]:
        try:
            model = StagingRecord.objects.get(id=record_id)
            entity = self._to_entity(model)
            entity.id = model.id
            return entity
        except StagingRecord.DoesNotExist:
            return None

    def get_pending_records(self, batch_id: Optional[str] = None) -> List[StagingRecordEntity]:
        qs = StagingRecord.objects.filter(status='pending')
        if batch_id:
            qs = qs.filter(import_batch_id=batch_id)
            
        entities = []
        for model in qs:
            entity = self._to_entity(model)
            entity.id = model.id
            entities.append(entity)
        return entities

    def save(self, record: StagingRecordEntity) -> StagingRecordEntity:
        record_id = getattr(record, 'id', None)
        if record_id:
            model = StagingRecord.objects.get(id=record_id)
            model = self._to_model(record, model)
            model.save()
        else:
            model = self._to_model(record)
            model.save()
            record.id = model.id
        return record
