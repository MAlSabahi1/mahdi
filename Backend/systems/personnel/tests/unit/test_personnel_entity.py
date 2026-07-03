import pytest
from datetime import date

from systems.personnel.domain.entities.personnel import PersonnelEntity
from systems.personnel.domain.value_objects.personnel import MilitaryNumberType, NationalIdStatus

def create_valid_personnel():
    return PersonnelEntity(
        military_number='7348799',
        full_name='محمد علي سعيد الفهد',
        current_rank_id=1,
        current_status_id=1,
        security_admin_id=1,
        national_id='12345678901',
        birth_date=date(1990, 1, 1),
        join_date=date(2010, 1, 1)
    )

def test_personnel_initialization():
    p = create_valid_personnel()
    assert p.military_number == '7348799'
    assert p.military_number_type == MilitaryNumberType.BASIC_PERSONNEL

def test_normalize_phone_number():
    p = create_valid_personnel()
    
    # تحويل الأرقام العربية
    p.phone_number = '٠١٢٣٤٥٦٧٨٩'
    p.normalize_phone_number()
    assert p.phone_number == '0123456789'
    
    # إزالة مفتاح اليمن 967
    p.phone_number = '967777123456'
    p.normalize_phone_number()
    assert p.phone_number == '777123456'
    
    # إزالة مفتاح اليمن +967
    p.phone_number = '+967777123456'
    p.normalize_phone_number()
    assert p.phone_number == '777123456'
    
    # إزالة المسافات والشرطات
    p.phone_number = '777 123-456'
    p.normalize_phone_number()
    assert p.phone_number == '777123456'
    
    # الكلمات التي تعني لا يوجد رقم
    p.phone_number = 'لا يوجد'
    p.normalize_phone_number()
    assert p.phone_number is None

def test_validate_arabic_name():
    p = create_valid_personnel()
    
    # اسم صحيح رباعي
    errors = p.validate_name()
    assert len(errors) == 0
    
    # اسم فيه أرقام إنجليزية
    p.full_name = 'محمد 123 سعيد اللقب'
    errors = p.validate_name()
    assert "الاسم يجب أن يحتوي على أحرف عربية فقط — بدون أرقام أو رموز أو أحرف لاتينية" in errors[0]
    
    # اسم قصير
    p.full_name = 'محمد علي سعيد'
    errors = p.validate_name()
    assert "الاسم يجب أن يكون 4 أجزاء على الأقل. تم إدخال 3 أجزاء فقط." in errors[0]

def test_military_number_types():
    p = create_valid_personnel()
    
    p.military_number = '6012345'
    assert p.military_number_type == MilitaryNumberType.OFFICER
    
    p.military_number = '7123456'
    assert p.military_number_type == MilitaryNumberType.BASIC_PERSONNEL
    
    p.military_number = '5123456'
    assert p.military_number_type == MilitaryNumberType.COMMITTEE_OR_NEWCOMER
    
    p.military_number = '123'
    assert p.military_number_type == MilitaryNumberType.UNKNOWN

def test_national_id_status():
    p = create_valid_personnel()
    
    p.national_id = '12345678901'
    assert p.national_id_status == NationalIdStatus.VALID
    
    p.national_id = None
    assert p.national_id_status == NationalIdStatus.MISSING
    
    p.national_id = '12345' # قصير
    assert p.national_id_status == NationalIdStatus.INVALID_LENGTH
    
    p.national_id = '123A5678901' # أحرف
    assert p.national_id_status == NationalIdStatus.INVALID_FORMAT

def test_age_and_service_years():
    p = create_valid_personnel()
    current = date(2026, 6, 24)
    
    # مواليد 1990 → 2026 = 36 سنة
    assert p.calculate_age(current) == 36
    
    # التحاق 2010 → 2026 = 16 سنة
    assert p.calculate_service_years(current) == 16

def test_update_completeness():
    p = create_valid_personnel()
    
    # لا توجد بصمة ولا صورة
    p.update_completeness(has_photo=False, has_fingerprint=False)
    assert p.is_complete is False
    
    # كل شيء موجود بالإضافة إلى الرقم الوطني الموجود أصلاً
    p.update_completeness(has_photo=True, has_fingerprint=True)
    assert p.is_complete is True
