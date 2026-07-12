import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()
from systems.personnel.models import PersonnelMaster
for military_number in ["6042041", "9900004"]:
    try:
        p = PersonnelMaster.objects.get(military_number=military_number)
        print(f"{military_number} expense_status: {p.expense_status}")
    except Exception as e:
        print(f"{military_number} error: {e}")
