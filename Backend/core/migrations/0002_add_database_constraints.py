"""
إضافة قيود ومشغلات على مستوى قاعدة البيانات
"""
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0001_initial'),
        ('personnel', '0001_initial'),
    ]

    operations = [
        # تفعيل pgcrypto للتشفير
        migrations.RunSQL(
            sql="CREATE EXTENSION IF NOT EXISTS pgcrypto;",
            reverse_sql="DROP EXTENSION IF EXISTS pgcrypto;"
        ),
        
        # CHECK constraint للرقم العسكري
        migrations.RunSQL(
            sql="""
            ALTER TABLE personnel_master 
            ADD CONSTRAINT check_military_number_format 
            CHECK (military_number ~ '^[0-9]{7}$');
            """,
            reverse_sql="""
            ALTER TABLE personnel_master 
            DROP CONSTRAINT IF EXISTS check_military_number_format;
            """
        ),
        
        # CHECK constraint للرقم الوطني
        migrations.RunSQL(
            sql="""
            ALTER TABLE personnel_master 
            ADD CONSTRAINT check_national_id_format 
            CHECK (national_id ~ '^[0-9]{11}$');
            """,
            reverse_sql="""
            ALTER TABLE personnel_master 
            DROP CONSTRAINT IF EXISTS check_national_id_format;
            """
        ),
        
        # Trigger لمنع تحديث military_number مباشرة
        migrations.RunSQL(
            sql="""
            CREATE OR REPLACE FUNCTION prevent_military_number_update()
            RETURNS TRIGGER AS $$
            BEGIN
                IF OLD.military_number != NEW.military_number THEN
                    RAISE EXCEPTION 'لا يمكن تحديث الرقم العسكري مباشرة';
                END IF;
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
            
            CREATE TRIGGER trigger_prevent_military_number_update
            BEFORE UPDATE ON personnel_master
            FOR EACH ROW
            EXECUTE FUNCTION prevent_military_number_update();
            """,
            reverse_sql="""
            DROP TRIGGER IF EXISTS trigger_prevent_military_number_update 
            ON personnel_master;
            DROP FUNCTION IF EXISTS prevent_military_number_update();
            """
        ),
        
        # Trigger لتحديث is_complete تلقائياً
        migrations.RunSQL(
            sql="""
            CREATE OR REPLACE FUNCTION update_is_complete()
            RETURNS TRIGGER AS $$
            BEGIN
                NEW.is_complete := (
                    NEW.photo IS NOT NULL AND 
                    NEW.fingerprint_hash IS NOT NULL AND 
                    NEW.national_id IS NOT NULL
                );
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
            
            CREATE TRIGGER trigger_update_is_complete
            BEFORE INSERT OR UPDATE ON personnel_master
            FOR EACH ROW
            EXECUTE FUNCTION update_is_complete();
            """,
            reverse_sql="""
            DROP TRIGGER IF EXISTS trigger_update_is_complete 
            ON personnel_master;
            DROP FUNCTION IF EXISTS update_is_complete();
            """
        ),
    ]
