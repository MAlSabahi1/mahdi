import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.base")
django.setup()

from django.db import connection

with connection.cursor() as cursor:
    try:
        cursor.execute("ALTER TABLE authorization_user_role DROP COLUMN profile_id CASCADE;")
        print("Dropped profile_id from authorization_user_role")
    except Exception as e:
        print("Error:", e)
