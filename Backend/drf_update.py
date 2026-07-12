import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()
from systems.personnel.models import PersonnelMaster
from systems.personnel.api.serializers.main_serializers import PersonnelUpdateSerializer

p = PersonnelMaster.objects.get(military_number="6042041")
# Reset to None first
p.expense_status = None
p.save()

s = PersonnelUpdateSerializer(p, data={'expense_status': 'has_expenses'}, partial=True)
s.is_valid(raise_exception=True)
s.save()

p.refresh_from_db()
print("Final expense_status:", p.expense_status)
