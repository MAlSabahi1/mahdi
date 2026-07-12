import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from systems.personnel.models import PersonnelMaster
p = PersonnelMaster.objects.get(military_number="9900005")
print("Current expense_status in DB:", repr(p.expense_status))
