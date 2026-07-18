import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from systems.personnel.models import SuggestedCorrection
from systems.personnel.api.serializers.main_serializers import SuggestedCorrectionSerializer

c = SuggestedCorrection.objects.last()
if c:
    print(f"Correction ID: {c.id}")
    print(f"is_printed in DB: {c.is_printed}")
    data = SuggestedCorrectionSerializer(c).data
    print(f"is_printed in Serializer: {data.get('is_printed', 'NOT FOUND')}")
else:
    print("No correction found")
