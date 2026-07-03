import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.base")
django.setup()
from django.db import connection
from infra.authorization.models import Role

with connection.cursor() as cursor:
    cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name='authorization_role';")
    db_columns = [row[0] for row in cursor.fetchall()]

django_columns = [f.column for f in Role._meta.local_fields]

with connection.cursor() as cursor:
    for col in db_columns:
        if col not in django_columns:
            print(f"Dropping obsolete column: {col}")
            cursor.execute(f"ALTER TABLE authorization_role DROP COLUMN IF EXISTS {col};")

print("Done dropping obsolete columns.")
