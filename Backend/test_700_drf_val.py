import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()
from systems.personnel.models import PersonnelMaster
from systems.personnel.api.serializers.main_serializers import PersonnelUpdateSerializer, PersonnelDetailSerializer

p = PersonnelMaster.objects.get(military_number="7000055")
data = PersonnelDetailSerializer(p).data
data['expense_status'] = 'no_expenses'

s = PersonnelUpdateSerializer(p, data=data, partial=True)
s.is_valid(raise_exception=True)
print("VALIDATED DATA:")
print(s.validated_data.get('expense_status'))
