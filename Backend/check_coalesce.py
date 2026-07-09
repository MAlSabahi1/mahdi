import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()
from systems.personnel.models import PersonnelMaster
from django.db.models.functions import Coalesce

qs = PersonnelMaster.objects.filter(current_status__classification__startswith='active').annotate(
    unit_name=Coalesce('central_department__name', 'branch__name', 'district_police__name')
)

for p in qs:
    print(f"Name: {p.full_name}")
    print(f"  Central: {p.central_department.name if p.central_department else 'None'}")
    print(f"  Branch: {p.branch.name if p.branch else 'None'}")
    print(f"  District: {p.district_police.name if p.district_police else 'None'}")
    print(f"  Coalesce unit_name: {p.unit_name}")
    print("---")
