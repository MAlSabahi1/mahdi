import os
import django
from django.apps import apps
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

ServiceStatus = apps.get_model('core', 'ServiceStatus')
data = json.load(open('fixtures/service_statuses.json'))
count = 0
for item in data:
    if item['model'] == 'core.servicestatus':
        fields = item['fields']
        obj, created = ServiceStatus.objects.update_or_create(
            name=fields['name'],
            defaults={'classification': fields.get('classification', 'active_full'), 'receives_salary': fields.get('receives_salary', True)}
        )
        count += 1
print(f'Successfully loaded/updated {count} ServiceStatuses!')
