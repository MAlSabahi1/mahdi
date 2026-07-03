import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.base")
django.setup()

from infra.accounts.serializers.user_serializers import UserCreateSerializer

data = {
    "username": "ahmed.mohamed",
    "email": "ahmed@example.com",
    "password": "password123",
    "full_name": "ahmed mohamed",
    "role_id": 1,
    "first_name": "ahmed",
    "last_name": "mohamed"
}

serializer = UserCreateSerializer(data=data)
if not serializer.is_valid():
    print("ERRORS:", serializer.errors)
else:
    print("VALID:", serializer.validated_data)
