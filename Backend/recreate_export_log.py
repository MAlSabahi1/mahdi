import os
import sys
import django

# Add the project root to the python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from django.db import connection
from systems.services.models import ExportLog

try:
    with connection.schema_editor() as schema_editor:
        schema_editor.create_model(ExportLog)
    print("Table for ExportLog ('services_export_log') created successfully and committed!")
except Exception as e:
    print(f"Error creating ExportLog table: {e}")
