import pytest
from datetime import datetime, date

from systems.personnel.domain.entities.corrections import SuggestedCorrectionEntity, RankSettlementEntity


def test_correction_validation():
    # Test valid correction
    corr = SuggestedCorrectionEntity(
        personnel_id=1,
        field_name='full_name',
        old_value='علي',
        new_value='علي محمد',
        correction_type='name_correction',
        supporting_document_id=10
    )
    corr.validate_request()  # Should not raise
    
    # Test invalid field
    corr_invalid_field = SuggestedCorrectionEntity(
        personnel_id=1,
        field_name='is_deleted',
        old_value='False',
        new_value='True',
        correction_type='other'
    )
    with pytest.raises(ValueError, match='غير مسموح بتصحيحه'):
        corr_invalid_field.validate_request()
        
    # Test missing document for sensitive correction
    corr_no_doc = SuggestedCorrectionEntity(
        personnel_id=1,
        field_name='full_name',
        old_value='علي',
        new_value='علي محمد',
        correction_type='name_correction'
    )
    with pytest.raises(ValueError, match='يتطلب إرفاق مستند داعم'):
        corr_no_doc.validate_request()


def test_correction_workflow():
    corr = SuggestedCorrectionEntity(
        personnel_id=1,
        field_name='phone_number',
        old_value='777123456',
        new_value='777654321',
        correction_type='phone_correction'
    )
    
    # Should start pending
    assert corr.status == 'pending'
    
    # Test approve
    corr.approve(reviewer_id=2)
    assert corr.status == 'approved'
    assert corr.reviewed_by_id == 2
    assert corr.reviewed_at is not None
    
    # Try to reject after approve
    with pytest.raises(ValueError, match='تمت معالجته مسبقاً'):
        corr.reject(reviewer_id=3, reason='خطأ')


def test_rank_settlement_validation():
    # Valid
    settlement = RankSettlementEntity(
        personnel_id=1,
        current_rank_id=2,
        new_rank_id=3,
        due_date=date(2025, 1, 1),
        decision_date=date(2025, 5, 1),
        decision_number='123/2025'
    )
    settlement.validate_request() # Should not raise
    
    # Invalid: Same rank
    bad_rank = RankSettlementEntity(
        personnel_id=1,
        current_rank_id=2,
        new_rank_id=2, # Same!
        due_date=date(2025, 1, 1),
        decision_date=date(2025, 5, 1),
        decision_number='123/2025'
    )
    with pytest.raises(ValueError, match='يجب أن تكون مختلفة عن الرتبة الحالية'):
        bad_rank.validate_request()
        
    # Invalid: No decision number
    bad_dec = RankSettlementEntity(
        personnel_id=1,
        current_rank_id=2,
        new_rank_id=3,
        due_date=date(2025, 1, 1),
        decision_date=date(2025, 5, 1),
        decision_number='   '
    )
    with pytest.raises(ValueError, match='يجب إدخال رقم القرار'):
        bad_dec.validate_request()
