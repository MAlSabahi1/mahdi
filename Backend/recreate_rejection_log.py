import os
import sys
import django

# Add the project root to the python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')

django.setup()

from django.db import connection, transaction
from systems.services.models import RejectionLog, ExportLog

try:
    with connection.schema_editor() as schema_editor:
        try:
            with transaction.atomic():
                schema_editor.create_model(RejectionLog)
            print("Table for RejectionLog ('services_rejection_log') created successfully!")
        except Exception as e:
            print(f"Error creating RejectionLog table (it might already exist): {e}")
        
        try:
            with transaction.atomic():
                schema_editor.create_model(ExportLog)
            print("Table for ExportLog ('services_export_log') created successfully!")
        except Exception as e:
            print(f"Error creating ExportLog table (it might already exist): {e}")

except Exception as e:
    print(f"Error connecting to schema editor: {e}")
