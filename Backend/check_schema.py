import os
import django
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.base")
django.setup()

from systems.services.models import ServiceCatalog

for s in ServiceCatalog.objects.filter(name_ar__icontains="شهيد"):
    print(s.name_ar)
    print(json.dumps(s.fields_schema, indent=2, ensure_ascii=False))
