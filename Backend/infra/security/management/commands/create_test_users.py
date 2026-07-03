from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import Governorate, Directorate
from infra.authorization.models import UserProfile, Role
from infra.accounts.models.security import SecurityProfile

User = get_user_model()

class Command(BaseCommand):
    help = 'إنشاء مستخدمين تجريبيين للنظام'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('🔄 جاري إنشاء المستخدمين التجريبيين...'))
        
        # إنشاء الأدوار
        self.stdout.write('📋 إنشاء الأدوار...')
        try:
            admin_role = Role.objects.get(code='ADMIN')
        except Role.DoesNotExist:
            admin_role = Role.objects.create(
                code='ADMIN',
                name='مدير النظام',
                priority=100
            )
        
        try:
            hr_role = Role.objects.get(code='HR_MANAGER')
        except Role.DoesNotExist:
            hr_role = Role.objects.create(
                code='HR_MANAGER',
                name='مدير الموارد البشرية',
                priority=80
            )
        
        try:
            viewer_role = Role.objects.get(code='VIEWER')
        except Role.DoesNotExist:
            viewer_role = Role.objects.create(
                code='VIEWER',
                name='مستخدم عادي',
                priority=20
            )

        # إنشاء محافظة ومديرية
        self.stdout.write('🏢 إنشاء المحافظات والمديريات...')
        gov, _ = Governorate.objects.get_or_create(
            code='MAR',
            defaults={'name': 'محافظة المحافظة الأولى'}
        )
        hr_dept, _ = Directorate.objects.get_or_create(
            code='HR',
            governorate=gov,
            defaults={'name': 'الموارد البشرية'}
        )

        # إنشاء المستخدمين
        self.stdout.write('👥 إنشاء المستخدمين...')
        users_data = [
            {
                'username': 'admin',
                'password': 'admin123',
                'first_name': 'مدير',
                'last_name': 'النظام',
                'email': 'admin@hrms.local',
                'role': admin_role,
                'is_superuser': True,
                'is_staff': True,
            },
            {
                'username': 'hr_manager',
                'password': 'hr123',
                'first_name': 'أحمد',
                'last_name': 'محمد',
                'email': 'hr@hrms.local',
                'role': hr_role,
            },
            {
                'username': 'viewer',
                'password': 'viewer123',
                'first_name': 'محمد',
                'last_name': 'علي',
                'email': 'viewer@hrms.local',
                'role': viewer_role,
            }
        ]

        for user_data in users_data:
            username = user_data['username']
            
            # حذف المستخدم إذا كان موجوداً
            if User.objects.filter(username=username).exists():
                User.objects.filter(username=username).delete()
                self.stdout.write(f'  ⚠️  حذف المستخدم القديم: {username}')
            
            # إنشاء المستخدم
            user = User.objects.create_user(
                username=username,
                password=user_data['password'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                email=user_data.get('email', ''),
                is_superuser=user_data.get('is_superuser', False),
                is_staff=user_data.get('is_staff', False)
            )
            
            # إنشاء SecurityProfile تلقائياً
            SecurityProfile.objects.create(user=user)
            
            # إنشاء الملف الشخصي
            profile = UserProfile.objects.create(
                user=user,
                role=user_data['role'],
                directorate=hr_dept
            )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'  ✅ {username} (كلمة المرور: {user_data["password"]})'
                )
            )

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS('✅ تم إنشاء المستخدمين بنجاح!'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write('')
        self.stdout.write('المستخدمون المتاحون:')
        self.stdout.write('')
        self.stdout.write('1. مدير النظام (Superuser):')
        self.stdout.write('   Username: admin')
        self.stdout.write('   Password: admin123')
        self.stdout.write('   الصلاحيات: جميع الصلاحيات')
        self.stdout.write('')
        self.stdout.write('2. مدير الموارد البشرية:')
        self.stdout.write('   Username: hr_manager')
        self.stdout.write('   Password: hr123')
        self.stdout.write('   الصلاحيات: إدارة الأفراد، التقارير')
        self.stdout.write('')
        self.stdout.write('3. مستخدم عادي:')
        self.stdout.write('   Username: viewer')
        self.stdout.write('   Password: viewer123')
        self.stdout.write('   الصلاحيات: عرض فقط')
        self.stdout.write('')
        self.stdout.write(self.style.WARNING('⚠️  تذكير: غيّر كلمات المرور في بيئة الإنتاج!'))
        self.stdout.write('')
