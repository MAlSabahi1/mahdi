import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from systems.services.service_rules.core import ServiceRulesDispatcher, ServiceValidationContext
from systems.personnel.models import PersonnelMaster
p = PersonnelMaster.objects.first()
ctx = ServiceRulesDispatcher.validate(
    personnel=p,
    service_code='SECONDED_FORM',
    form_data={'start_date': '2023-01-01', 'end_date': '2024-01-01'},
    uploaded_attachments=['secondment_order']
)
print(ctx.to_response_dict())
