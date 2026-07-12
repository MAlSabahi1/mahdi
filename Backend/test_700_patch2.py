import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from systems.personnel.models import PersonnelMaster
from systems.personnel.api.serializers.main_serializers import PersonnelDetailSerializer

User = get_user_model()
admin = User.objects.get(username='admin')
client = APIClient(HTTP_HOST='127.0.0.1')
client.force_authenticate(user=admin)

p = PersonnelMaster.objects.get(military_number="7000055")
data = PersonnelDetailSerializer(p).data
data['expense_status'] = 'no_expenses'
res = client.patch('/api/v1/personnel/7000055/', data, format='json')
p.refresh_from_db()
print("7000055 final status:", p.expense_status)
print("Response data:", res.data.get('expense_status'))
print("Response keys:", res.data.keys())
