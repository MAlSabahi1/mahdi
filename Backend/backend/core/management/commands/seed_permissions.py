"""
Seed Permissions — تهيئة سجلات Permission في core
═══════════════════════════════════════════════════
Usage: python manage.py seed_permissions
"""
from django.core.management.base import BaseCommand
from infra.authorization.models import Permission


# خريطة module.action.scope لكل صلاحية
PERMISSION_DEFINITIONS = [
    # personnel
    ('personnel.view.all', 'personnel', 'view', 'all', 'عرض الأفراد'),
    ('personnel.view.department', 'personnel', 'view', 'department', 'عرض أفراد الإدارة العامة'),
    ('personnel.view.governorate', 'personnel', 'view', 'governorate', 'عرض أفراد المحافظة'),
    ('personnel.create.all', 'personnel', 'create', 'all', 'إضافة فرد'),
    ('personnel.edit.all', 'personnel', 'edit', 'all', 'تعديل الأفراد'),
    ('personnel.delete.all', 'personnel', 'delete', 'all', 'حذف فرد (يتطلب تفويض مزدوج)', True),
    ('personnel.view_salary.all', 'personnel', 'view_salary', 'all', 'عرض الراتب'),
    ('personnel.edit_salary.all', 'personnel', 'edit_salary', 'all', 'تعديل الراتب'),
    ('personnel.view_military_number.all', 'personnel', 'view_military_number', 'all', 'عرض الرقم العسكري'),
    ('personnel.edit_military_number.all', 'personnel', 'edit_military_number', 'all', 'تعديل الرقم العسكري'),

    # services
    ('services.view.all', 'services', 'view', 'all', 'عرض الخدمات'),
    ('services.view.department', 'services', 'view', 'department', 'عرض خدمات الإدارة العامة'),
    ('services.create.all', 'services', 'create', 'all', 'إنشاء خدمة'),
    ('services.edit.all', 'services', 'edit', 'all', 'تعديل الخدمة'),
    ('services.delete.all', 'services', 'delete', 'all', 'حذف الخدمة'),
    ('services.approve.all', 'services', 'approve', 'all', 'اعتماد الخدمة'),
    ('services.reject.all', 'services', 'reject', 'all', 'رفض الخدمة'),
    ('services.escalate.all', 'services', 'escalate', 'all', 'تصعيد الخدمة'),

    # sheets (export/import)
    ('sheets.export.all', 'sheets', 'export', 'all', 'تصدير كشوفات'),
    ('sheets.import.all', 'sheets', 'import', 'all', 'رفع كشوفات'),

    # staging/corrections
    ('staging.review.all', 'staging', 'review', 'all', 'مراجعة التغييرات المقترحة'),
    ('staging.approve.all', 'staging', 'approve', 'all', 'اعتماد التغييرات'),
    ('staging.reject.all', 'staging', 'reject', 'all', 'رفض التغييرات'),
    ('corrections.request.all', 'corrections', 'request', 'all', 'طلب تصحيح بيانات (نموذج 23)'),
    ('corrections.approve.all', 'corrections', 'approve', 'all', 'اعتماد تصحيح بيانات'),

    # reconciliation
    ('reconciliation.create.all', 'reconciliation', 'create', 'all', 'إنشاء مهام مطابقة'),
    ('reconciliation.resolve.all', 'reconciliation', 'resolve', 'all', 'حل اختلافات المطابقة'),

    # months
    ('months.close.all', 'months', 'close', 'all', 'إقفال الشهر'),
    ('months.override_lock.all', 'months', 'override_lock', 'all', 'إلغاء إقفال الشهر', True),

    # audit
    ('audit.view.all', 'audit', 'view', 'all', 'عرض سجل التدقيق'),
    ('audit.verify.all', 'audit', 'verify', 'all', 'التحقق من توقيعات التدقيق'),
    ('audit.export.all', 'audit', 'export', 'all', 'تصدير سجل التدقيق'),

    # reports
    ('reports.view.all', 'reports', 'view', 'all', 'عرض التقارير'),
    ('reports.view.department', 'reports', 'view', 'department', 'عرض تقارير الإدارة العامة'),
    ('reports.print.all', 'reports', 'print', 'all', 'طباعة التقارير'),
    ('reports.export.all', 'reports', 'export', 'all', 'تصدير التقارير'),

    # admin
    ('admin.manage_users.all', 'admin', 'manage_users', 'all', 'إدارة المستخدمين والأدوار'),
    ('admin.manage_roles.all', 'admin', 'manage_roles', 'all', 'إنشاء وتعديل الأدوار'),
    ('admin.manage_dicts.all', 'admin', 'manage_dicts', 'all', 'إدارة القواميس'),
    ('admin.manage_settings.all', 'admin', 'manage_settings', 'all', 'إدارة الإعدادات العامة'),
    ('admin.manage_backups.all', 'admin', 'manage_backups', 'all', 'إدارة النسخ الاحتياطي'),

    # users (core CRUD)
    ('users.view.all', 'users', 'view', 'all', 'عرض المستخدمين'),
    ('users.create.all', 'users', 'create', 'all', 'إنشاء مستخدم'),
    ('users.update.all', 'users', 'update', 'all', 'تعديل مستخدم'),
    ('users.delete.all', 'users', 'delete', 'all', 'حذف مستخدم'),
    ('users.reset_password.all', 'users', 'reset_password', 'all', 'إعادة تعيين كلمة المرور'),
    ('users.unlock.all', 'users', 'unlock', 'all', 'فتح حساب مستخدم'),
    ('users.view_sessions.all', 'users', 'view_sessions', 'all', 'عرض جلسات المستخدمين'),

    # roles (core CRUD)
    ('roles.view.all', 'roles', 'view', 'all', 'عرض الأدوار'),
    ('roles.create.all', 'roles', 'create', 'all', 'إنشاء دور'),
    ('roles.update.all', 'roles', 'update', 'all', 'تعديل دور'),
    ('roles.delete.all', 'roles', 'delete', 'all', 'حذف دور'),
    ('roles.assign.all', 'roles', 'assign', 'all', 'إسناد دور'),

    # dual auth
    ('dual_auth.approve.all', 'dual_auth', 'approve', 'all', 'الموافقة على طلبات التفويض المزدوج', True),
    ('dual_auth.view.all', 'dual_auth', 'view', 'all', 'عرض طلبات التفويض المزدوج'),

    # security
    ('security.dashboard.all', 'security', 'dashboard', 'all', 'عرض لوحة المراقبة الأمنية'),
    ('security.shadow_tables.all', 'security', 'shadow_tables', 'all', 'عرض تاريخ الجداول'),

    # system
    ('system.settings.all', 'system', 'settings', 'all', 'إعدادات النظام'),
    ('system.backup.all', 'system', 'backup', 'all', 'النسخ الاحتياطي للنظام'),
    ('system.telemetry.all', 'system', 'telemetry', 'all', 'لوحة مراقبة الأداء'),

    # storage
    ('storage.upload.all', 'storage', 'upload', 'all', 'رفع ملفات'),
    ('storage.delete.all', 'storage', 'delete', 'all', 'حذف ملفات'),
    ('storage.view.all', 'storage', 'view', 'all', 'عرض ملفات'),

    # workflow
    ('workflow.view.all', 'workflow', 'view', 'all', 'عرض مسارات العمل'),
    ('workflow.manage.all', 'workflow', 'manage', 'all', 'إدارة مسارات العمل'),
]


class Command(BaseCommand):
    help = 'تهيئة جدول Permission بالصلاحيات الأساسية'

    def handle(self, *args, **options):
        created = 0
        updated = 0

        for entry in PERMISSION_DEFINITIONS:
            code = entry[0]
            module = entry[1]
            action = entry[2]
            scope = entry[3]
            label = entry[4]
            requires_dual = entry[5] if len(entry) > 5 else False

            obj, was_created = Permission.objects.update_or_create(
                code=code,
                defaults={
                    'module': module,
                    'action': action,
                    'scope': scope,
                    'label': label,
                    'requires_dual_auth': requires_dual,
                    'is_system': True,
                    'is_active': True,
                }
            )
            if was_created:
                created += 1
            else:
                updated += 1

        self.stdout.write(self.style.SUCCESS(
            f'✅ تم تهيئة الصلاحيات: {created} جديدة، {updated} محدثة، '
            f'الإجمالي: {Permission.objects.count()}'
        ))
