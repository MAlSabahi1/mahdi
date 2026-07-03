"""
Management Command - تصدير قالب Excel لإدارة معينة
الاستخدام: python manage.py export_template <directorate_id> <service_month>
"""
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from systems.services.export_service import export_template_for_department
from core.models import CentralDepartment

User = get_user_model()


class Command(BaseCommand):
    help = 'تصدير قالب Excel محمي لمديرية معينة'
    
    def add_arguments(self, parser):
        parser.add_argument(
            'directorate_id',
            type=int,
            help='معرف المديرية'
        )
        parser.add_argument(
            'service_month',
            type=str,
            help='شهر الخدمة بصيغة YYYY-MM (مثال: 2026-03)'
        )
        parser.add_argument(
            '--output',
            type=str,
            default='exported_template.xlsx',
            help='مسار ملف الإخراج'
        )
    
    def handle(self, *args, **options):
        directorate_id = options['directorate_id']
        service_month = options['service_month']
        output_path = options['output']
        
        try:
            # التحقق من وجود المديرية
            directorate = CentralDepartment.objects.get(id=directorate_id)
            self.stdout.write(f'المديرية: {directorate.name}')
            
            # الحصول على مستخدم النظام (أو إنشاء واحد للاختبار)
            user, created = User.objects.get_or_create(
                username='system',
                defaults={
                    'is_staff': True,
                    'is_superuser': True
                }
            )
            
            if created:
                user.set_password('system123')
                user.save()
                self.stdout.write(
                    self.style.WARNING('تم إنشاء مستخدم النظام (username: system, password: system123)')
                )
            
            # تصدير القالب
            self.stdout.write('جاري التصدير...')
            excel_file, filename = export_template_for_department(
                department_id=directorate_id,
                service_month=service_month,
                user=user
            )
            
            # حفظ الملف
            with open(output_path, 'wb') as f:
                f.write(excel_file.getvalue())
            
            self.stdout.write(
                self.style.SUCCESS(f'✓ تم التصدير بنجاح: {output_path}')
            )
            self.stdout.write(f'اسم الملف الأصلي: {filename}')
            
            # عرض الإحصائيات
            from systems.services.models import ExportLog
            latest_export = ExportLog.objects.latest('created_at')
            self.stdout.write(f'\nمعرف التصدير: {latest_export.export_id}')
            self.stdout.write(f'عدد الصفوف: {len(latest_export.row_uuids)}')
            self.stdout.write(f'Hash: {latest_export.file_hash[:16]}...')
            
        except CentralDepartment.DoesNotExist:
            raise CommandError(f'المديرية ذات المعرف {directorate_id} غير موجودة')
        except Exception as e:
            raise CommandError(f'خطأ أثناء التصدير: {str(e)}')
