import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from systems.services.api.serializers.disciplinary_serializers import DisciplinaryActionCreateSerializer

serializer = DisciplinaryActionCreateSerializer(data={
    "personnel": "6099999",
    "action_type": "military_detention",
    "source_type": "direct_superior",
    "issued_by_name": "Test",
    "decision_ref": "123",
    "issued_date": "2026-07-12",
    "effective_date": "2026-07-12",
    "duration_days": None,
    "description": "Test"
})
print("Valid:", serializer.is_valid())
print("Errors:", serializer.errors)
