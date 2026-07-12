import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from systems.personnel.models import PersonnelMaster
from systems.personnel.api.serializers.main_serializers import PersonnelDetailSerializer

p = PersonnelMaster.objects.get(military_number="9900005")
s = PersonnelDetailSerializer(p)
data = s.data
print("expense_status:", repr(data.get('expense_status')))
print("expense_status_display:", repr(data.get('expense_status_display')))
