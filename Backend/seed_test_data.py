import os
import sys
import django
from datetime import date

sys.path.append('/home/mahdi/Desktop/n/mahdi/Backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from systems.personnel.models import PersonnelMaster
from core.models.organization import SecurityAdministration, CentralDepartment, Branch, DistrictPolice
from core.models.personnel_refs import Rank, ServiceStatus, JobCategory, JobTitle, Qualification
from core.models.geography import GeoGovernorate, GeoDistrict

def seed_data():
    # 1. Setup Organization (Marib Governorate)
    geo_marib, _ = GeoGovernorate.objects.get_or_create(
        name_ar='مأرب',
        defaults={'name_en': 'Marib'}
    )
    
    try:
        marib = SecurityAdministration.objects.get(geo_governorate=geo_marib)
    except SecurityAdministration.DoesNotExist:
        marib = SecurityAdministration.objects.create(
            name='إدارة أمن محافظة مأرب',
            code='MAR', 
            geo_governorate=geo_marib, 
            is_active=True
        )

    # 1.5 Setup Geo District
    geo_city, _ = GeoDistrict.objects.get_or_create(
        name_ar='المدينة',
        governorate=geo_marib,
        defaults={'name_en': 'Al Madinah'}
    )

    # 2. Setup Units
    central_unit = CentralDepartment.objects.filter(name='مكتب المدير العام').first()
    if not central_unit:
        central_unit = CentralDepartment.objects.create(name='مكتب المدير العام', code='GM', security_admin=marib, is_active=True)
    
    branch_unit = Branch.objects.filter(name='فرع شرطة السير').first()
    if not branch_unit:
        branch_unit = Branch.objects.create(name='فرع شرطة السير', code='TRAF', security_admin=marib, is_active=True)

    district_unit = DistrictPolice.objects.filter(name='شرطة مديرية المدينة').first()
    if not district_unit:
        district_unit = DistrictPolice.objects.create(name='شرطة مديرية المدينة', code='CTY', security_admin=marib, geo_district=geo_city, is_active=True)

    # 3. Setup Ranks
    rank_1 = Rank.objects.filter(name='عقيد').first()
    rank_2 = Rank.objects.filter(name='نقيب').first()
    rank_3 = Rank.objects.filter(name='رقيب 1').first() or Rank.objects.filter(name='مساعد 1').first()
    rank_4 = Rank.objects.filter(name='جندي').first()
    if not rank_4:
        rank_4 = Rank.objects.create(name='جندي', order=99, is_officer=False)

    # 4. Setup Status (Active Full)
    active_status = ServiceStatus.objects.filter(classification='active_full').first()
    if not active_status:
        active_status = ServiceStatus.objects.filter(name='بالخدمة').first()
        if active_status:
            active_status.classification = 'active_full'
            active_status.save()
        else:
            active_status = ServiceStatus.objects.create(name='بالخدمة', classification='active_full', receives_salary=True)
            
    # 5. Setup Categories & Qualifications
    cat_admin = JobCategory.objects.filter(name='إدارية').first() or JobCategory.objects.create(name='إدارية')
    cat_field = JobCategory.objects.filter(name='ميدانية').first() or JobCategory.objects.create(name='ميدانية')
    
    qual_bachelor = Qualification.objects.filter(name='بكالوريوس').first() or Qualification.objects.first()
    qual_highschool = Qualification.objects.filter(name='ثانوية عامة').first() or Qualification.objects.last()

    # Clear existing test ones to avoid unique constraint issues
    PersonnelMaster.objects.filter(military_number__startswith='99').delete()

    # 6. Create Personnel
    people = [
        {
            'military_number': '9900001',
            'full_name': 'أحمد محمد علي سعيد',
            'national_id': '01010101010',
            'current_rank': rank_1,
            'current_status': active_status,
            'security_admin': marib,
            'central_department': central_unit,
            'category': cat_admin,
            'qualification': qual_bachelor,
            'join_date': date(2010, 1, 1),
            'birth_date': date(1980, 1, 1)
        },
        {
            'military_number': '9900002',
            'full_name': 'صالح عبدالله حسين طاهر',
            'national_id': '02020202020',
            'current_rank': rank_2,
            'current_status': active_status,
            'security_admin': marib,
            'central_department': central_unit,
            'category': cat_admin,
            'qualification': qual_bachelor,
            'join_date': date(2015, 1, 1),
            'birth_date': date(1990, 1, 1)
        },
        {
            'military_number': '9900003',
            'full_name': 'علي يحيى حسن فضل',
            'national_id': '03030303030',
            'current_rank': rank_3,
            'current_status': active_status,
            'security_admin': marib,
            'branch': branch_unit,
            'category': cat_field,
            'qualification': qual_highschool,
            'join_date': date(2018, 1, 1),
            'birth_date': date(1995, 1, 1)
        },
        {
            'military_number': '9900004',
            'full_name': 'ياسر عبدالعزيز محمد حمود',
            'national_id': '04040404040',
            'current_rank': rank_4,
            'current_status': active_status,
            'security_admin': marib,
            'district_police': district_unit,
            'category': cat_field,
            'qualification': qual_highschool,
            'join_date': date(2020, 1, 1),
            'birth_date': date(2000, 1, 1)
        },
        {
            'military_number': '9900005',
            'full_name': 'محمود صادق أحمد سعد',
            'national_id': '05050505050',
            'current_rank': rank_4,
            'current_status': active_status,
            'security_admin': marib,
            'district_police': district_unit,
            'category': cat_field,
            'qualification': qual_highschool,
            'join_date': date(2022, 1, 1),
            'birth_date': date(2002, 1, 1)
        }
    ]

    for p_data in people:
        PersonnelMaster.objects.create(**p_data)
        print(f"Created: {p_data['full_name']}")

    print("Successfully seeded 5 test personnel!")

if __name__ == '__main__':
    seed_data()
