import os
import django
from datetime import timedelta
from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.base")
django.setup()

from infra.authorization.models.field_permission import FieldPermission
from infra.authorization.models.policy import AccessPolicy
from infra.authorization.models.delegation import Delegation
from infra.authorization.models.emergency_access import EmergencyAccess
from django.contrib.auth import get_user_model

User = get_user_model()

print("Seeding Advanced Authorization Models...")

# 1. Field Permissions
field_perms_data = [
    {
        'module': 'personnel', 'field_name': 'basic_salary', 'label': 'الراتب الأساسي',
        'view_permission': 'PERSONNEL.READ.GLOBAL', 'edit_permission': 'PERSONNEL.WRITE.GLOBAL',
        'is_sensitive': True
    },
    {
        'module': 'personnel', 'field_name': 'national_id', 'label': 'الرقم الوطني',
        'view_permission': 'PERSONNEL.READ.GLOBAL', 'edit_permission': '',
        'is_sensitive': True
    },
    {
        'module': 'personnel', 'field_name': 'bank_account', 'label': 'الحساب البنكي (IBAN)',
        'view_permission': 'PERSONNEL.READ.GLOBAL', 'edit_permission': 'PERSONNEL.WRITE.GLOBAL',
        'is_sensitive': True
    }
]

fp_created = 0
for data in field_perms_data:
    fp, created = FieldPermission.objects.get_or_create(
        module=data['module'],
        field_name=data['field_name'],
        defaults={
            'label': data['label'],
            'view_permission': data['view_permission'],
            'edit_permission': data['edit_permission'],
            'is_sensitive': data['is_sensitive'],
            'is_active': True
        }
    )
    if created:
        fp_created += 1

# 2. Access Policies
policies_data = [
    {
        'code': 'BLOCK_MONTH_CLOSING_AFTER_HOURS',
        'name': 'سياسة حظر الإقفال في أوقات الذروة',
        'description': 'منع محاولة الإقفال خارج أوقات العمل الرسمية',
        'permission_code': 'MONTHS.APPROVE.GLOBAL',
        'model_name': 'MonthClosing',
        'effect': 'deny',
        'conditions': [
            {"field": "env.time", "op": "gt", "value": "15:00"},
            {"field": "env.time", "op": "lt", "value": "08:00"}
        ],
        'priority': 100,
        'is_active': True
    },
    {
        'code': 'INTERNAL_NETWORK_ONLY_FOR_AUDIT',
        'name': 'حصر الوصول عبر الشبكة الداخلية للتدقيق',
        'description': 'منع المدققين من الوصول لسجلات التدقيق من خارج شبكة الوزارة',
        'permission_code': 'AUDIT.READ.GLOBAL',
        'model_name': 'AuditLog',
        'effect': 'deny',
        'conditions': [
            {"field": "env.ip", "op": "not_in", "value": ["192.168.1.0/24", "10.0.0.0/8"]}
        ],
        'priority': 90,
        'is_active': True
    }
]

pol_created = 0
for data in policies_data:
    pol, created = AccessPolicy.objects.get_or_create(
        code=data['code'],
        defaults={
            'name': data['name'],
            'description': data['description'],
            'permission_code': data['permission_code'],
            'model_name': data['model_name'],
            'effect': data['effect'],
            'conditions': data['conditions'],
            'priority': data['priority'],
            'is_active': data['is_active']
        }
    )
    if created:
        pol_created += 1

# 3. Emergency Access & Delegations
admin_user = User.objects.filter(is_superuser=True).first() or User.objects.first()
other_user = User.objects.filter(is_superuser=False).first()

em_created = 0
del_created = 0

if admin_user and other_user:
    # Emergency Access for other_user
    em, created = EmergencyAccess.objects.get_or_create(
        user=other_user,
        status='active',
        defaults={
            'reason': 'حالة طوارئ لتسيير رواتب الشهر',
            'granted_by': admin_user,
            'granted_at': timezone.now(),
            'expires_at': timezone.now() + timedelta(hours=12)
        }
    )
    if created: em_created += 1

    # Delegation from Admin to other_user
    de, created = Delegation.objects.get_or_create(
        delegator=admin_user,
        delegate=other_user,
        status='active',
        defaults={
            'reason': 'إجازة سنوية لمدير النظام',
            'starts_at': timezone.now(),
            'ends_at': timezone.now() + timedelta(days=5)
        }
    )
    if created: del_created += 1

print(f"Successfully seeded: {fp_created} Field Permissions, {pol_created} Policies, {em_created} Emergency Accesses, {del_created} Delegations!")
