import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()
from systems.personnel.models import PersonnelMaster
p = PersonnelMaster.objects.get(military_number="6042041")
print("Current DB expense_status:", p.expense_status)
