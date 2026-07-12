import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory
from systems.personnel.api.views.main_views import PersonnelViewSet
from systems.personnel.models import PersonnelMaster

User = get_user_model()
admin = User.objects.get(username='admin')
factory = APIRequestFactory()

p = PersonnelMaster.objects.get(military_number="7000055")
p.expense_status = None
p.save()

request = factory.patch('/api/v1/personnel/7000055/', {'expense_status': 'no_expenses'}, format='json')
from rest_framework.request import Request
request = Request(request)
request.user = admin

view = PersonnelViewSet()
view.request = request
view.format_kwarg = None
view.action = 'partial_update'
view.kwargs = {'pk': '7000055'}

obj = view.get_object()
serializer = view.get_serializer(obj, data=request.data, partial=True)
print("IS VALID:", serializer.is_valid())
print("VALIDATED DATA:", serializer.validated_data)
view.perform_update(serializer)

p.refresh_from_db()
print("FINAL DB STATUS:", p.expense_status)
print("SERIALIZER DATA KEYS:", serializer.data.keys())
