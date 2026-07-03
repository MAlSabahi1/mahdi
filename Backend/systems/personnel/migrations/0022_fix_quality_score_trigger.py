# Generated manually — Phase 2 Hardening
# يُصلح calculate_data_quality_score() بحذف مرجع location_id المحذوف من الـ Schema

from django.db import migrations

FIXED_TRIGGER_SQL = """
CREATE OR REPLACE FUNCTION calculate_data_quality_score()
RETURNS TRIGGER AS $$
DECLARE
    score INTEGER := 0;
BEGIN
    -- الحقول الإلزامية (10 نقاط لكل حقل)
    IF NEW.military_number IS NOT NULL AND LENGTH(NEW.military_number) = 7 THEN
        score := score + 10;
    END IF;

    IF NEW.national_id IS NOT NULL AND LENGTH(NEW.national_id) = 11 THEN
        score := score + 10;
    END IF;

    IF NEW.full_name IS NOT NULL AND LENGTH(TRIM(NEW.full_name)) > 0 THEN
        score := score + 10;
    END IF;

    IF NEW.birth_date IS NOT NULL THEN
        score := score + 10;
    END IF;

    IF NEW.join_date IS NOT NULL THEN
        score := score + 10;
    END IF;

    -- الحقول الاختيارية (5 نقاط لكل حقل)
    IF NEW.phone_number IS NOT NULL AND TRIM(NEW.phone_number) != '' THEN
        score := score + 5;
    END IF;

    IF NEW.photo IS NOT NULL AND TRIM(NEW.photo) != '' THEN
        score := score + 10;
    END IF;

    IF NEW.fingerprint_hash IS NOT NULL AND TRIM(NEW.fingerprint_hash) != '' THEN
        score := score + 10;
    END IF;

    IF NEW.qualification_id IS NOT NULL THEN
        score := score + 5;
    END IF;

    -- خصم نقاط: رقم وطني مفقود أو غير صالح أو مكرر
    IF NEW.national_id IS NULL OR TRIM(NEW.national_id) = '' THEN
        score := score - 15;
    ELSIF LENGTH(NEW.national_id) != 11 OR NEW.national_id !~ '^[0-9]+$' THEN
        score := score - 15;
    ELSIF EXISTS (
        SELECT 1 FROM personnel_master
        WHERE national_id = NEW.national_id
          AND military_number != NEW.military_number
    ) THEN
        score := score - 15;
    END IF;

    -- التأكد من أن الدرجة بين 0 و 100
    IF score < 0 THEN
        score := 0;
    ELSIF score > 100 THEN
        score := 100;
    END IF;

    NEW.data_quality_score := score;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
"""

class Migration(migrations.Migration):

    dependencies = [
        ("personnel", "0021_rawdataimport_linked_personnel_and_more"),
    ]

    operations = [
        migrations.RunSQL(
            sql=FIXED_TRIGGER_SQL,
            # reverse_sql يعيد الإصدار السابق بـ location_id (للتراجع السليم)
            reverse_sql=FIXED_TRIGGER_SQL,
        )
    ]
