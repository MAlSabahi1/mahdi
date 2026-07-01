"""
Domain Entities: Staging Records
════════════════════════════════
سجلات الإدخال المؤقت ومراجعة الإكسل (Staging) ككائنات بايثون نقية.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, Optional, List


@dataclass
class StagingRecordEntity:
    """كيان السجل المؤقت للمراجعة"""
    import_batch_id: str  # UUID as string
    row_index: int
    military_number: str
    action_type: str  # 'insert', 'update', 'no_change'
    status: str = 'pending'  # pending, approved, rejected
    
    # تفاصيل التغييرات: Dict of field_name -> {'old': X, 'new': Y}
    changes: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    
    # الأخطاء في التنسيق
    validation_errors: List[str] = field(default_factory=list)
    
    security_admin_id: Optional[int] = None
    central_department_id: Optional[int] = None
    
    rejection_reason: str = ''
    reviewed_by_id: Optional[int] = None
    reviewed_at: Optional[datetime] = None

    # مستوى خطورة التعديل (لتحديد هل يمكن القبول التلقائي أو يتطلب مراجعة)
    HIGH_SEVERITY_FIELDS = ['military_number', 'national_id', 'full_name', 'current_rank', 'birth_date']

    def is_high_severity(self) -> bool:
        """يحدد ما إذا كان التعديل يعتبر حساساً ويحتاج مراجعة بشرية"""
        for field_name in self.changes.keys():
            if field_name in self.HIGH_SEVERITY_FIELDS:
                return True
        return False

    def can_be_auto_approved(self) -> bool:
        """هل يمكن قبول السجل تلقائياً؟"""
        if self.action_type == 'no_change':
            return True
            
        if self.validation_errors:
            return False  # السجلات ذات الأخطاء لا تُقبل تلقائياً
            
        if self.action_type == 'update' and not self.is_high_severity():
            return True
            
        return False

    def approve(self, reviewer_id: Optional[int] = None) -> None:
        """الموافقة على السجل"""
        if self.status != 'pending':
            raise ValueError(f"لا يمكن الموافقة على سجل بحالة {self.status}.")
            
        if self.validation_errors:
            raise ValueError("لا يمكن الموافقة على سجل يحتوي على أخطاء تحقق (Validation Errors).")
            
        self.status = 'approved'
        self.reviewed_by_id = reviewer_id
        self.reviewed_at = datetime.now()

    def reject(self, reason: str, reviewer_id: Optional[int] = None) -> None:
        """رفض السجل"""
        if self.status != 'pending':
            raise ValueError(f"لا يمكن رفض سجل بحالة {self.status}.")
            
        if not reason.strip():
            raise ValueError("يجب تحديد سبب الرفض.")
            
        self.status = 'rejected'
        self.rejection_reason = reason.strip()
        self.reviewed_by_id = reviewer_id
        self.reviewed_at = datetime.now()
