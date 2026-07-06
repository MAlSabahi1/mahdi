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
        # Convert proposed_change (JSON) to changes dict
        changes_dict = {}
        if isinstance(model.proposed_change, dict):
            changes_dict = {'status': {'new': model.proposed_change.get('status', '')}}
            # Also map the monthly variable
            if 'monthly_variable' in model.proposed_change:
                changes_dict['monthly_variable'] = model.proposed_change['monthly_variable']

        return StagingRecordEntity(
            import_batch_id=str(model.upload_batch_id),
            row_index=0,  # Not tracked in DB
            military_number=model.personnel.military_number if model.personnel else '',
            action_type='update',
            status=model.status,
            changes=changes_dict,
            validation_errors=[],
            security_admin_id=model.security_admin_id,
            central_department_id=model.personnel.central_department_id if model.personnel else None,
            rejection_reason=model.rejection_reason,
            reviewed_by_id=model.reviewed_by_id,
            reviewed_at=model.reviewed_at
        )

    def _to_model(self, entity: StagingRecordEntity, model: Optional[StagingRecord] = None) -> StagingRecord:
        if model is None:
            model = StagingRecord()
            
        # upload_batch_id is mapped from import_batch_id
        model.upload_batch_id = entity.import_batch_id
        model.status = entity.status
        # proposed_change mapped back if needed (usually we don't overwrite it here)
        
        model.security_admin_id = entity.security_admin_id
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
