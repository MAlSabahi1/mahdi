import pytest
from systems.services.domain.entities.staging import StagingRecordEntity

def test_staging_severity():
    # High severity
    high = StagingRecordEntity(
        import_batch_id="batch1",
        row_index=1,
        military_number="12345",
        action_type="update",
        changes={"full_name": {"old": "A", "new": "B"}}
    )
    assert high.is_high_severity()
    assert not high.can_be_auto_approved()
    
    # Low severity
    low = StagingRecordEntity(
        import_batch_id="batch1",
        row_index=2,
        military_number="12345",
        action_type="update",
        changes={"phone_number": {"old": "777", "new": "778"}}
    )
    assert not low.is_high_severity()
    assert low.can_be_auto_approved()
    
    # No changes
    no_change = StagingRecordEntity(
        import_batch_id="batch1",
        row_index=3,
        military_number="12345",
        action_type="no_change",
        changes={}
    )
    assert no_change.can_be_auto_approved()
    
    # Validation errors prevent auto approve
    with_error = StagingRecordEntity(
        import_batch_id="batch1",
        row_index=4,
        military_number="12345",
        action_type="update",
        changes={"phone_number": {"old": "777", "new": "778"}},
        validation_errors=["Invalid phone format"]
    )
    assert not with_error.is_high_severity()
    assert not with_error.can_be_auto_approved()

def test_staging_workflow():
    record = StagingRecordEntity(
        import_batch_id="batch1",
        row_index=1,
        military_number="12345",
        action_type="update"
    )
    
    assert record.status == 'pending'
    
    # Test reject without reason
    with pytest.raises(ValueError, match="يجب تحديد سبب"):
        record.reject(reason="", reviewer_id=1)
        
    # Test approve
    record.approve(reviewer_id=2)
    assert record.status == 'approved'
    assert record.reviewed_by_id == 2
    
    # Test double approve
    with pytest.raises(ValueError, match="لا يمكن الموافقة على سجل بحالة approved"):
        record.approve(reviewer_id=3)
