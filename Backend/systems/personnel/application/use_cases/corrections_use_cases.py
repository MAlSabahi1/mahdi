"""
Application Use Cases: Corrections & Rank Settlements
═════════════════════════════════════════════════════
حالات الاستخدام لتصحيح البيانات وتسوية الرتب.
"""
from dataclasses import dataclass
from datetime import date
from typing import Optional

from ...domain.entities.corrections import SuggestedCorrectionEntity, RankSettlementEntity
from ...domain.repositories.i_corrections_repo import ISuggestedCorrectionRepository, IRankSettlementRepository


from dataclasses import dataclass
from datetime import date
from typing import Optional

from ...domain.entities.corrections import SuggestedCorrectionEntity, RankSettlementEntity
from ...domain.repositories.i_corrections_repo import ISuggestedCorrectionRepository, IRankSettlementRepository
from ...domain.repositories.i_personnel_repo import IPersonnelRepository

# =================================================================================
# Pragmatic Imports for Audit and Event Log (Application Layer depending on Infra)
# =================================================================================
from infra.audit.models import AuditLog
from systems.services.infrastructure.models.event_log import ServiceEventLog


@dataclass
class RequestCorrectionCommand:
    personnel_id: int
    field_name: str
    old_value: str
    new_value: str
    correction_type: str
    requested_by_id: int
    supporting_document_id: Optional[int] = None


class RequestCorrectionUseCase:
    """طلب تصحيح جديد لبيانات الفرد"""
    def __init__(self, repo: ISuggestedCorrectionRepository, personnel_repo: IPersonnelRepository):
        self._repo = repo
        self._personnel_repo = personnel_repo

    def execute(self, cmd: RequestCorrectionCommand) -> SuggestedCorrectionEntity:
        personnel = self._personnel_repo.get_by_id(cmd.personnel_id)
        if not personnel:
            raise ValueError(f"الفرد غير موجود: {cmd.personnel_id}")

        entity = SuggestedCorrectionEntity(
            personnel_id=cmd.personnel_id,
            field_name=cmd.field_name,
            old_value=cmd.old_value,
            new_value=cmd.new_value,
            correction_type=cmd.correction_type,
            requested_by_id=cmd.requested_by_id,
            supporting_document_id=cmd.supporting_document_id
        )
        entity.validate_request()
        
        saved_entity = self._repo.save(entity)
        
        # إنشاء سجل تدقيق للطلب
        AuditLog.objects.create(
            user_id=cmd.requested_by_id,
            action='CREATE',
            model_name='SuggestedCorrection',
            object_id=str(saved_entity.id),
            new_data={'correction_type': cmd.correction_type, 'field': cmd.field_name, 'new_value': cmd.new_value}
        )
        return saved_entity


@dataclass
class ApproveCorrectionCommand:
    correction_id: int
    reviewer_id: int
    approval_document_id: Optional[int] = None


class ApproveCorrectionUseCase:
    """اعتماد طلب تصحيح وتطبيق التعديل على الفرد"""
    def __init__(self, repo: ISuggestedCorrectionRepository, personnel_repo: IPersonnelRepository):
        self._repo = repo
        self._personnel_repo = personnel_repo

    def execute(self, cmd: ApproveCorrectionCommand) -> SuggestedCorrectionEntity:
        entity = self._repo.get_by_id(cmd.correction_id)
        if not entity:
            raise ValueError(f"طلب التصحيح رقم {cmd.correction_id} غير موجود.")
            
        personnel = self._personnel_repo.get_by_id(entity.personnel_id)
        if not personnel:
            raise ValueError(f"الفرد غير موجود: {entity.personnel_id}")
            
        entity.approve(cmd.reviewer_id)
        if cmd.approval_document_id:
            entity.approval_document_id = cmd.approval_document_id
            
        # تطبيق التعديل على كيان الفرد
        if hasattr(personnel, entity.field_name):
            setattr(personnel, entity.field_name, entity.new_value)
            self._personnel_repo.save(personnel)
            
        saved_entity = self._repo.save(entity)
        
        # إنشاء ServiceEventLog
        ServiceEventLog.objects.create(
            personnel_id=personnel.id,
            event_date=date.today(),
            service_month=date.today().strftime('%Y-%m'),
            field_name=entity.field_name,
            old_value=entity.old_value,
            new_value=entity.new_value,
            order_document_id=saved_entity.supporting_document_id,
            created_by_id=cmd.reviewer_id
        )
        
        # إنشاء AuditLog
        AuditLog.objects.create(
            user_id=cmd.reviewer_id,
            action='UPDATE',
            model_name='PersonnelMaster',
            object_id=personnel.military_number,
            old_data={entity.field_name: entity.old_value},
            new_data={entity.field_name: entity.new_value}
        )
            
        return saved_entity


@dataclass
class RejectCorrectionCommand:
    correction_id: int
    reviewer_id: int
    reason: str


class RejectCorrectionUseCase:
    """رفض طلب تصحيح وتسجيل السبب"""
    def __init__(self, repo: ISuggestedCorrectionRepository):
        self._repo = repo

    def execute(self, cmd: RejectCorrectionCommand) -> SuggestedCorrectionEntity:
        entity = self._repo.get_by_id(cmd.correction_id)
        if not entity:
            raise ValueError(f"طلب التصحيح رقم {cmd.correction_id} غير موجود.")
            
        entity.reject(cmd.reviewer_id, cmd.reason)
        saved_entity = self._repo.save(entity)
        
        AuditLog.objects.create(
            user_id=cmd.reviewer_id,
            action='UPDATE',
            model_name='SuggestedCorrection',
            object_id=str(saved_entity.id),
            old_data={'status': 'pending'},
            new_data={'status': 'rejected', 'reason': cmd.reason}
        )
        return saved_entity


@dataclass
class RequestRankSettlementCommand:
    personnel_id: int
    current_rank_id: int
    new_rank_id: int
    due_date: date
    decision_date: date
    decision_number: str
    requested_by_id: int
    supporting_document_id: Optional[int] = None


class RequestRankSettlementUseCase:
    """طلب تسوية رتبة جديد"""
    def __init__(self, repo: IRankSettlementRepository):
        self._repo = repo

    def execute(self, cmd: RequestRankSettlementCommand) -> RankSettlementEntity:
        entity = RankSettlementEntity(
            personnel_id=cmd.personnel_id,
            current_rank_id=cmd.current_rank_id,
            new_rank_id=cmd.new_rank_id,
            due_date=cmd.due_date,
            decision_date=cmd.decision_date,
            decision_number=cmd.decision_number,
            requested_by_id=cmd.requested_by_id,
            supporting_document_id=cmd.supporting_document_id
        )
        entity.validate_request()
        
        saved_entity = self._repo.save(entity)
        
        AuditLog.objects.create(
            user_id=cmd.requested_by_id,
            action='CREATE',
            model_name='RankSettlement',
            object_id=str(saved_entity.id),
            new_data={'new_rank_id': cmd.new_rank_id, 'decision_number': cmd.decision_number}
        )
        return saved_entity


@dataclass
class ApproveRankSettlementCommand:
    settlement_id: int
    reviewer_id: int
    approval_document_id: Optional[int] = None


class ApproveRankSettlementUseCase:
    """اعتماد تسوية رتبة وتطبيقها"""
    def __init__(self, repo: IRankSettlementRepository, personnel_repo: IPersonnelRepository):
        self._repo = repo
        self._personnel_repo = personnel_repo

    def execute(self, cmd: ApproveRankSettlementCommand) -> RankSettlementEntity:
        entity = self._repo.get_by_id(cmd.settlement_id)
        if not entity:
            raise ValueError(f"طلب تسوية الرتبة رقم {cmd.settlement_id} غير موجود.")
            
        personnel = self._personnel_repo.get_by_id(entity.personnel_id)
        if not personnel:
            raise ValueError(f"الفرد غير موجود: {entity.personnel_id}")
            
        entity.approve(cmd.reviewer_id)
        if cmd.approval_document_id:
            entity.approval_document_id = cmd.approval_document_id
            
        # تطبيق الترقية على الفرد
        old_rank_id = personnel.current_rank_id
        personnel.current_rank_id = entity.new_rank_id
        self._personnel_repo.save(personnel)
            
        saved_entity = self._repo.save(entity)
        
        ServiceEventLog.objects.create(
            personnel_id=personnel.id,
            event_date=entity.decision_date or date.today(),
            service_month=date.today().strftime('%Y-%m'),
            field_name='current_rank',
            old_value=str(old_rank_id),
            new_value=str(entity.new_rank_id),
            order_document_id=saved_entity.supporting_document_id,
            created_by_id=cmd.reviewer_id
        )

        AuditLog.objects.create(
            user_id=cmd.reviewer_id,
            action='SETTLEMENT',
            model_name='RankSettlement',
            object_id=str(saved_entity.id),
            old_data={'rank_id': old_rank_id},
            new_data={'rank_id': entity.new_rank_id, 'decision_number': entity.decision_number}
        )
        return saved_entity


@dataclass
class RejectRankSettlementCommand:
    settlement_id: int
    reviewer_id: int
    reason: str


class RejectRankSettlementUseCase:
    """رفض تسوية رتبة"""
    def __init__(self, repo: IRankSettlementRepository):
        self._repo = repo

    def execute(self, cmd: RejectRankSettlementCommand) -> RankSettlementEntity:
        entity = self._repo.get_by_id(cmd.settlement_id)
        if not entity:
            raise ValueError(f"طلب تسوية الرتبة رقم {cmd.settlement_id} غير موجود.")
            
        entity.reject(cmd.reviewer_id, cmd.reason)
        saved_entity = self._repo.save(entity)
        
        AuditLog.objects.create(
            user_id=cmd.reviewer_id,
            action='UPDATE',
            model_name='RankSettlement',
            object_id=str(saved_entity.id),
            old_data={'status': 'pending'},
            new_data={'status': 'rejected', 'reason': cmd.reason}
        )
        return saved_entity
