"""
خدمة تصحيح البيانات الأساسية - جسر (Bridge)
تم نقل المنطق إلى أنظمة Clean Architecture (Use Cases).
هذا الملف يعمل كواجهة توافقية للحفاظ على التوافقية مع الـ Views القديمة.
"""

from typing import Dict, Optional
from infra.storage.models import Document
from systems.personnel.models import SuggestedCorrection

# Import Clean Architecture Components
from systems.personnel.infrastructure.repositories.django_corrections_repo import DjangoSuggestedCorrectionRepository
from systems.personnel.infrastructure.repositories.django_personnel_repo import DjangoPersonnelRepository
from systems.personnel.application.use_cases.corrections_use_cases import (
    RequestCorrectionCommand,
    RequestCorrectionUseCase,
    ApproveCorrectionCommand,
    ApproveCorrectionUseCase,
    RejectCorrectionCommand,
    RejectCorrectionUseCase
)


class CorrectionValidationError(Exception):
    pass


class CorrectionService:
    ALLOWED_CORRECTION_FIELDS = [
        'full_name',
        'national_id',
        'birth_date',
        'join_date',
        'phone_number',
    ]
    
    def __init__(self, user):
        self.user = user
        self.repo = DjangoSuggestedCorrectionRepository()
        self.personnel_repo = DjangoPersonnelRepository()

    def request_correction(self, personnel_id: int, correction_type: str, new_value: str, field_name: str, supporting_document: Optional[Document] = None) -> SuggestedCorrection:
        if field_name not in self.ALLOWED_CORRECTION_FIELDS:
            raise CorrectionValidationError(
                f'الحقل "{field_name}" غير مسموح بتصحيحه. '
                f'الحقول المسموحة: {", ".join(self.ALLOWED_CORRECTION_FIELDS)}'
            )
            
        governorate = getattr(self.user, 'profile', None) and self.user.profile.governorate
        personnel = self.personnel_repo.get_by_id(personnel_id)
        if not personnel:
            raise CorrectionValidationError(f'الفرد غير موجود: {personnel_id}')
            
        if governorate and personnel.governorate_id != governorate.id:
            raise CorrectionValidationError('لا يمكنك طلب تعديل على فرد خارج محافظتك')
            
        old_value = getattr(personnel, field_name, '')
        
        cmd = RequestCorrectionCommand(
            personnel_id=personnel_id,
            field_name=field_name,
            old_value=str(old_value),
            new_value=str(new_value),
            correction_type=correction_type,
            requested_by_id=self.user.id,
            supporting_document_id=supporting_document.id if supporting_document else None
        )
        
        uc = RequestCorrectionUseCase(self.repo, self.personnel_repo)
        try:
            result = uc.execute(cmd)
            # Return the actual Django model for backward compatibility
            return SuggestedCorrection.objects.get(id=result.id)
        except ValueError as e:
            raise CorrectionValidationError(str(e))

    def approve_correction(self, correction_id: int) -> Dict:
        cmd = ApproveCorrectionCommand(
            correction_id=correction_id,
            reviewer_id=self.user.id
        )
        uc = ApproveCorrectionUseCase(self.repo, self.personnel_repo)
        
        try:
            # Governorate check before execution
            entity = self.repo.get_by_id(correction_id)
            if not entity:
                raise CorrectionValidationError('الطلب غير موجود أو تمت معالجته مسبقا')
                
            governorate = getattr(self.user, 'profile', None) and self.user.profile.governorate
            if governorate:
                # Need to check personnel's governorate
                personnel = self.personnel_repo.get_by_id(entity.personnel_id)
                if personnel and personnel.governorate_id != governorate.id:
                    raise CorrectionValidationError('لا تملك صلاحية اعتماد هذا الطلب في محافظة أخرى')
            
            result = uc.execute(cmd)
            personnel = self.personnel_repo.get_by_id(result.personnel_id)
            
            return {
                'success': True,
                'correction_id': result.id,
                'military_number': personnel.military_number if personnel else '',
                'field': result.field_name,
                'status': 'approved'
            }
        except ValueError as e:
            raise CorrectionValidationError(str(e))

    def reject_correction(self, correction_id: int, reason: str) -> Dict:
        if not reason or not reason.strip():
            raise CorrectionValidationError('يرجى تقديم سبب لرفض طلب التصحيح')
            
        cmd = RejectCorrectionCommand(
            correction_id=correction_id,
            reviewer_id=self.user.id,
            reason=reason
        )
        uc = RejectCorrectionUseCase(self.repo)
        
        try:
            entity = self.repo.get_by_id(correction_id)
            if not entity:
                raise CorrectionValidationError('الطلب غير موجود أو تمت معالجته مسبقا')
                
            governorate = getattr(self.user, 'profile', None) and self.user.profile.governorate
            if governorate:
                personnel = self.personnel_repo.get_by_id(entity.personnel_id)
                if personnel and personnel.governorate_id != governorate.id:
                    raise CorrectionValidationError('لا تملك صلاحية رفض هذا الطلب في محافظة أخرى')
            
            result = uc.execute(cmd)
            return {
                'success': True,
                'correction_id': result.id,
                'status': 'rejected',
                'reason': reason
            }
        except ValueError as e:
            raise CorrectionValidationError(str(e))
