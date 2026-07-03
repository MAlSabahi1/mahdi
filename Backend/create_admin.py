import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.base")
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

if not User.objects.filter(username="admin").exists():
    user = User.objects.create_superuser("admin", "admin@example.com", "admin123")
    user.is_staff = True
    user.save()
    print("Admin user created successfully! Username: admin | Password: admin123")
else:
    # Update password just in case
    u = User.objects.get(username="admin")
    u.set_password("admin123")
    u.is_staff = True
    u.save()
    print("Admin user already existed. Password reset to: admin123 and is_staff set to True")

