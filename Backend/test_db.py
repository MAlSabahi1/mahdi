import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.base")
django.setup()

from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'authorization_user_role';")
    for row in cursor.fetchall():
        print(row)
