import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from systems.personnel.models import PersonnelMaster
p = PersonnelMaster.objects.filter(current_status__isnull=False).first()
if p:
    print(p.current_status.classification)
    print(p.current_status.get_classification_display())
