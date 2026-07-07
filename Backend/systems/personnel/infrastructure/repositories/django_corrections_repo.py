"""
Infrastructure Repositories: Corrections & Rank Settlements
═══════════════════════════════════════════════════════════
تطبيق المستودعات باستخدام Django ORM.
"""
from typing import Optional
from ...domain.entities.corrections import SuggestedCorrectionEntity, RankSettlementEntity
from ...domain.repositories.i_corrections_repo import ISuggestedCorrectionRepository, IRankSettlementRepository
from systems.personnel.models import SuggestedCorrection, RankSettlement


class DjangoSuggestedCorrectionRepository(ISuggestedCorrectionRepository):
    
    def _to_entity(self, model: SuggestedCorrection) -> SuggestedCorrectionEntity:
        return SuggestedCorrectionEntity(
            personnel_id=model.personnel_id,
            field_name=model.field_name,
            old_value=model.old_value,
            new_value=model.new_value,
            correction_type=model.correction_type,
            status=model.status,
            supporting_document_id=model.supporting_document_id,
            approval_document_id=model.approval_document_id,
            requested_by_id=model.requested_by_id,
            requested_at=model.requested_at,
            reviewed_by_id=model.reviewed_by_id,
            reviewed_at=model.reviewed_at,
            rejection_reason=model.rejection_reason
        )
        
    def _to_model(self, entity: SuggestedCorrectionEntity, model: Optional[SuggestedCorrection] = None) -> SuggestedCorrection:
        if model is None:
            model = SuggestedCorrection()
            # Auto-assign governorate from personnel (infrastructure detail)
            if entity.personnel_id:
                from systems.personnel.models import PersonnelMaster
                try:
                    p = PersonnelMaster.objects.get(id=entity.personnel_id)
                    model.governorate_id = p.governorate_id
                except PersonnelMaster.DoesNotExist:
                    pass
            
        model.personnel_id = entity.personnel_id
        model.field_name = entity.field_name
        model.old_value = entity.old_value
        model.new_value = entity.new_value
        model.correction_type = entity.correction_type
        model.status = entity.status
        model.supporting_document_id = entity.supporting_document_id
        model.approval_document_id = entity.approval_document_id
        model.requested_by_id = entity.requested_by_id
        model.reviewed_by_id = entity.reviewed_by_id
        model.reviewed_at = entity.reviewed_at
        model.rejection_reason = entity.rejection_reason
        return model

    def get_by_id(self, correction_id: int) -> Optional[SuggestedCorrectionEntity]:
        try:
            model = SuggestedCorrection.objects.get(id=correction_id)
            entity = self._to_entity(model)
            # إضافة الـ ID للكيان مؤقتاً لتسهيل التحديث
            entity.id = model.id
            return entity
        except SuggestedCorrection.DoesNotExist:
            return None

    def save(self, correction: SuggestedCorrectionEntity) -> SuggestedCorrectionEntity:
        correction_id = getattr(correction, 'id', None)
        if correction_id:
            model = SuggestedCorrection.objects.get(id=correction_id)
            model = self._to_model(correction, model)
            model.save()
        else:
            model = self._to_model(correction)
            model.save()
            correction.id = model.id
            correction.requested_at = model.requested_at
        return correction


class DjangoRankSettlementRepository(IRankSettlementRepository):
    
    def _to_entity(self, model: RankSettlement) -> RankSettlementEntity:
        return RankSettlementEntity(
            personnel_id=model.personnel_id,
            current_rank_id=model.current_rank_id,
            new_rank_id=model.new_rank_id,
            due_date=model.due_date,
            decision_date=model.decision_date,
            decision_number=model.decision_number,
            settlement_type=model.settlement_type,
            status=model.status,
            new_military_number=model.new_military_number,
            supporting_document_id=model.supporting_document_id,
            approval_document_id=model.approval_document_id,
            requested_by_id=model.requested_by_id,
            requested_at=model.requested_at,
            reviewed_by_id=model.reviewed_by_id,
            reviewed_at=model.reviewed_at,
            rejection_reason=model.rejection_reason
        )

    def _to_model(self, entity: RankSettlementEntity, model: Optional[RankSettlement] = None) -> RankSettlement:
        if model is None:
            model = RankSettlement()
            
        model.personnel_id = entity.personnel_id
        model.current_rank_id = entity.current_rank_id
        model.new_rank_id = entity.new_rank_id
        model.due_date = entity.due_date
        model.decision_date = entity.decision_date
        model.decision_number = entity.decision_number
        model.settlement_type = entity.settlement_type
        model.status = entity.status
        model.new_military_number = entity.new_military_number
        model.supporting_document_id = entity.supporting_document_id
        model.approval_document_id = entity.approval_document_id
        model.requested_by_id = entity.requested_by_id
        model.reviewed_by_id = entity.reviewed_by_id
        model.reviewed_at = entity.reviewed_at
        model.rejection_reason = entity.rejection_reason
        return model

    def get_by_id(self, settlement_id: int) -> Optional[RankSettlementEntity]:
        try:
            model = RankSettlement.objects.get(id=settlement_id)
            entity = self._to_entity(model)
            entity.id = model.id
            return entity
        except RankSettlement.DoesNotExist:
            return None

    def save(self, settlement: RankSettlementEntity) -> RankSettlementEntity:
        settlement_id = getattr(settlement, 'id', None)
        if settlement_id:
            model = RankSettlement.objects.get(id=settlement_id)
            model = self._to_model(settlement, model)
            model.save()
        else:
            model = self._to_model(settlement)
            model.save()
            settlement.id = model.id
            settlement.requested_at = model.requested_at
        return settlement
