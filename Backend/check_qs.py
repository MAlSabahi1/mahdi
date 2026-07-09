import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()
from systems.personnel.models import PersonnelMaster
from django.db.models.functions import Coalesce
from django.db.models import Count

qs = PersonnelMaster.objects.filter(current_status__classification__startswith='active')
qs = qs.annotate(
    unit_name=Coalesce('central_department__name', 'branch__name', 'district_police__name')
).values(
    'unit_name', 
    'current_rank__name'
).annotate(
    count=Count('military_number')
)

for row in qs:
    print(row)
