import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from systems.personnel.models import PersonnelMaster
from infra.authorization.services.permission_service import PermissionService

User = get_user_model()
user = User.objects.get(username='marib_admin')

print("Direct filter:")
qs1 = PersonnelMaster.objects.filter(security_admin=user.authz_profile.security_admin)
print(f"Direct Count: {qs1.count()}")

print("\nPermissionService.get_scoped_queryset:")
qs2 = PermissionService.get_scoped_queryset(user, PersonnelMaster.objects.all(), 'personnel.view.*')
print(f"Scoped Count: {qs2.count()}")

print("\nWhat does profile.get_accessible_security_admin_ids() return?")
print(user.authz_profile.get_accessible_security_admin_ids())

print("\nCheck what parts[2] is:")
print('personnel.view.*'.split('.')[2])

