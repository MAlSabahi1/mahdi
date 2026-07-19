import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from systems.personnel.models import PersonnelMaster
from systems.services.models import StatusChangeForm

qs = PersonnelMaster.objects.select_related(
    'current_rank', 'qualification', 'security_admin',
    'central_department', 'branch', 'district_police',
    'position', 'job_title', 'category', 'current_status',
    'force_classification'
)

print(f"Total: {qs.count()}")
try:
    for p in qs:
        pass
    print("Queryset iteration successful!")
except Exception as e:
    import traceback
    traceback.print_exc()

