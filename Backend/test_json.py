import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()
from core.models.personnel_refs import ServiceStatus
from systems.personnel.models import PersonnelMaster

for s in ServiceStatus.objects.all():
    count = PersonnelMaster.objects.filter(current_status=s).count()
    print(f'Name: {s.name}, Class: {s.classification}, Count: {count}')
