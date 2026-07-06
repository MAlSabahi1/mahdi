"""
Permission Registry — ثوابت الصلاحيات المركزية
═══════════════════════════════════════════════════
لا نصوص مبعثرة في الكود — كل الأكواد هنا.

الاستخدام:
    from infra.authorization.registry.permissions import Perms
    if PermissionService.has_permission(user, Perms.USERS_VIEW):
        ...
"""


class Perms:
    """
    سجل الصلاحيات المركزي الشامل.
    كل صلاحية = ثابت يُمنع التكرار وأخطاء الإملاء.

    التنسيق: module.action.scope
    """

    # ══════════════════════════════════════════════════════════════
    # المستخدمين (users)
    # ══════════════════════════════════════════════════════════════
    USERS_VIEW = "users.view.all"
    USERS_CREATE = "users.create.all"
    USERS_UPDATE = "users.update.all"
    USERS_DELETE = "users.delete.all"
    USERS_RESET_PASSWORD = "users.reset_password.all"
    USERS_UNLOCK = "users.unlock.all"
    USERS_VIEW_SESSIONS = "users.view_sessions.all"

    # ══════════════════════════════════════════════════════════════
    # الأدوار والصلاحيات (roles)
    # ══════════════════════════════════════════════════════════════
    ROLES_VIEW = "roles.view.all"
    ROLES_CREATE = "roles.create.all"
    ROLES_UPDATE = "roles.update.all"
    ROLES_DELETE = "roles.delete.all"
    ROLES_ASSIGN = "roles.assign.all"

    # ══════════════════════════════════════════════════════════════
    # شؤون الأفراد (personnel)
    # ══════════════════════════════════════════════════════════════
    PERSONNEL_VIEW = "personnel.view.all"
    PERSONNEL_VIEW_OWN_DEPT = "personnel.view.department"
    PERSONNEL_VIEW_OWN_GOV = "personnel.view.governorate"
    PERSONNEL_CREATE = "personnel.create.all"
    PERSONNEL_EDIT = "personnel.edit.all"
    PERSONNEL_DELETE = "personnel.delete.all"
    PERSONNEL_IMPORT = "personnel.import.all"
    PERSONNEL_CHECK_NATIONAL_ID = "personnel.check_national_id.all"
    PERSONNEL_UPDATE_NATIONAL_ID = "personnel.update_national_id.all"
    # Field Permissions
    PERSONNEL_VIEW_SALARY = "personnel.view_salary.all"
    PERSONNEL_EDIT_SALARY = "personnel.edit_salary.all"
    PERSONNEL_VIEW_MILITARY_NUM = "personnel.view_military_number.all"
    PERSONNEL_EDIT_MILITARY_NUM = "personnel.edit_military_number.all"

    # ══════════════════════════════════════════════════════════════
    # التسويات (rank_settlement)
    # ══════════════════════════════════════════════════════════════
    RANK_SETTLEMENT_VIEW = "rank_settlement.view.all"
    RANK_SETTLEMENT_CREATE = "rank_settlement.create.all"
    RANK_SETTLEMENT_EDIT = "rank_settlement.edit.all"
    RANK_SETTLEMENT_DELETE = "rank_settlement.delete.all"
    RANK_SETTLEMENT_EXECUTE = "rank_settlement.execute.all"

    # ══════════════════════════════════════════════════════════════
    # التصحيحات المقترحة (corrections)
    # ══════════════════════════════════════════════════════════════
    CORRECTIONS_VIEW = "corrections.view.all"
    CORRECTIONS_REQUEST = "corrections.request.all"
    CORRECTIONS_APPROVE = "corrections.approve.all"
    CORRECTIONS_REJECT = "corrections.reject.all"

    # ══════════════════════════════════════════════════════════════
    # الكشوفات — تصدير واستيراد (sheets)
    # ══════════════════════════════════════════════════════════════
    SHEETS_EXPORT = "sheets.export.all"
    SHEETS_IMPORT = "sheets.import.all"

    # ══════════════════════════════════════════════════════════════
    # التغييرات المعلقة — المراجعة والاعتماد (staging)
    # ══════════════════════════════════════════════════════════════
    STAGING_VIEW = "staging.view.all"
    STAGING_REVIEW = "staging.review.all"
    STAGING_APPROVE = "staging.approve.all"
    STAGING_REJECT = "staging.reject.all"
    STAGING_BULK_APPROVE = "staging.bulk_approve.all"

    # ══════════════════════════════════════════════════════════════
    # المطابقة (reconciliation)
    # ══════════════════════════════════════════════════════════════
    RECONCILIATION_VIEW = "reconciliation.view.all"
    RECONCILIATION_CREATE = "reconciliation.create.all"
    RECONCILIATION_RESOLVE = "reconciliation.resolve.all"

    # ══════════════════════════════════════════════════════════════
    # إقفال الشهور (months)
    # ══════════════════════════════════════════════════════════════
    MONTHS_VIEW = "months.view.all"
    MONTHS_CLOSE = "months.close.all"
    MONTHS_OVERRIDE_LOCK = "months.override_lock.all"

    # ══════════════════════════════════════════════════════════════
    # التقارير (reports)
    # ══════════════════════════════════════════════════════════════
    REPORTS_VIEW = "reports.view.all"
    REPORTS_VIEW_OWN_DEPT = "reports.view.department"
    REPORTS_EXPORT = "reports.export.all"
    REPORTS_PRINT = "reports.print.all"
    REPORTS_GENERATE = "reports.generate.all"

    # ══════════════════════════════════════════════════════════════
    # التدقيق (audit)
    # ══════════════════════════════════════════════════════════════
    AUDIT_VIEW = "audit.view.all"
    AUDIT_EXPORT = "audit.export.all"
    AUDIT_VERIFY = "audit.verify.all"
    AUDIT_LOGIN_VIEW = "audit.login_view.all"

    # ══════════════════════════════════════════════════════════════
    # النظام والإعدادات (system / admin)
    # ══════════════════════════════════════════════════════════════
    SYSTEM_SETTINGS = "system.settings.all"
    SYSTEM_BACKUP = "system.backup.all"
    SYSTEM_TELEMETRY = "system.telemetry.all"
    ADMIN_MANAGE_USERS = "admin.manage_users.all"
    ADMIN_MANAGE_ROLES = "admin.manage_roles.all"
    ADMIN_MANAGE_DICTS = "admin.manage_dicts.all"
    ADMIN_MANAGE_SETTINGS = "admin.manage_settings.all"
    ADMIN_MANAGE_BACKUPS = "admin.manage_backups.all"

    # ══════════════════════════════════════════════════════════════
    # الملفات والمرفقات (storage)
    # ══════════════════════════════════════════════════════════════
    STORAGE_UPLOAD = "storage.upload.all"
    STORAGE_DELETE = "storage.delete.all"
    STORAGE_VIEW = "storage.view.all"
    STORAGE_REPLACE = "storage.replace.all"

    # ══════════════════════════════════════════════════════════════
    # التفويض المزدوج (dual_auth)
    # ══════════════════════════════════════════════════════════════
    DUAL_AUTH_VIEW = "dual_auth.view.all"
    DUAL_AUTH_APPROVE = "dual_auth.approve.all"

    # ══════════════════════════════════════════════════════════════
    # الأمن والمراقبة (security)
    # ══════════════════════════════════════════════════════════════
    SECURITY_DASHBOARD = "security.dashboard.all"
    SECURITY_SHADOW_TABLES = "security.shadow_tables.all"

    # ══════════════════════════════════════════════════════════════
    # Workflow / سير العمليات
    # ══════════════════════════════════════════════════════════════
    WORKFLOW_VIEW = "workflow.view.all"
    WORKFLOW_MANAGE = "workflow.manage.all"

    # ══════════════════════════════════════════════════════════════
    # الهيكل التنظيمي (organization)
    # ══════════════════════════════════════════════════════════════
    ORG_VIEW = "organization.view.all"
    ORG_CREATE = "organization.create.all"
    ORG_EDIT = "organization.edit.all"
    ORG_DELETE = "organization.delete.all"

    # ══════════════════════════════════════════════════════════════
    # القواميس والمعاجم (dictionaries)
    # ══════════════════════════════════════════════════════════════
    DICT_VIEW = "dictionaries.view.all"
    DICT_CREATE = "dictionaries.create.all"
    DICT_EDIT = "dictionaries.edit.all"
    DICT_DELETE = "dictionaries.delete.all"

    # ══════════════════════════════════════════════════════════════
    # البيانات الخام (raw_data)
    # ══════════════════════════════════════════════════════════════
    RAW_DATA_VIEW = "raw_data.view.all"
    RAW_DATA_IMPORT = "raw_data.import.all"

    # ══════════════════════════════════════════════════════════════
    # لوحة المعلومات (dashboard)
    # ══════════════════════════════════════════════════════════════
    DASHBOARD_VIEW = "dashboard.view.all"
    DASHBOARD_VIEW_OWN_DEPT = "dashboard.view.department"

    # ══════════════════════════════════════════════════════════════
    # Compliance / الالتزام
    # ══════════════════════════════════════════════════════════════
    COMPLIANCE_VIEW = "compliance.view.all"

    # ══════════════════════════════════════════════════════════════
    # Webhooks
    # ══════════════════════════════════════════════════════════════
    WEBHOOK_VIEW = "webhooks.view.all"
    WEBHOOK_MANAGE = "webhooks.manage.all"

    # ══════════════════════════════════════════════════════════════
    # الخدمات العامة (services) — legacy compatibility
    # ══════════════════════════════════════════════════════════════
    SERVICES_VIEW = "services.view.all"
    SERVICES_VIEW_OWN_DEPT = "services.view.department"
    SERVICES_CREATE = "services.create.all"
    SERVICES_EDIT = "services.edit.all"
    SERVICES_DELETE = "services.delete.all"
    SERVICES_APPROVE = "services.approve.all"
    SERVICES_REJECT = "services.reject.all"
    SERVICES_ESCALATE = "services.escalate.all"

    # ══════════════════════════════════════════════════════════════
    # التفويض (delegation)
    # ══════════════════════════════════════════════════════════════
    DELEGATION_VIEW = "delegation.view.all"
    DELEGATION_CREATE = "delegation.create.all"
    DELEGATION_REVOKE = "delegation.revoke.all"

    # ══════════════════════════════════════════════════════════════
    # الوصول الطارئ (emergency)
    # ══════════════════════════════════════════════════════════════
    EMERGENCY_VIEW = "emergency.view.all"
    EMERGENCY_GRANT = "emergency.grant.all"
    EMERGENCY_REVOKE = "emergency.revoke.all"
    EMERGENCY_REVIEW = "emergency.review.all"

    # ══════════════════════════════════════════════════════════════
    # السياسات (policies)
    # ══════════════════════════════════════════════════════════════
    POLICY_VIEW = "policy.view.all"
    POLICY_CREATE = "policy.create.all"
    POLICY_EDIT = "policy.edit.all"
    POLICY_DELETE = "policy.delete.all"

    # ══════════════════════════════════════════════════════════════
    # قيود السجلات (record_acl)
    # ══════════════════════════════════════════════════════════════
    RECORD_ACL_VIEW = "record_acl.view.all"
    RECORD_ACL_CREATE = "record_acl.create.all"
    RECORD_ACL_DELETE = "record_acl.delete.all"

    # ══════════════════════════════════════════════════════════════
    # السكرتارية (secretariat)
    # ══════════════════════════════════════════════════════════════
    SECRETARIAT_VIEW         = "secretariat.view.all"           # عرض كل المراسلات
    SECRETARIAT_VIEW_OWN     = "secretariat.view.own"           # عرض المراسلات المتعلقة بالمستخدم/قسمه
    SECRETARIAT_VIEW_CONFIDENTIAL = "secretariat.view.confidential" # عرض المراسلات السرية والسرية للغاية
    SECRETARIAT_CREATE       = "secretariat.create.all"         # إنشاء مراسلة
    SECRETARIAT_EDIT         = "secretariat.edit.all"           # تعديل مراسلة
    SECRETARIAT_DELETE       = "secretariat.delete.all"         # حذف مراسلة
    SECRETARIAT_TASK_MANAGE  = "secretariat.task.manage"        # إنشاء وإدارة التكليفات (السكرتارية)
    SECRETARIAT_TASK_EXECUTE = "secretariat.task.execute"       # استلام وإكمال التكليفات (الموظف المكلف)
    SECRETARIAT_COVER_LETTER = "secretariat.covering_letter.create"  # توليد خطاب تغطية الرد

    # ══════════════════════════════════════════════════════════════
    # الجزاءات والانضباط (disciplinary)
    # ══════════════════════════════════════════════════════════════
    DISCIPLINARY_VIEW = "disciplinary.view.all"
    DISCIPLINARY_CREATE = "disciplinary.create.all"
    DISCIPLINARY_EDIT = "disciplinary.edit.all"
    DISCIPLINARY_NOTIFY_MINISTRY = "disciplinary.notify_ministry.all"
    ABSENCE_VIEW = "absence.view.all"
    ABSENCE_CREATE = "absence.create.all"
    ABSENCE_CLOSE = "absence.close.all"
    VERDICT_VIEW = "verdict.view.all"
    VERDICT_CREATE = "verdict.create.all"
    VERDICT_EXECUTE = "verdict.execute.all"

    @classmethod
    def all_permissions(cls) -> list:
        """جميع الصلاحيات المُسجّلة."""
        return [
            v for k, v in vars(cls).items()
            if isinstance(v, str) and not k.startswith('_') and '.' in v
        ]

    @classmethod
    def get_module_permissions(cls, module: str) -> list:
        """صلاحيات نظام فرعي معين."""
        return [
            v for v in cls.all_permissions()
            if v.startswith(f"{module}.")
        ]


# ══════════════════════════════════════════════════════════════
# مجموعات الصلاحيات — لتنظيم العرض في Admin UI
# ══════════════════════════════════════════════════════════════
PERMISSION_GROUPS = {
    # code: (name, icon, display_order)
    'users': ('المستخدمين', 'users', 10),
    'roles': ('الأدوار والصلاحيات', 'shield', 20),
    'personnel': ('شؤون الأفراد', 'user-check', 30),
    'rank_settlement': ('التسويات', 'award', 40),
    'corrections': ('التصحيحات', 'edit-3', 50),
    'services': ('الخدمات', 'briefcase', 60),
    'sheets': ('الكشوفات', 'file-spreadsheet', 70),
    'staging': ('المراجعة والاعتماد', 'check-square', 80),
    'reconciliation': ('المطابقة', 'git-merge', 90),
    'months': ('إقفال الشهور', 'calendar', 100),
    'reports': ('التقارير', 'bar-chart-2', 110),
    'audit': ('التدقيق', 'eye', 120),
    'organization': ('الهيكل التنظيمي', 'git-branch', 130),
    'dictionaries': ('القواميس', 'book-open', 140),
    'storage': ('الملفات', 'hard-drive', 150),
    'security': ('الأمن', 'lock', 160),
    'dual_auth': ('التفويض المزدوج', 'user-plus', 170),
    'delegation': ('التفويض', 'repeat', 180),
    'emergency': ('الطوارئ', 'alert-triangle', 190),
    'policy': ('السياسات', 'sliders', 200),
    'record_acl': ('قيود السجلات', 'shield-off', 210),
    'dashboard': ('لوحة المعلومات', 'layout', 220),
    'system': ('النظام', 'settings', 230),
    'compliance': ('الالتزام', 'check-circle', 240),
    'raw_data': ('البيانات الخام', 'database', 250),
    'secretariat': ('السكرتارية', 'mail', 260),
    'disciplinary': ('الجزاءات والانضباط', 'alert-octagon', 270),
}


# ══════════════════════════════════════════════════════════════
# الحقول الحساسة — Field-Level Security
# ══════════════════════════════════════════════════════════════
FIELD_PERMISSIONS = {
    # (module, field_name): (label, view_permission, edit_permission, is_sensitive)
    ('personnel', 'salary'): (
        'الراتب', Perms.PERSONNEL_VIEW_SALARY, Perms.PERSONNEL_EDIT_SALARY, True,
    ),
    ('personnel', 'military_number'): (
        'الرقم العسكري', Perms.PERSONNEL_VIEW_MILITARY_NUM, Perms.PERSONNEL_EDIT_MILITARY_NUM, True,
    ),
}


# ══════════════════════════════════════════════════════════════
# Legacy Compatibility Mapping
# ══════════════════════════════════════════════════════════════
LEGACY_TO_NEW_MAPPING = {
    'view_personnel': 'personnel.view.all',
    'edit_personnel_basic': 'personnel.edit.all',
    'edit_personnel_status': 'personnel.edit.all',
    'delete_personnel': 'personnel.delete.all',
    'export_sheet': 'sheets.export.all',
    'import_sheet': 'sheets.import.all',
    'import_data': 'raw_data.import.all',
    'review_staging': 'staging.review.all',
    'approve_change': 'staging.approve.all',
    'reject_change': 'staging.reject.all',
    'create_reconciliation': 'reconciliation.create.all',
    'resolve_reconciliation': 'reconciliation.resolve.all',
    'close_month': 'months.close.all',
    'override_lock': 'months.override_lock.all',
    'view_audit_log': 'audit.view.all',
    'verify_audit_signatures': 'audit.verify.all',
    'view_reports': 'reports.view.all',
    'print_reports': 'reports.print.all',
    'export_reports': 'reports.export.all',
    'manage_users': 'admin.manage_users.all',
    'manage_roles': 'admin.manage_roles.all',
    'manage_dictionaries': 'admin.manage_dicts.all',
    'manage_settings': 'admin.manage_settings.all',
    'manage_backups': 'admin.manage_backups.all',
    'approve_dual_auth': 'dual_auth.approve.all',
    'view_dual_auth': 'dual_auth.view.all',
    'view_security_dashboard': 'security.dashboard.all',
    'view_shadow_tables': 'security.shadow_tables.all',
    'request_correction': 'corrections.request.all',
    'approve_correction': 'corrections.approve.all',
}


# ══════════════════════════════════════════════════════════════
# أسماء الشاشات بالعربي — يُستخدم في واجهة مصفوفة الصلاحيات
# ══════════════════════════════════════════════════════════════
SCREEN_LABELS = {
    'users': 'المستخدمين',
    'roles': 'المجموعات',
    'personnel': 'شؤون الأفراد',
    'rank_settlement': 'التسويات',
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
    'dual_auth': 'التفويض المزدوج',
    'security': 'الأمن والمراقبة',
    'workflow': 'سير العمليات',
    'organization': 'الهيكل التنظيمي',
    'dictionaries': 'القواميس',
    'raw_data': 'البيانات الخام',
    'dashboard': 'لوحة المعلومات',
    'compliance': 'الالتزام',
    'webhooks': 'الـ Webhooks',
    'services': 'الخدمات',
    'secretariat': 'السكرتارية',
    'disciplinary': 'الجزاءات والانضباط',
    'delegation': 'التفويض',
    'emergency': 'الوصول الطارئ',
    'policy': 'السياسات',
    'record_acl': 'قيود السجلات',
}

# ══════════════════════════════════════════════════════════════
# تصنيف الأفعال إلى أعمدة — يُستخدم في مصفوفة الصلاحيات
# ══════════════════════════════════════════════════════════════
def classify_permission(perm) -> str:
    """
    تصنيف الصلاحية باحترافية:
    - الصلاحيات الأساسية (عرض، إضافة، تعديل، حذف) تذهب للأعمدة الرئيسية فقط إذا كان النطاق all.
    - الصلاحيات المخصصة (عرض راتب، قسم معين، تغيير حالة فرعية) تذهب لعمود 'custom'.
    - العمليات التشغيلية (اعتماد، تصدير، إدارة) تذهب لأعمدتها الخاصة.
    """
    action = perm.action
    scope = perm.scope

    # 1. الصلاحيات الأساسية ذات النطاقات المخصصة (مثل view.department) تذهب لعمود مخصص
    core_actions = ['view', 'create', 'edit', 'update', 'delete', 'remove']
    if action in core_actions and scope != 'all':
        return 'custom'

    # 2. الصلاحيات الأساسية المطلقة
    if action == 'view': return 'view'
    if action in ['create', 'add', 'generate']: return 'create'
    if action in ['edit', 'update']: return 'edit'
    if action in ['delete', 'remove']: return 'delete'

    # 3. العمليات التشغيلية المنفصلة
    groups = {
        'approve': ['approve', 'reject', 'bulk_approve', 'review'],
        'export': ['export', 'print'],
        'manage': ['manage', 'settings', 'backup', 'manage_users', 'manage_roles', 'manage_dicts', 'manage_settings', 'manage_backups'],
        'execute': ['execute', 'escalate', 'verify', 'close', 'override_lock', 'resolve'],
        'import': ['import', 'upload'],
    }

    for category, actions in groups.items():
        if action in actions:
            return category

    # 4. أي شيء آخر يعتبر مخصصاً (مثل: view_salary, edit_military_number, reset_password)
    return 'custom'


# ══════════════════════════════════════════════════════════════
# الوصف العربي لكل صلاحية — يُستخدم عند الـ seed
# ══════════════════════════════════════════════════════════════
PERMISSION_LABELS = {
    # users
    'users.view.all': ('عرض المستخدمين', 'action'),
    'users.create.all': ('إنشاء مستخدم جديد', 'action'),
    'users.update.all': ('تعديل بيانات مستخدم', 'action'),
    'users.delete.all': ('حذف / تعطيل مستخدم', 'action'),
    'users.reset_password.all': ('إعادة تعيين كلمة المرور', 'action'),
    'users.unlock.all': ('فتح حساب مقفل', 'action'),
    'users.view_sessions.all': ('عرض جلسات المستخدمين', 'data'),
    # roles
    'roles.view.all': ('عرض الأدوار', 'action'),
    'roles.create.all': ('إنشاء دور', 'action'),
    'roles.update.all': ('تعديل دور', 'action'),
    'roles.delete.all': ('حذف / تعطيل دور', 'action'),
    'roles.assign.all': ('إسناد / إلغاء دور لمستخدم', 'action'),
    # personnel
    'personnel.view.all': ('عرض جميع الأفراد', 'data'),
    'personnel.view.department': ('عرض أفراد الإدارة فقط', 'data'),
    'personnel.view.governorate': ('عرض أفراد المحافظة فقط', 'data'),
    'personnel.create.all': ('إضافة فرد جديد', 'action'),
    'personnel.edit.all': ('تعديل بيانات فرد', 'action'),
    'personnel.delete.all': ('حذف فرد', 'action'),
    'personnel.import.all': ('استيراد أفراد من ملف', 'action'),
    'personnel.check_national_id.all': ('التحقق من الرقم الوطني', 'action'),
    'personnel.update_national_id.all': ('تحديث الرقم الوطني', 'action'),
    'personnel.view_salary.all': ('عرض الراتب', 'field'),
    'personnel.edit_salary.all': ('تعديل الراتب', 'field'),
    'personnel.view_military_number.all': ('عرض الرقم العسكري', 'field'),
    'personnel.edit_military_number.all': ('تعديل الرقم العسكري', 'field'),
    # rank_settlement
    'rank_settlement.view.all': ('عرض التسويات', 'action'),
    'rank_settlement.create.all': ('إنشاء تسوية رتبة', 'action'),
    'rank_settlement.edit.all': ('تعديل تسوية رتبة', 'action'),
    'rank_settlement.delete.all': ('حذف تسوية رتبة', 'action'),
    'rank_settlement.execute.all': ('تنفيذ تسوية رتبة', 'action'),
    # corrections
    'corrections.view.all': ('عرض التصحيحات', 'action'),
    'corrections.request.all': ('طلب تصحيح بيانات', 'action'),
    'corrections.approve.all': ('اعتماد تصحيح بيانات', 'action'),
    'corrections.reject.all': ('رفض تصحيح بيانات', 'action'),
    # sheets
    'sheets.export.all': ('تصدير كشوفات Excel', 'action'),
    'sheets.import.all': ('رفع كشوفات Excel', 'action'),
    # staging
    'staging.view.all': ('عرض التغييرات المعلقة', 'action'),
    'staging.review.all': ('مراجعة التغييرات المقترحة', 'action'),
    'staging.approve.all': ('اعتماد التغييرات', 'action'),
    'staging.reject.all': ('رفض التغييرات', 'action'),
    'staging.bulk_approve.all': ('اعتماد مجمّع للتغييرات', 'action'),
    # reconciliation
    'reconciliation.view.all': ('عرض مهام المطابقة', 'action'),
    'reconciliation.create.all': ('إنشاء مهمة مطابقة', 'action'),
    'reconciliation.resolve.all': ('حل اختلافات المطابقة', 'action'),
    # months
    'months.view.all': ('عرض اللقطات الشهرية', 'action'),
    'months.close.all': ('إقفال الشهر', 'action'),
    'months.override_lock.all': ('كسر إقفال الشهر', 'action'),
    # reports
    'reports.view.all': ('عرض التقارير', 'page'),
    'reports.view.department': ('عرض تقارير الإدارة فقط', 'data'),
    'reports.export.all': ('تصدير التقارير', 'action'),
    'reports.print.all': ('طباعة التقارير', 'action'),
    'reports.generate.all': ('إنشاء تقرير مخصص', 'action'),
    # audit
    'audit.view.all': ('عرض سجل التدقيق', 'page'),
    'audit.export.all': ('تصدير سجل التدقيق', 'action'),
    'audit.verify.all': ('التحقق من تواقيع التدقيق', 'action'),
    'audit.login_view.all': ('عرض سجل تسجيل الدخول', 'page'),
    # system / admin
    'system.settings.all': ('إدارة إعدادات النظام', 'action'),
    'system.backup.all': ('إنشاء نسخ احتياطية', 'action'),
    'system.telemetry.all': ('عرض مقاييس أداء النظام', 'page'),
    'admin.manage_users.all': ('إدارة المستخدمين (مدير)', 'page'),
    'admin.manage_roles.all': ('إدارة الأدوار (مدير)', 'page'),
    'admin.manage_dicts.all': ('إدارة القواميس والمعاجم', 'page'),
    'admin.manage_settings.all': ('إدارة إعدادات المدير', 'page'),
    'admin.manage_backups.all': ('إدارة النسخ الاحتياطية', 'page'),
    # storage
    'storage.upload.all': ('رفع ملفات ومرفقات', 'action'),
    'storage.delete.all': ('حذف ملفات ومرفقات', 'action'),
    'storage.view.all': ('عرض الملفات والمرفقات', 'action'),
    'storage.replace.all': ('استبدال ملف مرفق', 'action'),
    # dual_auth
    'dual_auth.view.all': ('عرض طلبات التفويض المزدوج', 'page'),
    'dual_auth.approve.all': ('الموافقة على طلبات التفويض المزدوج', 'action'),
    # security
    'security.dashboard.all': ('عرض لوحة الأمن', 'page'),
    'security.shadow_tables.all': ('عرض الجداول الاحتياطية', 'data'),
    # workflow
    'workflow.view.all': ('عرض سير العمليات', 'page'),
    'workflow.manage.all': ('إدارة سير العمليات', 'action'),
    # organization
    'organization.view.all': ('عرض الهيكل التنظيمي', 'page'),
    'organization.create.all': ('إضافة وحدة تنظيمية', 'action'),
    'organization.edit.all': ('تعديل الهيكل التنظيمي', 'action'),
    'organization.delete.all': ('حذف وحدة تنظيمية', 'action'),
    # dictionaries
    'dictionaries.view.all': ('عرض القواميس', 'page'),
    'dictionaries.create.all': ('إضافة عنصر قاموس', 'action'),
    'dictionaries.edit.all': ('تعديل عنصر قاموس', 'action'),
    'dictionaries.delete.all': ('حذف عنصر قاموس', 'action'),
    # raw_data
    'raw_data.view.all': ('عرض البيانات الخام', 'page'),
    'raw_data.import.all': ('استيراد بيانات خام', 'action'),
    # dashboard
    'dashboard.view.all': ('عرض لوحة المعلومات', 'page'),
    'dashboard.view.department': ('عرض لوحة معلومات الإدارة', 'page'),
    # compliance
    'compliance.view.all': ('عرض سجل الالتزام', 'page'),
    # webhooks
    'webhooks.view.all': ('عرض إعدادات الـ Webhooks', 'page'),
    'webhooks.manage.all': ('إدارة إعدادات الـ Webhooks', 'action'),
    # services (legacy)
    'services.view.all': ('عرض الخدمات', 'page'),
    'services.view.department': ('عرض خدمات الإدارة فقط', 'data'),
    'services.create.all': ('إنشاء خدمة', 'action'),
    'services.edit.all': ('تعديل خدمة', 'action'),
    'services.delete.all': ('حذف خدمة', 'action'),
    'services.approve.all': ('اعتماد خدمة', 'action'),
    'services.reject.all': ('رفض خدمة', 'action'),
    'services.escalate.all': ('تصعيد خدمة', 'action'),
    # secretariat
    'secretariat.view.all': ('عرض جميع المراسلات', 'page'),
    'secretariat.view.own': ('عرض المراسلات المُكلَّف بها فقط', 'data'),
    'secretariat.view.confidential': ('عرض المراسلات السرية والسرية للغاية', 'data'),
    'secretariat.create.all': ('إنشاء مراسلة جديدة', 'action'),
    'secretariat.edit.all': ('تعديل بيانات مراسلة', 'action'),
    'secretariat.delete.all': ('حذف مراسلة', 'action'),
    'secretariat.task.manage': ('إنشاء وإدارة التكليفات', 'action'),
    'secretariat.task.execute': ('استلام وإكمال التكليفات', 'action'),
    'secretariat.covering_letter.create': ('توليد خطاب تغطية الرد الصادر', 'action'),
}
