"""
Domain Entity: PersonnelMaster
═════════════════════════════════
كيان الفرد الأساسي — מכيل قواعد الأعمال.
Python نقي — لا Django.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date
from typing import Optional
import re

from ..value_objects.personnel import NationalIdStatus, MilitaryNumberType, ExpenseStatus


# جدول تحويل الأرقام العربية
ARABIC_DIGIT_MAP = str.maketrans('٠١٢٣٤٥٦٧٨٩', '0123456789')


@dataclass
class PersonnelEntity:
    """
    كيان الفرد، يعكس البيانات الأساسية وقواعد التحقق (Clean Architecture).
    """
    # ── الهوية ──
    military_number:     str
    full_name:           str
    current_rank_id:     int
    current_status_id:   int
    security_admin_id:   int

    old_military_number: Optional[str] = None
    national_id:         Optional[str] = None
    
    # ── البيانات الشخصية ──
    birth_date:          Optional[date] = None
    join_date:           Optional[date] = None
    phone_number:        Optional[str] = None
    
    # ── الهيكل التنظيمي ──
    central_department_id: Optional[int] = None
    branch_id:             Optional[int] = None
    district_police_id:    Optional[int] = None
    division_id:           Optional[int] = None
    unit_id:               Optional[int] = None

    # ── التوصيف الوظيفي ──
    category_id:             Optional[int] = None
    job_title_id:            Optional[int] = None
    position_id:             Optional[int] = None
    force_classification_id: Optional[int] = None
    
    # ── علامات واحصائيات ──
    is_complete:        bool = False
    is_data_clean:      bool = False
    data_quality_score: int  = 0
    is_deleted:         bool = False
    
    expense_status: Optional[ExpenseStatus] = None

    # ══════════════════════════════════════════════════════════════
    # Business Rules (قواعد الأعمال)
    # ══════════════════════════════════════════════════════════════

    def normalize_phone_number(self) -> None:
        """تطبيع رقم الهاتف وإزالة الأرقام العربية والرموز"""
        if not self.phone_number:
            return
            
        no_phone_phrases = ['لا يوجد', 'بدون رقم', 'لايوجد', 'بدون', '-', 'لا']
        cleaned = str(self.phone_number).strip()
        
        if cleaned.lower() in no_phone_phrases or cleaned in no_phone_phrases:
            self.phone_number = None
            return
            
        cleaned = cleaned.translate(ARABIC_DIGIT_MAP)
        cleaned = re.sub(r'[\s\-\.\(\)\+]', '', cleaned)
        
        if cleaned.startswith('00967'):
            cleaned = cleaned[5:]
        elif cleaned.startswith('967'):
            cleaned = cleaned[3:]
        elif cleaned.startswith('+967'):
            cleaned = cleaned[4:]
            
        self.phone_number = cleaned if cleaned else None

    def validate_name(self) -> list[str]:
        """التحقق من صحة الاسم (بدون أخطاء Django Exception)"""
        errors = []
        if not self.full_name:
            return ["الاسم مطلوب"]
            
        if re.search(r'[0-9a-zA-Z]', self.full_name):
            errors.append("الاسم يجب أن يحتوي على أحرف عربية فقط — بدون أرقام أو رموز أو أحرف لاتينية")
            
        if not re.match(r'^[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF\s\-]+$', self.full_name.strip()):
            errors.append("الاسم يحتوي على رموز غير مسموحة")
            
        parts = self.full_name.strip().split()
        if len(parts) < 4:
            errors.append(f"الاسم يجب أن يكون 4 أجزاء على الأقل. تم إدخال {len(parts)} أجزاء فقط.")
        if len(parts) > 7:
            errors.append(f"الاسم يجب ألا يزيد عن 7 أجزاء. تم إدخال {len(parts)} أجزاء.")
            
        return errors

    def update_completeness(self, has_photo: bool, has_fingerprint: bool) -> None:
        """تحديث حالة اكتمال البيانات بناءً على وجود صورة وبصمة ورقم وطني"""
        self.is_complete = all([
            has_photo,
            has_fingerprint,
            bool(self.national_id)
        ])

    def change_status(self, new_status_id: int) -> None:
        """تغيير الحالة الخدمية"""
        self.current_status_id = new_status_id

    # ══════════════════════════════════════════════════════════════
    # Computed Properties (خصائص محسوبة)
    # ══════════════════════════════════════════════════════════════

    @property
    def military_number_type(self) -> MilitaryNumberType:
        if not self.military_number or len(str(self.military_number)) < 2:
            return MilitaryNumberType.UNKNOWN
            
        mn = str(self.military_number)
        prefix = mn[:2]
        first_digit = mn[0]
        
        if prefix == '60':
            return MilitaryNumberType.OFFICER
        elif first_digit == '7':
            return MilitaryNumberType.BASIC_PERSONNEL
        elif first_digit == '5':
            return MilitaryNumberType.COMMITTEE_OR_NEWCOMER
            
        return MilitaryNumberType.UNKNOWN

    @property
    def national_id_status(self) -> NationalIdStatus:
        if not self.national_id:
            return NationalIdStatus.MISSING
        if not str(self.national_id).isdigit():
            return NationalIdStatus.INVALID_FORMAT
        if len(str(self.national_id)) != 11:
            return NationalIdStatus.INVALID_LENGTH
        return NationalIdStatus.VALID

    def calculate_age(self, current_date: date) -> Optional[int]:
        if not self.birth_date:
            return None
        return current_date.year - self.birth_date.year - (
            (current_date.month, current_date.day) < (self.birth_date.month, self.birth_date.day)
        )
        
    def calculate_service_years(self, current_date: date) -> Optional[int]:
        if not self.join_date:
            return None
        return current_date.year - self.join_date.year - (
            (current_date.month, current_date.day) < (self.join_date.month, self.join_date.day)
        )
