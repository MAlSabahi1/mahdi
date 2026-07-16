from datetime import date
from dateutil.relativedelta import relativedelta
from systems.personnel.models import PersonnelMaster
from core.models import ServiceStatus, Rank

active_status = ServiceStatus.objects.filter(name__in=['في الخدمة', 'عامل', 'ميدان', 'نشط', 'موجود']).first()
if not active_status:
    active_status, _ = ServiceStatus.objects.get_or_create(name='في الخدمة')

rank = Rank.objects.first()
if not rank:
    rank = Rank.objects.create(name='رقيب أول')

today = date.today()

# 1. Person who exceeded retirement age (Age > 60)
birth_date_exceeded = today - relativedelta(years=62)
join_date_exceeded = today - relativedelta(years=20)
p1, created = PersonnelMaster.objects.update_or_create(
    military_number="9000001",
    defaults={
        'full_name': 'تجربة رجل عجوز متقاعد',
        'birth_date': birth_date_exceeded,
        'join_date': join_date_exceeded,
        'current_status': active_status,
        'current_rank': rank
    }
)
print(f"[{'Created' if created else 'Updated'}] {p1.full_name} - Age: 62 (Exceeded)")

# 2. Person who exceeded service time (Service > 35)
birth_date_service = today - relativedelta(years=55)
join_date_service = today - relativedelta(years=36)
p2, created = PersonnelMaster.objects.update_or_create(
    military_number="9000002",
    defaults={
        'full_name': 'تجربة خدمة طويلة جدا',
        'birth_date': birth_date_service,
        'join_date': join_date_service,
        'current_status': active_status,
        'current_rank': rank
    }
)
print(f"[{'Created' if created else 'Updated'}] {p2.full_name} - Service: 36 (Exceeded)")

# 3. Person approaching retirement (Less than 6 months left)
birth_date_approaching = today - relativedelta(years=59, months=8)
join_date_approaching = today - relativedelta(years=10)
p3, created = PersonnelMaster.objects.update_or_create(
    military_number="9000003",
    defaults={
        'full_name': 'تجربة قريب من التقاعد',
        'birth_date': birth_date_approaching,
        'join_date': join_date_approaching,
        'current_status': active_status,
        'current_rank': rank
    }
)
print(f"[{'Created' if created else 'Updated'}] {p3.full_name} - Approaching Retirement")
