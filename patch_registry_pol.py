import re

file_path = "/home/mahdi/Desktop/POL/mahdi/Backend/systems/services/application/registries/form_registry.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update FormField
if "disabled: bool = False" not in content:
    content = content.replace(
        "    help_text: str = ''         # توضيح إضافي",
        "    help_text: str = ''         # توضيح إضافي\n    disabled: bool = False      # هل الحقل معطل\n    default: str = ''           # قيمة افتراضية"
    )

# 2. Update _field_dict
if "'disabled': getattr" not in content:
    content = content.replace(
        "                'help_text': f.help_text or None,",
        "                'help_text': f.help_text or None,\n                'disabled': getattr(f, 'disabled', False),\n                'default': getattr(f, 'default', ''),"
    )

# 3. Insert Category into fields=(
categories = {
    'retirement_age': 'كبار سن',
    'death': 'وفيات',
    'missing': 'مفقودين',
    'medical_unfit': 'عدم اللياقة الصحية',
    'end_of_service': 'إنهاء مدة',
    'retired': 'محال للتقاعد',
    'imprisoned': 'سجناء',
    'escort': 'المعيات',
    'martyr': 'الشهداء',
    'study_leave': 'مفرغين للدراسة',
    'seconded': 'المنتدبين'
}

for key, val in categories.items():
    if f"default='{val}'" not in content:
        pattern = r"('" + key + r"': FormDefinition\([\s\S]*?fields=\(\n)"
        replacement = r"\1            FormField('category', 'الفئة', 'text', required=True, disabled=True, default='" + val + "'),\n"
        content = re.sub(pattern, replacement, content)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("POL Registry Patched Successfully")
