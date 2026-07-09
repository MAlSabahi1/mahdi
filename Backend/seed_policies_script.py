import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.base")
django.setup()

from infra.authorization.models.field_permission import FieldPermission
from infra.authorization.models.policy import AccessPolicy
from infra.authorization.models.role import Role

print("Seeding Field Permissions and Policies...")

# Get existing roles
hr_role = Role.objects.filter(code='HR_MANAGER').first()
entry_role = Role.objects.filter(code='DATA_ENTRY').first()
auditor_role = Role.objects.filter(code='GENERAL_AUDITOR').first()
admin_role = Role.objects.filter(code='SYSTEM_ADMIN').first()

# 1. Field Permissions (ABAC) for Personnel model
field_perms_data = [
    # Salary field is highly sensitive
    {'role': hr_role, 'model_name': 'PersonnelMaster', 'field_name': 'basic_salary', 'can_read': True, 'can_write': True},
    {'role': entry_role, 'model_name': 'PersonnelMaster', 'field_name': 'basic_salary', 'can_read': False, 'can_write': False},
    {'role': auditor_role, 'model_name': 'PersonnelMaster', 'field_name': 'basic_salary', 'can_read': True, 'can_write': False},
    
    # Contact info
    {'role': entry_role, 'model_name': 'PersonnelMaster', 'field_name': 'phone_number', 'can_read': True, 'can_write': True},
    
    # ID info
    {'role': entry_role, 'model_name': 'PersonnelMaster', 'field_name': 'national_id', 'can_read': True, 'can_write': False},
]

fp_created = 0
for data in field_perms_data:
    if data['role']:
        fp, created = FieldPermission.objects.get_or_create(
            role=data['role'],
            model_name=data['model_name'],
            field_name=data['field_name'],
            defaults={
                'can_read': data['can_read'],
                'can_write': data['can_write']
            }
        )
        if created:
            fp_created += 1

# 2. Access Policies (Rule-based access)
policies_data = [
    {
        'name': 'سياسة حظر الإقفال في أوقات الذروة',
        'code': 'BLOCK_MONTH_CLOSING_AFTER_HOURS',
        'description': 'منع أي محاولة لإقفال الشهور خارج أوقات العمل الرسمية حتى لمدراء النظام',
        'policy_type': 'TIME_BASED',
        'effect': 'DENY',
        'conditions': {"start_time": "15:00", "end_time": "08:00"},
        'is_active': True
    },
    {
        'name': 'الاعتماد الثنائي الإلزامي للرواتب',
        'code': 'REQUIRE_DUAL_AUTH_SALARY_CHANGES',
        'description': 'تفعيل الاعتماد الثنائي الإلزامي عند أي تعديل على الراتب الأساسي',
        'policy_type': 'REQUIRE_DUAL_AUTH',
        'effect': 'ALLOW',
        'conditions': {"target_field": "basic_salary", "action": "WRITE"},
        'is_active': True
    },
    {
        'name': 'حصر الوصول عبر الشبكة الداخلية (IP)',
        'code': 'INTERNAL_NETWORK_ONLY_FOR_AUDIT',
        'description': 'منع المدققين من الوصول لسجلات التدقيق من خارج شبكة الوزارة',
        'policy_type': 'IP_BASED',
        'effect': 'DENY',
        'conditions': {"allowed_ips": ["192.168.1.0/24", "10.0.0.0/8"]},
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
            'policy_type': data['policy_type'],
            'effect': data['effect'],
            'conditions': data['conditions'],
            'is_active': data['is_active']
        }
    )
    if created:
        pol_created += 1

print(f"Successfully seeded {fp_created} Field Permissions and {pol_created} Access Policies!")
