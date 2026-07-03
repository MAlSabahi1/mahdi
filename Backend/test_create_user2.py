import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.base")
django.setup()

from infra.accounts.services.user_service import UserService

try:
    user = UserService.create_user(
        username="test_new_user",
        password="password123",
        full_name="test user",
        email="test@example.com",
    )
    print("USER CREATED:", user)
except Exception as e:
    print("EXCEPTION:", getattr(e, 'message', str(e)))
