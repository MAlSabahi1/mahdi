import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()
from core.models.personnel_refs import Rank
for r in Rank.objects.all().order_by('order'):
    print(f"'{r.name}',")
