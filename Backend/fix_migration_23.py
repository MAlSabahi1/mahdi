import os
import django
import sys
from django.db import connection

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

def fix_migration_23():
    with connection.cursor() as cursor:
        print("Dropping lingering tables from migration 0023 (if they exist)...")
        # CASCADE ensures any lingering constraints/indexes like unique_service_workflow_order are also dropped
        cursor.execute('DROP TABLE IF EXISTS services_service_workflow_step CASCADE;')
        cursor.execute('DROP TABLE IF EXISTS services_workflow_stage CASCADE;')
        
    print("✅ Cleanup complete! You can now run 'python manage.py migrate' again.")

if __name__ == "__main__":
    fix_migration_23()
