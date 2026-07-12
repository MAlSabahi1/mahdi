import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory
from systems.personnel.api.serializers.main_serializers import PersonnelUpdateSerializer, PersonnelDetailSerializer
from systems.personnel.models import PersonnelMaster

User = get_user_model()
admin = User.objects.get(username='admin')
factory = APIRequestFactory()

p = PersonnelMaster.objects.get(military_number="7000055")
p.expense_status = None
p.save()

data = PersonnelDetailSerializer(p).data
data['expense_status'] = 'no_expenses'
request = factory.patch('/api/v1/personnel/7000055/', data, format='json')

from rest_framework.request import Request
request = Request(request)
request.user = admin

# Simulate ViewSet logic
serializer = PersonnelUpdateSerializer(p, data=request.data, partial=True, context={'request': request})
if serializer.is_valid():
    print("VALIDATED DATA HAS EXPENSE STATUS:", 'expense_status' in serializer.validated_data)
    serializer.save()
else:
    print("ERRORS:", serializer.errors)

p.refresh_from_db()
print("DB STATUS AFTER SAVE:", p.expense_status)
