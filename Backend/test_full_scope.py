import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.conf import settings
settings.ALLOWED_HOSTS.append('testserver')

from django.contrib.auth import get_user_model
from django.test import Client
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()
user = User.objects.get(username='marib_admin')
token = str(RefreshToken.for_user(user).access_token)
client = Client(HTTP_AUTHORIZATION=f'Bearer {token}')

endpoints = [
    ('/api/v1/personnel/dashboard/stats/',     'لوحة الإحصائيات'),
    ('/api/v1/personnel/dashboard/analytics/', 'لوحة التحليلات'),
    ('/api/v1/personnel/dashboard/alerts/',    'مركز التنبيهات'),
    ('/api/v1/personnel/dashboard/compliance/','الالتزام الإداري'),
    ('/api/v1/personnel/',                     'قائمة الأفراد'),
    ('/api/v1/reports/categorical-summary/?level=central', 'التقرير الفئوي'),
]

print(f'=== اختبار حساب marib_admin ===\n')
for url, name in endpoints:
    r = client.get(url)
    data = r.json()
    
    # استخراج الأرقام المهمة
    summary = ''
    if 'total_personnel' in data:
        summary = f"total_personnel={data['total_personnel']}, branches={data.get('active_branches','-')}"
    elif 'count' in data:
        summary = f"count={data['count']}"
    elif 'data' in data and isinstance(data['data'], list):
        summary = f"items={len(data['data'])}"
    elif 'force_distribution' in data:
        total = sum(x.get('value',0) for x in data.get('status_distribution',[]))
        summary = f"status_total={total}"
    elif 'data_quality_alerts' in data:
        summary = f"alerts={len(data.get('data_quality_alerts',[]))}, pending={data.get('stats',{}).get('pending_requests_count',0)}"
    elif 'compliance_by_region' in data:
        summary = f"regions={len(data.get('compliance_by_region',[]))}"
    
    status_icon = '✅' if r.status_code == 200 else '❌'
    print(f'{status_icon} [{r.status_code}] {name}')
    print(f'       {summary}')
    print()

print('=== انتهى الاختبار ===')
