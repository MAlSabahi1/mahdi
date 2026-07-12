import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()
from systems.personnel.models import PersonnelMaster
from systems.personnel.api.serializers.main_serializers import PersonnelUpdateSerializer

p = PersonnelMaster.objects.get(military_number="7000055")
s = PersonnelUpdateSerializer(p)
print("expense_status in rep?", 'expense_status' in s.data)
print("Keys:", s.data.keys())
