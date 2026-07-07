"""
Domain Entities: Corrections & Rank Settlements
Base class definitions for personal details suggestions and rank adjustments.
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
        'military_number',
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

        # التحقق من الصيغة حسب نوع التصحيح والحقل
        if self.correction_type == 'national_id_correction' or self.field_name == 'national_id':
            if not self.new_value or not self.new_value.isdigit() or len(self.new_value) != 11:
                raise ValueError('الرقم الوطني يجب أن يتكون من 11 رقماً بالضبط ويحتوي على أرقام فقط.')
                
        elif self.correction_type == 'military_number_correction' or self.field_name == 'military_number':
            if not self.new_value or not self.new_value.isdigit() or len(self.new_value) != 7:
                raise ValueError('الرقم العسكري يجب أن يتكون من 7 أرقام بالضبط ويحتوي على أرقام فقط.')
            if self.new_value.startswith('0'):
                raise ValueError('الرقم العسكري لا يمكن أن يبدأ بالرقم 0.')

        elif self.correction_type == 'name_correction' or self.field_name == 'full_name':
            import re
            # الاسم يجب أن يحتوي على أحرف عربية ومسافات فقط
            if not re.match(r'^[؀-ۿݐ-ݿﭐ-﷿ﹰ-﻿\s\-]+$', self.new_value.strip()):
                raise ValueError('الاسم يجب أن يحتوي على أحرف عربية ومسافات فقط.')
            parts = self.new_value.strip().split()
            if len(parts) < 4:
                raise ValueError('الاسم يجب أن يكون رباعياً على الأقل (الاسم + الأب + الجد + اللقب).')
            if len(parts) > 7:
                raise ValueError('الاسم يجب ألا يزيد عن 7 أجزاء.')
            if self.new_value.strip() == self.old_value.strip():
                raise ValueError('الاسم الجديد يجب أن يكون مختلفاً عن الاسم الحالي.')

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
    settlement_type: str
    status: str = 'pending'
    new_military_number: Optional[str] = None
    
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

        if self.settlement_type == 'personnel_to_officer':
            if not self.new_military_number:
                raise ValueError('تسوية فرد إلى ضابط تتطلب إدخال الرقم العسكري الجديد.')
            if not self.new_military_number.isdigit() or len(self.new_military_number) != 7:
                raise ValueError('الرقم العسكري الجديد للضابط يجب أن يكون 7 أرقام.')
            if not self.new_military_number.startswith('60'):
                raise ValueError('الرقم العسكري الجديد للضابط يجب أن يبدأ بـ 60.')
        elif self.settlement_type in ('same_class_promotion', 'demotion'):
            if self.new_military_number:
                raise ValueError('هذا النوع من التسوية لا يتطلب رقماً عسكرياً جديداً.')

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
