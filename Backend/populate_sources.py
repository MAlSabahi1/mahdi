import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from systems.reports.models import ReportDataSource

sources = [
    {"name": "البيانات الأساسية للقوة العاملة", "model_name": "personnel.PersonnelMaster", "description": "يحتوي على كافة بيانات الأفراد الأساسية"},
    {"name": "حركات الغياب والإيقاف", "model_name": "personnel.Movement", "description": "تتبع حركات الإيقاف والغياب والانتداب"}
]

for s in sources:
    ReportDataSource.objects.get_or_create(model_name=s["model_name"], defaults=s)

print("Data sources populated.")
