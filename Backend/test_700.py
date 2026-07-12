import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()
from systems.personnel.models import PersonnelMaster
p = PersonnelMaster.objects.get(military_number="7000055")
print("7000055 expense_status:", p.expense_status)
