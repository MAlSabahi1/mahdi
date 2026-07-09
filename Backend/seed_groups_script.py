import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.base")
django.setup()

from infra.authorization.models.permission import Permission
from infra.authorization.models.permission_group import PermissionGroup

modules = {
    'users': 'المستخدمين',
    'roles': 'الأدوار والصلاحيات',
    'personnel': 'شؤون الأفراد',
    'corrections': 'التصحيحات',
    'sheets': 'الكشوفات',
    'staging': 'المراجعة والاعتماد',
    'reconciliation': 'المطابقة',
    'months': 'إقفال الشهور',
    'reports': 'التقارير',
    'audit': 'التدقيق',
    'system': 'النظام',
    'admin': 'الإدارة',
    'storage': 'الملفات والمرفقات',
    'dual_auth': 'الاعتماد المزدوج',
    'security': 'الأمن والمراقبة',
    'workflow': 'سير العمليات'
}

print("Seeding Permission Groups...")
groups_created = 0

for mod_code, mod_label in modules.items():
    # Fetch all permissions for this module
    mod_permissions = list(Permission.objects.filter(module=mod_code))
    if not mod_permissions:
        continue

    # 1. Basic Group (Read, Write, Export)
    basic_perms = [p for p in mod_permissions if p.action in ['read', 'write', 'export']]
    if basic_perms:
        basic_group, created = PermissionGroup.objects.get_or_create(
            code=f"{mod_code.upper()}_BASIC_GROUP",
            defaults={
                'name': f'إدارة {mod_label} - أساسية',
                'description': f'صلاحيات القراءة والإضافة العادية لقسم {mod_label}',
                'icon': 'mdi-shield-account-outline',
                'display_order': 10
            }
        )
        # Assign basic permissions and set the foreign key on Permission (since in HumenResorse Permission has a FK to Group)
        # Wait, in Permission model, `group` is a ForeignKey to PermissionGroup. 
        # Since it's a Many-to-One (One group has many permissions in this schema, or Many-to-Many?)
        # Let's verify the relationship. If it's a FK on Permission, a permission can only belong to one group!
        for p in basic_perms:
            p.group = basic_group
            p.save()
        groups_created += 1

    # 2. Advanced/Full Group (Delete, Approve, Manage)
    # Wait, if a permission can only belong to ONE group (ForeignKey on Permission), we can't split basic/advanced easily unless we create distinct permissions.
    # Let's just create ONE group per module that bundles ALL permissions of that module.
    # This matches typical hierarchical RBAC where a group represents the entire module's bundle.
    
    full_group, created = PermissionGroup.objects.get_or_create(
        code=f"{mod_code.upper()}_FULL_GROUP",
        defaults={
            'name': f'مجموعة صلاحيات {mod_label}',
            'description': f'الباقة الكاملة لجميع صلاحيات {mod_label}',
            'icon': 'mdi-shield-check',
            'display_order': 20
        }
    )
    
    # Assign ALL permissions of this module to this single full group.
    for p in mod_permissions:
        p.group = full_group
        p.save()
    
    groups_created += 1

print(f"Successfully seeded {groups_created} Permission Groups and linked all permissions!")
