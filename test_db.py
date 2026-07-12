import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from systems.personnel.models import PersonnelMaster
try:
    p = PersonnelMaster.objects.get(military_number="6042041")
    print(p.full_name)
except Exception as e:
    print(e)
