"""
Migration: إضافة فهارس متقدمة لتحسين الأداء
الغرض: تسريع الاستعلامات الشائعة والمعقدة
"""
from django.db import migrations
from django.contrib.postgres.operations import TrigramExtension, BtreeGinExtension


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0005_add_database_triggers'),
        ('personnel', '0003_rawdataimport_suggestedcorrection_and_more'),
        ('services', '0004_phase4_webhook_report'),
    ]

    operations = [
        # تفعيل امتدادات PostgreSQL للبحث المتقدم
        TrigramExtension(),
        BtreeGinExtension(),

        # ========================================
        # Composite Indexes - فهارس مركبة
        # ========================================
        
        # 1. البحث عن الأفراد حسب الإدارة والحالة (استعلام شائع جداً)
        migrations.RunSQL(
            sql="""
            CREATE INDEX IF NOT EXISTS idx_personnel_dept_status_rank ON personnel_master 
            (current_department_id, current_status_id, current_rank_id)
            WHERE is_complete = TRUE;
            """,
            reverse_sql="DROP INDEX IF EXISTS idx_personnel_dept_status_rank;"
        ),

        # 2. البحث عن الأفراد حسب الحالة والإدارة (للتقارير)
        migrations.RunSQL(
            sql="""
            CREATE INDEX IF NOT EXISTS idx_personnel_status_dept ON personnel_master 
            (current_status_id, current_department_id)
            INCLUDE (military_number, full_name, current_rank_id);
            """,
            reverse_sql="DROP INDEX IF EXISTS idx_personnel_status_dept;"
        ),

        # 3. البحث في سجل الأحداث حسب الفرد والشهر (استعلام متكرر)
        migrations.RunSQL(
            sql="""
            CREATE INDEX IF NOT EXISTS idx_eventlog_personnel_month_field ON services_event_log 
            (personnel_id, service_month, field_name)
            INCLUDE (old_value, new_value, event_date);
            """,
            reverse_sql="DROP INDEX IF EXISTS idx_eventlog_personnel_month_field;"
        ),

        # 4. البحث في سجل الأحداث حسب الشهر (للتقارير الشهرية)
        migrations.RunSQL(
            sql="""
            CREATE INDEX IF NOT EXISTS idx_eventlog_month_created ON services_event_log 
            (service_month, created_at DESC)
            INCLUDE (personnel_id, field_name, new_value);
            """,
            reverse_sql="DROP INDEX IF EXISTS idx_eventlog_month_created;"
        ),

        # 5. البحث في AuditLog حسب المستخدم والتاريخ
        migrations.RunSQL(
            sql="""
            CREATE INDEX IF NOT EXISTS idx_auditlog_user_timestamp ON services_audit_log 
            (user_id, timestamp DESC)
            INCLUDE (action, model_name, object_id);
            """,
            reverse_sql="DROP INDEX IF EXISTS idx_auditlog_user_timestamp;"
        ),

        # 6. البحث في AuditLog حسب النموذج والكائن
        migrations.RunSQL(
            sql="""
            CREATE INDEX IF NOT EXISTS idx_auditlog_model_object ON services_audit_log 
            (model_name, object_id, timestamp DESC);
            """,
            reverse_sql="DROP INDEX IF EXISTS idx_auditlog_model_object;"
        ),

        # ========================================
        # Partial Indexes - فهارس جزئية
        # ========================================

        # 7. الأفراد غير المكتملين فقط (للمتابعة)
        migrations.RunSQL(
            sql="""
            CREATE INDEX IF NOT EXISTS idx_personnel_incomplete ON personnel_master 
            (current_department_id, data_quality_score)
            WHERE is_complete = FALSE;
            """,
            reverse_sql="DROP INDEX IF EXISTS idx_personnel_incomplete;"
        ),

        # 8. الأفراد المؤقتين فقط
        migrations.RunSQL(
            sql="""
            CREATE INDEX IF NOT EXISTS idx_personnel_temporary ON personnel_master 
            (military_number, full_name)
            WHERE is_temporary = TRUE;
            """,
            reverse_sql="DROP INDEX IF EXISTS idx_personnel_temporary;"
        ),

        # 9. الأرقام الوطنية المكررة فقط
        migrations.RunSQL(
            sql="""
            CREATE INDEX IF NOT EXISTS idx_personnel_duplicate_national_id ON personnel_master 
            (national_id, national_id_duplicate_of_id)
            WHERE national_id_status = 'duplicate';
            """,
            reverse_sql="DROP INDEX IF EXISTS idx_personnel_duplicate_national_id;"
        ),

        # 10. StagingRecord المعلقة فقط (للمراجعة)
        migrations.RunSQL(
            sql="""
            CREATE INDEX IF NOT EXISTS idx_staging_pending ON services_staging_record 
            (upload_batch_id, severity, created_at DESC)
            WHERE status = 'pending';
            """,
            reverse_sql="DROP INDEX IF EXISTS idx_staging_pending;"
        ),

        # 11. StagingRecord التي تتطلب مستندات
        migrations.RunSQL(
            sql="""
            CREATE INDEX IF NOT EXISTS idx_staging_requires_doc ON services_staging_record 
            (personnel_id, created_at DESC)
            WHERE requires_document = TRUE AND status = 'pending';
            """,
            reverse_sql="DROP INDEX IF EXISTS idx_staging_requires_doc;"
        ),

        # 12. الاقتراحات المعلقة فقط
        migrations.RunSQL(
            sql="""
            CREATE INDEX IF NOT EXISTS idx_suggestions_pending ON personnel_suggested_correction 
            (personnel_id, correction_type, requested_at DESC)
            WHERE status = 'pending';
            """,
            reverse_sql="DROP INDEX IF EXISTS idx_suggestions_pending;"
        ),

        # ========================================
        # GIN Indexes - للبحث النصي السريع
        # ========================================

        # 13. البحث في الأسماء (Full Text Search)
        migrations.RunSQL(
            sql="""
            CREATE INDEX IF NOT EXISTS idx_personnel_name_gin ON personnel_master 
            USING gin (full_name gin_trgm_ops);
            """,
            reverse_sql="DROP INDEX IF EXISTS idx_personnel_name_gin;"
        ),

        # 14. البحث في ملاحظات الأفراد
        migrations.RunSQL(
            sql="""
            CREATE INDEX IF NOT EXISTS idx_personnel_notes_gin ON personnel_master 
            USING gin (notes gin_trgm_ops)
            WHERE notes IS NOT NULL AND notes != '';
            """,
            reverse_sql="DROP INDEX IF EXISTS idx_personnel_notes_gin;"
        ),

        # ========================================
        # JSON Indexes - للبحث في حقول JSON
        # ========================================

        # 15. البحث في proposed_change في StagingRecord
        migrations.RunSQL(
            sql="""
            CREATE INDEX IF NOT EXISTS idx_staging_proposed_change ON services_staging_record 
            USING gin (proposed_change);
            """,
            reverse_sql="DROP INDEX IF EXISTS idx_staging_proposed_change;"
        ),

        # 16. البحث في result في ReconciliationTask
        migrations.RunSQL(
            sql="""
            CREATE INDEX IF NOT EXISTS idx_reconciliation_result ON services_reconciliation_task 
            USING gin (result)
            WHERE result IS NOT NULL;
            """,
            reverse_sql="DROP INDEX IF EXISTS idx_reconciliation_result;"
        ),

        # 17. البحث في data في MonthlySnapshot
        migrations.RunSQL(
            sql="""
            CREATE INDEX IF NOT EXISTS idx_snapshot_data ON services_monthly_snapshot 
            USING gin (data);
            """,
            reverse_sql="DROP INDEX IF EXISTS idx_snapshot_data;"
        ),

        # ========================================
        # Covering Indexes - فهارس تغطية
        # ========================================

        # 18. قائمة الأفراد مع جميع البيانات الأساسية (تجنب الرجوع للجدول)
        migrations.RunSQL(
            sql="""
            CREATE INDEX IF NOT EXISTS idx_personnel_list_covering ON personnel_master 
            (current_department_id, current_status_id)
            INCLUDE (military_number, full_name, current_rank_id, national_id, phone_number);
            """,
            reverse_sql="DROP INDEX IF EXISTS idx_personnel_list_covering;"
        ),

        # 19. سجل الأحداث مع البيانات الكاملة
        migrations.RunSQL(
            sql="""
            CREATE INDEX IF NOT EXISTS idx_eventlog_covering ON services_event_log 
            (service_month, personnel_id)
            INCLUDE (field_name, old_value, new_value, event_date, created_by_id);
            """,
            reverse_sql="DROP INDEX IF EXISTS idx_eventlog_covering;"
        ),

        # ========================================
        # Expression Indexes - فهارس على تعبيرات
        # ========================================

        # 20. البحث بالأحرف الصغيرة في الأسماء
        migrations.RunSQL(
            sql="""
            CREATE INDEX IF NOT EXISTS idx_personnel_name_lower ON personnel_master 
            (LOWER(full_name));
            """,
            reverse_sql="DROP INDEX IF EXISTS idx_personnel_name_lower;"
        ),

        # 21. البحث حسب السنة في تاريخ الميلاد
        migrations.RunSQL(
            sql="""
            CREATE INDEX IF NOT EXISTS idx_personnel_birth_year ON personnel_master 
            (EXTRACT(YEAR FROM birth_date));
            """,
            reverse_sql="DROP INDEX IF EXISTS idx_personnel_birth_year;"
        ),

        # 22. البحث حسب سنوات الخدمة (محذوف - AGE() ليست IMMUTABLE)
        # migrations.RunSQL(
        #     sql="""
        #     CREATE INDEX IF NOT EXISTS idx_personnel_service_years ON personnel_master 
        #     (EXTRACT(YEAR FROM AGE(CURRENT_DATE, join_date)));
        #     """,
        #     reverse_sql="DROP INDEX IF EXISTS idx_personnel_service_years;"
        # ),

        # ========================================
        # Indexes للعلاقات الأجنبية المتكررة
        # ========================================

        # 23. Department children (للهيكل الشجري)
        migrations.RunSQL(
            sql="""
            CREATE INDEX IF NOT EXISTS idx_department_parent_level ON core_department 
            (parent_id, level)
            WHERE parent_id IS NOT NULL;
            """,
            reverse_sql="DROP INDEX IF EXISTS idx_department_parent_level;"
        ),

        # 24. JobTitle by category
        migrations.RunSQL(
            sql="""
            CREATE INDEX IF NOT EXISTS idx_jobtitle_category_name ON core_job_title 
            (category_id, name);
            """,
            reverse_sql="DROP INDEX IF EXISTS idx_jobtitle_category_name;"
        ),

        # ========================================
        # Indexes للتقارير والإحصائيات
        # ========================================

        # 25. عدد الأفراد حسب الإدارة والرتبة (نموذج 1)
        migrations.RunSQL(
            sql="""
            CREATE INDEX IF NOT EXISTS idx_personnel_dept_rank_status ON personnel_master 
            (current_department_id, current_rank_id, current_status_id);
            """,
            reverse_sql="DROP INDEX IF EXISTS idx_personnel_dept_rank_status;"
        ),

        # 26. عدد الأفراد حسب المؤهل
        migrations.RunSQL(
            sql="""
            CREATE INDEX IF NOT EXISTS idx_personnel_qualification ON personnel_master 
            (qualification_id, current_department_id)
            WHERE qualification_id IS NOT NULL;
            """,
            reverse_sql="DROP INDEX IF EXISTS idx_personnel_qualification;"
        ),

        # ========================================
        # Indexes للأمان والتدقيق
        # ========================================

        # 27. AuditLog للعمليات الحساسة فقط
        migrations.RunSQL(
            sql="""
            CREATE INDEX IF NOT EXISTS idx_auditlog_sensitive ON services_audit_log 
            (action, model_name, timestamp DESC)
            WHERE action IN ('DELETE', 'UPDATE');
            """,
            reverse_sql="DROP INDEX IF EXISTS idx_auditlog_sensitive;"
        ),

        # 28. Document verification
        migrations.RunSQL(
            sql="""
            CREATE INDEX IF NOT EXISTS idx_document_hash ON services_document 
            (file_hash)
            WHERE status = 'committed';
            """,
            reverse_sql="DROP INDEX IF EXISTS idx_document_hash;"
        ),

        # ========================================
        # Statistics Update - تحديث الإحصائيات
        # ========================================
        migrations.RunSQL(
            sql="""
            -- تحديث إحصائيات الجداول الرئيسية
            ANALYZE personnel_master;
            ANALYZE services_event_log;
            ANALYZE services_audit_log;
            ANALYZE services_staging_record;
            ANALYZE core_department;
            ANALYZE core_service_status;
            """,
            reverse_sql="-- No reverse needed"
        ),
    ]
