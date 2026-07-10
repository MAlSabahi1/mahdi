import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from systems.personnel.models import PersonnelMaster
from systems.personnel.api.serializers.main_serializers import PersonnelUpdateSerializer

personnel = PersonnelMaster.objects.get(military_number="7000055")
data = {}
serializer = PersonnelUpdateSerializer(personnel, data=data, partial=True)
print("Is valid?", serializer.is_valid())
print("Errors:", serializer.errors)
