#!/usr/bin/env python3
"""
Backend Architecture Restructuring Script
ينقل التطبيقات من الهيكل المسطح إلى platform/ + systems/ + extensions/
مع الحفاظ على app_label الأصلي لكل تطبيق (لا تغيير DB).
"""
import os
import shutil
import re
from pathlib import Path

BACKEND = Path("/home/mahdi/Desktop/POL/backend")

# ====================================================================
# خريطة النقل: (مصدر, وجهة, app_label_جديد_في_apps_py)
# ====================================================================
PLATFORM_APPS = [
    ("accounts",      "platform/accounts",      "accounts"),
    ("authorization", "platform/authorization",  "authorization"),
    ("audit",         "platform/audit",          "audit"),
    ("security",      "platform/security",       "security"),
    ("storage",       "platform/storage",        "storage"),
    ("workflows",     "platform/workflows",      "workflows"),
]

SYSTEMS_APPS = [
    ("personnel", "systems/personnel", "personnel"),
]

EXTENSIONS = [
    # webhooks سينتقل لاحقاً
]

# ====================================================================
# الاستيرادات القديمة → الجديدة
# ====================================================================
IMPORT_REPLACEMENTS = {
    # platform apps
    "from accounts.":      "from infra.accounts.",
    "import accounts.":    "import infra.accounts.",
    "from authorization.": "from infra.authorization.",
    "import authorization.": "import infra.authorization.",
    "from audit.":         "from infra.audit.",
    "import audit.":       "import infra.audit.",
    "from security.":      "from infra.security.",
    "import security.":    "import infra.security.",
    "from storage.":       "from infra.storage.",
    "import storage.":     "import infra.storage.",
    "from workflows.":     "from infra.workflows.",
    "import workflows.":   "import infra.workflows.",
    # systems
    "from systems.personnel.":     "from systems.personnel.",
    "import personnel.":   "import systems.personnel.",
    # hrms config
    "from hrms.":          "from config.",
    "import hrms.":        "import config.",
    "'hrms.":              "'config.",
    '"hrms.':              '"config.',
}

# ملفات/مجلدات لا نلمسها
SKIP_DIRS = {"__pycache__", ".pytest_cache", "migrations", "shared", "systems", "extensions", "config", "platform"}
SKIP_FILES = {"manage.py"}


def copy_app(src_name: str, dst_path: str, label: str):
    """ينقل تطبيق كامل من src → dst."""
    src = BACKEND / src_name
    dst = BACKEND / dst_path

    if not src.exists():
        print(f"  ⚠️  المصدر غير موجود: {src}")
        return False

    # إنشاء مجلد الوجهة
    dst.mkdir(parents=True, exist_ok=True)

    # نسخ جميع الملفات
    copied = 0
    for item in src.iterdir():
        dst_item = dst / item.name
        if item.is_dir():
            if item.name not in {"__pycache__", ".pytest_cache"}:
                if dst_item.exists():
                    shutil.copytree(item, dst_item, dirs_exist_ok=True,
                                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
                else:
                    shutil.copytree(item, dst_item,
                                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
                copied += 1
        elif item.name.endswith(".py") and item.name != "__pycache__":
            shutil.copy2(item, dst_item)
            copied += 1

    print(f"  ✅ نُقل {src_name} → {dst_path} ({copied} عنصر)")
    return True


def ensure_init(path: Path):
    """يضمن وجود __init__.py في كل مجلد."""
    (path / "__init__.py").touch(exist_ok=True)


def create_platform_structure():
    """ينشئ هيكل platform/"""
    platform = BACKEND / "platform"
    platform.mkdir(exist_ok=True)
    ensure_init(platform)
    print("✅ platform/ تم إنشاؤه")


def update_apps_py(dst_path: str, new_name: str, label: str):
    """يحدّث apps.py بمسار Python الجديد مع الحفاظ على label."""
    apps_file = BACKEND / dst_path / "apps.py"
    if not apps_file.exists():
        print(f"  ⚠️  apps.py غير موجود في {dst_path}")
        return

    content = apps_file.read_text()

    # استبدال name = 'old' بـ name = 'new' + label
    old_name = new_name.split("/")[-1].replace("/", ".")
    new_module_name = dst_path.replace("/", ".")

    # تحديث name
    content = re.sub(
        r"name\s*=\s*['\"]" + re.escape(old_name) + r"['\"]",
        f"name = '{new_module_name}'",
        content
    )
    # تحديث name إذا لم يكن محدداً بالقديم
    content = re.sub(
        r"(class \w+Config\(AppConfig\):.*?\n(?:.*\n)*?)\s*(name\s*=\s*['\"](?!platform|systems|extensions)[^'\"]+['\"])",
        lambda m: m.group(0).replace(
            re.search(r"name\s*=\s*['\"][^'\"]+['\"]", m.group(0)).group(),
            f"name = '{new_module_name}'"
        ),
        content,
        flags=re.MULTILINE
    )

    # إضافة label إذا لم يكن موجوداً
    if f"label = '{label}'" not in content and f'label = "{label}"' not in content:
        content = content.replace(
            f"name = '{new_module_name}'",
            f"name = '{new_module_name}'\n    label = '{label}'"
        )

    apps_file.write_text(content)
    print(f"  ✅ apps.py محدَّث: {dst_path}")


def update_imports_in_file(filepath: Path, replacements: dict) -> int:
    """يحدث استيرادات ملف واحد. يرجع عدد التغييرات."""
    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception:
        return 0

    original = content
    for old, new in replacements.items():
        content = content.replace(old, new)

    if content != original:
        filepath.write_text(content, encoding="utf-8")
        return content.count("platform.") - original.count("platform.")  # rough count
    return 0


def update_all_imports(base_dirs: list, replacements: dict):
    """يحدث جميع الاستيرادات في المجلدات المحددة."""
    total = 0
    for base_dir in base_dirs:
        base = BACKEND / base_dir
        if not base.exists():
            continue
        for filepath in base.rglob("*.py"):
            if "__pycache__" in str(filepath):
                continue
            changes = update_imports_in_file(filepath, replacements)
            if changes:
                total += 1
    print(f"  ✅ تم تحديث الاستيرادات في {total} ملف")


def update_settings():
    """يحدّث INSTALLED_APPS في config/settings/base.py"""
    settings_file = BACKEND / "config" / "settings" / "base.py"
    hrms_settings = BACKEND / "hrms" / "settings.py"

    if not settings_file.exists():
        print("  ⚠️  config/settings/base.py غير موجود")
        return

    # قراءة settings الحالي من hrms
    hrms_content = hrms_settings.read_text() if hrms_settings.exists() else ""

    # قراءة base.py الحالي
    base_content = settings_file.read_text()

    # تحديث INSTALLED_APPS
    new_installed_apps = """INSTALLED_APPS = [
    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',

    # Third party
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'django_fsm',
    'guardian',
    'django_filters',
    'drf_spectacular',
    'django_celery_results',
    'simple_history',

    # Platform — البنية التحتية المشتركة
    'infra.accounts.apps.AccountsConfig',
    'infra.authorization.apps.AuthorizationConfig',
    'infra.audit.apps.AuditConfig',
    'infra.security.apps.SecurityConfig',
    'infra.storage.apps.StorageConfig',
    'infra.workflows.apps.WorkflowsConfig',

    # Core — البيانات المرجعية
    'core.apps.CoreConfig',

    # Systems — الأنظمة التشغيلية
    'systems.personnel.apps.PersonnelConfig',

    # Services (مؤقتاً حتى التقسيم الكامل)
    'services.apps.ServicesConfig',

    # Extensions
    'extensions.webhooks',
]"""

    # استبدال INSTALLED_APPS القديم
    if "INSTALLED_APPS" in base_content:
        base_content = re.sub(
            r"INSTALLED_APPS\s*=\s*\[.*?\]",
            new_installed_apps,
            base_content,
            flags=re.DOTALL
        )
    else:
        base_content += "\n\n" + new_installed_apps

    settings_file.write_text(base_content)
    print("  ✅ INSTALLED_APPS محدَّث في config/settings/base.py")


def update_manage_py():
    """يحدّث manage.py لاستخدام config.settings"""
    manage = BACKEND / "manage.py"
    content = manage.read_text()
    content = content.replace(
        "os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hrms.settings')",
        "os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')"
    )
    manage.write_text(content)
    print("  ✅ manage.py محدَّث → config.settings.base")


def update_root_urlconf():
    """يحدّث ROOT_URLCONF في settings"""
    settings_file = BACKEND / "config" / "settings" / "base.py"
    content = settings_file.read_text()
    content = content.replace("ROOT_URLCONF = 'hrms.urls'", "ROOT_URLCONF = 'config.urls'")
    if "ROOT_URLCONF" not in content:
        content += "\nROOT_URLCONF = 'config.urls'\n"
    settings_file.write_text(content)
    print("  ✅ ROOT_URLCONF محدَّث → config.urls")


def create_extensions_webhooks():
    """ينشئ extensions/webhooks/"""
    ext = BACKEND / "extensions"
    wb = ext / "webhooks"
    wb.mkdir(parents=True, exist_ok=True)
    ensure_init(ext)
    ensure_init(wb)

    # نسخ webhooks.py
    src = BACKEND / "services" / "webhooks.py"
    if src.exists():
        shutil.copy2(src, wb / "webhooks.py")
        # إنشاء apps.py بسيط
        (wb / "apps.py").write_text("""from django.apps import AppConfig

class WebhooksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'extensions.webhooks'
    label = 'webhooks'
    verbose_name = 'الويب هوكس'
""")
        print("  ✅ extensions/webhooks/ تم إنشاؤه")


def main():
    print("=" * 60)
    print("🏗️  بدء إعادة الهيكلة المعمارية للباك اند")
    print("=" * 60)

    # المرحلة 1: platform/
    print("\n📦 المرحلة 1: إنشاء platform/")
    create_platform_structure()
    for src, dst, label in PLATFORM_APPS:
        print(f"\n  → {src} → {dst}")
        copy_app(src, dst, label)
        update_apps_py(dst, dst, label)

    # المرحلة 2: systems/personnel/
    print("\n📦 المرحلة 2: systems/personnel/")
    # personnel/ الجذر موجود والأفضل منه systems/personnel/ (30 migration)
    # نسخ من personnel/ القديم ما هو ناقص في systems/personnel/
    src_personnel = BACKEND / "personnel"
    dst_personnel = BACKEND / "systems" / "personnel"
    dst_personnel.mkdir(parents=True, exist_ok=True)
    ensure_init(BACKEND / "systems")
    ensure_init(dst_personnel)

    for item in src_personnel.iterdir():
        dst_item = dst_personnel / item.name
        if item.name in {"__pycache__", ".pytest_cache"}:
            continue
        if not dst_item.exists():
            if item.is_dir():
                shutil.copytree(item, dst_item,
                                ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            else:
                shutil.copy2(item, dst_item)
    print("  ✅ systems/personnel/ مكتمل")
    update_apps_py("systems/personnel", "systems/personnel", "personnel")

    # المرحلة 3: extensions/webhooks/
    print("\n📦 المرحلة 3: extensions/webhooks/")
    create_extensions_webhooks()

    # المرحلة 4: تحديث الاستيرادات
    print("\n📦 المرحلة 4: تحديث الاستيرادات")
    dirs_to_update = [
        "platform", "systems", "extensions", "config",
        "core", "services",
        # لا نحدث المجلدات القديمة (accounts/ etc) لأنها ستُحذف لاحقاً
    ]
    update_all_imports(dirs_to_update, IMPORT_REPLACEMENTS)

    # المرحلة 5: الإعدادات
    print("\n📦 المرحلة 5: تحديث الإعدادات")
    update_settings()
    update_manage_py()
    update_root_urlconf()

    print("\n" + "=" * 60)
    print("✅ اكتملت عملية إعادة الهيكلة!")
    print("=" * 60)
    print("\nالخطوات التالية:")
    print("  1. تشغيل Docker: docker-compose up -d db redis")
    print("  2. تشغيل: python manage.py check")
    print("  3. تشغيل: python manage.py migrate")
    print("  4. حذف المجلدات القديمة بعد التحقق")


if __name__ == "__main__":
    main()
