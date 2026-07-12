import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()
from systems.personnel.models import PersonnelMaster
p = PersonnelMaster.objects.get(military_number="6042041")
print("Status:", p.expense_status)
print("Display:", p.get_expense_status_display())
