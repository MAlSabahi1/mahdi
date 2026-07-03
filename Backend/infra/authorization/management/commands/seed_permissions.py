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
from infra.authorization.models.role import Role, RolePermission
from infra.authorization.registry.permissions import Perms, PERMISSION_LABELS


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
    ],

    'inquiry': [
        Perms.DASHBOARD_VIEW_OWN_DEPT,
        Perms.PERSONNEL_VIEW,
        Perms.REPORTS_VIEW,
        Perms.ORG_VIEW,
        Perms.DICT_VIEW,
        Perms.COMPLIANCE_VIEW,
        Perms.STORAGE_VIEW,
    ],

    'viewer': [
        Perms.DASHBOARD_VIEW_OWN_DEPT,
        Perms.PERSONNEL_VIEW_OWN_DEPT,
        Perms.REPORTS_VIEW_OWN_DEPT,
        Perms.ORG_VIEW,
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

        # ── 1. زرع / تحديث الصلاحيات ──
        created_count = 0
        updated_count = 0

        for code, (label, category) in PERMISSION_LABELS.items():
            parts = code.split('.')
            module = parts[0]
            action = parts[1] if len(parts) > 1 else 'view'
            scope = parts[2] if len(parts) > 2 else 'all'

            perm, created = Permission.objects.update_or_create(
                code=code,
                defaults={
                    'module': module,
                    'action': action,
                    'scope': scope,
                    'label': label,
                    'category': category,
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
            f'(المجموع: {Permission.objects.filter(is_active=True).count()})'
        )

        # ── 2. تعيين الصلاحيات للأدوار ──
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

        self.stdout.write(self.style.SUCCESS('\n✅ تم بنجاح!'))
