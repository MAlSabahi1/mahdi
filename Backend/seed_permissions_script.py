import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.base")
django.setup()

from infra.authorization.models.permission import Permission

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

actions = [
    ('read', 'عرض وقراءة'),
    ('write', 'إضافة وتعديل'),
    ('delete', 'حذف'),
    ('export', 'تصدير بيانات'),
    ('approve', 'مراجعة واعتماد'),
    ('manage', 'إدارة كاملة')
]

scope = 'global'

permissions_to_create = []

for mod_code, mod_label in modules.items():
    for act_code, act_label in actions:
        code = f"{mod_code.upper()}.{act_code.upper()}.{scope.upper()}"
        label = f"{act_label} - {mod_label}"
        
        requires_dual = False
        if act_code in ['delete', 'approve', 'manage']:
            requires_dual = True
            
        is_system = False
        if mod_code in ['system', 'security', 'admin']:
            is_system = True

        permissions_to_create.append(
            Permission(
                code=code,
                module=mod_code,
                action=act_code,
                scope=scope,
                label=label,
                category=mod_label,
                is_active=True,
                is_system=is_system,
                requires_dual_auth=requires_dual
            )
        )

Permission.objects.bulk_create(permissions_to_create, ignore_conflicts=True)
print(f"Successfully seeded {len(permissions_to_create)} permissions!")
