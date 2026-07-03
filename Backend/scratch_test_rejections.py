import sys
import os
sys.path.append("/home/mahdi/Desktop/POL/backend")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

import django
django.setup()

from services.tests.test_api_phase4 import ServicesAPITestBase
from django.contrib.auth import get_user_model
User = get_user_model()

test_base = ServicesAPITestBase()
test_base.setUpTestData()
client, user = test_base._create_authenticated_client('export_tester', supervises_all=True)

response = client.get('/api/v1/service-cycle/rejections/export/')
print("Status:", response.status_code)
if response.status_code >= 400:
    print("Content:", response.content.decode('utf-8'))
