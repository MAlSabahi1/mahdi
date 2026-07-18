import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from django.test import Client
from systems.personnel.models import SuggestedCorrection

# Get the correction
try:
    corr = SuggestedCorrection.objects.get(id=17)
    print(f"Before: is_printed = {corr.is_printed}")

    c = Client()
    # We need to authenticate, but for now let's just call the view directly if possible, 
    # or print the URL resolver match.
    
    response = c.post('/api/v1/personnel/corrections/17/mark_printed/')
    print(f"Response status: {response.status_code}")
    if response.status_code != 200:
        print(f"Response body: {response.content}")

    corr.refresh_from_db()
    print(f"After: is_printed = {corr.is_printed}")

except Exception as e:
    print(f"Error: {e}")
