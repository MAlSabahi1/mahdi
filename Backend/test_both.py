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

for num in ["6042041", "7000055"]:
    p = PersonnelMaster.objects.get(military_number=num)
    data = PersonnelDetailSerializer(p).data
    data['expense_status'] = 'no_expenses'
    res = client.patch(f'/api/v1/personnel/{num}/', data, format='json')
    p.refresh_from_db()
    print(f"{num} final status:", p.expense_status)
    print(f"{num} response expense_status:", res.data.get('expense_status'))
