import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()
from systems.personnel.models import PersonnelMaster
field = PersonnelMaster._meta.get_field('expense_status')
print(field.name, field.editable)
