"""
Management Command - استيراد ملف خدمات معدل
الاستخدام:
    python manage.py import_service_file <file_path> <export_id> [--service-month YYYY-MM]
"""
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from systems.services.import_service import import_service_file, ImportValidationError
import json

User = get_user_model()


class Command(BaseCommand):
    help = 'استيراد ملف خدمات معدل من إدارة'
    
    def add_arguments(self, parser):
        parser.add_argument(
            'file_path',
            type=str,
            help='مسار ملف Excel المراد استيراده'
        )
        parser.add_argument(
            'export_id',
            type=str,
            help='معرف التصدير (UUID)'
        )
        parser.add_argument(
            '--service-month',
            type=str,
            help='شهر الخدمة (YYYY-MM)',
            default=None
        )
        parser.add_argument(
            '--user-id',
            type=int,
            help='معرف المستخدم (افتراضي: 1)',
            default=1
        )
    
    def handle(self, *args, **options):
        file_path = options['file_path']
        export_id = options['export_id']
        service_month = options['service_month']
        user_id = options['user_id']
        
        # الحصول على المستخدم
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise CommandError(f'المستخدم بالمعرف {user_id} غير موجود')
        
        # قراءة الملف
        try:
            with open(file_path, 'rb') as f:
                file_content = f.read()
        except FileNotFoundError:
            raise CommandError(f'الملف {file_path} غير موجود')
        except Exception as e:
            raise CommandError(f'خطأ في قراءة الملف: {str(e)}')
        
        # استيراد الملف
        self.stdout.write('جاري استيراد الملف...')
        
        try:
            report = import_service_file(
                file_content=file_content,
                export_id=export_id,
                user=user,
                service_month=service_month
            )
            
            # عرض التقرير
            self.stdout.write(self.style.SUCCESS('\n✅ تم الاستيراد بنجاح!\n'))
            
            self.stdout.write(self.style.WARNING('📊 الإحصائيات:'))
            self.stdout.write(f"  - الإدارة: {report['directorate']}")
            self.stdout.write(f"  - شهر الخدمة: {report['service_month']}")
            self.stdout.write(f"  - معرف الدفعة: {report['batch_id']}")
            self.stdout.write(f"  - إجمالي الصفوف: {report['stats']['total_rows']}")
            self.stdout.write(f"  - التغييرات المكتشفة: {report['stats']['changes_detected']}")
            self.stdout.write(f"    • أخضر (لا يحتاج مستند): {report['stats']['green_changes']}")
            self.stdout.write(f"    • أصفر (يحتاج مستند): {report['stats']['yellow_changes']}")
            self.stdout.write(f"    • أحمر (غير متوقع): {report['stats']['red_changes']}")
            self.stdout.write(f"  - الأخطاء: {report['stats']['errors']}")
            self.stdout.write(f"  - التحذيرات: {report['stats']['warnings']}")
            
            # عرض الأخطاء
            if report['errors']:
                self.stdout.write(self.style.ERROR('\n❌ الأخطاء:'))
                for error in report['errors'][:10]:  # أول 10 أخطاء
                    self.stdout.write(
                        f"  - [{error.get('sheet')}:{error.get('row')}] "
                        f"{error.get('error')}"
                    )
                if len(report['errors']) > 10:
                    self.stdout.write(f"  ... و {len(report['errors']) - 10} خطأ آخر")
            
            # عرض التحذيرات
            if report['warnings']:
                self.stdout.write(self.style.WARNING('\n⚠️  التحذيرات:'))
                for warning in report['warnings'][:10]:  # أول 10 تحذيرات
                    self.stdout.write(
                        f"  - [{warning.get('sheet')}:{warning.get('row')}] "
                        f"{warning.get('warning')}"
                    )
                if len(report['warnings']) > 10:
                    self.stdout.write(f"  ... و {len(report['warnings']) - 10} تحذير آخر")
            
            # الرسالة الملخصة
            self.stdout.write(f"\n📝 {report['message']}")
            
            # حفظ التقرير كـ JSON
            report_file = f"import_report_{report['batch_id']}.json"
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2, default=str)
            self.stdout.write(
                self.style.SUCCESS(f"\n💾 تم حفظ التقرير الكامل في: {report_file}")
            )
            
        except ImportValidationError as e:
            raise CommandError(f'خطأ في التحقق من صحة الملف: {str(e)}')
        except Exception as e:
            raise CommandError(f'خطأ غير متوقع: {str(e)}')
