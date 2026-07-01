import sys
import os
sys.path.append("/home/mahdi/Desktop/POL/backend")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

import django
django.setup()

from django.test import RequestFactory
from django.contrib.auth import get_user_model
from services.views import WebhookConfigViewSet
from services.tests.test_api_phase4 import ServicesAPITestBase

User = get_user_model()
client, user = ServicesAPITestBase()._create_authenticated_client('wh_creator', supervises_all=True)
response = client.post('/api/v1/service-cycle/webhooks/', {
    'url': 'https://example.com/webhook',
    'secret': 'supersecret123',
    'events': ['rejection.created', 'import.completed'],
    'is_active': True,
}, format='json')

print("Status:", response.status_code)
print("Data:", response.data)
