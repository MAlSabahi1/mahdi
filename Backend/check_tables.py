import os
import django
from django.db import connection
import sys

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Use 'config.settings' instead of 'mahdi.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

tables = connection.introspection.table_names()
print("Tables related to status_change:")
for t in tables:
    if 'status' in t.lower():
        print(" -", t)
