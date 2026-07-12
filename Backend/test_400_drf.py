import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()
from systems.personnel.models import PersonnelMaster
from systems.personnel.api.serializers.main_serializers import PersonnelUpdateSerializer

p = PersonnelMaster.objects.get(military_number="9900004")
s = PersonnelUpdateSerializer(p, data={'expense_status': 'no_expenses'}, partial=True)
if not s.is_valid():
    print("VALIDATION ERROR:", s.errors)
else:
    print("VALID!")
