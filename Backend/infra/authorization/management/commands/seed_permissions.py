"""
seed_permissions — زرع جميع الصلاحيات في قاعدة البيانات
═══════════════════════════════════════════════════════════
يقرأ من PERMISSION_LABELS في registry/permissions.py
ويُنشئ/يُحدّث كل صلاحية في جدول Permission.

ثم يُعيّن الصلاحيات المناسبة لكل دور.

الاستخدام:
    python manage.py seed_permissions
    python manage.py seed_permissions --reset-roles  # إعادة تعيين صلاحيات الأدوار
"""
from django.core.management.base import BaseCommand
from django.db import transaction

from infra.authorization.models.permission import Permission
from infra.authorization.models.permission_group import PermissionGroup
from infra.authorization.models.field_permission import FieldPermission
from infra.authorization.models.role import Role, RolePermission
from infra.authorization.registry.permissions import (
    Perms, PERMISSION_LABELS, PERMISSION_GROUPS, FIELD_PERMISSIONS,
)


# ══════════════════════════════════════════════════════════════
# خارطة الأدوار → الصلاحيات
# ══════════════════════════════════════════════════════════════
ROLE_PERMISSIONS = {
    'super_admin': '__ALL__',  # يحصل على كل شيء

    'governorate_admin': [
        # لوحة المعلومات
        Perms.DASHBOARD_VIEW,
        # الأفراد
        Perms.PERSONNEL_VIEW, Perms.PERSONNEL_CREATE,
        Perms.PERSONNEL_EDIT, Perms.PERSONNEL_DELETE,
        Perms.PERSONNEL_IMPORT,
        Perms.PERSONNEL_VIEW_SALARY, Perms.PERSONNEL_VIEW_MILITARY_NUM,
        Perms.PERSONNEL_CHECK_NATIONAL_ID, Perms.PERSONNEL_UPDATE_NATIONAL_ID,
        # التسويات
        Perms.RANK_SETTLEMENT_VIEW, Perms.RANK_SETTLEMENT_CREATE,
        Perms.RANK_SETTLEMENT_EDIT, Perms.RANK_SETTLEMENT_EXECUTE,
        # التصحيحات
        Perms.CORRECTIONS_VIEW, Perms.CORRECTIONS_APPROVE, Perms.CORRECTIONS_REJECT,
        # الكشوفات
        Perms.SHEETS_EXPORT, Perms.SHEETS_IMPORT,
        # المراجعة والاعتماد
        Perms.STAGING_VIEW, Perms.STAGING_REVIEW,
        Perms.STAGING_APPROVE, Perms.STAGING_REJECT,
        Perms.STAGING_BULK_APPROVE,
        # المطابقة
        Perms.RECONCILIATION_VIEW, Perms.RECONCILIATION_CREATE,
        Perms.RECONCILIATION_RESOLVE,
        # إقفال الشهور
        Perms.MONTHS_VIEW, Perms.MONTHS_CLOSE, Perms.MONTHS_OVERRIDE_LOCK,
        # التقارير
        Perms.REPORTS_VIEW, Perms.REPORTS_EXPORT,
        Perms.REPORTS_PRINT, Perms.REPORTS_GENERATE,
        # التدقيق
        Perms.AUDIT_VIEW, Perms.AUDIT_EXPORT, Perms.AUDIT_LOGIN_VIEW,
        # الهيكل التنظيمي
        Perms.ORG_VIEW, Perms.ORG_CREATE, Perms.ORG_EDIT,
        # القواميس
        Perms.DICT_VIEW, Perms.DICT_CREATE, Perms.DICT_EDIT,
        # الالتزام
        Perms.COMPLIANCE_VIEW,
        # المستخدمين والأدوار (محدود)
        Perms.USERS_VIEW,
        Perms.ROLES_VIEW,
        # الملفات
        Perms.STORAGE_VIEW, Perms.STORAGE_UPLOAD,
        # البيانات الخام
        Perms.RAW_DATA_VIEW, Perms.RAW_DATA_IMPORT,
        # التفويض المزدوج
        Perms.DUAL_AUTH_VIEW, Perms.DUAL_AUTH_APPROVE,
        # ══ السكرتارية — صلاحيات كاملة ══
        Perms.SECRETARIAT_VIEW, Perms.SECRETARIAT_CREATE,
        Perms.SECRETARIAT_EDIT, Perms.SECRETARIAT_DELETE,
        Perms.SECRETARIAT_TASK_MANAGE,
        Perms.SECRETARIAT_COVER_LETTER,
    ],

    'services_chief': [
        Perms.DASHBOARD_VIEW,
        Perms.PERSONNEL_VIEW, Perms.PERSONNEL_EDIT,
        Perms.PERSONNEL_VIEW_SALARY, Perms.PERSONNEL_VIEW_MILITARY_NUM,
        Perms.CORRECTIONS_VIEW, Perms.CORRECTIONS_APPROVE, Perms.CORRECTIONS_REJECT,
        Perms.SHEETS_EXPORT, Perms.SHEETS_IMPORT,
        Perms.STAGING_VIEW, Perms.STAGING_REVIEW,
        Perms.STAGING_APPROVE, Perms.STAGING_REJECT,
        Perms.STAGING_BULK_APPROVE,
        Perms.RECONCILIATION_VIEW, Perms.RECONCILIATION_CREATE,
        Perms.RECONCILIATION_RESOLVE,
        Perms.MONTHS_VIEW, Perms.MONTHS_CLOSE,
        Perms.REPORTS_VIEW, Perms.REPORTS_EXPORT, Perms.REPORTS_PRINT,
        Perms.AUDIT_VIEW,
        Perms.DUAL_AUTH_VIEW,
        Perms.COMPLIANCE_VIEW,
        Perms.RAW_DATA_VIEW, Perms.RAW_DATA_IMPORT,
        Perms.STORAGE_VIEW, Perms.STORAGE_UPLOAD,
        Perms.RANK_SETTLEMENT_VIEW,
        Perms.ORG_VIEW,
        # ══ السكرتارية — إدارة التكليفات ══
        Perms.SECRETARIAT_VIEW, Perms.SECRETARIAT_CREATE,
        Perms.SECRETARIAT_EDIT,
        Perms.SECRETARIAT_TASK_MANAGE,
        Perms.SECRETARIAT_TASK_EXECUTE,
        Perms.SECRETARIAT_COVER_LETTER,
    ],

    'data_entry': [
        Perms.DASHBOARD_VIEW_OWN_DEPT,
        Perms.PERSONNEL_VIEW, Perms.PERSONNEL_EDIT,
        Perms.PERSONNEL_CREATE,
        Perms.SHEETS_IMPORT,
        Perms.CORRECTIONS_REQUEST,
        Perms.STORAGE_VIEW, Perms.STORAGE_UPLOAD,
        Perms.RAW_DATA_VIEW,
        Perms.RANK_SETTLEMENT_VIEW,
        # ══ السكرتارية — تنفيذ المهام المسندة فقط ══
        Perms.SECRETARIAT_VIEW_OWN,
        Perms.SECRETARIAT_TASK_EXECUTE,
    ],

    'inspector': [
        Perms.AUDIT_EXPORT,
        Perms.AUDIT_VERIFY,
        Perms.AUDIT_VIEW,
        Perms.DUAL_AUTH_VIEW,
        Perms.PERSONNEL_VIEW,
        Perms.REPORTS_EXPORT,
        Perms.REPORTS_PRINT,
        Perms.REPORTS_VIEW,
        Perms.REPORTS_GENERATE,
        # ══ السكرتارية — عرض للمراجعة فقط ══
        Perms.SECRETARIAT_VIEW,
    ],

    'inquiry': [
        Perms.DASHBOARD_VIEW_OWN_DEPT,
        Perms.PERSONNEL_VIEW,
        Perms.REPORTS_VIEW,
        Perms.ORG_VIEW,
        Perms.DICT_VIEW,
        Perms.COMPLIANCE_VIEW,
        Perms.STORAGE_VIEW,
        # لا دخول للسكرتارية
    ],

    'viewer': [
        Perms.DASHBOARD_VIEW_OWN_DEPT,
        Perms.PERSONNEL_VIEW_OWN_DEPT,
        Perms.REPORTS_VIEW_OWN_DEPT,
        Perms.ORG_VIEW,
        # ══ السكرتارية — تنفيذ مهامه فقط ══
        Perms.SECRETARIAT_VIEW_OWN,
        Perms.SECRETARIAT_TASK_EXECUTE,
    ],

    'dept_coordinator': [
        Perms.PERSONNEL_VIEW,
        Perms.REPORTS_PRINT,
        Perms.REPORTS_VIEW,
        Perms.SHEETS_IMPORT,
        # ══ السكرتارية — عرض وإدارة تكليفات ══
        Perms.SECRETARIAT_VIEW,
        Perms.SECRETARIAT_TASK_MANAGE,
        Perms.SECRETARIAT_TASK_EXECUTE,
    ],
}


class Command(BaseCommand):
    help = 'زرع جميع الصلاحيات في قاعدة البيانات وتعيينها للأدوار'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset-roles', action='store_true',
            help='إعادة تعيين صلاحيات جميع الأدوار (يحذف التعيينات الحالية)',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING('═' * 60))
        self.stdout.write(self.style.MIGRATE_HEADING(' 🔑 زرع الصلاحيات الشاملة'))
        self.stdout.write(self.style.MIGRATE_HEADING('═' * 60))

        # ── 0. زرع مجموعات الصلاحيات (Permission Groups) ──
        self.stdout.write(self.style.MIGRATE_HEADING('── 0. مجموعات الصلاحيات ──'))
        groups_created = 0
        groups_updated = 0
        
        group_objects = {}
        for code, (name, icon, order) in PERMISSION_GROUPS.items():
            group, created = PermissionGroup.objects.update_or_create(
                code=code,
                defaults={
                    'name': name,
                    'icon': icon,
                    'display_order': order,
                    'is_active': True,
                }
            )
            group_objects[code] = group
            if created:
                groups_created += 1
            else:
                groups_updated += 1
                
        self.stdout.write(
            f'  ✅ المجموعات: {groups_created} جديدة، {groups_updated} محدّثة\n'
        )

        # ── 1. زرع / تحديث الصلاحيات ──
        self.stdout.write(self.style.MIGRATE_HEADING('── 1. الصلاحيات ──'))
        created_count = 0
        updated_count = 0

        for code, details in PERMISSION_LABELS.items():
            parts = code.split('.')
            if len(parts) < 3:
                continue

            module = parts[0]
            action = parts[1]
            scope = parts[2]
            
            if isinstance(details, tuple) and len(details) == 2:
                label, category = details
            elif isinstance(details, dict):
                label = details.get('label', '')
                category = details.get('category', 'action')
            else:
                label = str(details)
                category = 'action'

            # تحديد المجموعة بناءً على الوحدة (module)
            group = group_objects.get(module)

            perm, created = Permission.objects.update_or_create(
                code=code,
                defaults={
                    'module': module,
                    'action': action,
                    'scope': scope,
                    'label': label,
                    'category': category,
                    'group': group,
                    'is_active': True,
                    'is_system': True,
                }
            )
            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(
            f'  ✅ صلاحيات: {created_count} جديدة، {updated_count} محدّثة '
            f'(المجموع: {Permission.objects.filter(is_active=True).count()})\n'
        )

        # ── 2. تعيين الصلاحيات للأدوار ──
        self.stdout.write(self.style.MIGRATE_HEADING('── 2. تعيين الصلاحيات للأدوار ──'))
        reset_roles = options.get('reset_roles', False)

        for role_code, perm_codes in ROLE_PERMISSIONS.items():
            try:
                role = Role.objects.get(code=role_code)
            except Role.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f'  ⚠️  الدور {role_code} غير موجود — تخطي')
                )
                continue

            if perm_codes == '__ALL__':
                all_perms = Permission.objects.filter(is_active=True)
                if reset_roles:
                    RolePermission.objects.filter(role=role).delete()
                for perm in all_perms:
                    RolePermission.objects.get_or_create(
                        role=role, permission=perm
                    )
                self.stdout.write(
                    f'  👑 {role.name}: {all_perms.count()} صلاحية (الكل)'
                )
            else:
                if reset_roles:
                    RolePermission.objects.filter(role=role).delete()
                assigned = 0
                for perm_code in perm_codes:
                    try:
                        perm = Permission.objects.get(code=perm_code)
                        _, was_created = RolePermission.objects.get_or_create(
                            role=role, permission=perm
                        )
                        if was_created:
                            assigned += 1
                    except Permission.DoesNotExist:
                        self.stdout.write(
                            self.style.WARNING(
                                f'  ⚠️  صلاحية {perm_code} غير موجودة!'
                            )
                        )
                total = role.permissions.count()
                self.stdout.write(
                    f'  🔧 {role.name}: +{assigned} جديدة (المجموع: {total})'
                )

        # ── 3. زرع الحقول الحساسة (Field Permissions) ──
        self.stdout.write('\n' + self.style.MIGRATE_HEADING('── 3. الحقول الحساسة ──'))
        fp_created = 0
        fp_updated = 0
        
        for (module, field_name), (label, view_perm, edit_perm, is_sensitive) in FIELD_PERMISSIONS.items():
            fp, created = FieldPermission.objects.update_or_create(
                module=module,
                field_name=field_name,
                defaults={
                    'label': label,
                    'view_permission': view_perm,
                    'edit_permission': edit_perm,
                    'is_sensitive': is_sensitive,
                    'is_active': True,
                }
            )
            if created:
                fp_created += 1
            else:
                fp_updated += 1
                
        self.stdout.write(
            f'  ✅ قيود الحقول: {fp_created} جديدة، {fp_updated} محدّثة'
        )

        self.stdout.write(self.style.SUCCESS('\n✅ تم بنجاح!'))
