import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from systems.services.infrastructure.models.reports_bi import BIDataSource

sources = [
    {
        "name": "البيانات الأساسية للقوة العاملة", 
        "source_type": "orm_model", 
        "target": "personnel.PersonnelMaster", 
        "description": "يحتوي على كافة بيانات الأفراد الأساسية"
    },
    {
        "name": "حركات الغياب والإيقاف", 
        "source_type": "orm_model", 
        "target": "personnel.Movement", 
        "description": "تتبع حركات الإيقاف والغياب والانتداب"
    }
]

for s in sources:
    BIDataSource.objects.get_or_create(target=s["target"], defaults=s)

print("BI Data sources populated.")
