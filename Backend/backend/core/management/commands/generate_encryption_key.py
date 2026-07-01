"""
Management Command - توليد مفتاح تشفير جديد
الاستخدام:
    python manage.py generate_encryption_key
    
التحسينات:
- التحقق من وجود مفتاح قديم
- تسجيل العملية في AuditLog
- نسخ إلى Clipboard (اختياري)
"""
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone
from core.encryption import generate_encryption_key
import os


class Command(BaseCommand):
    help = 'توليد مفتاح تشفير جديد لحماية البيانات الحساسة'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='فرض توليد مفتاح جديد حتى لو كان هناك مفتاح موجود'
        )
        parser.add_argument(
            '--copy',
            action='store_true',
            help='نسخ المفتاح إلى Clipboard تلقائياً'
        )
    
    def handle(self, *args, **options):
        # فحص بيئة الإنتاج
        if not settings.DEBUG and not options['force']:
            self.stdout.write(self.style.ERROR('\n⚠️  خطير: أنت تحاول توليد مفتاح في بيئة الإنتاج (Production)!\n'))
            self.stdout.write(self.style.ERROR('⚠️  هذا سيجعل جميع البيانات المشفرة غير قابلة للقراءة!\n'))
            self.stdout.write(self.style.WARNING('⚠️  استخدم --force إذا كنت متأكداً تماماً\n'))
            return
        
        # التحقق من وجود مفتاح قديم
        existing_key = getattr(settings, 'FIELD_ENCRYPTION_KEY', None)
        
        if existing_key and not options['force']:
            self.stdout.write(self.style.WARNING('\n⚠️  تحذير: يوجد مفتاح تشفير موجود بالفعل!\n'))
            self.stdout.write(self.style.ERROR('⚠️  استبدال المفتاح سيجعل جميع البيانات المشفرة غير قابلة للقراءة!\n'))
            self.stdout.write(self.style.WARNING('⚠️  إذا كنت متأكداً، استخدم --force\n'))
            
            confirm = input('هل تريد المتابعة؟ (yes/no): ')
            if confirm.lower() != 'yes':
                self.stdout.write(self.style.SUCCESS('\n✅ تم الإلغاء. المفتاح القديم لم يتغير.\n'))
                return
        
        # توليد المفتاح
        key = generate_encryption_key()
        
        self.stdout.write(self.style.SUCCESS('\n✅ تم توليد مفتاح التشفير بنجاح!\n'))
        self.stdout.write(self.style.WARNING('⚠️  احفظ هذا المفتاح في مكان آمن!\n'))
        self.stdout.write(self.style.WARNING('⚠️  لا تشارك هذا المفتاح مع أحد!\n'))
        self.stdout.write(self.style.WARNING('⚠️  فقدان هذا المفتاح يعني فقدان البيانات المشفرة!\n'))
        
        self.stdout.write('\n' + '='*70)
        self.stdout.write(f'\nFIELD_ENCRYPTION_KEY={key}\n')
        self.stdout.write('='*70 + '\n')
        
        self.stdout.write(self.style.SUCCESS('\n📝 أضف هذا المفتاح إلى ملف .env:\n'))
        self.stdout.write(f'   FIELD_ENCRYPTION_KEY={key}\n')
        
        self.stdout.write(self.style.SUCCESS('\n📝 أو أضفه إلى settings.py:\n'))
        self.stdout.write(f"   FIELD_ENCRYPTION_KEY = '{key}'\n")
        
        # نسخ إلى Clipboard (اختياري)
        if options['copy']:
            try:
                import pyperclip
                pyperclip.copy(key)
                self.stdout.write(self.style.SUCCESS('\n✅ تم نسخ المفتاح إلى Clipboard!\n'))
            except ImportError:
                self.stdout.write(self.style.WARNING('\n⚠️  pyperclip غير مثبت. لم يتم النسخ.\n'))
                self.stdout.write('   pip install pyperclip\n')
        
        # تسجيل في AuditLog
        try:
            from infra.audit.models import AuditLog
            from django.contrib.auth import get_user_model
            
            User = get_user_model()
            # محاولة الحصول على superuser
            admin_user = User.objects.filter(is_superuser=True).first()
            
            if admin_user:
                AuditLog.objects.create(
                    user=admin_user,
                    action='CREATE',
                    model_name='EncryptionKey',
                    object_id='new_key',
                    new_data={'generated_at': str(timezone.now())},
                    ip_address='127.0.0.1'
                )
                self.stdout.write(self.style.SUCCESS('\n✅ تم تسجيل العملية في AuditLog\n'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'\n⚠️  فشل التسجيل في AuditLog: {e}\n'))
