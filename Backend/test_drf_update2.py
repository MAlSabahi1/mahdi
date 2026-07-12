import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()
from systems.personnel.models import PersonnelMaster
from systems.personnel.api.serializers.main_serializers import PersonnelUpdateSerializer

p = PersonnelMaster.objects.get(military_number="6042041")
print("Before:", p.expense_status)
s = PersonnelUpdateSerializer(p, data={'expense_status': 'no_expenses'}, partial=True)
s.is_valid(raise_exception=True)
s.save()
p.refresh_from_db()
print("After:", p.expense_status)
