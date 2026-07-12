import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from django.conf import settings
settings.ALLOWED_HOSTS.append('testserver')

from rest_framework.test import APIClient
from infra.accounts.models import User

client = APIClient()
user = User.objects.first()
client.force_authenticate(user=user)

res = client.get('/api/v1/personnel/6099999/')
print("Status:", res.status_code)
if res.status_code == 200:
    print("Birth Date:", res.data.get('birth_date'))
    print("Qualification Name:", res.data.get('qualification_name'))
    print("Expense Status:", res.data.get('expense_status_display'))
else:
    print(res.content)
