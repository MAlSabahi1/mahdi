import os
import django
from django.test import Client
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

settings.ALLOWED_HOSTS.append('testserver')
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()
user = User.objects.get(username='marib_admin')

refresh = RefreshToken.for_user(user)
token = str(refresh.access_token)
client = Client(HTTP_AUTHORIZATION=f'Bearer {token}')

response = client.get('/api/v1/personnel/')
print(f"Status: {response.status_code}")
data = response.json()
print(f"Count: {data.get('count')}")
for p in data.get('results', []):
    print(f" - {p.get('full_name')} ({p.get('military_number')})")

