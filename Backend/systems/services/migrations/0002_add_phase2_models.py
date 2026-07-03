# Generated manually for Phase 2
import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0001_initial"),
        ("core", "0004_alter_department_options_and_more"),
        ("personnel", "0003_rawdataimport_suggestedcorrection_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # تحديث StagingRecord
        migrations.AddField(
            model_name="stagingrecord",
            name="upload_batch_id",
            field=models.UUIDField(
                default=uuid.uuid4, verbose_name="معرف دفعة الرفع"
            ),
        ),
        migrations.AddField(
            model_name="stagingrecord",
            name="severity",
            field=models.CharField(
                choices=[
                    ("low", "منخفض - لا يحتاج مستند"),
                    ("high", "عالي - يحتاج مستند"),
                ],
                default="low",
                max_length=10,
                verbose_name="الأهمية",
            ),
        ),
        migrations.AddField(
            model_name="stagingrecord",
            name="requires_document",
            field=models.BooleanField(default=False, verbose_name="يتطلب مستند"),
        ),
        migrations.AddField(
            model_name="stagingrecord",
            name="name_mismatch",
            field=models.BooleanField(default=False, verbose_name="اختلاف في الاسم"),
        ),
        migrations.AddField(
            model_name="stagingrecord",
            name="rank_mismatch",
            field=models.BooleanField(default=False, verbose_name="اختلاف في الرتبة"),
        ),
        migrations.AddField(
            model_name="stagingrecord",
            name="national_id_mismatch",
            field=models.BooleanField(
                default=False, verbose_name="اختلاف في الرقم الوطني"
            ),
        ),
        # إضافة فهارس جديدة لـ StagingRecord
        migrations.AddIndex(
            model_name="stagingrecord",
            index=models.Index(
                fields=["upload_batch_id"], name="services_st_upload__idx"
            ),
        ),
        migrations.AddIndex(
            model_name="stagingrecord",
            index=models.Index(fields=["severity"], name="services_st_severit_idx"),
        ),
        # إنشاء ExportLog
        migrations.CreateModel(
            name="ExportLog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="تاريخ الإنشاء"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث"),
                ),
                (
                    "export_id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        unique=True,
                        verbose_name="معرف التصدير",
                    ),
                ),
                (
                    "service_month",
                    models.CharField(max_length=7, verbose_name="شهر الخدمة"),
                ),
                ("file_hash", models.CharField(max_length=64, verbose_name="Hash الملف")),
                ("row_uuids", models.JSONField(verbose_name="UUIDs الصفوف")),
                (
                    "editable_columns",
                    models.JSONField(verbose_name="الأعمدة القابلة للتعديل"),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "قيد الانتظار"),
                            ("returned", "تم الإرجاع"),
                            ("expired", "منتهي الصلاحية"),
                        ],
                        default="pending",
                        max_length=20,
                        verbose_name="الحالة",
                    ),
                ),
                (
                    "department",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="export_logs",
                        to="core.department",
                        verbose_name="الإدارة",
                    ),
                ),
                (
                    "exported_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="exports",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="صدّر بواسطة",
                    ),
                ),
            ],
            options={
                "verbose_name": "سجل تصدير",
                "verbose_name_plural": "سجلات التصدير",
                "db_table": "services_export_log",
                "ordering": ["-created_at"],
            },
        ),
        # إنشاء RejectionLog
        migrations.CreateModel(
            name="RejectionLog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="تاريخ الإنشاء"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث"),
                ),
                (
                    "service_month",
                    models.CharField(max_length=7, verbose_name="شهر الخدمة"),
                ),
                (
                    "proposed_status",
                    models.TextField(verbose_name="الحالة المقترحة"),
                ),
                (
                    "rejection_reason",
                    models.TextField(verbose_name="سبب الرفض"),
                ),
                (
                    "rejected_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الرفض"),
                ),
                (
                    "department",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="rejections",
                        to="core.department",
                        verbose_name="الإدارة",
                    ),
                ),
                (
                    "personnel",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="rejections",
                        to="personnel.personnelmaster",
                        verbose_name="الفرد",
                    ),
                ),
                (
                    "rejected_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="rejections",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="رفض بواسطة",
                    ),
                ),
                (
                    "staging_record",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="rejections",
                        to="services.stagingrecord",
                        verbose_name="السجل المؤقت",
                    ),
                ),
            ],
            options={
                "verbose_name": "سجل رفض",
                "verbose_name_plural": "سجلات الرفوضات",
                "db_table": "services_rejection_log",
                "ordering": ["-rejected_at"],
            },
        ),
        # إنشاء DepartmentCompliance
        migrations.CreateModel(
            name="DepartmentCompliance",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="تاريخ الإنشاء"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث"),
                ),
                (
                    "service_month",
                    models.CharField(max_length=7, verbose_name="شهر الخدمة"),
                ),
                (
                    "submitted_at",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="تاريخ التسليم"
                    ),
                ),
                (
                    "error_count",
                    models.IntegerField(default=0, verbose_name="عدد الأخطاء"),
                ),
                (
                    "rejected_changes_count",
                    models.IntegerField(default=0, verbose_name="عدد التغييرات المرفوضة"),
                ),
                (
                    "late_days",
                    models.IntegerField(default=0, verbose_name="أيام التأخير"),
                ),
                (
                    "quality_score",
                    models.IntegerField(default=100, verbose_name="درجة الجودة"),
                ),
                (
                    "department",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="compliance_records",
                        to="core.department",
                        verbose_name="الإدارة",
                    ),
                ),
            ],
            options={
                "verbose_name": "التزام إدارة",
                "verbose_name_plural": "التزام الإدارات",
                "db_table": "services_department_compliance",
                "ordering": ["-service_month", "department"],
                "unique_together": {("department", "service_month")},
            },
        ),
        # إضافة فهارس
        migrations.AddIndex(
            model_name="exportlog",
            index=models.Index(fields=["export_id"], name="services_ex_export__idx"),
        ),
        migrations.AddIndex(
            model_name="exportlog",
            index=models.Index(
                fields=["department", "service_month"], name="services_ex_departm_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="exportlog",
            index=models.Index(fields=["status"], name="services_ex_status_idx"),
        ),
        migrations.AddIndex(
            model_name="rejectionlog",
            index=models.Index(
                fields=["department", "service_month"], name="services_re_departm_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="rejectionlog",
            index=models.Index(
                fields=["rejected_at"], name="services_re_rejecte_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="departmentcompliance",
            index=models.Index(
                fields=["service_month"], name="services_de_service_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="departmentcompliance",
            index=models.Index(
                fields=["quality_score"], name="services_de_quality_idx"
            ),
        ),
    ]
