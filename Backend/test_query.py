import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()
from django.db.models import Q
from systems.personnel.models import PersonnelMaster
from core.models.personnel_refs import ServiceStatus

qs = ServiceStatus.objects.filter(classification='inactive_perm')
print("All perm inactive statuses:")
for s in qs:
    print(s.name)
