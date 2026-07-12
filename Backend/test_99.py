import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()
from systems.personnel.models import PersonnelMaster
p = PersonnelMaster.objects.get(military_number="9900004")
print("9900004 status:", p.expense_status)
