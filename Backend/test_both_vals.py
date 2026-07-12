import os, django, json
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()
from systems.personnel.models import PersonnelMaster
from systems.personnel.api.serializers.main_serializers import PersonnelDetailSerializer

p1 = PersonnelMaster.objects.get(military_number="6042041")
data1 = PersonnelDetailSerializer(p1).data

p2 = PersonnelMaster.objects.get(military_number="7000055")
data2 = PersonnelDetailSerializer(p2).data

print("--- 6042041 ---")
for k,v in data1.items():
    if v != data2.get(k):
        print(f"{k}: {v} != {data2.get(k)}")
