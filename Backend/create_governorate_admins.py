"""
سكريبت إنشاء حسابات مدراء المحافظات
الاستخدام:
    python manage.py shell < create_governorate_admins.py

يُنشئ حساباً لكل محافظة بنمط:
  اسم المستخدم: <رمز المحافظة>_admin
  كلمة المرور: GovernorateAdmin@2025
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

from django.contrib.auth import get_user_model
from infra.authorization.models.role import Role
from infra.authorization.models.user_profile import UserProfile
from core.models.organization import SecurityAdministration

User = get_user_model()
role = Role.objects.get(code='governorate_admin')
DEFAULT_PASSWORD = 'GovernorateAdmin@2025'

# رموز المحافظات بالإنجليزية
SA_CODES = {
    'إدارة أمن أمانة العاصمة': 'sanaa_capital',
    'إدارة أمن صنعاء':          'sanaa',
    'إدارة أمن عدن':            'aden',
    'إدارة أمن الحديدة':        'hodeidah',
    'إدارة أمن ذمار':           'dhamar',
    'إدارة أمن عمران':          'amran',
    'إدارة أمن حجة':            'hajjah',
    'إدارة أمن إب':             'ibb',
    'إدارة أمن البيضاء':        'albayda',
    'إدارة أمن صعدة':           'saada',
    'إدارة أمن تعز':            'taiz',
    'إدارة أمن شبوة':           'shabwah',
    'إدارة أمن الجوف':          'jawf',
    'إدارة أمن الضالع':         'dhale',
    'إدارة أمن مأرب':           'marib',
    'إدارة أمن حضرموت':         'hadramout',
    'إدارة أمن المهرة':         'mahrah',
    'إدارة أمن الضالع':         'dhale',
    'إدارة أمن المحويت':        'mahwit',
    'إدارة أمن لحج':            'lahj',
    'إدارة أمن ريمة':           'raymah',
    'إدارة أمن سقطرى':          'socotra',
    'إدارة أمن أبين':           'abyan',
    'إدارة أمن المحافظة الأولى':'gov1',
}

print("إنشاء حسابات مدراء المحافظات...\n")
created = []
skipped = []

for sa in SecurityAdministration.objects.all():
    username = SA_CODES.get(sa.name)
    if not username:
        # توليد تلقائي من الاسم
        username = sa.name.replace('إدارة أمن ', '').replace(' ', '_') + '_admin'

    if not username.endswith('_admin'):
        username = username + '_admin'

    # تخطي marib_admin إذا كان موجوداً
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
        skipped.append(f'  ↩ {username} (موجود مسبقاً)')
        # تأكد أن UserProfile مرتبط بالإدارة الأمنية الصحيحة
        profile, _ = UserProfile.objects.get_or_create(user=user, defaults={'role': role, 'security_admin': sa})
        if profile.security_admin != sa:
            profile.security_admin = sa
            profile.save()
        continue

    user = User.objects.create_user(
        username=username,
        password=DEFAULT_PASSWORD,
        first_name=f'مدير {sa.name}',
        is_active=True,
        is_staff=True,
    )
    UserProfile.objects.create(
        user=user,
        role=role,
        security_admin=sa,
        supervises_all=False,
    )
    created.append(f'  ✅ {username} → {sa.name}')

print("تم الإنشاء:")
for m in created:
    print(m)

print("\nموجود مسبقاً:")
for m in skipped:
    print(m)

print(f"\n📋 كلمة المرور لجميع الحسابات الجديدة: {DEFAULT_PASSWORD}")
print("\n📋 قائمة الحسابات والمحافظات:")
for profile in UserProfile.objects.filter(role__code='governorate_admin').select_related('user', 'security_admin').order_by('security_admin__name'):
    print(f"  {profile.user.username:25} → {profile.security_admin}")
