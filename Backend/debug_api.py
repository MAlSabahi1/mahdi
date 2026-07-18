from django.test import Client
from django.contrib.auth import get_user_model
import json

User = get_user_model()
u = User.objects.first()
c = Client(SERVER_NAME='localhost')
c.force_login(u)
res = c.get('/api/v1/personnel/9900003/')
if res.status_code == 200:
    data = res.json()
    for d in data.get('documents', []):
        if d['context_type'] == 'StatusChangeForm':
            print("Doc dict:", d)
else:
    print("API returned:", res.status_code)
