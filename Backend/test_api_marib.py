import os
import django
from django.test import Client
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Allow testserver
settings.ALLOWED_HOSTS.append('testserver')

from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()
user = User.objects.get(username='marib_admin')

refresh = RefreshToken.for_user(user)
token = str(refresh.access_token)

client = Client(HTTP_AUTHORIZATION=f'Bearer {token}')

response_cat = client.get('/api/v1/reports/categorical-summary/?level=central')
print("\nCategorical Response Status:", response_cat.status_code)
print("Categorical Response Data:", response_cat.content.decode('utf-8')[:500])

response_wf = client.get('/api/v1/personnel/reports/workforce-summary/?level=central')
print("\nWorkforce Summary Response Status:", response_wf.status_code)
print("Workforce Summary Response Data:", response_wf.content.decode('utf-8')[:500])

