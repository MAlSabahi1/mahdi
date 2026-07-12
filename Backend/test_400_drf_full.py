import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()
from systems.personnel.models import PersonnelMaster
from systems.personnel.api.serializers.main_serializers import PersonnelUpdateSerializer, PersonnelDetailSerializer

p = PersonnelMaster.objects.get(military_number="9900004")
data = PersonnelDetailSerializer(p).data
data['expense_status'] = 'no_expenses'

s = PersonnelUpdateSerializer(p, data=data, partial=True)
if not s.is_valid():
    print("VALIDATION ERROR:", s.errors)
else:
    print("VALID!")
