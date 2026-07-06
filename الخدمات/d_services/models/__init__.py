import os
import importlib

# استيراد جميع الملفات داخل المجلد الحالي
for module in os.listdir(os.path.dirname(__file__)):
    if module.endswith('.py') and module != '__init__.py':
        importlib.import_module(f'{__name__}.{module[:-3]}')
