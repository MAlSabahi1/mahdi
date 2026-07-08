import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from systems.services.models import ServiceCatalog

for s in ServiceCatalog.objects.filter(code__in=['R01', 'R02', 'R03']):
    s.fields_schema = None # Clear it to force reload or set it
    s.save()

from django.core.management import call_command
call_command('seed_service_catalog')
print("SEEDED SUCCESSFULLY!")
