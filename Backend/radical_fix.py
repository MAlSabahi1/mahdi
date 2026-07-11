import os
import django
import sys
from django.db import connection

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

def radical_fix():
    print("🚀 بدء الحل الجذري لتنظيف قاعدة البيانات من التعارضات...")
    with connection.cursor() as cursor:
        # 1. إجبار حذف الفهرس/الشرط (Constraint) الذي يسبب المشكلة
        print("جاري حذف الشرط unique_service_workflow_order إن وجد...")
        try:
            cursor.execute("DROP INDEX IF EXISTS unique_service_workflow_order CASCADE;")
        except Exception as e:
            print(f"ملاحظة عند حذف الفهرس: {e}")

        # 2. البحث عن الجدول المرتبط بالشرط (إن وجد كـ Constraint) وحذفه
        try:
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.table_constraints 
                WHERE constraint_name = 'unique_service_workflow_order';
            """)
            rows = cursor.fetchall()
            for row in rows:
                table_name = row[0]
                print(f"تم العثور على الشرط في الجدول {table_name}، جاري حذفه...")
                cursor.execute(f"ALTER TABLE {table_name} DROP CONSTRAINT IF EXISTS unique_service_workflow_order CASCADE;")
        except Exception as e:
            print(f"ملاحظة عند البحث عن الشرط: {e}")

        # 3. التأكد من حذف جداول الترحيل 0023 من الجذور لتفادي DuplicateTable
        print("جاري تنظيف جداول المرحلة 0023...")
        cursor.execute('DROP TABLE IF EXISTS services_service_workflow_step CASCADE;')
        cursor.execute('DROP TABLE IF EXISTS services_workflow_stage CASCADE;')

    print("✅ تم التنظيف الجذري بنجاح! يمكنك الآن تشغيل أوامر التهيئة.")

if __name__ == "__main__":
    radical_fix()
