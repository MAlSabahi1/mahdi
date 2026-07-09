import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from core.models.organization import SecurityAdministration, CentralDepartment, DistrictPolice
from systems.personnel.models import PersonnelMaster

marib = SecurityAdministration.objects.filter(name__contains='مأرب').first()
print(f"Marib SA: {marib}")

if marib:
    cd = CentralDepartment.objects.filter(security_admin=marib).first()
    dp = DistrictPolice.objects.filter(security_admin=marib).first()
    
    p1 = PersonnelMaster.objects.filter(military_number='6042041').first()
    if p1 and cd:
        p1.security_admin = marib
        p1.central_department = cd
        p1.save()
        print(f"Updated {p1.full_name} to {cd.name}")
        
    p2 = PersonnelMaster.objects.filter(military_number='7000055').first()
    if p2 and dp:
        p2.security_admin = marib
        p2.district_police = dp
        p2.save()
        print(f"Updated {p2.full_name} to {dp.name}")
