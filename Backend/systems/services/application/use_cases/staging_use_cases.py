"""
Application Use Cases: Staging Records
══════════════════════════════════════
حالات الاستخدام لمراجعة سجلات الإدخال.
"""
from dataclasses import dataclass
from typing import List

from ...domain.entities.staging import StagingRecordEntity
from ...domain.repositories.i_staging_repo import IStagingRecordRepository


from dataclasses import dataclass
from datetime import date
from typing import List, Optional

from ...domain.entities.staging import StagingRecordEntity
from ...domain.repositories.i_staging_repo import IStagingRecordRepository
from systems.personnel.domain.repositories.i_personnel_repo import IPersonnelRepository

# =================================================================================
# Pragmatic Imports for Audit, Event Log, Rejection Log, and Compliance
# =================================================================================
from infra.audit.models import AuditLog
from systems.services.infrastructure.models.event_log import ServiceEventLog
from systems.services.infrastructure.models.logs import RejectionLog
from systems.services.infrastructure.models.snapshots import DirectorateCompliance
from core.models import ServiceStatus


@dataclass
class ReviewStagingCommand:
    record_id: int
    reviewer_id: int
    action: str  # 'approve' or 'reject'
    reason: str = ''
    document_id: Optional[int] = None


class ReviewStagingRecordUseCase:
    """مراجعة يدوية لسجل إدخال (موافقة أو رفض) وتطبيق التغييرات الفعلية"""
    def __init__(self, repo: IStagingRecordRepository, personnel_repo: IPersonnelRepository):
        self._repo = repo
        self._personnel_repo = personnel_repo

    def execute(self, cmd: ReviewStagingCommand) -> StagingRecordEntity:
        entity = self._repo.get_by_id(cmd.record_id)
        if not entity:
            raise ValueError(f"السجل رقم {cmd.record_id} غير موجود.")
            
        personnel = self._personnel_repo.get_by_military_number(entity.military_number)
        if not personnel:
            raise ValueError(f"الفرد ذو الرقم {entity.military_number} غير موجود.")
            
        if cmd.action == 'approve':
            entity.approve(cmd.reviewer_id)
            
            # 1. تحديث حالة الفرد
            new_status_name = entity.changes.get('status', {}).get('new', '')
            old_status_name = entity.changes.get('status', {}).get('old', '')
            
            try:
                new_status = ServiceStatus.objects.get(name=new_status_name)
            except ServiceStatus.DoesNotExist:
                raise ValueError(f"الحالة المقترحة غير موجودة في النظام: {new_status_name}")
                
            personnel.current_status_id = new_status.id
            self._personnel_repo.save(personnel)
            
            # 2. إنشاء ServiceEventLog
            ServiceEventLog.objects.create(
                personnel_id=personnel.id,
                event_date=date.today(),
                service_month=date.today().strftime('%Y-%m'),
                field_name='current_status',
                old_value=old_status_name,
                new_value=new_status_name,
                order_document_id=cmd.document_id,
                created_by_id=cmd.reviewer_id
            )
            
            # 3. إنشاء AuditLog
            AuditLog.objects.create(
                user_id=cmd.reviewer_id,
                action='UPDATE',
                model_name='PersonnelMaster',
                object_id=personnel.military_number,
                old_data={'current_status': old_status_name},
                new_data={'current_status': new_status_name}
            )
            
        elif cmd.action == 'reject':
            entity.reject(cmd.reason, cmd.reviewer_id)
            
            service_month = date.today().strftime('%Y-%m')
            
            # 1. إنشاء RejectionLog
            RejectionLog.objects.create(
                staging_record_id=entity.id,
                central_department_id=personnel.central_department_id,
                service_month=service_month,
                personnel_id=personnel.id,
                proposed_status=entity.changes.get('status', {}).get('new', ''),
                rejection_reason=cmd.reason,
                rejected_by_id=cmd.reviewer_id
            )
            
            # 2. تحديث DirectorateCompliance
            if personnel.central_department_id:
                compliance, _ = DirectorateCompliance.objects.get_or_create(
                    central_department_id=personnel.central_department_id,
                    service_month=service_month,
                    defaults={'quality_score': 100}
                )
                compliance.rejected_changes_count += 1
                compliance.save(update_fields=['rejected_changes_count'])
                
            # 3. إنشاء AuditLog
            AuditLog.objects.create(
                user_id=cmd.reviewer_id,
                action='UPDATE',
                model_name='StagingRecord',
                object_id=str(entity.id),
                old_data={'status': 'pending'},
                new_data={'status': 'rejected', 'reason': cmd.reason}
            )
        else:
            raise ValueError("الإجراء غير معروف. استخدم 'approve' أو 'reject'.")
            
        return self._repo.save(entity)


@dataclass
class AutoApproveBatchCommand:
    batch_id: str
    reviewer_id: int


class AutoApproveLowSeverityUseCase:
    """الموافقة التلقائية على السجلات ذات التعديلات الطفيفة في دفعة معينة"""
    def __init__(self, repo: IStagingRecordRepository, personnel_repo: IPersonnelRepository):
        self._repo = repo
        self._personnel_repo = personnel_repo

    def execute(self, cmd: AutoApproveBatchCommand) -> List[StagingRecordEntity]:
        pending_records = self._repo.get_pending_records(batch_id=cmd.batch_id)
        approved_records = []
        
        # We reuse the ReviewStagingRecordUseCase logic
        review_uc = ReviewStagingRecordUseCase(self._repo, self._personnel_repo)
        
        for entity in pending_records:
            if entity.can_be_auto_approved():
                review_cmd = ReviewStagingCommand(
                    record_id=entity.id,
                    reviewer_id=cmd.reviewer_id,
                    action='approve'
                )
                review_uc.execute(review_cmd)
                approved_records.append(entity)
                
        return approved_records

