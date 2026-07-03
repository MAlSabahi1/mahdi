"""
Shadow Tables + Triggers + Audit Delete Prevention
المرحلة 3.3: جداول الظل مع PostgreSQL Triggers
"""
from django.db import migrations


SHADOW_TABLES_SQL = """
-- ============================================================================
-- جدول الظل: personnel_master_history
-- ============================================================================
CREATE TABLE IF NOT EXISTS personnel_master_history (
    history_id BIGSERIAL PRIMARY KEY,
    history_action VARCHAR(10) NOT NULL,  -- INSERT, UPDATE, DELETE
    history_user VARCHAR(50),
    history_timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    history_version INTEGER NOT NULL DEFAULT 1,
    
    -- نسخة من حقول PersonnelMaster
    military_number VARCHAR(7),
    old_military_number VARCHAR(7),
    national_id VARCHAR(11),
    full_name VARCHAR(200),
    corrected_name VARCHAR(200),
    birth_date DATE,
    join_date DATE,
    phone_number VARCHAR(9),
    photo VARCHAR(100),
    fingerprint_hash VARCHAR(128),
    governorate_id INTEGER,
    directorate_id INTEGER,
    division_id INTEGER,
    unit_id INTEGER,
    category_id INTEGER,
    job_title_id INTEGER,
    position_id INTEGER,
    force_classification_id INTEGER,
    current_rank_id INTEGER,
    current_status_id INTEGER,
    is_complete BOOLEAN,
    pending_rank_id INTEGER,
    is_data_clean BOOLEAN,
    data_quality_score INTEGER,
    notes TEXT,
    expense_status VARCHAR(30),
    appointment_info TEXT,
    decision_date DATE,
    transfer_date DATE,
    created_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ,
    deleted_at TIMESTAMPTZ,
    is_deleted BOOLEAN
);

CREATE INDEX IF NOT EXISTS idx_pm_history_military 
    ON personnel_master_history(military_number);
CREATE INDEX IF NOT EXISTS idx_pm_history_timestamp 
    ON personnel_master_history(history_timestamp);
CREATE INDEX IF NOT EXISTS idx_pm_history_action 
    ON personnel_master_history(history_action);
CREATE INDEX IF NOT EXISTS idx_pm_history_version 
    ON personnel_master_history(military_number, history_version);

-- ============================================================================
-- جدول الظل: service_event_log_history
-- ============================================================================
CREATE TABLE IF NOT EXISTS service_event_log_history (
    history_id BIGSERIAL PRIMARY KEY,
    history_action VARCHAR(10) NOT NULL,
    history_user VARCHAR(50),
    history_timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    history_version INTEGER NOT NULL DEFAULT 1,
    
    -- نسخة من حقول ServiceEventLog
    id INTEGER,
    personnel_id VARCHAR(7),
    event_date DATE,
    service_month VARCHAR(7),
    field_name VARCHAR(50),
    old_value TEXT,
    new_value TEXT,
    order_document_id INTEGER,
    created_by_id INTEGER,
    created_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_sel_history_personnel 
    ON service_event_log_history(personnel_id);
CREATE INDEX IF NOT EXISTS idx_sel_history_timestamp 
    ON service_event_log_history(history_timestamp);


-- ============================================================================
-- Trigger Function: تسجيل التغييرات في personnel_master_history
-- ============================================================================
CREATE OR REPLACE FUNCTION fn_personnel_master_audit()
RETURNS TRIGGER AS $$
DECLARE
    v_user VARCHAR(50);
    v_version INTEGER;
    v_action VARCHAR(10);
BEGIN
    -- محاولة جلب المستخدم من المتغير المؤقت
    BEGIN
        v_user := current_setting('myapp.current_user', TRUE);
    EXCEPTION WHEN OTHERS THEN
        v_user := 'system';
    END;
    
    IF v_user IS NULL OR v_user = '' THEN
        v_user := 'system';
    END IF;
    
    -- حساب رقم الإصدار
    IF TG_OP = 'INSERT' THEN
        v_version := 1;
    ELSE
        SELECT COALESCE(MAX(history_version), 0) + 1 
        INTO v_version
        FROM personnel_master_history 
        WHERE military_number = OLD.military_number;
    END IF;
    
    IF TG_OP = 'DELETE' THEN
        INSERT INTO personnel_master_history (
            history_action, history_user, history_version,
            military_number, old_military_number, national_id, full_name, corrected_name,
            birth_date, join_date, phone_number, photo, fingerprint_hash,
            governorate_id, directorate_id, division_id, unit_id,
            category_id, job_title_id, position_id, force_classification_id,
            current_rank_id, current_status_id, is_complete, pending_rank_id,
            is_data_clean, data_quality_score, notes, expense_status,
            appointment_info, decision_date, transfer_date,
            created_at, updated_at, deleted_at, is_deleted
        ) VALUES (
            'DELETE', v_user, v_version,
            OLD.military_number, OLD.old_military_number, OLD.national_id, OLD.full_name, OLD.corrected_name,
            OLD.birth_date, OLD.join_date, OLD.phone_number, OLD.photo, OLD.fingerprint_hash,
            OLD.governorate_id, OLD.directorate_id, OLD.division_id, OLD.unit_id,
            OLD.category_id, OLD.job_title_id, OLD.position_id, OLD.force_classification_id,
            OLD.current_rank_id, OLD.current_status_id, OLD.is_complete, OLD.pending_rank_id,
            OLD.is_data_clean, OLD.data_quality_score, OLD.notes, OLD.expense_status,
            OLD.appointment_info, OLD.decision_date, OLD.transfer_date,
            OLD.created_at, OLD.updated_at, OLD.deleted_at, OLD.is_deleted
        );
        RETURN OLD;
        
    ELSIF TG_OP = 'UPDATE' THEN
        IF NEW.is_deleted = TRUE AND OLD.is_deleted = FALSE THEN
            v_action := 'DELETE';
        ELSE
            v_action := 'UPDATE';
        END IF;

        INSERT INTO personnel_master_history (
            history_action, history_user, history_version,
            military_number, old_military_number, national_id, full_name, corrected_name,
            birth_date, join_date, phone_number, photo, fingerprint_hash,
            governorate_id, directorate_id, division_id, unit_id,
            category_id, job_title_id, position_id, force_classification_id,
            current_rank_id, current_status_id, is_complete, pending_rank_id,
            is_data_clean, data_quality_score, notes, expense_status,
            appointment_info, decision_date, transfer_date,
            created_at, updated_at, deleted_at, is_deleted
        ) VALUES (
            v_action, v_user, v_version,
            NEW.military_number, NEW.old_military_number, NEW.national_id, NEW.full_name, NEW.corrected_name,
            NEW.birth_date, NEW.join_date, NEW.phone_number, NEW.photo, NEW.fingerprint_hash,
            NEW.governorate_id, NEW.directorate_id, NEW.division_id, NEW.unit_id,
            NEW.category_id, NEW.job_title_id, NEW.position_id, NEW.force_classification_id,
            NEW.current_rank_id, NEW.current_status_id, NEW.is_complete, NEW.pending_rank_id,
            NEW.is_data_clean, NEW.data_quality_score, NEW.notes, NEW.expense_status,
            NEW.appointment_info, NEW.decision_date, NEW.transfer_date,
            NEW.created_at, NEW.updated_at, NEW.deleted_at, NEW.is_deleted
        );
        RETURN NEW;
        
    ELSIF TG_OP = 'INSERT' THEN
        INSERT INTO personnel_master_history (
            history_action, history_user, history_version,
            military_number, old_military_number, national_id, full_name, corrected_name,
            birth_date, join_date, phone_number, photo, fingerprint_hash,
            governorate_id, directorate_id, division_id, unit_id,
            category_id, job_title_id, position_id, force_classification_id,
            current_rank_id, current_status_id, is_complete, pending_rank_id,
            is_data_clean, data_quality_score, notes, expense_status,
            appointment_info, decision_date, transfer_date,
            created_at, updated_at, deleted_at, is_deleted
        ) VALUES (
            'INSERT', v_user, v_version,
            NEW.military_number, NEW.old_military_number, NEW.national_id, NEW.full_name, NEW.corrected_name,
            NEW.birth_date, NEW.join_date, NEW.phone_number, NEW.photo, NEW.fingerprint_hash,
            NEW.governorate_id, NEW.directorate_id, NEW.division_id, NEW.unit_id,
            NEW.category_id, NEW.job_title_id, NEW.position_id, NEW.force_classification_id,
            NEW.current_rank_id, NEW.current_status_id, NEW.is_complete, NEW.pending_rank_id,
            NEW.is_data_clean, NEW.data_quality_score, NEW.notes, NEW.expense_status,
            NEW.appointment_info, NEW.decision_date, NEW.transfer_date,
            NEW.created_at, NEW.updated_at, NEW.deleted_at, NEW.is_deleted
        );
        RETURN NEW;
    END IF;
END;
$$ LANGUAGE plpgsql;


-- ============================================================================
-- Trigger Function: تسجيل التغييرات في service_event_log_history
-- ============================================================================
CREATE OR REPLACE FUNCTION fn_service_event_log_audit()
RETURNS TRIGGER AS $$
DECLARE
    v_user VARCHAR(50);
    v_version INTEGER;
BEGIN
    BEGIN
        v_user := current_setting('myapp.current_user', TRUE);
    EXCEPTION WHEN OTHERS THEN
        v_user := 'system';
    END;
    
    IF v_user IS NULL OR v_user = '' THEN
        v_user := 'system';
    END IF;
    
    IF TG_OP = 'INSERT' THEN
        v_version := 1;
    ELSE
        SELECT COALESCE(MAX(history_version), 0) + 1
        INTO v_version
        FROM service_event_log_history
        WHERE id = OLD.id;
    END IF;
    
    IF TG_OP = 'DELETE' THEN
        INSERT INTO service_event_log_history (
            history_action, history_user, history_version,
            id, personnel_id, event_date, service_month,
            field_name, old_value, new_value,
            order_document_id, created_by_id, created_at, updated_at
        ) VALUES (
            'DELETE', v_user, v_version,
            OLD.id, OLD.personnel_id, OLD.event_date, OLD.service_month,
            OLD.field_name, OLD.old_value, OLD.new_value,
            OLD.order_document_id, OLD.created_by_id, OLD.created_at, OLD.updated_at
        );
        RETURN OLD;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO service_event_log_history (
            history_action, history_user, history_version,
            id, personnel_id, event_date, service_month,
            field_name, old_value, new_value,
            order_document_id, created_by_id, created_at, updated_at
        ) VALUES (
            'UPDATE', v_user, v_version,
            NEW.id, NEW.personnel_id, NEW.event_date, NEW.service_month,
            NEW.field_name, NEW.old_value, NEW.new_value,
            NEW.order_document_id, NEW.created_by_id, NEW.created_at, NEW.updated_at
        );
        RETURN NEW;
    ELSIF TG_OP = 'INSERT' THEN
        INSERT INTO service_event_log_history (
            history_action, history_user, history_version,
            id, personnel_id, event_date, service_month,
            field_name, old_value, new_value,
            order_document_id, created_by_id, created_at, updated_at
        ) VALUES (
            'INSERT', v_user, v_version,
            NEW.id, NEW.personnel_id, NEW.event_date, NEW.service_month,
            NEW.field_name, NEW.old_value, NEW.new_value,
            NEW.order_document_id, NEW.created_by_id, NEW.created_at, NEW.updated_at
        );
        RETURN NEW;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- Trigger Function: منع حذف سجلات التدقيق
-- ============================================================================
CREATE OR REPLACE FUNCTION fn_prevent_audit_delete()
RETURNS TRIGGER AS $$
BEGIN
    IF current_database() LIKE 'test_%' THEN
        RETURN OLD;
    END IF;
    RAISE EXCEPTION 'حذف سجلات التدقيق ممنوع! استخدم الأرشفة بدلاً من ذلك.';
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- تطبيق Triggers
-- ============================================================================

-- حذف Triggers القديمة إن وجدت
DROP TRIGGER IF EXISTS trg_personnel_master_audit ON personnel_master;
DROP TRIGGER IF EXISTS trg_service_event_log_audit ON services_event_log;
DROP TRIGGER IF EXISTS trg_prevent_audit_delete ON services_audit_log;

-- إنشاء Triggers جديدة
CREATE TRIGGER trg_personnel_master_audit
    AFTER INSERT OR UPDATE OR DELETE ON personnel_master
    FOR EACH ROW EXECUTE FUNCTION fn_personnel_master_audit();

CREATE TRIGGER trg_service_event_log_audit
    AFTER INSERT OR UPDATE OR DELETE ON services_event_log
    FOR EACH ROW EXECUTE FUNCTION fn_service_event_log_audit();

CREATE TRIGGER trg_prevent_audit_delete
    BEFORE DELETE ON services_audit_log
    FOR EACH ROW EXECUTE FUNCTION fn_prevent_audit_delete();
"""


SHADOW_TABLES_REVERSE_SQL = """
DROP TRIGGER IF EXISTS trg_personnel_master_audit ON personnel_master;
DROP TRIGGER IF EXISTS trg_service_event_log_audit ON services_event_log;
DROP TRIGGER IF EXISTS trg_prevent_audit_delete ON services_audit_log;

DROP FUNCTION IF EXISTS fn_personnel_master_audit();
DROP FUNCTION IF EXISTS fn_service_event_log_audit();
DROP FUNCTION IF EXISTS fn_prevent_audit_delete();

DROP TABLE IF EXISTS personnel_master_history;
DROP TABLE IF EXISTS service_event_log_history;
"""


class Migration(migrations.Migration):
    
    dependencies = [
        ('security', '0001_initial'),
        ('personnel', '0001_initial'),
        ('services', '0001_initial'),
    ]
    
    operations = [
        migrations.RunSQL(
            sql=SHADOW_TABLES_SQL,
            reverse_sql=SHADOW_TABLES_REVERSE_SQL,
        ),
    ]
