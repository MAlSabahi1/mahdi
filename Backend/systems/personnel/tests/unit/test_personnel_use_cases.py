import pytest
from datetime import date

from systems.personnel.domain.entities.personnel import PersonnelEntity
from systems.personnel.domain.repositories.i_personnel_repo import IPersonnelRepository
from systems.personnel.application.use_cases.personnel_use_cases import (
    RegisterPersonnelUseCase, RegisterPersonnelCommand,
    UpdateCompletenessUseCase, UpdateCompletenessCommand
)

class InMemoryPersonnelRepository(IPersonnelRepository):
    def __init__(self):
        self.db = {}

    def get_by_military_number(self, military_number: str):
        return self.db.get(military_number)

    def get_by_national_id(self, national_id: str):
        for p in self.db.values():
            if p.national_id == national_id:
                return p
        return None

    def save(self, personnel: PersonnelEntity):
        self.db[personnel.military_number] = personnel

    def soft_delete(self, military_number: str):
        if military_number in self.db:
            self.db[military_number].is_deleted = True

@pytest.fixture
def repo():
    return InMemoryPersonnelRepository()

def test_register_personnel_success(repo):
    uc = RegisterPersonnelUseCase(repo)
    cmd = RegisterPersonnelCommand(
        military_number='7123456',
        full_name='أحمد محمد علي سعيد',
        current_rank_id=1,
        current_status_id=1,
        security_admin_id=1,
        national_id='12345678901',
        phone_number='٠١٢٣٤٥٦٧٨٩'
    )
    
    personnel = uc.execute(cmd)
    
    assert personnel.military_number == '7123456'
    assert personnel.phone_number == '0123456789' # Normalized
    
    saved_personnel = repo.get_by_military_number('7123456')
    assert saved_personnel is not None

def test_register_duplicate_military_number(repo):
    uc = RegisterPersonnelUseCase(repo)
    cmd = RegisterPersonnelCommand(
        military_number='7123456',
        full_name='أحمد محمد علي سعيد',
        current_rank_id=1,
        current_status_id=1,
        security_admin_id=1
    )
    uc.execute(cmd) # First time success
    
    with pytest.raises(ValueError, match="الرقم العسكري 7123456 مسجل مسبقاً"):
        uc.execute(cmd) # Second time failure

def test_register_duplicate_national_id(repo):
    uc = RegisterPersonnelUseCase(repo)
    cmd1 = RegisterPersonnelCommand(
        military_number='7123456',
        full_name='أحمد محمد علي سعيد',
        current_rank_id=1,
        current_status_id=1,
        security_admin_id=1,
        national_id='12345678901'
    )
    uc.execute(cmd1)
    
    cmd2 = RegisterPersonnelCommand(
        military_number='7654321', # Different military number
        full_name='سعيد محمد علي أحمد',
        current_rank_id=1,
        current_status_id=1,
        security_admin_id=1,
        national_id='12345678901' # Same national ID
    )
    
    with pytest.raises(ValueError, match="الرقم الوطني 12345678901 مسجل مسبقاً"):
        uc.execute(cmd2)

def test_register_invalid_name(repo):
    uc = RegisterPersonnelUseCase(repo)
    cmd = RegisterPersonnelCommand(
        military_number='7123456',
        full_name='Ahmed Ali', # English and short
        current_rank_id=1,
        current_status_id=1,
        security_admin_id=1
    )
    
    with pytest.raises(ValueError, match="الاسم يجب أن يحتوي على أحرف عربية"):
        uc.execute(cmd)

def test_update_completeness(repo):
    # Setup
    uc_reg = RegisterPersonnelUseCase(repo)
    uc_reg.execute(RegisterPersonnelCommand(
        military_number='7123456',
        full_name='أحمد محمد علي سعيد',
        current_rank_id=1,
        current_status_id=1,
        security_admin_id=1,
        national_id='12345678901'
    ))
    
    # Update completeness
    uc_comp = UpdateCompletenessUseCase(repo)
    cmd = UpdateCompletenessCommand(
        military_number='7123456',
        has_photo=True,
        has_fingerprint=True
    )
    
    personnel = uc_comp.execute(cmd)
    
    assert personnel.is_complete is True
    
    # Verify in DB
    saved = repo.get_by_military_number('7123456')
    assert saved.is_complete is True

def test_update_completeness_not_found(repo):
    uc_comp = UpdateCompletenessUseCase(repo)
    cmd = UpdateCompletenessCommand(
        military_number='9999999',
        has_photo=True,
        has_fingerprint=True
    )
    
    with pytest.raises(ValueError, match="غير موجود"):
        uc_comp.execute(cmd)
