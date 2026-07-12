import requests
import json
import os, django

# 1. Setup django to generate token
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
User = get_user_model()
admin = User.objects.get(username='admin')
token, _ = Token.objects.get_or_create(user=admin)

# 2. Get 6042041 data (simulate GET /api/v1/personnel/6042041/)
url_get = "http://127.0.0.1:8000/api/v1/personnel/6042041/"
headers = {"Authorization": f"Token {token.key}"}
get_res = requests.get(url_get, headers=headers)
data = get_res.json()

# 3. Simulate frontend form update
data['expense_status'] = 'no_expenses'

# 4. Simulate PATCH /api/v1/personnel/6042041/
url_patch = "http://127.0.0.1:8000/api/v1/personnel/6042041/"
patch_res = requests.patch(url_patch, json=data, headers=headers)
print("PATCH STATUS:", patch_res.status_code)

# 5. Check DB directly
from systems.personnel.models import PersonnelMaster
p = PersonnelMaster.objects.get(military_number="6042041")
print("FINAL DB STATUS:", p.expense_status)
