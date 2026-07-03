"""
Core Migration 0012 — نقل RBAC + Audit + Notification إلى core
═══════════════════════════════════════════════════════════════════
يستخدم SeparateDatabaseAndState لنقل الجداول بدون فقدان البيانات:
- Role: security_role → core_role
- UserProfile: security_user_profile → core_user_profile
- AuditLog: services_audit_log → core_audit_log
- NotificationRecord: services_notification → core_notification

+ جداول جديدة تماماً:
- Permission (core_permission)
- RolePermission (core_role_permission)
- UserRole (core_user_role)
- LoginAuditLog (core_login_audit_log)
"""
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_directorate_node_type_position_allowed_categories_and_more'),
        ('security', '0006_merge_20260425_1600'),
        ('services', '0013_custom_templates'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # ══════════════════════════════════════════════════════════
        # 1. جداول جديدة تماماً (CreateModel عادي)
        # ══════════════════════════════════════════════════════════
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')),
                ('code', models.CharField(max_length=100, unique=True, verbose_name='الكود')),
                ('module', models.CharField(max_length=50, verbose_name='النظام الفرعي')),
                ('action', models.CharField(max_length=50, verbose_name='الفعل')),
                ('scope', models.CharField(default='all', max_length=50, verbose_name='النطاق')),
                ('label', models.CharField(max_length=200, verbose_name='الوصف بالعربي')),
                ('description', models.TextField(blank=True, verbose_name='شرح تفصيلي')),
                ('is_active', models.BooleanField(default=True, verbose_name='نشطة')),
                ('requires_dual_auth', models.BooleanField(default=False, verbose_name='تتطلب تفويض مزدوج')),
                ('is_system', models.BooleanField(default=True, verbose_name='صلاحية نظامية')),
            ],
            options={
                'verbose_name': 'صلاحية',
                'verbose_name_plural': 'الصلاحيات',
                'db_table': 'core_permission',
                'ordering': ['module', 'action', 'scope'],
                'unique_together': {('module', 'action', 'scope')},
            },
        ),
        migrations.CreateModel(
            name='LoginAuditLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username_attempted', models.CharField(max_length=150, verbose_name='اسم المستخدم المُدخل')),
                ('action', models.CharField(choices=[
                    ('LOGIN_SUCCESS', 'دخول ناجح'), ('LOGIN_FAILED', 'دخول فاشل'),
                    ('LOGOUT', 'خروج'), ('TOKEN_REFRESH', 'تجديد توكن'),
                    ('ACCOUNT_LOCKED', 'قفل حساب'), ('ACCOUNT_UNLOCKED', 'فتح حساب'),
                    ('PASSWORD_CHANGED', 'تغيير كلمة مرور'), ('PASSWORD_RESET', 'إعادة تعيين كلمة مرور'),
                ], max_length=20, verbose_name='الحدث')),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True, verbose_name='عنوان IP')),
                ('user_agent', models.TextField(blank=True, default='', verbose_name='User Agent')),
                ('failure_reason', models.CharField(blank=True, default='', max_length=30, verbose_name='سبب الفشل')),
                ('extra_data', models.JSONField(blank=True, null=True, verbose_name='بيانات إضافية')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='التوقيت')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                           related_name='login_audit_logs', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'سجل دخول',
                'verbose_name_plural': 'سجلات الدخول',
                'db_table': 'core_login_audit_log',
                'ordering': ['-timestamp'],
            },
        ),

        # ══════════════════════════════════════════════════════════
        # 2. نقل Role من security إلى core
        # ══════════════════════════════════════════════════════════
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.CreateModel(
                    name='Role',
                    fields=[
                        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                        ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')),
                        ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')),
                        ('name', models.CharField(max_length=100, unique=True, verbose_name='اسم الدور')),
                        ('code', models.CharField(max_length=50, unique=True, verbose_name='الرمز الداخلي')),
                        ('description', models.TextField(blank=True, verbose_name='الوصف')),
                        ('is_active', models.BooleanField(default=True, verbose_name='نشط')),
                        ('is_system_role', models.BooleanField(default=False, verbose_name='دور نظامي')),
                        ('permissions', models.JSONField(default=list, verbose_name='صلاحيات قديمة (legacy)')),
                        ('visible_pages', models.JSONField(default=list, verbose_name='الصفحات المسموحة')),
                        ('priority', models.IntegerField(default=0, verbose_name='الأولوية')),
                        ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                                          related_name='created_roles', to=settings.AUTH_USER_MODEL)),
                    ],
                    options={
                        'verbose_name': 'دور',
                        'verbose_name_plural': 'الأدوار',
                        'db_table': 'core_role',
                        'ordering': ['-priority', 'name'],
                    },
                ),
            ],
            database_operations=[
                migrations.RunSQL(
                    sql='ALTER TABLE security_role RENAME TO core_role;',
                    reverse_sql='ALTER TABLE core_role RENAME TO security_role;',
                ),
            ],
        ),

        # M2M for Role.permissions_m2m
        migrations.CreateModel(
            name='RolePermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='role_permissions', to='core.role')),
                ('permission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='role_permissions', to='core.permission')),
                ('granted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'core_role_permission',
                'unique_together': {('role', 'permission')},
            },
        ),
        migrations.AddField(
            model_name='role',
            name='permissions_m2m',
            field=models.ManyToManyField(blank=True, related_name='roles', through='core.RolePermission', to='core.permission', verbose_name='الصلاحيات'),
        ),

        # ══════════════════════════════════════════════════════════
        # 3. نقل UserProfile من security إلى core
        # ══════════════════════════════════════════════════════════
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.CreateModel(
                    name='UserProfile',
                    fields=[
                        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                        ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')),
                        ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')),
                        ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
                        ('role', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='primary_users', to='core.role', verbose_name='الدور الأساسي')),
                        ('governorate', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='staff_profiles', to='core.governorate')),
                        ('directorate', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='staff_profiles', to='core.directorate')),
                        ('division', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='staff_profiles', to='core.division')),
                        ('unit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='staff_profiles', to='core.unit')),
                        ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='staff_profiles', to='core.department')),
                        ('supervises_all_departments', models.BooleanField(default=False)),
                        ('can_override_lock', models.BooleanField(default=False)),
                        ('requires_two_factor', models.BooleanField(default=False)),
                        ('is_account_locked', models.BooleanField(default=False)),
                        ('failed_login_attempts', models.IntegerField(default=0)),
                        ('locked_until', models.DateTimeField(blank=True, null=True)),
                        ('last_login_ip', models.GenericIPAddressField(blank=True, null=True)),
                        ('last_login_user_agent', models.TextField(blank=True)),
                        ('language', models.CharField(default='ar', max_length=5)),
                        ('admin_notes', models.TextField(blank=True)),
                    ],
                    options={
                        'db_table': 'core_user_profile',
                        'verbose_name': 'ملف مستخدم',
                        'verbose_name_plural': 'ملفات المستخدمين',
                    },
                ),
            ],
            database_operations=[
                migrations.RunSQL(
                    sql='ALTER TABLE security_user_profile RENAME TO core_user_profile;',
                    reverse_sql='ALTER TABLE core_user_profile RENAME TO security_user_profile;',
                ),
            ],
        ),
        # M2M for supervised_departments (already exists — just rename)
        migrations.SeparateDatabaseAndState(
            state_operations=[],
            database_operations=[
                migrations.RunSQL(
                    sql='ALTER TABLE IF EXISTS security_user_profile_supervised_departments RENAME TO core_userprofile_supervised_departments;',
                    reverse_sql='ALTER TABLE IF EXISTS core_userprofile_supervised_departments RENAME TO security_user_profile_supervised_departments;',
                ),
            ],
        ),
        # UserRole through table
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_roles', to=settings.AUTH_USER_MODEL)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_roles', to='core.userprofile')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_role_assignments', to='core.role')),
                ('is_active', models.BooleanField(default=True)),
                ('assigned_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='role_assignments_given', to=settings.AUTH_USER_MODEL)),
                ('assigned_at', models.DateTimeField(auto_now_add=True)),
                ('expires_at', models.DateTimeField(blank=True, null=True)),
                ('notes', models.TextField(blank=True)),
            ],
            options={
                'db_table': 'core_user_role',
                'unique_together': {('user', 'role')},
            },
        ),
        migrations.AddField(
            model_name='userprofile',
            name='supervised_departments',
            field=models.ManyToManyField(blank=True, related_name='supervisors', to='core.department'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='additional_roles',
            field=models.ManyToManyField(blank=True, related_name='additional_users', through='core.UserRole', to='core.role'),
        ),

        # ══════════════════════════════════════════════════════════
        # 4. نقل AuditLog من services إلى core
        # ══════════════════════════════════════════════════════════
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.CreateModel(
                    name='AuditLog',
                    fields=[
                        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                        ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                                    related_name='audit_logs', to=settings.AUTH_USER_MODEL)),
                        ('action', models.CharField(max_length=50)),
                        ('model_name', models.CharField(max_length=100)),
                        ('object_id', models.CharField(max_length=100)),
                        ('old_data', models.JSONField(blank=True, null=True)),
                        ('new_data', models.JSONField(blank=True, null=True)),
                        ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                        ('user_agent', models.TextField(blank=True, default='')),
                        ('timestamp', models.DateTimeField(auto_now_add=True)),
                        ('signature', models.CharField(blank=True, max_length=64)),
                    ],
                    options={
                        'db_table': 'core_audit_log',
                        'ordering': ['-timestamp'],
                    },
                ),
            ],
            database_operations=[
                migrations.RunSQL(
                    sql='ALTER TABLE services_audit_log RENAME TO core_audit_log;',
                    reverse_sql='ALTER TABLE core_audit_log RENAME TO services_audit_log;',
                ),
            ],
        ),

        # ══════════════════════════════════════════════════════════
        # 5. نقل NotificationRecord من services إلى core
        # ══════════════════════════════════════════════════════════
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.CreateModel(
                    name='NotificationRecord',
                    fields=[
                        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                        ('created_at', models.DateTimeField(auto_now_add=True)),
                        ('updated_at', models.DateTimeField(auto_now=True)),
                        ('notification_type', models.CharField(max_length=30)),
                        ('title', models.CharField(max_length=200)),
                        ('message', models.TextField()),
                        ('priority', models.CharField(default='normal', max_length=10)),
                        ('target_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL)),
                        ('triggered_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='triggered_notifications', to=settings.AUTH_USER_MODEL)),
                        ('is_read', models.BooleanField(default=False)),
                        ('read_at', models.DateTimeField(blank=True, null=True)),
                        ('related_object_type', models.CharField(blank=True, max_length=100)),
                        ('related_object_id', models.CharField(blank=True, max_length=100)),
                        ('action_url', models.CharField(blank=True, max_length=500)),
                        ('extra_data', models.JSONField(blank=True, null=True)),
                    ],
                    options={
                        'db_table': 'core_notification',
                        'ordering': ['-created_at'],
                    },
                ),
            ],
            database_operations=[
                migrations.RunSQL(
                    sql='ALTER TABLE services_notification RENAME TO core_notification;',
                    reverse_sql='ALTER TABLE core_notification RENAME TO services_notification;',
                ),
                migrations.RunSQL(
                    sql="""
                    ALTER TABLE core_notification ADD COLUMN IF NOT EXISTS triggered_by_id INTEGER NULL REFERENCES accounts_user(id) DEFERRABLE INITIALLY DEFERRED;
                    ALTER TABLE core_notification ADD COLUMN IF NOT EXISTS related_object_type VARCHAR(100) DEFAULT '' NOT NULL;
                    ALTER TABLE core_notification ADD COLUMN IF NOT EXISTS related_object_id VARCHAR(100) DEFAULT '' NOT NULL;
                    ALTER TABLE core_notification ADD COLUMN IF NOT EXISTS extra_data JSONB NULL;
                    """,
                    reverse_sql="""
                    ALTER TABLE core_notification DROP COLUMN IF EXISTS triggered_by_id;
                    ALTER TABLE core_notification DROP COLUMN IF EXISTS related_object_type;
                    ALTER TABLE core_notification DROP COLUMN IF EXISTS related_object_id;
                    ALTER TABLE core_notification DROP COLUMN IF EXISTS extra_data;
                    """
                ),
            ],
        ),

        # ══════════════════════════════════════════════════════════
        # 6. فهارس
        # ══════════════════════════════════════════════════════════
        migrations.AddIndex(model_name='permission', index=models.Index(fields=['module'], name='core_perm_module_idx')),
        migrations.AddIndex(model_name='permission', index=models.Index(fields=['is_active'], name='core_perm_active_idx')),
        migrations.AddIndex(model_name='role', index=models.Index(fields=['code'], name='core_role_code_idx')),
        migrations.AddIndex(model_name='role', index=models.Index(fields=['is_active'], name='core_role_active_idx')),
        migrations.AddIndex(model_name='loginauditlog', index=models.Index(fields=['action', 'timestamp'], name='core_login_action_ts_idx')),
        migrations.AddIndex(model_name='loginauditlog', index=models.Index(fields=['user', 'timestamp'], name='core_login_user_ts_idx')),
        migrations.AddIndex(model_name='loginauditlog', index=models.Index(fields=['timestamp'], name='core_login_ts_idx')),
    ]
