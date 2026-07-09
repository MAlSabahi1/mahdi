import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.base")
django.setup()

from core.models.personnel_refs import JobCategory

categories = ["إدارية", "ميدانية", "فنية", "تخصصية", "حرفية"]

for index, name in enumerate(categories):
    JobCategory.objects.filter(name=name).update(sort_order=index + 1)
    
print("Updated sort orders successfully.")
