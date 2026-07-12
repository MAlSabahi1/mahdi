import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()
from systems.personnel.models import PersonnelMaster
from systems.personnel.api.serializers.main_serializers import PersonnelUpdateSerializer

p = PersonnelMaster.objects.get(military_number="6042041")
s = PersonnelUpdateSerializer(p, data={"expense_status": "no_expenses"}, partial=True)
print("Is valid?", s.is_valid())
if not s.is_valid():
    print(s.errors)
else:
    s.save()
    print("Saved. New DB value:", p.expense_status)
