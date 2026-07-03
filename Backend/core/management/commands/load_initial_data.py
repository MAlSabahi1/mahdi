"""
Command لتحميل البيانات الأولية
"""
from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'تحميل البيانات الأولية (الرتب، الحالات، المؤهلات، الفئات)'

    def handle(self, *args, **options):
        self.stdout.write('🔄 جاري تحميل البيانات الأولية...\n')
        
        # تحميل الرتب
        self.stdout.write('📊 تحميل الرتب...')
        call_command('loaddata', 'initial_data.json')
        self.stdout.write(self.style.SUCCESS('✅ تم تحميل 17 رتبة'))
        
        # تحميل الحالات الخدمية
        self.stdout.write('📊 تحميل الحالات الخدمية...')
        call_command('loaddata', 'service_statuses.json')
        self.stdout.write(self.style.SUCCESS('✅ تم تحميل 16 حالة خدمية'))
        
        # تحميل المؤهلات والفئات
        self.stdout.write('📊 تحميل المؤهلات والفئات...')
        call_command('loaddata', 'qualifications_categories.json')
        self.stdout.write(self.style.SUCCESS('✅ تم تحميل 8 مؤهلات و 5 فئات'))
        
        self.stdout.write(self.style.SUCCESS('\n✅ تم تحميل جميع البيانات الأولية بنجاح!'))
