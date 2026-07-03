"""
Domain Entities: Snapshots
════════════════════════════
اللقطات الشهرية ومتابعة الالتزام ككائنات بايثون نقية.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, Optional


@dataclass
class MonthlySnapshotEntity:
    """كيان اللقطة الشهرية"""
    service_month: str  # YYYY-MM
    data: Dict[str, Any]
    security_admin_id: Optional[int] = None
    central_department_id: Optional[int] = None
    locked: bool = False
    
    def lock(self) -> None:
        """قفل اللقطة لمنع التعديل عليها"""
        self.locked = True

    def is_empty(self) -> bool:
        """التحقق إذا كانت اللقطة فارغة من البيانات"""
        return not bool(self.data)


@dataclass
class DirectorateComplianceEntity:
    """كيان متابعة التزام الإدارات"""
    service_month: str
    security_admin_id: Optional[int] = None
    central_department_id: Optional[int] = None
    
    submitted_at: Optional[datetime] = None
    error_count: int = 0
    rejected_changes_count: int = 0
    late_days: int = 0
    quality_score: int = 100

    def calculate_quality_score(self) -> None:
        """
        حساب درجة الجودة بناءً على الأخطاء، الرفض، والتأخير.
        قواعد افتراضية:
        - كل خطأ يخصم نقطة.
        - كل تغيير مرفوض يخصم نقطتين.
        - كل يوم تأخير يخصم 3 نقاط.
        - لا يمكن أن تقل الدرجة عن 0.
        """
        deductions = (
            (self.error_count * 1) +
            (self.rejected_changes_count * 2) +
            (self.late_days * 3)
        )
        self.quality_score = max(0, 100 - deductions)

    def mark_submitted(self, submission_date: datetime, deadline_date: datetime) -> None:
        """تسجيل التسليم وحساب أيام التأخير"""
        self.submitted_at = submission_date
        if submission_date > deadline_date:
            delta = submission_date - deadline_date
            self.late_days = delta.days
        else:
            self.late_days = 0
        
        self.calculate_quality_score()
