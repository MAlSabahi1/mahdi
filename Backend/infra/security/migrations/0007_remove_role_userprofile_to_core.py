"""
Security Migration 0007 — حذف Role و UserProfile من state فقط
═══════════════════════════════════════════════════════════════
الجداول نُقلت فعلياً في core migration 0012.
هنا نزيل النماذج من state الـ security app فقط.
"""
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('security', '0006_merge_20260425_1600'),
        ('core', '0012_move_to_core_rbac'),
    ]

    operations = [
        # حذف UserProfile من state (الجدول انتقل إلى core)
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.DeleteModel(name='UserProfile'),
            ],
            database_operations=[],  # الجدول أُعيد تسميته في core migration
        ),
        # حذف Role من state (الجدول انتقل إلى core)
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.DeleteModel(name='Role'),
            ],
            database_operations=[],  # الجدول أُعيد تسميته في core migration
        ),
    ]
