import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from systems.personnel.models import PersonnelMaster
from systems.personnel.api.serializers.main_serializers import PersonnelListSerializer

p = PersonnelMaster.objects.filter(current_status__isnull=False).first()
if p:
    ser = PersonnelListSerializer(p)
    print(ser.data.get('status_classification_display'))
else:
    print("No personnel with status found")
