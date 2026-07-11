import os
import django
import sys

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from django.db import connection
from django.db.migrations.executor import MigrationExecutor

def recreate_missing_table():
    print("Loading migration state...")
    executor = MigrationExecutor(connection)
    
    # We need to get the exact schema of StatusChangeForm as it was right after migration 0021
    # This prevents creating columns from 0022 which would cause the migrate command to fail later
    target_migration = ('services', '0021_disciplinaryaction_absencerecord_and_more')
    
    print("Extracting model schema for StatusChangeForm at migration 0021...")
    project_state = executor.loader.project_state([target_migration])
    OldStatusChangeForm = project_state.apps.get_model('services', 'StatusChangeForm')
    
    print("Creating the missing table in the database...")
    with connection.schema_editor() as schema_editor:
        try:
            schema_editor.create_model(OldStatusChangeForm)
            print("✅ Table 'services_status_change_form' successfully recreated!")
        except Exception as e:
            print(f"❌ Failed to create table: {e}")

if __name__ == "__main__":
    recreate_missing_table()
