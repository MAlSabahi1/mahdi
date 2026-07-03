"""
Security Tests - اختبارات المرحلة 3 الشاملة

يغطي:
- RBAC: أدوار + صلاحيات
- ABAC: نطاق الإدارات
- HMAC: توقيع + تحقق + كشف تلاعب
- تفويض مزدوج: طلب + موافقة + رفض + انتهاء
- Shadow Tables: INSERT/UPDATE/DELETE triggers
- Account lockout
- System settings
"""
import pytest
from datetime import date, timedelta
from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import connection

# النماذج التنظيمية الجديدة
from core.models import (
    SecurityAdministration, GeoGovernorate, GeoDistrict,
    Rank, ServiceStatus, Qualification,
    JobCategory, JobTitle
)
from core.models.organization import CentralDepartment
from systems.personnel.models import PersonnelMaster
from systems.services.models import ServiceEventLog
from infra.audit.models import AuditLog
from infra.accounts.models import SecurityProfile
from infra.security.models import (
    Role, UserProfile, DualAuthorizationRequest,
    MetricsSnapshot, SystemSetting,
    SYSTEM_PERMISSIONS
)
from infra.security.permissions import (
    has_permission, has_department_scope,
    has_permission_for_department, check_permission,
    filter_by_department_scope, requires_four_eyes,
)
from infra.security.audit_signing import (
    compute_signature, verify_signature, verify_all_signatures
)
from infra.security.dual_auth_service import DualAuthorizationService, DualAuthError
from infra.security.telemetry_service import TelemetryService

User = get_user_model()


class SecurityTestBase(TestCase):
    """قاعدة مشتركة لاختبارات الأمان"""
    
    @classmethod
    def setUpTestData(cls):
        # إدارات الأمن (بدل Governorate و Directorate)
        cls.geo_gov = GeoGovernorate.objects.create(name='المحافظة الثانية')
        cls.sec_admin = SecurityAdministration.objects.create(
            name='أمن المحافظة الثانية الرئيسية',
            governorate=cls.geo_gov,
        )
        cls.sec_admin2 = SecurityAdministration.objects.create(
            name='أمن المحافظة الثانية الفرعي',
            governorate=cls.geo_gov,
        )
        cls.sec_admin3 = SecurityAdministration.objects.create(
            name='أمن المحافظة الثانية الثاني',
            governorate=cls.geo_gov,
        )
        # aliases للتوافق مع الاختبارات التي تستخدم dept1/2/3
        cls.dept1 = cls.sec_admin
        cls.dept2 = cls.sec_admin2
        cls.dept3 = cls.sec_admin3
        cls.gov = cls.geo_gov

        # الأدوار
        cls.admin_role = Role.objects.get(code='super_admin')
        cls.chief_role = Role.objects.get(code='services_chief')
        cls.inspector_role = Role.objects.get(code='inspector')
        cls.viewer_role = Role.objects.get(code='viewer')
        cls.data_entry_role = Role.objects.get(code='data_entry')

        # الرتبة والحالة والمؤهل
        cls.rank = Rank.objects.create(name='رقيب', order=5)
        cls.status = ServiceStatus.objects.create(
            name='على رأس العمل',
            classification='active_full',
        )
        cls.qualification = Qualification.objects.create(
            name='ثانوية', order=1
        )
        cls.geo_district = GeoDistrict.objects.create(
            name='مديرية طرابلس',
            governorate=cls.geo_gov,
        )
    
    def _create_user_with_profile(self, username, role, directorate=None,
                                   supervised_directorates=None, supervises_all=False):
        """مساعد: إنشاء مستخدم مع ملف"""
        user = User.objects.create_user(
            username=username, password='test123456'
        )
        profile = UserProfile.objects.create(
            user=user,
            role=role,
            security_admin=directorate,   # directorate هنا = security_admin
            supervises_all=supervises_all,
        )
        if supervised_directorates:
            profile.supervised_security_admins.set(supervised_directorates)
        SecurityProfile.objects.create(user=user)
        return user, profile
    
    def _create_personnel(self, military_number, security_admin=None):
        """مساعد: إنشاء فرد"""
        return PersonnelMaster.objects.create(
            military_number=military_number,
            national_id=f'{military_number}1234',
            full_name=f'فرد {military_number}',
            birth_date=date(1990, 1, 1),
            join_date=date(2010, 1, 1),
            security_admin=security_admin or self.dept1,
            current_rank=self.rank,
            current_status=self.status,
            qualification=self.qualification,
            geo_location=self.geo_district,
        )


# ============================================================================
# اختبارات RBAC (المهمة 3.1)
# ============================================================================

class TestRBACRoles(SecurityTestBase):
    """اختبار نظام الأدوار الديناميكي"""
    
    def test_default_roles_created(self):
        """التحقق من إنشاء الأدوار الافتراضية"""
        self.assertEqual(Role.objects.filter(is_system_role=True).count(), 6)
    
    def test_admin_has_all_permissions(self):
        """مدير النظام يملك جميع الصلاحيات"""
        admin_role = Role.objects.get(code='super_admin')
        self.assertTrue(admin_role.has_permission('view_personnel'))
        self.assertTrue(admin_role.has_permission('delete_personnel'))
        self.assertTrue(admin_role.has_permission('manage_users'))
        self.assertTrue(admin_role.has_permission('override_lock'))
    
    def test_viewer_has_limited_permissions(self):
        """المستخدم العادي لديه صلاحيات محدودة"""
        viewer = Role.objects.get(code='viewer')
        self.assertTrue(viewer.has_permission('view_personnel'))
        self.assertTrue(viewer.has_permission('view_reports'))
        self.assertFalse(viewer.has_permission('edit_personnel_basic'))
        self.assertFalse(viewer.has_permission('export_sheet'))
        self.assertFalse(viewer.has_permission('manage_users'))
    
    def test_chief_permissions(self):
        """رئيس الخدمات يملك صلاحيات المراجعة والاعتماد"""
        chief = Role.objects.get(code='services_chief')
        self.assertTrue(chief.has_permission('export_sheet'))
        self.assertTrue(chief.has_permission('import_sheet'))
        self.assertTrue(chief.has_permission('approve_change'))
        self.assertTrue(chief.has_permission('reject_change'))
        self.assertTrue(chief.has_permission('close_month'))
        self.assertFalse(chief.has_permission('override_lock'))
        self.assertFalse(chief.has_permission('manage_users'))
    
    def test_inspector_readonly(self):
        """المفتش: عرض + تدقيق فقط"""
        inspector = Role.objects.get(code='inspector')
        self.assertTrue(inspector.has_permission('view_personnel'))
        self.assertTrue(inspector.has_permission('view_audit_log'))
        self.assertTrue(inspector.has_permission('verify_audit_signatures'))
        self.assertFalse(inspector.has_permission('edit_personnel_basic'))
        self.assertFalse(inspector.has_permission('approve_change'))
    
    def test_custom_role_creation(self):
        """إنشاء دور مخصص"""
        from infra.authorization.models import Permission, RolePermission
        custom_role = Role.objects.create(
            name='مراقب مالي',
            code='financial_auditor',
            priority=50,
        )
        # تعيين الصلاحيات عبر RolePermission
        for code in ['personnel.view.all', 'reports.view.all', 'audit.view.all']:
            perm = Permission.objects.filter(code=code).first()
            if perm:
                RolePermission.objects.get_or_create(role=custom_role, permission=perm)
        self.assertTrue(custom_role.has_permission('view_personnel'))
        self.assertFalse(custom_role.has_permission('edit_personnel_basic'))
    
    def test_has_any_permission(self):
        """فحص أي صلاحية"""
        viewer = Role.objects.get(code='viewer')
        self.assertTrue(viewer.has_any_permission('view_personnel', 'edit_personnel_basic'))
        self.assertFalse(viewer.has_any_permission('edit_personnel_basic', 'manage_users'))
    
    def test_has_all_permissions(self):
        """فحص جميع الصلاحيات"""
        admin = Role.objects.get(code='super_admin')
        self.assertTrue(admin.has_all_permissions('view_personnel', 'manage_users'))
        
        viewer = Role.objects.get(code='viewer')
        self.assertFalse(viewer.has_all_permissions('view_personnel', 'manage_users'))
    
    def test_available_permissions_list(self):
        """قائمة الصلاحيات المتاحة"""
        perms = Role.get_available_permissions()
        self.assertGreater(len(perms), 20)
        codes = [p[0] for p in perms]
        # اختبار بالأكواد الجديدة
        self.assertIn('personnel.view.all', codes)
        self.assertIn('admin.manage_users.all', codes)


# ============================================================================
# اختبارات ABAC - النطاق (المهمة 3.2)
# ============================================================================

class TestABACScope(SecurityTestBase):
    """اختبار نظام الصلاحيات على مستوى الكائن"""
    
    def test_superuser_accesses_all(self):
        """المستخدم الأعلى يصل لكل شيء"""
        user = User.objects.create_superuser(
            username='superadmin', password='test123456'
        )
        self.assertTrue(has_permission(user, 'anything'))
        self.assertTrue(has_department_scope(user, self.dept1.pk))
        self.assertTrue(has_department_scope(user, self.dept2.pk))
    
    def test_chief_scope_limited(self):
        """رئيس الخدمات يرى إداراته فقط"""
        user, profile = self._create_user_with_profile(
            'chief1', self.chief_role,
            supervised_directorates=[self.dept1, self.dept2]
        )
        self.assertTrue(has_department_scope(user, self.dept1.pk))
        self.assertTrue(has_department_scope(user, self.dept2.pk))
        self.assertFalse(has_department_scope(user, self.dept3.pk))
    
    def test_chief_supervises_all(self):
        """رئيس خدمات يشرف على الكل"""
        user, profile = self._create_user_with_profile(
            'chief_all', self.chief_role,
            supervises_all=True
        )
        self.assertTrue(has_department_scope(user, self.dept1.pk))
        self.assertTrue(has_department_scope(user, self.dept3.pk))
    
    def test_normal_user_own_dept_only(self):
        """المستخدم العادي: إدارته فقط"""
        user, profile = self._create_user_with_profile(
            'normal1', self.viewer_role,
            directorate=self.dept1,
        )
        self.assertTrue(has_department_scope(user, self.dept1.pk))
        self.assertFalse(has_department_scope(user, self.dept2.pk))
    
    def test_combined_permission_and_scope(self):
        """فحص مركب: الصلاحية + النطاق"""
        user, profile = self._create_user_with_profile(
            'chief2', self.chief_role,
            supervised_directorates=[self.dept1]
        )
        self.assertTrue(has_permission_for_department(
            user, 'export_sheet', self.dept1.pk
        ))
        self.assertFalse(has_permission_for_department(
            user, 'export_sheet', self.dept3.pk
        ))
    
    def test_no_profile_denied(self):
        """مستخدم بدون ملف → رفض"""
        user = User.objects.create_user(
            username='noprofile', password='test123456'
        )
        self.assertFalse(has_permission(user, 'view_personnel'))
        self.assertFalse(has_department_scope(user, self.dept1.pk))
    
    def test_filter_by_scope(self):
        """تصفية QuerySet حسب النطاق"""
        user, _ = self._create_user_with_profile(
            'chief_filter', self.chief_role,
            supervised_directorates=[self.dept1]
        )

        # إنشاء أفراد في إدارات مختلفة
        self._create_personnel('1000001', self.dept1)
        self._create_personnel('1000002', self.dept2)

        qs = PersonnelMaster.objects.all()
        filtered = filter_by_department_scope(
            user, qs, 'security_admin'
        )
        self.assertEqual(filtered.count(), 1)
        self.assertEqual(filtered.first().military_number, '1000001')
    
    def test_accessible_department_ids(self):
        """قائمة الإدارات المتاحة"""
        user, profile = self._create_user_with_profile(
            'chief_ids', self.chief_role,
            directorate=self.dept1,
            supervised_directorates=[self.dept2]
        )
        ids = profile.get_accessible_security_admin_ids()
        self.assertIn(self.dept1.pk, ids)
        self.assertIn(self.dept2.pk, ids)
        self.assertNotIn(self.dept3.pk, ids)
    
    def test_four_eyes_detection(self):
        """كشف العمليات التي تتطلب تفويض مزدوج"""
        self.assertTrue(requires_four_eyes('delete_personnel'))
        self.assertTrue(requires_four_eyes('override_lock'))
        self.assertFalse(requires_four_eyes('export_sheet'))


# ============================================================================
# اختبارات HMAC Signing (المهمة 3.5)
# ============================================================================

class TestHMACSigning(SecurityTestBase):
    """اختبار التوقيع الرقمي لسجلات التدقيق"""
    
    def test_audit_log_auto_signed(self):
        """سجل التدقيق يُوقع تلقائياً"""
        user, _ = self._create_user_with_profile(
            'signer', self.admin_role
        )
        log = AuditLog.objects.create(
            user=user,
            action='CREATE',
            model_name='TestModel',
            object_id='1',
            new_data={'test': 'data'},
        )
        self.assertTrue(len(log.signature) > 0)
    
    def test_signature_verification_valid(self):
        """توقيع صحيح → True"""
        user, _ = self._create_user_with_profile(
            'verifier', self.admin_role
        )
        log = AuditLog.objects.create(
            user=user,
            action='UPDATE',
            model_name='PersonnelMaster',
            object_id='1234567',
            old_data={'status': 'active'},
            new_data={'status': 'inactive'},
        )
        self.assertTrue(verify_signature(log))
        self.assertTrue(log.verify())
    
    def test_signature_tamper_detection(self):
        """تلاعب بالبيانات → توقيع غير صحيح"""
        user, _ = self._create_user_with_profile(
            'tamper_test', self.admin_role
        )
        log = AuditLog.objects.create(
            user=user,
            action='UPDATE',
            model_name='PersonnelMaster',
            object_id='1234567',
            old_data={'status': 'active'},
            new_data={'status': 'inactive'},
        )
        
        # تلاعب مباشر بالبيانات (تجاوز save → bypass HMAC)
        AuditLog.objects.filter(pk=log.pk).update(
            new_data={'status': 'TAMPERED!'}
        )
        log.refresh_from_db()
        
        self.assertFalse(verify_signature(log))
        self.assertFalse(log.verify())
    
    def test_verify_all_signatures(self):
        """فحص جماعي للتوقيعات"""
        user, _ = self._create_user_with_profile(
            'bulk_verify', self.admin_role
        )
        # إنشاء عدة سجلات
        logs = []
        for i in range(3):
            log = AuditLog.objects.create(
                user=user,
                action='VIEW',
                model_name='Test',
                object_id=str(i),
            )
            logs.append(log)
        
        # التحقق من كل سجل على حدة
        for log in logs:
            log.refresh_from_db()
            self.assertTrue(verify_signature(log), 
                          f"Signature verification failed for log {log.pk}")
        
        # فحص جماعي للسجلات الجديدة فقط
        result = verify_all_signatures(
            queryset=AuditLog.objects.filter(
                pk__in=[log.pk for log in logs]
            )
        )
        self.assertEqual(result['total'], 3)
        self.assertEqual(result['valid'], 3)
        self.assertEqual(result['tampered'], 0)
    
    def test_unsigned_record_detection(self):
        """كشف سجلات بدون توقيع"""
        user, _ = self._create_user_with_profile(
            'unsigned_test', self.admin_role
        )
        # إنشاء سجل بدون توقيع
        log = AuditLog(
            user=user,
            action='VIEW',
            model_name='Test',
            object_id='1',
        )
        log.signature = ''
        # تجاوز save override
        AuditLog.objects.bulk_create([log])
        
        self.assertFalse(verify_signature(log))


# ============================================================================
# اختبارات التفويض المزدوج (المهمة 3.6)
# ============================================================================

class TestDualAuthorization(SecurityTestBase):
    """اختبار مبدأ العينين الأربع"""
    
    def test_create_request(self):
        """إنشاء طلب تفويض"""
        user, _ = self._create_user_with_profile(
            'requester1', self.chief_role
        )
        service = DualAuthorizationService(user)
        
        request = service.create_request(
            action_type='DELETE_PERSONNEL',
            target_object_type='PersonnelMaster',
            target_object_id='1234567',
            reason='فرد متوفى - نقل للأرشيف',
        )
        
        self.assertEqual(request.status, 'pending')
        self.assertEqual(request.requester, user)
        self.assertIsNotNone(request.expires_at)
    
    def test_approve_request(self):
        """الموافقة على طلب تفويض"""
        requester, _ = self._create_user_with_profile(
            'req_approve', self.chief_role
        )
        approver, _ = self._create_user_with_profile(
            'appr_approve', self.admin_role
        )
        
        # إنشاء فرد ليتم حذفه
        self._create_personnel('2000001', self.dept1)
        
        # إنشاء الطلب
        req_service = DualAuthorizationService(requester)
        request = req_service.create_request(
            action_type='DELETE_PERSONNEL',
            target_object_type='PersonnelMaster',
            target_object_id='2000001',
            reason='حذف نهائي',
        )
        
        # الموافقة
        appr_service = DualAuthorizationService(approver)
        result = appr_service.approve_request(request.pk)
        
        request.refresh_from_db()
        self.assertEqual(request.status, 'executed')
        self.assertEqual(request.approver, approver)
        self.assertTrue(result['success'])
        
        # التحقق من الحذف
        self.assertFalse(
            PersonnelMaster.objects.filter(
                military_number='2000001'
            ).exists()
        )
    
    def test_reject_request(self):
        """رفض طلب تفويض"""
        requester, _ = self._create_user_with_profile(
            'req_reject', self.chief_role
        )
        approver, _ = self._create_user_with_profile(
            'appr_reject', self.admin_role
        )
        
        req_service = DualAuthorizationService(requester)
        request = req_service.create_request(
            action_type='UNLOCK_MONTH',
            target_object_type='MonthlySnapshot',
            target_object_id='2025-03',
            reason='تصحيح خطأ',
        )
        
        appr_service = DualAuthorizationService(approver)
        result = appr_service.reject_request(
            request.pk, reason='لا يوجد مبرر كافٍ'
        )
        
        request.refresh_from_db()
        self.assertEqual(request.status, 'rejected')
        self.assertEqual(result['status'], 'rejected')
    
    def test_same_user_cannot_approve(self):
        """الطالب لا يمكنه الموافقة على طلبه"""
        user, _ = self._create_user_with_profile(
            'self_approve', self.admin_role
        )
        
        self._create_personnel('3000001', self.dept1)
        
        service = DualAuthorizationService(user)
        request = service.create_request(
            action_type='DELETE_PERSONNEL',
            target_object_type='PersonnelMaster',
            target_object_id='3000001',
            reason='حذف',
        )
        
        with self.assertRaises(DualAuthError):
            service.approve_request(request.pk)
    
    def test_duplicate_request_prevented(self):
        """منع تكرار الطلب"""
        user, _ = self._create_user_with_profile(
            'dup_test', self.chief_role
        )
        service = DualAuthorizationService(user)
        
        service.create_request(
            action_type='UNLOCK_MONTH',
            target_object_type='MonthlySnapshot',
            target_object_id='2025-04',
            reason='سبب 1',
        )
        
        with self.assertRaises(DualAuthError):
            service.create_request(
                action_type='UNLOCK_MONTH',
                target_object_type='MonthlySnapshot',
                target_object_id='2025-04',
                reason='سبب 2',
            )
    
    def test_expire_old_requests(self):
        """انتهاء الطلبات القديمة"""
        user, _ = self._create_user_with_profile(
            'expire_test', self.chief_role
        )
        
        request = DualAuthorizationRequest.objects.create(
            requester=user,
            action_type='UNLOCK_MONTH',
            target_object_type='MonthlySnapshot',
            target_object_id='2025-01',
            request_data={'reason': 'test'},
            expires_at=timezone.now() - timedelta(days=1),
        )
        
        result = DualAuthorizationService.expire_old_requests()
        self.assertEqual(result['expired_count'], 1)
        
        request.refresh_from_db()
        self.assertEqual(request.status, 'expired')
    
    def test_reason_required(self):
        """السبب إلزامي"""
        user, _ = self._create_user_with_profile(
            'no_reason', self.chief_role
        )
        service = DualAuthorizationService(user)
        
        with self.assertRaises(DualAuthError):
            service.create_request(
                action_type='DELETE_PERSONNEL',
                target_object_type='PersonnelMaster',
                target_object_id='9999999',
                reason='',
            )


# ============================================================================
# اختبارات Shadow Tables (المهمة 3.3)
# ============================================================================

class TestShadowTables(SecurityTestBase):
    """اختبار جداول الظل"""
    
    def test_insert_triggers_history(self):
        """إدراج فرد يُنشئ سجلاً في جدول الظل"""
        personnel = self._create_personnel('4000001', self.dept1)
        
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT COUNT(*) FROM personnel_master_history "
                "WHERE military_number = %s AND history_action = 'INSERT'",
                ['4000001']
            )
            count = cursor.fetchone()[0]
        
        self.assertGreaterEqual(count, 1)
    
    def test_update_triggers_history(self):
        """تحديث فرد يُنشئ سجلاً في جدول الظل"""
        personnel = self._create_personnel('4000002', self.dept1)
        
        # تحديث
        personnel.full_name = 'اسم جديد'
        personnel.save()
        
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT COUNT(*) FROM personnel_master_history "
                "WHERE military_number = %s AND history_action = 'UPDATE'",
                ['4000002']
            )
            count = cursor.fetchone()[0]
        
        self.assertGreaterEqual(count, 1)
    
    def test_delete_triggers_history(self):
        """حذف فرد يُسجل في جدول الظل"""
        personnel = self._create_personnel('4000003', self.dept1)
        personnel.delete()
        
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT COUNT(*) FROM personnel_master_history "
                "WHERE military_number = %s AND history_action = 'DELETE'",
                ['4000003']
            )
            count = cursor.fetchone()[0]
        
        self.assertGreaterEqual(count, 1)
    
    def test_history_version_increments(self):
        """رقم الإصدار يزيد مع كل تغيير"""
        personnel = self._create_personnel('4000004', self.dept1)
        
        # تحديثان
        personnel.full_name = 'تعديل 1'
        personnel.save()
        personnel.full_name = 'تعديل 2'
        personnel.save()
        
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT MAX(history_version) FROM personnel_master_history "
                "WHERE military_number = %s",
                ['4000004']
            )
            max_version = cursor.fetchone()[0]
        
        self.assertGreaterEqual(max_version, 2)
    
    def test_point_in_time_query(self):
        """استعلام النقطة الزمنية - حالة الفرد في وقت سابق"""
        personnel = self._create_personnel('4000005', self.dept1)
        original_name = personnel.full_name
        
        personnel.full_name = 'اسم محدث'
        personnel.save()
        
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT full_name FROM personnel_master_history "
                "WHERE military_number = %s AND history_action = 'INSERT' "
                "ORDER BY history_timestamp LIMIT 1",
                ['4000005']
            )
            row = cursor.fetchone()
        
        self.assertEqual(row[0], original_name)


# ============================================================================
# اختبارات أمان الحساب
# ============================================================================

class TestAccountSecurity(SecurityTestBase):
    """اختبار قفل الحساب ومحاولات الدخول الفاشلة"""
    
    def test_account_lockout_after_5_failures(self):
        """قفل الحساب بعد 5 محاولات فاشلة"""
        user, profile = self._create_user_with_profile(
            'lockout_test', self.viewer_role
        )
        sec_profile = user.security_profile
        
        for i in range(5):
            sec_profile.record_failed_attempt(ip_address='127.0.0.1')
        
        sec_profile.refresh_from_db()
        self.assertTrue(sec_profile.is_locked)
        self.assertTrue(sec_profile.check_lock_state())
    
    def test_locked_user_has_no_permissions(self):
        """حساب مغلق = لا صلاحيات"""
        user, profile = self._create_user_with_profile(
            'locked_perm', self.admin_role
        )
        sec_profile = user.security_profile
        
        # قفل الحساب
        for i in range(5):
            sec_profile.record_failed_attempt(ip_address='127.0.0.1')
        
        self.assertFalse(has_permission(user, 'view_personnel'))
    
    def test_reset_after_successful_login(self):
        """إعادة تعيين بعد دخول ناجح"""
        user, profile = self._create_user_with_profile(
            'reset_test', self.viewer_role
        )
        sec_profile = user.security_profile
        
        sec_profile.record_failed_attempt(ip_address='127.0.0.1')
        sec_profile.record_failed_attempt(ip_address='127.0.0.1')
        self.assertEqual(sec_profile.failed_login_attempts, 2)
        
        sec_profile.unlock()
        self.assertEqual(sec_profile.failed_login_attempts, 0)
        self.assertFalse(sec_profile.is_locked)
    
    def test_lockout_expires(self):
        """انتهاء مدة الإغلاق"""
        user, profile = self._create_user_with_profile(
            'expire_lock', self.viewer_role
        )
        sec_profile = user.security_profile
        
        for i in range(5):
            sec_profile.record_failed_attempt(ip_address='127.0.0.1')
        
        # تعيين انتهاء في الماضي
        sec_profile.locked_until = timezone.now() - timedelta(minutes=1)
        sec_profile.save()
        
        self.assertFalse(sec_profile.check_lock_state())


# ============================================================================
# اختبارات إعدادات النظام
# ============================================================================

class TestSystemSettings(SecurityTestBase):
    """اختبار إعدادات النظام"""
    
    def test_default_settings_created(self):
        """التحقق من إنشاء الإعدادات الافتراضية"""
        self.assertIsNotNone(SystemSetting.get_value('max_upload_size_mb'))
        self.assertEqual(SystemSetting.get_value('default_month_lock_day'), 20)
    
    def test_set_and_get_value(self):
        """تعيين وجلب قيمة"""
        SystemSetting.set_value('test_key', 42, description='قيمة اختبار')
        self.assertEqual(SystemSetting.get_value('test_key'), 42)
    
    def test_get_default_for_missing(self):
        """قيمة افتراضية للمفتاح غير الموجود"""
        result = SystemSetting.get_value('nonexistent', default='fallback')
        self.assertEqual(result, 'fallback')


# ============================================================================
# اختبارات المراقبة الأمنية (المهمة 3.7)
# ============================================================================

class TestTelemetry(SecurityTestBase):
    """اختبار خدمة المراقبة الأمنية"""
    
    def test_collect_metrics(self):
        """تجميع الإحصائيات"""
        service = TelemetryService()
        metrics = service.collect_all_metrics()
        
        self.assertIn('login_failures', metrics)
        self.assertIn('active_sessions', metrics)
        self.assertIn('pending_dual_auth', metrics)
        self.assertIn('system_health', metrics)
    
    def test_dashboard_data(self):
        """بيانات لوحة المراقبة"""
        service = TelemetryService()
        service.collect_all_metrics()
        
        dashboard = service.get_dashboard_data()
        self.assertIn('login_failures', dashboard)
        self.assertIn('system_health', dashboard)
    
    def test_metrics_snapshot_saved(self):
        """حفظ لقطات الإحصائيات"""
        initial_count = MetricsSnapshot.objects.count()
        
        service = TelemetryService()
        service.collect_all_metrics()
        
        new_count = MetricsSnapshot.objects.count()
        self.assertGreater(new_count, initial_count)
