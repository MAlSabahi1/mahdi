import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from systems.personnel.infrastructure.models.personnel_models import PersonnelMaster
from systems.personnel.api.serializers.main_serializers import PersonnelUpdateSerializer, PersonnelDetailSerializer

# Fetch the personnel record
personnel = PersonnelMaster.objects.get(military_number='9900003')
print("Before update DB values:")
print(f"Birth Gov: {personnel.birth_governorate_id}, Dist: {personnel.birth_district_id}")

# Simulate Update
data = {
    'birth_governorate': 10,
    'birth_district': 146,
    'birth_sub_district': 1277,
    'birth_village': 16541
}

serializer = PersonnelUpdateSerializer(personnel, data=data, partial=True)
if serializer.is_valid():
    serializer.save()
    print("Update successful.")
else:
    print("Errors:", serializer.errors)

personnel.refresh_from_db()
print("After update DB values:")
print(f"Birth Gov: {personnel.birth_governorate_id}, Dist: {personnel.birth_district_id}")

# Simulate GET Request
detail_serializer = PersonnelDetailSerializer(personnel)
print("Detail Serializer Output:")
print(f"birth_gov_id: {detail_serializer.data.get('birth_gov_id')}")
print(f"birth_district_id: {detail_serializer.data.get('birth_district_id')}")
