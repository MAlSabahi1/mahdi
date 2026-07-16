import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from systems.personnel.models import PersonnelMaster
print("Total personnel:", PersonnelMaster.objects.count())
