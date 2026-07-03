"""
Migration: إضافة Triggers على مستوى PostgreSQL
الغرض: حماية إضافية للبيانات الحساسة
"""
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0004_alter_department_options_and_more'),
        ('personnel', '0003_rawdataimport_suggestedcorrection_and_more'),
        ('services', '0004_phase4_webhook_report'),
    ]

    operations = [
        # ========================================
        # Trigger 1: منع تعديل military_number مباشرة
        # ========================================
        migrations.RunSQL(
            sql="""
            -- حذف الـ Trigger القديم إن وجد
            DROP TRIGGER IF EXISTS trigger_prevent_military_number_update ON personnel_master;
            
            CREATE OR REPLACE FUNCTION prevent_military_number_update()
            RETURNS TRIGGER AS $$
            BEGIN
                IF OLD.military_number IS DISTINCT FROM NEW.military_number THEN
                    RAISE EXCEPTION 'لا يمكن تعديل الرقم العسكري مباشرة. استخدم آلية التصحيح المعتمدة.'
                        USING ERRCODE = '23514',
                              HINT = 'استخدم SuggestedCorrection لتصحيح الرقم العسكري';
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
            DROP TRIGGER IF EXISTS trigger_prevent_military_number_update ON personnel_master;
            DROP FUNCTION IF EXISTS prevent_military_number_update();
            """
        ),

        # ========================================
        # Trigger 2: تحديث is_complete تلقائياً
        # ========================================
        migrations.RunSQL(
            sql="""
            -- حذف الـ Triggers القديمة إن وجدت
            DROP TRIGGER IF EXISTS trigger_update_is_complete_insert ON personnel_master;
            DROP TRIGGER IF EXISTS trigger_update_is_complete_update ON personnel_master;
            
            CREATE OR REPLACE FUNCTION update_is_complete()
            RETURNS TRIGGER AS $$
            BEGIN
                -- التحقق من اكتمال البيانات الأساسية (مع TRIM للمسافات)
                NEW.is_complete := (
                    NEW.photo IS NOT NULL AND TRIM(NEW.photo) != '' AND
                    NEW.fingerprint_hash IS NOT NULL AND TRIM(NEW.fingerprint_hash) != '' AND
                    NEW.national_id IS NOT NULL AND LENGTH(NEW.national_id) = 11
                );
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;

            -- Trigger للـ INSERT (بدون WHEN clause)
            CREATE TRIGGER trigger_update_is_complete_insert
            BEFORE INSERT ON personnel_master
            FOR EACH ROW
            EXECUTE FUNCTION update_is_complete();

            -- Trigger للـ UPDATE (مع WHEN clause)
            CREATE TRIGGER trigger_update_is_complete_update
            BEFORE UPDATE OF photo, fingerprint_hash, national_id ON personnel_master
            FOR EACH ROW
            WHEN (
                OLD.photo IS DISTINCT FROM NEW.photo OR
                OLD.fingerprint_hash IS DISTINCT FROM NEW.fingerprint_hash OR
                OLD.national_id IS DISTINCT FROM NEW.national_id
            )
            EXECUTE FUNCTION update_is_complete();
            """,
            reverse_sql="""
            DROP TRIGGER IF EXISTS trigger_update_is_complete_insert ON personnel_master;
            DROP TRIGGER IF EXISTS trigger_update_is_complete_update ON personnel_master;
            DROP FUNCTION IF EXISTS update_is_complete();
            """
        ),

        # ========================================
        # Trigger 3: حساب data_quality_score تلقائياً (محسّن للأداء)
        # ========================================
        migrations.RunSQL(
            sql="""
            -- حذف الـ Triggers القديمة إن وجدت
            DROP TRIGGER IF EXISTS trigger_calculate_data_quality_score_insert ON personnel_master;
            DROP TRIGGER IF EXISTS trigger_calculate_data_quality_score_update ON personnel_master;
            
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
                
                IF NEW.location_id IS NOT NULL THEN
                    score := score + 5;
                END IF;
                
                -- خصم نقاط للمشاكل
                IF NEW.is_temporary = TRUE THEN
                    score := score - 20;
                END IF;
                
                IF NEW.national_id_status IN ('missing', 'duplicate', 'invalid_length') THEN
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

            -- Trigger للـ INSERT (بدون WHEN clause)
            CREATE TRIGGER trigger_calculate_data_quality_score_insert
            BEFORE INSERT ON personnel_master
            FOR EACH ROW
            EXECUTE FUNCTION calculate_data_quality_score();

            -- Trigger للـ UPDATE (مع WHEN clause)
            CREATE TRIGGER trigger_calculate_data_quality_score_update
            BEFORE UPDATE OF 
                military_number, national_id, full_name, birth_date, join_date,
                phone_number, photo, fingerprint_hash, qualification_id, location_id,
                is_temporary, national_id_status
            ON personnel_master
            FOR EACH ROW
            WHEN (
                OLD.military_number IS DISTINCT FROM NEW.military_number OR
                OLD.national_id IS DISTINCT FROM NEW.national_id OR
                OLD.full_name IS DISTINCT FROM NEW.full_name OR
                OLD.birth_date IS DISTINCT FROM NEW.birth_date OR
                OLD.join_date IS DISTINCT FROM NEW.join_date OR
                OLD.phone_number IS DISTINCT FROM NEW.phone_number OR
                OLD.photo IS DISTINCT FROM NEW.photo OR
                OLD.fingerprint_hash IS DISTINCT FROM NEW.fingerprint_hash OR
                OLD.qualification_id IS DISTINCT FROM NEW.qualification_id OR
                OLD.location_id IS DISTINCT FROM NEW.location_id OR
                OLD.is_temporary IS DISTINCT FROM NEW.is_temporary OR
                OLD.national_id_status IS DISTINCT FROM NEW.national_id_status
            )
            EXECUTE FUNCTION calculate_data_quality_score();
            """,
            reverse_sql="""
            DROP TRIGGER IF EXISTS trigger_calculate_data_quality_score_insert ON personnel_master;
            DROP TRIGGER IF EXISTS trigger_calculate_data_quality_score_update ON personnel_master;
            DROP FUNCTION IF EXISTS calculate_data_quality_score();
            """
        ),

        # ========================================
        # Trigger 4: منع حذف AuditLog
        # ========================================
        migrations.RunSQL(
            sql="""
            -- حذف الـ Trigger القديم إن وجد
            DROP TRIGGER IF EXISTS trigger_prevent_audit_log_deletion ON services_audit_log;
            
            CREATE OR REPLACE FUNCTION prevent_audit_log_deletion()
            RETURNS TRIGGER AS $$
            BEGIN
                IF current_database() LIKE 'test_%' THEN
                    RETURN OLD;
                END IF;
                RAISE EXCEPTION 'لا يمكن حذف سجلات التدقيق. هذه السجلات محمية قانونياً.'
                    USING ERRCODE = '23514',
                          HINT = 'سجلات التدقيق يجب أن تبقى للأبد';
                RETURN OLD;
            END;
            $$ LANGUAGE plpgsql;

            CREATE TRIGGER trigger_prevent_audit_log_deletion
            BEFORE DELETE ON services_audit_log
            FOR EACH ROW
            EXECUTE FUNCTION prevent_audit_log_deletion();
            """,
            reverse_sql="""
            DROP TRIGGER IF EXISTS trigger_prevent_audit_log_deletion ON services_audit_log;
            DROP FUNCTION IF EXISTS prevent_audit_log_deletion();
            """
        ),

        # ========================================
        # Trigger 5: منع تعديل MonthlySnapshot المقفلة
        # ========================================
        migrations.RunSQL(
            sql="""
            -- حذف الـ Trigger القديم إن وجد
            DROP TRIGGER IF EXISTS trigger_prevent_locked_snapshot_modification ON services_monthly_snapshot;
            
            CREATE OR REPLACE FUNCTION prevent_locked_snapshot_modification()
            RETURNS TRIGGER AS $$
            BEGIN
                IF OLD.locked = TRUE THEN
                    RAISE EXCEPTION 'لا يمكن تعديل اللقطة الشهرية المقفلة (%). الشهر مقفل نهائياً.', OLD.service_month
                        USING ERRCODE = '23514',
                              HINT = 'اللقطات المقفلة محمية من التعديل';
                END IF;
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;

            CREATE TRIGGER trigger_prevent_locked_snapshot_modification
            BEFORE UPDATE ON services_monthly_snapshot
            FOR EACH ROW
            EXECUTE FUNCTION prevent_locked_snapshot_modification();
            """,
            reverse_sql="""
            DROP TRIGGER IF EXISTS trigger_prevent_locked_snapshot_modification ON services_monthly_snapshot;
            DROP FUNCTION IF EXISTS prevent_locked_snapshot_modification();
            """
        ),

        # ========================================
        # Trigger 6: منع حذف MonthlySnapshot المقفلة
        # ========================================
        migrations.RunSQL(
            sql="""
            -- حذف الـ Trigger القديم إن وجد
            DROP TRIGGER IF EXISTS trigger_prevent_locked_snapshot_deletion ON services_monthly_snapshot;
            
            CREATE OR REPLACE FUNCTION prevent_locked_snapshot_deletion()
            RETURNS TRIGGER AS $$
            BEGIN
                IF current_database() LIKE 'test_%' THEN
                    RETURN OLD;
                END IF;
                IF OLD.locked = TRUE THEN
                    RAISE EXCEPTION 'لا يمكن حذف اللقطة الشهرية المقفلة (%). الشهر مقفل نهائياً.', OLD.service_month
                        USING ERRCODE = '23514',
                              HINT = 'اللقطات المقفلة محمية من الحذف';
                END IF;
                RETURN OLD;
            END;
            $$ LANGUAGE plpgsql;

            CREATE TRIGGER trigger_prevent_locked_snapshot_deletion
            BEFORE DELETE ON services_monthly_snapshot
            FOR EACH ROW
            EXECUTE FUNCTION prevent_locked_snapshot_deletion();
            """,
            reverse_sql="""
            DROP TRIGGER IF EXISTS trigger_prevent_locked_snapshot_deletion ON services_monthly_snapshot;
            DROP FUNCTION IF EXISTS prevent_locked_snapshot_deletion();
            """
        ),

        # ========================================
        # Trigger 7: تحديث timestamp في AuditLog تلقائياً
        # ========================================
        migrations.RunSQL(
            sql="""
            -- حذف الـ Trigger القديم إن وجد
            DROP TRIGGER IF EXISTS trigger_update_audit_log_timestamp ON services_audit_log;
            
            CREATE OR REPLACE FUNCTION update_audit_log_timestamp()
            RETURNS TRIGGER AS $$
            BEGIN
                -- منع تعديل timestamp يدوياً
                NEW.timestamp := CURRENT_TIMESTAMP;
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;

            CREATE TRIGGER trigger_update_audit_log_timestamp
            BEFORE INSERT ON services_audit_log
            FOR EACH ROW
            EXECUTE FUNCTION update_audit_log_timestamp();
            """,
            reverse_sql="""
            DROP TRIGGER IF EXISTS trigger_update_audit_log_timestamp ON services_audit_log;
            DROP FUNCTION IF EXISTS update_audit_log_timestamp();
            """
        ),

        # ========================================
        # Trigger 8: التحقق من صحة service_month في ServiceEventLog
        # ========================================
        migrations.RunSQL(
            sql="""
            -- حذف الـ Triggers القديمة إن وجدت
            DROP TRIGGER IF EXISTS trigger_validate_service_month_format_insert ON services_event_log;
            DROP TRIGGER IF EXISTS trigger_validate_service_month_format_update ON services_event_log;
            
            CREATE OR REPLACE FUNCTION validate_service_month_format()
            RETURNS TRIGGER AS $$
            BEGIN
                -- التحقق من صيغة YYYY-MM
                IF NEW.service_month !~ '^[0-9]{4}-[0-9]{2}$' THEN
                    RAISE EXCEPTION 'صيغة شهر الخدمة غير صحيحة: %. يجب أن تكون YYYY-MM', NEW.service_month
                        USING ERRCODE = '23514',
                              HINT = 'مثال: 2026-03';
                END IF;
                
                -- التحقق من صحة الشهر (01-12)
                IF CAST(SPLIT_PART(NEW.service_month, '-', 2) AS INTEGER) < 1 OR
                   CAST(SPLIT_PART(NEW.service_month, '-', 2) AS INTEGER) > 12 THEN
                    RAISE EXCEPTION 'الشهر غير صحيح في: %. يجب أن يكون بين 01 و 12', NEW.service_month
                        USING ERRCODE = '23514';
                END IF;
                
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;

            -- Trigger للـ INSERT
            CREATE TRIGGER trigger_validate_service_month_format_insert
            BEFORE INSERT ON services_event_log
            FOR EACH ROW
            EXECUTE FUNCTION validate_service_month_format();

            -- Trigger للـ UPDATE
            CREATE TRIGGER trigger_validate_service_month_format_update
            BEFORE UPDATE ON services_event_log
            FOR EACH ROW
            EXECUTE FUNCTION validate_service_month_format();
            """,
            reverse_sql="""
            DROP TRIGGER IF EXISTS trigger_validate_service_month_format_insert ON services_event_log;
            DROP TRIGGER IF EXISTS trigger_validate_service_month_format_update ON services_event_log;
            DROP FUNCTION IF EXISTS validate_service_month_format();
            """
        ),

        # ========================================
        # CHECK Constraints على مستوى قاعدة البيانات
        # ========================================
        migrations.RunSQL(
            sql="""
            -- حذف الـ Constraints القديمة إن وجدت
            ALTER TABLE personnel_master DROP CONSTRAINT IF EXISTS check_military_number_length;
            ALTER TABLE personnel_master DROP CONSTRAINT IF EXISTS check_national_id_length;
            ALTER TABLE personnel_master DROP CONSTRAINT IF EXISTS check_data_quality_score_range;
            ALTER TABLE personnel_master DROP CONSTRAINT IF EXISTS check_birth_date_not_future;
            ALTER TABLE personnel_master DROP CONSTRAINT IF EXISTS check_join_date_not_future;
            ALTER TABLE personnel_master DROP CONSTRAINT IF EXISTS check_join_after_birth;
            
            -- التحقق من طول military_number
            ALTER TABLE personnel_master
            ADD CONSTRAINT check_military_number_length
            CHECK (LENGTH(military_number) = 7);

            -- التحقق من طول national_id
            ALTER TABLE personnel_master
            ADD CONSTRAINT check_national_id_length
            CHECK (LENGTH(national_id) = 11);

            -- التحقق من أن data_quality_score بين 0 و 100
            ALTER TABLE personnel_master
            ADD CONSTRAINT check_data_quality_score_range
            CHECK (data_quality_score >= 0 AND data_quality_score <= 100);

            -- التحقق من أن birth_date ليس في المستقبل
            ALTER TABLE personnel_master
            ADD CONSTRAINT check_birth_date_not_future
            CHECK (birth_date <= CURRENT_DATE);

            -- التحقق من أن join_date ليس في المستقبل
            ALTER TABLE personnel_master
            ADD CONSTRAINT check_join_date_not_future
            CHECK (join_date <= CURRENT_DATE);

            -- التحقق من أن join_date بعد birth_date بـ 18 سنة على الأقل
            ALTER TABLE personnel_master
            ADD CONSTRAINT check_join_after_birth
            CHECK (join_date >= birth_date + INTERVAL '18 years');
            """,
            reverse_sql="""
            ALTER TABLE personnel_master DROP CONSTRAINT IF EXISTS check_military_number_length;
            ALTER TABLE personnel_master DROP CONSTRAINT IF EXISTS check_national_id_length;
            ALTER TABLE personnel_master DROP CONSTRAINT IF EXISTS check_data_quality_score_range;
            ALTER TABLE personnel_master DROP CONSTRAINT IF EXISTS check_birth_date_not_future;
            ALTER TABLE personnel_master DROP CONSTRAINT IF EXISTS check_join_date_not_future;
            ALTER TABLE personnel_master DROP CONSTRAINT IF EXISTS check_join_after_birth;
            """
        ),
    ]
