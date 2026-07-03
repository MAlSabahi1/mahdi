from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('security', '0002_shadow_tables'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            CREATE MATERIALIZED VIEW mv_personnel_snapshot AS
            SELECT DISTINCT ON (military_number) *
            FROM personnel_master_history
            ORDER BY military_number, history_version DESC;

            CREATE UNIQUE INDEX idx_mv_personnel_snapshot_military 
            ON mv_personnel_snapshot(military_number);
            """,
            reverse_sql="""
            DROP MATERIALIZED VIEW IF EXISTS mv_personnel_snapshot;
            """
        ),
    ]
