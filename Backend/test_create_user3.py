import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.base")
django.setup()

from infra.accounts.services.user_service import UserService
from infra.authorization.services.role_service import RoleService

try:
    user = UserService.create_user(
        username="test_admin_user",
        password="StrongPassword123!",
        full_name="test admin",
        email="test_admin@example.com",
    )
    print("USER CREATED:", user.id)
    
    # Try assigning role 1
    RoleService.assign_role_to_user(
        user_id=str(user.id),
        role_id=1,
    )
    print("ROLE ASSIGNED!")
except Exception as e:
    print("EXCEPTION:", getattr(e, 'message', str(e)))
