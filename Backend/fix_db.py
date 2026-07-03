import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.base")
django.setup()
from django.db import connection
with connection.cursor() as cursor:
    cursor.execute("ALTER TABLE authorization_role DROP COLUMN IF EXISTS permissions;")
print("Dropped permissions column")
