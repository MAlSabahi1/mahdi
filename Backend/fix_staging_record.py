import os
import django
import sys

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from django.db import connection
from django.db.migrations.executor import MigrationExecutor

def recreate_missing_staging_record():
    print("Loading migration state...")
    executor = MigrationExecutor(connection)
    
    # We need the exact schema of StagingRecord just before 0033
    target_migration = ('services', '0032_bidatasource_alter_servicecatalog_execution_action_and_more')
    
    print("Extracting model schema for StagingRecord at migration 0032...")
    project_state = executor.loader.project_state([target_migration])
    OldStagingRecord = project_state.apps.get_model('services', 'StagingRecord')
    
    print("Creating the missing table in the database...")
    with connection.schema_editor() as schema_editor:
        try:
            schema_editor.create_model(OldStagingRecord)
            print("✅ Table 'services_staging_record' successfully recreated!")
        except Exception as e:
            print(f"❌ Failed to create table: {e}")

if __name__ == "__main__":
    recreate_missing_staging_record()
