import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()
from systems.personnel.api.serializers.main_serializers import PersonnelUpdateSerializer
s = PersonnelUpdateSerializer()
print(list(s.fields.keys()))
