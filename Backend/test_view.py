import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from systems.personnel.views import PersonnelViewSet
view = PersonnelViewSet()
view.action = 'list'
serializer_class = view.get_serializer_class()
print("Serializer class:", serializer_class)
