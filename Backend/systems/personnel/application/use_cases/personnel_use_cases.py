"""
Application Use Cases: Personnel
═════════════════════════════════
حالات الاستخدام لنظام الأفراد.
تعمل كطبقة التنسيق (Orchestration) بين الـ Domain والـ Repositories.
"""
from dataclasses import dataclass
from typing import Optional
from datetime import date

from ...domain.entities.personnel import PersonnelEntity
from ...domain.repositories.i_personnel_repo import IPersonnelRepository


@dataclass
class RegisterPersonnelCommand:
    military_number:   str
    full_name:         str
    current_rank_id:   int
    current_status_id: int
    security_admin_id: int
    
    national_id:       Optional[str] = None
    birth_date:        Optional[date] = None
    join_date:         Optional[date] = None
    phone_number:      Optional[str] = None

    central_department_id: Optional[int] = None
    branch_id:             Optional[int] = None
    district_police_id:    Optional[int] = None
    division_id:           Optional[int] = None
    unit_id:               Optional[int] = None

    category_id:             Optional[int] = None
    job_title_id:            Optional[int] = None
    position_id:             Optional[int] = None
    force_classification_id: Optional[int] = None


class RegisterPersonnelUseCase:
    """
    تسجيل فرد جديد في النظام.
    يضمن تطبيق قواعد الأسماء والهواتف وتحديد نوع الرقم العسكري قبل الحفظ.
    """
    def __init__(self, repo: IPersonnelRepository):
        self._repo = repo

    def execute(self, cmd: RegisterPersonnelCommand) -> PersonnelEntity:
        # 1. التحقق من عدم التكرار
        if self._repo.get_by_military_number(cmd.military_number):
            raise ValueError(f"الرقم العسكري {cmd.military_number} مسجل مسبقاً.")
            
        if cmd.national_id and self._repo.get_by_national_id(cmd.national_id):
            raise ValueError(f"الرقم الوطني {cmd.national_id} مسجل مسبقاً مع فرد آخر.")

        # 2. إنشاء الكيان
        personnel = PersonnelEntity(
            military_number=cmd.military_number,
            full_name=cmd.full_name,
            current_rank_id=cmd.current_rank_id,
            current_status_id=cmd.current_status_id,
            security_admin_id=cmd.security_admin_id,
            national_id=cmd.national_id,
            birth_date=cmd.birth_date,
            join_date=cmd.join_date,
            phone_number=cmd.phone_number,
            
            central_department_id=cmd.central_department_id,
            branch_id=cmd.branch_id,
            district_police_id=cmd.district_police_id,
            division_id=cmd.division_id,
            unit_id=cmd.unit_id,
            
            category_id=cmd.category_id,
            job_title_id=cmd.job_title_id,
            position_id=cmd.position_id,
            force_classification_id=cmd.force_classification_id
        )

        # 3. تطبيق قواعد الأعمال
        personnel.normalize_phone_number()
        
        name_errors = personnel.validate_name()
        if name_errors:
            raise ValueError(" | ".join(name_errors))

        # 4. الحفظ
        self._repo.save(personnel)
        return personnel


@dataclass
class UpdateCompletenessCommand:
    military_number: str
    has_photo:       bool
    has_fingerprint: bool


class UpdateCompletenessUseCase:
    """
    تحديث علامة اكتمال بيانات الفرد (بعد رفع صورة أو أخذ بصمة).
    """
    def __init__(self, repo: IPersonnelRepository):
        self._repo = repo

    def execute(self, cmd: UpdateCompletenessCommand) -> PersonnelEntity:
        personnel = self._repo.get_by_military_number(cmd.military_number)
        if not personnel:
            raise ValueError(f"الفرد ذو الرقم العسكري {cmd.military_number} غير موجود.")

        personnel.update_completeness(cmd.has_photo, cmd.has_fingerprint)
        self._repo.save(personnel)
        
        return personnel
