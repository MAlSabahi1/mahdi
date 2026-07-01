"""
Data Migration: إنشاء الأدوار المفقودة وتعيين صلاحياتها
═══════════════════════════════════════════════════════
ينشئ الأدوار: inspector, dept_coordinator, governorate_admin, inquiry
إذا لم تكن موجودة، ويربطها بالصلاحيات الصحيحة.
"""
from django.db import migrations


def create_missing_roles_and_assign_permissions(apps, schema_editor):
    Role = apps.get_model('authorization', 'Role')
    Permission = apps.get_model('authorization', 'Permission')
    RolePermission = apps.get_model('authorization', 'RolePermission')

    # تعريف الأدوار المفقودة
    missing_roles = [
        {
            'name': 'مفتش',
            'code': 'inspector',
            'description': 'عرض فقط مع صلاحيات التدقيق والتقارير',
            'is_system_role': True,
            'priority': 60,
        },
        {
            'name': 'منسق إدارة',
            'code': 'dept_coordinator',
            'description': 'مسؤول عن رفع الكشوفات لإدارته',
            'is_system_role': True,
            'priority': 30,
        },
        {
            'name': 'مدير المحافظة',
            'code': 'governorate_admin',
            'description': 'إدارة شاملة على مستوى المحافظة',
            'is_system_role': True,
            'priority': 90,
        },
        {
            'name': 'استعلامات',
            'code': 'inquiry',
            'description': 'عرض محدود للاستعلام',
            'is_system_role': True,
            'priority': 20,
        },
    ]

    for role_data in missing_roles:
        Role.objects.get_or_create(
            code=role_data['code'],
            defaults={k: v for k, v in role_data.items() if k != 'code'}
        )

    # خريطة صلاحيات الأدوار المفقودة
    role_perms_map = {
        'inspector': [
            'personnel.view.all',
            'audit.view.all',
            'audit.verify.all',
            'audit.export.all',
            'reports.view.all',
            'reports.print.all',
            'reports.export.all',
            'dual_auth.view.all',
            'security.shadow_tables.all',
        ],
        'dept_coordinator': [
            'personnel.view.all',
            'sheets.import.all',
            'reports.view.all',
            'reports.print.all',
        ],
        'governorate_admin': [
            'personnel.view.all',
            'personnel.create.all',
            'personnel.edit.all',
            'personnel.delete.all',
            'sheets.export.all',
            'sheets.import.all',
            'staging.review.all',
            'staging.approve.all',
            'staging.reject.all',
            'reconciliation.create.all',
            'reconciliation.resolve.all',
            'months.close.all',
            'months.override_lock.all',
            'audit.view.all',
            'audit.export.all',
            'reports.view.all',
            'reports.print.all',
            'reports.export.all',
            'corrections.approve.all',
            'corrections.request.all',
            'dual_auth.view.all',
            'dual_auth.approve.all',
            'admin.manage_users.all',
            'admin.manage_roles.all',
            'admin.manage_dicts.all',
        ],
        'inquiry': [
            'personnel.view.all',
            'reports.view.all',
        ],
    }

    for role_code, perm_codes in role_perms_map.items():
        try:
            role = Role.objects.get(code=role_code)
        except Role.DoesNotExist:
            continue

        # حذف الصلاحيات القديمة وإعادة تعيينها
        RolePermission.objects.filter(role=role).delete()
        for code in perm_codes:
            try:
                perm = Permission.objects.get(code=code)
                RolePermission.objects.get_or_create(role=role, permission=perm)
            except Permission.DoesNotExist:
                pass


def rollback(apps, schema_editor):
    Role = apps.get_model('authorization', 'Role')
    for code in ['inspector', 'dept_coordinator', 'governorate_admin', 'inquiry']:
        Role.objects.filter(code=code, is_system_role=True).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('authorization', '0003_seed_permissions_and_roles'),
        ('security', '0009_delete_usersession'),
    ]

    operations = [
        migrations.RunPython(
            create_missing_roles_and_assign_permissions,
            rollback,
        ),
    ]
