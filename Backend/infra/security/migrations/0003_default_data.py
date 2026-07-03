"""
Data Migration: إنشاء الأدوار الافتراضية والإعدادات
"""
from django.db import migrations


def create_default_roles(apps, schema_editor):
    """إنشاء الأدوار النظامية الافتراضية"""
    Role = apps.get_model('security', 'Role')
    
    roles = [
        {
            'name': 'مدير النظام',
            'code': 'super_admin',
            'description': 'صلاحيات كاملة على جميع النظام',
            'is_system_role': True,
            'priority': 100,
            'permissions': [
                'view_personnel', 'edit_personnel_basic', 'edit_personnel_status',
                'delete_personnel', 'export_sheet', 'import_sheet',
                'review_staging', 'approve_change', 'reject_change',
                'create_reconciliation', 'resolve_reconciliation',
                'close_month', 'override_lock',
                'view_audit_log', 'verify_audit_signatures',
                'view_reports', 'print_reports', 'export_reports',
                'manage_users', 'manage_roles', 'manage_dictionaries',
                'manage_settings', 'manage_backups',
                'approve_dual_auth', 'view_dual_auth',
                'view_security_dashboard', 'view_shadow_tables',
                'request_correction', 'approve_correction',
            ],
            'visible_pages': [
                '/dashboard', '/personnel', '/personnel/detail',
                '/services', '/services/export', '/services/import',
                '/services/review', '/services/reconciliation',
                '/services/snapshot', '/services/compliance',
                '/admin', '/admin/users', '/admin/roles',
                '/admin/dictionaries', '/admin/audit',
                '/admin/shadow-tables', '/admin/dual-auth',
                '/admin/settings', '/admin/backups',
                '/admin/telemetry', '/reports',
            ],
        },
        {
            'name': 'رئيس الخدمات',
            'code': 'services_chief',
            'description': 'إدارة الكشوفات الشهرية والمراجعة والاعتماد',
            'is_system_role': True,
            'priority': 80,
            'permissions': [
                'view_personnel', 'edit_personnel_status',
                'export_sheet', 'import_sheet',
                'review_staging', 'approve_change', 'reject_change',
                'create_reconciliation', 'resolve_reconciliation',
                'close_month',
                'view_audit_log', 'view_reports', 'print_reports',
                'export_reports', 'view_dual_auth',
            ],
            'visible_pages': [
                '/dashboard', '/personnel',
                '/services', '/services/export', '/services/import',
                '/services/review', '/services/reconciliation',
                '/services/snapshot', '/services/compliance',
                '/reports',
            ],
        },
        {
            'name': 'مفتش',
            'code': 'inspector',
            'description': 'عرض فقط مع صلاحيات التدقيق والتقارير',
            'is_system_role': True,
            'priority': 60,
            'permissions': [
                'view_personnel', 'view_audit_log',
                'verify_audit_signatures',
                'view_reports', 'print_reports', 'export_reports',
                'view_dual_auth', 'view_shadow_tables',
            ],
            'visible_pages': [
                '/dashboard', '/personnel',
                '/reports', '/admin/audit',
                '/admin/shadow-tables',
            ],
        },
        {
            'name': 'مدخل بيانات',
            'code': 'data_entry',
            'description': 'إدخال وتعديل بيانات الأفراد',
            'is_system_role': True,
            'priority': 40,
            'permissions': [
                'view_personnel', 'edit_personnel_basic',
                'import_sheet', 'request_correction',
            ],
            'visible_pages': [
                '/dashboard', '/personnel',
                '/services/import',
            ],
        },
        {
            'name': 'منسق إدارة',
            'code': 'dept_coordinator',
            'description': 'مسؤول عن رفع الكشوفات لإدارته',
            'is_system_role': True,
            'priority': 30,
            'permissions': [
                'view_personnel', 'import_sheet',
                'view_reports',
            ],
            'visible_pages': [
                '/dashboard', '/personnel',
                '/services/import', '/reports',
            ],
        },
        {
            'name': 'مستخدم عادي',
            'code': 'viewer',
            'description': 'عرض فقط بدون أي تعديل',
            'is_system_role': True,
            'priority': 10,
            'permissions': [
                'view_personnel', 'view_reports',
            ],
            'visible_pages': [
                '/dashboard', '/personnel', '/reports',
            ],
        },
    ]
    
    for role_data in roles:
        Role.objects.get_or_create(
            code=role_data['code'],
            defaults=role_data
        )


def create_default_settings(apps, schema_editor):
    """إنشاء الإعدادات الافتراضية"""
    SystemSetting = apps.get_model('security', 'SystemSetting')
    
    settings = [
        ('default_month_lock_day', 20, 'اليوم الافتراضي لإقفال الشهر', 'general'),
        ('max_upload_size_mb', 20, 'الحد الأقصى لحجم الملف بالميجابايت', 'import_export'),
        ('fuzzy_match_threshold', 85, 'حد التشابه في المطابقة الذكية (%)', 'import_export'),
        ('session_timeout_minutes', 30, 'مدة انتهاء الجلسة بالدقائق', 'security'),
        ('max_failed_logins', 5, 'الحد الأقصى لمحاولات الدخول الفاشلة', 'security'),
        ('account_lockout_minutes', 30, 'مدة قفل الحساب بالدقائق', 'security'),
        ('dual_auth_expiry_days', 7, 'مدة انتهاء طلب التفويض المزدوج بالأيام', 'security'),
        ('temp_file_expiry_minutes', 30, 'مدة انتهاء الملفات المؤقتة بالدقائق', 'import_export'),
        ('metrics_collection_interval_minutes', 5, 'فترة تجميع الإحصائيات بالدقائق', 'performance'),
    ]
    
    for key, value, desc, category in settings:
        SystemSetting.objects.get_or_create(
            key=key,
            defaults={
                'value': value,
                'description': desc,
                'category': category,
            }
        )


def reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    
    dependencies = [
        ('security', '0002_shadow_tables'),
    ]
    
    operations = [
        migrations.RunPython(create_default_roles, reverse),
        migrations.RunPython(create_default_settings, reverse),
    ]
