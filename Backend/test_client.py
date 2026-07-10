import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
User = get_user_model()
user = User.objects.filter(is_superuser=True).first()

client = Client()
client.force_login(user)

response = client.get('/api/v1/personnel/?limit=1', SERVER_NAME='127.0.0.1')
import json
print(json.dumps(response.json(), ensure_ascii=False, indent=2))
