import pytest
from datetime import datetime
from uuid import uuid4

from systems.services.domain.entities.status_change_form import StatusChangeFormEntity
from systems.services.domain.value_objects.status_change import FormStatus, FormType, ApprovalLevel

def create_valid_form(status=FormStatus.DRAFT):
    return StatusChangeFormEntity(
        id=uuid4(),
        personnel_id=1,
        security_admin_id=10,
        form_type=FormType.MARTYR,
        submitted_by_id=100,
        status=status
    )

def test_form_initial_state():
    form = create_valid_form()
    assert form.status == FormStatus.DRAFT
    assert form.can_be_submitted() is True
    assert form.is_approved() is False

def test_submit_form():
    form = create_valid_form()
    now = datetime.now()
    
    form.submit(now)
    
    assert form.status == FormStatus.PENDING_SERVICES
    assert form.submitted_at == now
    assert form.can_be_submitted() is False

def test_submit_already_submitted_form():
    form = create_valid_form(status=FormStatus.PENDING_SERVICES)
    with pytest.raises(ValueError, match="يمكن تقديم المسودات فقط"):
        form.submit(datetime.now())

def test_full_approval_flow():
    form = create_valid_form(status=FormStatus.PENDING_SERVICES)
    now = datetime.now()
    
    # 1. Services Approval
    assert form.can_be_approved_by(ApprovalLevel.SERVICES) is True
    form.approve(ApprovalLevel.SERVICES, approved_by_id=101, approved_at=now)
    assert form.status == FormStatus.PENDING_HR
    assert form.services_approved_by_id == 101
    
    # 2. HR Approval
    assert form.can_be_approved_by(ApprovalLevel.HR) is True
    form.approve(ApprovalLevel.HR, approved_by_id=102, approved_at=now)
    assert form.status == FormStatus.PENDING_DIRECTOR
    assert form.hr_approved_by_id == 102
    
    # 3. Director Approval
    assert form.can_be_approved_by(ApprovalLevel.DIRECTOR) is True
    form.approve(ApprovalLevel.DIRECTOR, approved_by_id=103, approved_at=now)
    assert form.status == FormStatus.APPROVED
    assert form.director_approved_by_id == 103
    assert form.is_approved() is True

def test_invalid_approval_level():
    form = create_valid_form(status=FormStatus.PENDING_SERVICES)
    
    with pytest.raises(ValueError, match="لا يمكن اعتماد استمارة"):
        # محاولة اعتماد المدير قبل الخدمات
        form.approve(ApprovalLevel.DIRECTOR, approved_by_id=103, approved_at=datetime.now())

def test_reject_form():
    form = create_valid_form(status=FormStatus.PENDING_HR)
    
    assert form.can_be_rejected() is True
    form.reject("سبب الرفض", rejected_by_id=104)
    
    assert form.status == FormStatus.REJECTED
    assert form.rejection_reason == "سبب الرفض"
    assert form.rejected_by_id == 104

def test_cannot_reject_draft_or_approved():
    draft_form = create_valid_form(status=FormStatus.DRAFT)
    with pytest.raises(ValueError):
        draft_form.reject("رفض", 1)
        
    approved_form = create_valid_form(status=FormStatus.APPROVED)
    with pytest.raises(ValueError):
        approved_form.reject("رفض", 1)
