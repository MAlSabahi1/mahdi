# Migration 0023 — Phase 2 Hardening
# يُصلح fn_personnel_master_audit() و personnel_master_history
# بإضافة الأعمدة الجديدة وتحديث الـ Trigger ليتوافق مع المعمارية الجديدة

from django.db import migrations

# 1. أضف الأعمدة الجديدة إلى جدول الـ history
ADD_HISTORY_COLS_SQL = """
ALTER TABLE personnel_master_history
    ADD COLUMN IF NOT EXISTS security_admin_id     INTEGER,
    ADD COLUMN IF NOT EXISTS central_department_id INTEGER,
    ADD COLUMN IF NOT EXISTS branch_id             INTEGER,
    ADD COLUMN IF NOT EXISTS district_police_id    INTEGER,
    ADD COLUMN IF NOT EXISTS geo_location_id       INTEGER;
"""

# 2. أعد بناء الـ Trigger بالحقول الصحيحة
FIXED_AUDIT_TRIGGER_SQL = """
CREATE OR REPLACE FUNCTION fn_personnel_master_audit()
RETURNS TRIGGER AS $$
DECLARE
    v_user    TEXT;
    v_version INTEGER;
BEGIN
    BEGIN
        v_user := current_setting('app.current_user', true);
    EXCEPTION WHEN OTHERS THEN
        v_user := 'system';
    END;

    BEGIN
        v_version := current_setting('app.schema_version', true)::INTEGER;
    EXCEPTION WHEN OTHERS THEN
        v_version := 1;
    END;

    IF TG_OP = 'INSERT' THEN
        INSERT INTO personnel_master_history (
            history_action, history_user, history_version,
            military_number, old_military_number, national_id, full_name, corrected_name,
            birth_date, join_date, phone_number, photo, fingerprint_hash,
            security_admin_id, central_department_id, branch_id, district_police_id,
            division_id, unit_id, geo_location_id,
            category_id, job_title_id, position_id, force_classification_id,
            current_rank_id, current_status_id, is_complete, pending_rank_id,
            is_data_clean, data_quality_score, notes, expense_status,
            appointment_info, decision_date, transfer_date,
            created_at, updated_at, deleted_at, is_deleted
        ) VALUES (
            'INSERT', v_user, v_version,
            NEW.military_number, NEW.old_military_number, NEW.national_id, NEW.full_name, NEW.corrected_name,
            NEW.birth_date, NEW.join_date, NEW.phone_number, NEW.photo, NEW.fingerprint_hash,
            NEW.security_admin_id, NEW.central_department_id, NEW.branch_id, NEW.district_police_id,
            NEW.division_id, NEW.unit_id, NEW.geo_location_id,
            NEW.category_id, NEW.job_title_id, NEW.position_id, NEW.force_classification_id,
            NEW.current_rank_id, NEW.current_status_id, NEW.is_complete, NEW.pending_rank_id,
            NEW.is_data_clean, NEW.data_quality_score, NEW.notes, NEW.expense_status,
            NEW.appointment_info, NEW.decision_date, NEW.transfer_date,
            NEW.created_at, NEW.updated_at, NEW.deleted_at, NEW.is_deleted
        );
        RETURN NEW;

    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO personnel_master_history (
            history_action, history_user, history_version,
            military_number, old_military_number, national_id, full_name, corrected_name,
            birth_date, join_date, phone_number, photo, fingerprint_hash,
            security_admin_id, central_department_id, branch_id, district_police_id,
            division_id, unit_id, geo_location_id,
            category_id, job_title_id, position_id, force_classification_id,
            current_rank_id, current_status_id, is_complete, pending_rank_id,
            is_data_clean, data_quality_score, notes, expense_status,
            appointment_info, decision_date, transfer_date,
            created_at, updated_at, deleted_at, is_deleted
        ) VALUES (
            'UPDATE', v_user, v_version,
            NEW.military_number, NEW.old_military_number, NEW.national_id, NEW.full_name, NEW.corrected_name,
            NEW.birth_date, NEW.join_date, NEW.phone_number, NEW.photo, NEW.fingerprint_hash,
            NEW.security_admin_id, NEW.central_department_id, NEW.branch_id, NEW.district_police_id,
            NEW.division_id, NEW.unit_id, NEW.geo_location_id,
            NEW.category_id, NEW.job_title_id, NEW.position_id, NEW.force_classification_id,
            NEW.current_rank_id, NEW.current_status_id, NEW.is_complete, NEW.pending_rank_id,
            NEW.is_data_clean, NEW.data_quality_score, NEW.notes, NEW.expense_status,
            NEW.appointment_info, NEW.decision_date, NEW.transfer_date,
            NEW.created_at, NEW.updated_at, NEW.deleted_at, NEW.is_deleted
        );
        RETURN NEW;

    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO personnel_master_history (
            history_action, history_user, history_version,
            military_number, old_military_number, national_id, full_name, corrected_name,
            birth_date, join_date, phone_number, photo, fingerprint_hash,
            security_admin_id, central_department_id, branch_id, district_police_id,
            division_id, unit_id, geo_location_id,
            category_id, job_title_id, position_id, force_classification_id,
            current_rank_id, current_status_id, is_complete, pending_rank_id,
            is_data_clean, data_quality_score, notes, expense_status,
            appointment_info, decision_date, transfer_date,
            created_at, updated_at, deleted_at, is_deleted
        ) VALUES (
            'DELETE', v_user, v_version,
            OLD.military_number, OLD.old_military_number, OLD.national_id, OLD.full_name, OLD.corrected_name,
            OLD.birth_date, OLD.join_date, OLD.phone_number, OLD.photo, OLD.fingerprint_hash,
            OLD.security_admin_id, OLD.central_department_id, OLD.branch_id, OLD.district_police_id,
            OLD.division_id, OLD.unit_id, OLD.geo_location_id,
            OLD.category_id, OLD.job_title_id, OLD.position_id, OLD.force_classification_id,
            OLD.current_rank_id, OLD.current_status_id, OLD.is_complete, OLD.pending_rank_id,
            OLD.is_data_clean, OLD.data_quality_score, OLD.notes, OLD.expense_status,
            OLD.appointment_info, OLD.decision_date, OLD.transfer_date,
            OLD.created_at, OLD.updated_at, OLD.deleted_at, OLD.is_deleted
        );
        RETURN OLD;
    END IF;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;
"""


class Migration(migrations.Migration):

    dependencies = [
        ("personnel", "0022_fix_quality_score_trigger"),
    ]

    operations = [
        # أولاً: أضف الأعمدة الجديدة لجدول الـ history
        migrations.RunSQL(
            sql=ADD_HISTORY_COLS_SQL,
            reverse_sql="SELECT 1;",  # الأعمدة القديمة تبقى للتراجع الآمن
        ),
        # ثانياً: أعد بناء الـ Audit Trigger بالحقول الصحيحة
        migrations.RunSQL(
            sql=FIXED_AUDIT_TRIGGER_SQL,
            reverse_sql=FIXED_AUDIT_TRIGGER_SQL,  # نفس الإصلاح للتراجع
        ),
    ]
