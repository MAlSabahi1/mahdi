from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('personnel', '0007_personnelmaster_category_and_more'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            ALTER TABLE personnel_master 
            ADD CONSTRAINT chk_min_age 
            CHECK (join_date >= birth_date + INTERVAL '18 years');
            """,
            reverse_sql="""
            ALTER TABLE personnel_master 
            DROP CONSTRAINT IF EXISTS chk_min_age;
            """
        )
    ]
