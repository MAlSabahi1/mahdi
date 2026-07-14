import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.base")
django.setup()
from systems.personnel.models import PersonnelMaster
from systems.personnel.api.serializers.main_serializers import PersonnelUpdateSerializer

p = PersonnelMaster.objects.first()
if p:
    data = {
        'birth_governorate': 1,
        'birth_district': 1,
        'birth_sub_district': 1,
        'birth_village': 1,
        'residence_governorate': 1,
        'residence_district': 1,
        'residence_sub_district': 1,
        'residence_village': 1,
        'id_issue_date': '2020-01-01',
        'id_issue_place': 'Sanaa'
    }
    serializer = PersonnelUpdateSerializer(p, data=data, partial=True)
    if serializer.is_valid():
        print("Serializer is valid!")
    else:
        print("Serializer errors:", serializer.errors)
