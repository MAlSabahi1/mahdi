import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from systems.personnel.models import PersonnelMaster
from core.models import Rank, ServiceStatus, SecurityAdministration

def seed():
    mil_num = '7000055'
    if PersonnelMaster.objects.filter(military_number=mil_num).exists():
        print(f"Personnel with military number {mil_num} already exists.")
    else:
        try:
            rank = Rank.objects.get(id=15) # جندي
            status = ServiceStatus.objects.get(id=1) # تعمل في الميدان
            sec_admin = SecurityAdministration.objects.get(id=2) # إدارة أمن أمانة العاصمة
            
            p = PersonnelMaster(
                military_number=mil_num,
                full_name='محمد علي حسن صالح',
                birth_date='1990-01-01',
                join_date='2010-01-01',
                phone_number='777777777',
                security_admin=sec_admin,
                current_rank=rank,
                current_status=status,
                is_data_clean=True,
                data_quality_score=100
            )
            p.full_clean()
            p.save()
            print(f"Successfully created test personnel: {p.full_name} ({p.military_number})")
        except Exception as e:
            print(f"Error seeding personnel: {e}")

if __name__ == '__main__':
    seed()
