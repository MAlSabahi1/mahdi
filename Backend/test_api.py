from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model
from django.test.client import RequestFactory
from systems.personnel.api.views.detailed_reports_views import TempInactiveReportsView

user = get_user_model().objects.get(username='admin')
request = RequestFactory().get('/api/v1/reports/detailed-reports/temp-inactive/', {'report_id': 'report_11'})
request.user = user

view = TempInactiveReportsView.as_view()
response = view(request)
print("Data count:", len(response.data['data']))
for d in response.data['data']:
    print(d)
