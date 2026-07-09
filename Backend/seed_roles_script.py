import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.base")
django.setup()

from infra.authorization.models.role import Role
from infra.authorization.models.permission_group import PermissionGroup

roles_data = [
    {
        'code': 'SYSTEM_ADMIN',
        'name': 'مدير النظام الشامل',
        'description': 'صلاحيات كاملة على كل أجزاء النظام (مدير أعلى)',
        'is_system_role': True,
        'priority': 100,
        'groups': ['SYSTEM_FULL_GROUP', 'SECURITY_FULL_GROUP', 'ADMIN_FULL_GROUP', 'USERS_FULL_GROUP', 'ROLES_FULL_GROUP']
    },
    {
        'code': 'HR_MANAGER',
        'name': 'مدير الموارد البشرية',
        'description': 'مسؤول عن إدارة شؤون الأفراد والهيكلة',
        'is_system_role': False,
        'priority': 80,
        'groups': ['PERSONNEL_FULL_GROUP', 'SHEETS_FULL_GROUP', 'REPORTS_FULL_GROUP']
    },
    {
        'code': 'DATA_ENTRY',
        'name': 'مدخل بيانات',
        'description': 'إدخال البيانات الأساسية والمستندات',
        'is_system_role': False,
        'priority': 30,
        'groups': ['PERSONNEL_FULL_GROUP', 'STORAGE_FULL_GROUP']
    },
    {
        'code': 'GENERAL_AUDITOR',
        'name': 'مدقق عام (Compliance)',
        'description': 'مراقبة ومراجعة السجلات وعمليات المطابقة',
        'is_system_role': False,
        'priority': 90,
        'groups': ['AUDIT_FULL_GROUP', 'RECONCILIATION_FULL_GROUP', 'REPORTS_FULL_GROUP', 'STAGING_FULL_GROUP']
    }
]

print("Seeding Roles...")

roles_created = 0

for data in roles_data:
    role, created = Role.objects.get_or_create(
        code=data['code'],
        defaults={
            'name': data['name'],
            'description': data['description'],
            'is_system_role': data['is_system_role'],
            'priority': data['priority']
        }
    )
    
    # Retrieve the corresponding groups
    groups = PermissionGroup.objects.filter(code__in=data['groups'])
    # In this schema, a Role has a ManyToMany to Permissions or PermissionGroups?
    # Let's check the fields of Role model. 
    # Usually a Role has `permissions` (ManyToMany to Permission). 
    # Since we linked permissions to groups, we need to gather all permissions in these groups and assign them to the role.
    
    # Fetch all permissions belonging to the requested groups
    from infra.authorization.models.permission import Permission
    perms_to_add = Permission.objects.filter(group__in=groups)
    
    # Add them to the role
    role.permissions.add(*perms_to_add)
    roles_created += 1

print(f"Successfully seeded {roles_created} Roles and assigned permissions via groups!")
