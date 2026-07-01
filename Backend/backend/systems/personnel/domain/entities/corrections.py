"""
Domain Entities: Corrections & Rank Settlements
═══════════════════════════════════════════════
التصحيحات المقترحة وتسويات الرتب ككائنات بايثون نقية تدير قواعد الأعمال.
"""
from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Dict, Any, Optional, List


@dataclass
class SuggestedCorrectionEntity:
    """كيان اقتراح التصحيح لبيانات الفرد"""
    personnel_id: int
    field_name: str
    old_value: str
    new_value: str
    correction_type: str
    status: str = 'pending'
    
    supporting_document_id: Optional[int] = None
    approval_document_id: Optional[int] = None
    
    requested_by_id: Optional[int] = None
    requested_at: Optional[datetime] = None
    
    reviewed_by_id: Optional[int] = None
    reviewed_at: Optional[datetime] = None
    rejection_reason: str = ''
    
    # قائمة الحقول المسموح بتعديلها
    ALLOWED_CORRECTION_FIELDS = [
        'full_name',
        'national_id',
        'birth_date',
        'join_date',
        'phone_number',
    ]

    # متطلبات المستندات لكل نوع تصحيح
    DOCUMENT_REQUIREMENTS = {
        'name_correction': True,
        'national_id_correction': False,
        'military_number_correction': True,
    }

    def validate_request(self) -> None:
        """التحقق من صحة طلب التصحيح قبل الحفظ"""
        if self.field_name not in self.ALLOWED_CORRECTION_FIELDS:
            raise ValueError(
                f'الحقل "{self.field_name}" غير مسموح بتصحيحه. '
                f'الحقول المسموحة: {", ".join(self.ALLOWED_CORRECTION_FIELDS)}'
            )
            
        requires_doc = self.DOCUMENT_REQUIREMENTS.get(self.correction_type, False)
        if requires_doc and not self.supporting_document_id:
            raise ValueError(f'نوع التصحيح "{self.correction_type}" يتطلب إرفاق مستند داعم.')

    def approve(self, reviewer_id: int) -> None:
        """اعتماد طلب التصحيح"""
        if self.status != 'pending':
            raise ValueError('لا يمكن اعتماد طلب تمت معالجته مسبقاً.')
        
        self.status = 'approved'
        self.reviewed_by_id = reviewer_id
        self.reviewed_at = datetime.now()

    def reject(self, reviewer_id: int, reason: str) -> None:
        """رفض طلب التصحيح مع ذكر السبب"""
        if self.status != 'pending':
            raise ValueError('لا يمكن رفض طلب تمت معالجته مسبقاً.')
            
        if not reason or not reason.strip():
            raise ValueError('يجب توفير سبب لرفض الطلب.')
            
        self.status = 'rejected'
        self.rejection_reason = reason.strip()
        self.reviewed_by_id = reviewer_id
        self.reviewed_at = datetime.now()


@dataclass
class RankSettlementEntity:
    """كيان تسوية الرتب (الترقيات)"""
    personnel_id: int
    current_rank_id: int
    new_rank_id: int
    due_date: date
    decision_date: date
    decision_number: str
    status: str = 'pending'
    
    supporting_document_id: Optional[int] = None
    approval_document_id: Optional[int] = None
    
    requested_by_id: Optional[int] = None
    requested_at: Optional[datetime] = None
    
    reviewed_by_id: Optional[int] = None
    reviewed_at: Optional[datetime] = None
    rejection_reason: str = ''

    def validate_request(self) -> None:
        """التحقق من صحة طلب تسوية الرتبة"""
        if self.current_rank_id == self.new_rank_id:
            raise ValueError('الرتبة الجديدة يجب أن تكون مختلفة عن الرتبة الحالية.')
            
        if self.decision_date > date.today():
            raise ValueError('تاريخ القرار لا يمكن أن يكون في المستقبل.')

        if not self.decision_number.strip():
            raise ValueError('يجب إدخال رقم القرار.')

    def approve(self, reviewer_id: int) -> None:
        """اعتماد تسوية الرتبة"""
        if self.status != 'pending':
            raise ValueError('لا يمكن اعتماد تسوية تمت معالجتها مسبقاً.')
        
        self.status = 'approved'
        self.reviewed_by_id = reviewer_id
        self.reviewed_at = datetime.now()

    def reject(self, reviewer_id: int, reason: str) -> None:
        """رفض تسوية الرتبة"""
        if self.status != 'pending':
            raise ValueError('لا يمكن رفض تسوية تمت معالجتها مسبقاً.')
            
        if not reason or not reason.strip():
            raise ValueError('يجب توفير سبب لرفض التسوية.')
            
        self.status = 'rejected'
        self.rejection_reason = reason.strip()
        self.reviewed_by_id = reviewer_id
        self.reviewed_at = datetime.now()
