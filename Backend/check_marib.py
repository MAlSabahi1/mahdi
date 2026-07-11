from django.contrib.auth import get_user_model
from core.models.organization import SecurityAdministration
from systems.personnel.models import PersonnelMaster
from infra.authorization.services.permission_service import PermissionService

User = get_user_model()
user = User.objects.get(username='marib_admin')

print(f"User: {user.username}")
profile = user.authz_profile
print(f"Profile Security Admin: {profile.security_admin.name if profile.security_admin else 'None'}")

sa_ids = profile.get_accessible_security_admin_ids()
print(f"Accessible SA IDs: {sa_ids}")

marib_personnel_count = PersonnelMaster.objects.filter(security_admin_id__in=sa_ids).count()
print(f"Personnel in Marib SA: {marib_personnel_count}")

total_personnel = PersonnelMaster.objects.count()
print(f"Total Personnel in DB: {total_personnel}")

perms = PermissionService.get_user_permissions(user)
print(f"User Permissions: {len(perms)} perms found")
if not perms:
    print("WARNING: User has no permissions! Maybe the role 'gov_admin' has no permissions assigned in DB.")

# Let's check role permissions
role = profile.role
role_perms = role.permissions.all()
print(f"Role '{role.name}' has {role_perms.count()} permissions.")
