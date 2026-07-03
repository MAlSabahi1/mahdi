import pytest
from datetime import datetime, timedelta

from systems.services.domain.entities.snapshots import MonthlySnapshotEntity, DirectorateComplianceEntity

def test_monthly_snapshot_lock():
    snapshot = MonthlySnapshotEntity(
        service_month='2026-06',
        data={'total': 100}
    )
    assert not snapshot.locked
    assert not snapshot.is_empty()
    
    snapshot.lock()
    assert snapshot.locked

def test_monthly_snapshot_empty():
    snapshot = MonthlySnapshotEntity(
        service_month='2026-06',
        data={}
    )
    assert snapshot.is_empty()

def test_compliance_quality_score_calculation():
    comp = DirectorateComplianceEntity(
        service_month='2026-06'
    )
    
    # لا أخطاء = 100%
    comp.calculate_quality_score()
    assert comp.quality_score == 100
    
    # 5 أخطاء (يخصم 5)
    comp.error_count = 5
    comp.calculate_quality_score()
    assert comp.quality_score == 95
    
    # 2 تغييرات مرفوضة (تخصم 4)
    comp.rejected_changes_count = 2
    comp.calculate_quality_score()
    assert comp.quality_score == 91
    
    # 3 أيام تأخير (تخصم 9)
    comp.late_days = 3
    comp.calculate_quality_score()
    assert comp.quality_score == 82
    
    # أخطاء كارثية تنزل تحت الصفر، لكن الدالة تحدها بـ 0
    comp.late_days = 50 # 150 points
    comp.calculate_quality_score()
    assert comp.quality_score == 0

def test_compliance_submission():
    comp = DirectorateComplianceEntity(
        service_month='2026-06'
    )
    
    deadline = datetime(2026, 6, 5, 23, 59, 59)
    
    # تسليم قبل الموعد
    on_time = datetime(2026, 6, 4, 10, 0, 0)
    comp.mark_submitted(on_time, deadline)
    assert comp.late_days == 0
    assert comp.quality_score == 100
    
    # تسليم بعد الموعد بيومين
    late = datetime(2026, 6, 8, 10, 0, 0) # تأخير 2 أيام (3 أيام تقريباً لأنها تعدت الـ 24 ساعة مرتين)
    comp.mark_submitted(late, deadline)
    assert comp.late_days == 2 # 8-5 = 3 بس timedelta.days للفرق بين 8 و 5 = 2.4 => 2 days
    
    # Let's adjust to be sure
    late2 = deadline + timedelta(days=2, hours=1)
    comp.mark_submitted(late2, deadline)
    assert comp.late_days == 2
    assert comp.quality_score == 94 # 100 - (2 * 3)
