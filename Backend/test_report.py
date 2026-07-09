import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hrms.settings')
django.setup()

from systems.personnel.models import PersonnelMaster
from django.db.models import Count
from django.db.models.functions import Coalesce
from core.models.organization import CentralDepartment, Branch, DistrictPolice, SecurityAdministration

print("Checking Central Departments...")
print(list(CentralDepartment.objects.filter(is_active=True).values_list('name', flat=True))[:2])

level = 'all'
level_field_map = {
    'central': 'central_department__name',
    'branch': 'branch__name',
    'district': 'district_police__name',
    'security_admin': 'security_admin__name',
}

try:
    qs = PersonnelMaster.objects.filter(current_status__name='بالخدمة')
    
    if level == 'all':
        qs = qs.annotate(
            unit_name=Coalesce('central_department__name', 'branch__name', 'district_police__name')
        ).values(
            'unit_name', 
            'current_rank__name'
        ).annotate(
            count=Count('military_number')
        )
        group_field = 'unit_name'
    else:
        group_field = level_field_map[level]
        qs = qs.values(group_field, 'current_rank__name').annotate(count=Count('military_number'))
        
    print("QS test:", list(qs[:2]))
    print("Success!")
except Exception as e:
    import traceback
    traceback.print_exc()
