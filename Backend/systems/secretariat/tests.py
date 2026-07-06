import uuid
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework.test import APIClient
from decimal import Decimal

from core.models import (
    SecurityAdministration, GeoGovernorate, CentralDepartment, 
    Rank, ServiceStatus, Qualification
)
from core.models.notification import NotificationRecord
from infra.authorization.models import Role, UserProfile
from systems.personnel.models import PersonnelMaster
from systems.secretariat.models import (
    Correspondence, CorrespondenceReferral, InventoryItem, InventoryRequest, FinancialAllocation, Expense
)

User = get_user_model()


class SecretariatSystemTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        from django.core.management import call_command
        call_command('seed_permissions')
        
        # 1. تهيئة الكيانات الإدارية العامة
        cls.gov = GeoGovernorate.objects.create(name_ar='المحافظة التجريبية', name_en='Test Gov')
        cls.sec_admin = SecurityAdministration.objects.create(
            name="إدارة أمن السكرتارية", 
            code="SEC_TEST",
            geo_governorate=cls.gov
        )
        cls.dept = CentralDepartment.objects.create(
            name='إدارة الأمن العام', 
            code='GEN_SEC',
            security_admin=cls.sec_admin
        )
        
        cls.rank = Rank.objects.create(name='ملازم', order=1)
        cls.status_active = ServiceStatus.objects.create(
            name='على رأس العمل', classification='active_full'
        )
        cls.qualification = Qualification.objects.create(name='بكالوريوس', order=2)
        
        # 2. تهيئة الموظفين
        cls.personnel = PersonnelMaster.objects.create(
            military_number='9999999', national_id='99999999999',
            full_name='العقيد المشرف', birth_date='1980-01-01', join_date='2000-01-01',
            current_rank=cls.rank, central_department=cls.dept,
            current_status=cls.status_active, qualification=cls.qualification,
        )
        
        # 3. تهيئة الأدوار والصلاحيات
        cls.admin_role = Role.objects.get(code='super_admin')
        cls.chief_role = Role.objects.get(code='services_chief')
        cls.data_entry_role = Role.objects.get(code='data_entry')
        
        # إسناد صلاحية عرض السكرتارية لدور مدخل البيانات لغرض الفحص
        from infra.authorization.models.permission import Permission
        from infra.authorization.models.role import RolePermission
        from infra.authorization.registry.permissions import Perms
        view_perm = Permission.objects.get(code=Perms.SECRETARIAT_VIEW)
        RolePermission.objects.get_or_create(role=cls.data_entry_role, permission=view_perm)
        
        # 4. تهيئة المستخدمين والاختبارات
        cls.admin_user = User.objects.create_user(username='admin_test', password='testpass123')
        UserProfile.objects.create(user=cls.admin_user, role=cls.admin_role, security_admin=cls.sec_admin, supervises_all=True)

        cls.chief_user = User.objects.create_user(username='chief_test', password='testpass123')
        UserProfile.objects.create(user=cls.chief_user, role=cls.chief_role, security_admin=cls.sec_admin)

        cls.entry_user = User.objects.create_user(username='entry_test', password='testpass123')
        UserProfile.objects.create(user=cls.entry_user, role=cls.data_entry_role, security_admin=cls.sec_admin)

    def test_confidential_correspondence_filtering(self):
        """التحقق من حظر المراسلات السرية عن مدخلي البيانات الذين لا يملكون الصلاحية"""
        # إنشاء مراسلة عادية
        c_normal = Correspondence.objects.create(
            type='incoming',
            reference_number='REF-NORMAL-1',
            subject='خطاب عادي تجريبي',
            date='2026-07-06',
            sender='الوزارة',
            receiver='الإدارة',
            confidentiality_level='normal',
            security_admin=self.sec_admin,
            created_by=self.admin_user
        )
        
        # إنشاء مراسلة سرية جداً
        c_secret = Correspondence.objects.create(
            type='incoming',
            reference_number='REF-SECRET-1',
            subject='خطاب سري جداً تجريبي',
            date='2026-07-06',
            sender='الوزارة',
            receiver='الإدارة',
            confidentiality_level='very_confidential',
            security_admin=self.sec_admin,
            created_by=self.admin_user
        )

        # 1. تجربة جلب البيانات بمستخدم عادي (مدخل بيانات - لا يملك صلاحية السرية)
        client = APIClient()
        client.force_authenticate(user=self.entry_user)
        response = client.get('/api/v1/secretariat/correspondences/')
        self.assertEqual(response.status_code, 200)
        
        results = response.json().get('results', response.json())
        ref_numbers = [r['reference_number'] for r in results]
        
        # يجب أن يرى العادي ولا يرى السري
        self.assertIn('REF-NORMAL-1', ref_numbers)
        self.assertNotIn('REF-SECRET-1', ref_numbers)

        # 2. تجربة جلب البيانات بمستخدم رئيس الخدمات (يملك صلاحية السرية)
        client.force_authenticate(user=self.chief_user)
        response = client.get('/api/v1/secretariat/correspondences/')
        self.assertEqual(response.status_code, 200)
        
        results_chief = response.json().get('results', response.json())
        ref_numbers_chief = [r['reference_number'] for r in results_chief]
        
        # يجب أن يرى المراسلتين معاً
        self.assertIn('REF-NORMAL-1', ref_numbers_chief)
        self.assertIn('REF-SECRET-1', ref_numbers_chief)

    def test_expense_budget_exceeded(self):
        """التحقق من أن النظام يمنع المصروفات التي تتجاوز الاعتماد المالي المرصود"""
        allocation = FinancialAllocation.objects.create(
            month='2026-07-01',
            allocated_amount=Decimal('1000.00'),
            security_admin=self.sec_admin,
            created_by=self.admin_user
        )
        
        # صرف مصروف مسموح به
        Expense.objects.create(
            allocation=allocation,
            amount=Decimal('800.00'),
            date='2026-07-06',
            description='شراء حبر طابعات',
            category='قرطاسية',
            security_admin=self.sec_admin,
            created_by=self.admin_user
        )

        # محاولة صرف مصروف يتجاوز المبلغ المتبقي (200.00)
        invalid_expense = Expense(
            allocation=allocation,
            amount=Decimal('300.00'),
            date='2026-07-06',
            description='صيانة مكتبية',
            category='صيانة',
            security_admin=self.sec_admin,
            created_by=self.admin_user
        )
        
        with self.assertRaises(ValidationError):
            invalid_expense.full_clean()

    def test_inventory_request_stock_deduction_and_low_stock_notification(self):
        """التحقق من خصم الكمية من المخزن وإرسال تنبيه النظام عند تخطي الحد الأدنى"""
        item = InventoryItem.objects.create(
            type='stationery',
            name='ورق A4 فاخر',
            code='INV-A4-PAPER',
            quantity_in_stock=10,
            minimum_stock_level=5,
            security_admin=self.sec_admin
        )
        
        # إنشاء طلب صرف كمية 6 (تتبقى 4 في المخزن وهي أقل من الحد الأدنى 5)
        req = InventoryRequest.objects.create(
            item=item,
            requested_by=self.personnel,
            quantity=6,
            status='pending',
            security_admin=self.sec_admin,
            created_by=self.admin_user
        )
        
        # تحديث الحالة إلى approved
        req.status = 'approved'
        req.save()

        # التحقق من خصم المخزون
        item.refresh_from_db()
        self.assertEqual(item.quantity_in_stock, 4)

        # التحقق من إنشاء إشعار النظام بنفاد الكمية
        notifications = NotificationRecord.objects.filter(
            title__icontains="تنبيه نفاد كمية مخزنية",
            target_user=self.admin_user
        )
        self.assertTrue(notifications.exists())
        self.assertIn("ورق A4 فاخر", notifications.first().message)

    def test_correspondence_referrals_and_replies_linking(self):
        """التحقق من إنشاء إحالة مراسلة وربط الرد الصادر بالوارد"""
        c_in = Correspondence.objects.create(
            type='incoming',
            reference_number='REF-IN-100',
            subject='طلب ترقية موظف',
            date='2026-07-06',
            sender='المنطقة العسكرية',
            receiver='شؤون الضباط',
            security_admin=self.sec_admin,
            created_by=self.admin_user
        )
        
        # إنشاء إحالة للمدير
        referral = CorrespondenceReferral.objects.create(
            correspondence=c_in,
            referred_by=self.admin_user,
            referred_to=self.personnel,
            instructions='يرجى دراسة الطلب وإبداء الرأي المالي والمهني',
            status='pending',
            security_admin=self.sec_admin,
            created_by=self.admin_user
        )
        
        self.assertEqual(referral.correspondence, c_in)
        self.assertEqual(referral.status, 'pending')

        # إنشاء رد صادر مرتبط بالوارد
        c_out = Correspondence.objects.create(
            type='outgoing',
            reference_number='REF-OUT-100',
            subject='رد على طلب ترقية موظف',
            date='2026-07-06',
            sender='شؤون الضباط',
            receiver='المنطقة العسكرية',
            parent_correspondence=c_in,
            security_admin=self.sec_admin,
            created_by=self.admin_user
        )
        
        self.assertEqual(c_out.parent_correspondence, c_in)
        self.assertEqual(c_in.replies.first(), c_out)
        self.assertIsNotNone(c_out.tracking_token)
