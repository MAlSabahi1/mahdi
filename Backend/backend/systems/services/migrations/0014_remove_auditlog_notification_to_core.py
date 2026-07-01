"""
Services Migration 0014 — حذف AuditLog و NotificationRecord من state فقط
═══════════════════════════════════════════════════════════════════════════
الجداول نُقلت فعلياً في core migration 0012.
هنا نزيل النماذج من state الـ services app فقط.
"""
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0013_custom_templates'),
        ('core', '0012_move_to_core_rbac'),
    ]

    operations = [
        # حذف AuditLog من state (الجدول انتقل إلى core)
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.DeleteModel(name='AuditLog'),
            ],
            database_operations=[],  # الجدول أُعيد تسميته في core migration
        ),
        # حذف NotificationRecord من state (الجدول انتقل إلى core)
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.DeleteModel(name='NotificationRecord'),
            ],
            database_operations=[],  # الجدول أُعيد تسميته في core migration
        ),
    ]
