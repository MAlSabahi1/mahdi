from django.contrib.auth import get_user_model
from core.models.organization import SecurityAdministration
from infra.authorization.models.role import Role
from infra.authorization.models.user_profile import UserProfile

User = get_user_model()

marib_sa = SecurityAdministration.objects.filter(name__icontains='مأرب').first()
if not marib_sa:
    print("Error: Could not find SecurityAdministration for Marib (مأرب).")
else:
    role = Role.objects.filter(name__icontains='محافظة').first()
    if not role:
        role = Role.objects.filter(code='gov_admin').first()
        if not role:
            role = Role.objects.create(code='gov_admin', name='مدير أمن محافظة', is_active=True)
            print("Created new role: gov_admin")

    username = 'marib_admin'
    password = 'Password123!'
    user, created = User.objects.get_or_create(username=username)
    user.set_password(password)
    user.first_name = 'مدير'
    user.last_name = 'أمن مأرب'
    user.is_active = True
    user.save()
    if created:
        print(f"Created user: {username}")
    else:
        print(f"Updated existing user: {username}")

    profile, p_created = UserProfile.objects.get_or_create(user=user, defaults={
        'role': role,
        'security_admin': marib_sa
    })
    
    if not p_created:
        profile.role = role
        profile.security_admin = marib_sa
        profile.save()
        print(f"Updated profile for {username}")
    else:
        print(f"Created profile for {username}")

    print(f"\n--- SUCCESS ---")
    print(f"Username: {username}")
    print(f"Password: {password}")
    print(f"Security Admin: {marib_sa.name}")
    print(f"Role: {role.name}")
