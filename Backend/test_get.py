import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()
from systems.personnel.models import PersonnelMaster
from systems.personnel.api.serializers.main_serializers import PersonnelDetailSerializer

p = PersonnelMaster.objects.get(military_number="6099999")
print("6099999 expense_status in DB:", p.expense_status)
s = PersonnelDetailSerializer(p)
print("expense_status_display in serializer:", s.data.get('expense_status_display'))
print("expense_status in serializer:", s.data.get('expense_status'))
