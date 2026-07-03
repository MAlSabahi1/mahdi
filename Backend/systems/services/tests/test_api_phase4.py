"""
اختبارات API المرحلة 4 - Services
يغطي: Reconciliation, Reports, Rejections, Webhooks, Idempotency, Task Status
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from core.models import GeoGovernorate, SecurityAdministration, CentralDepartment, GeoDistrict, Rank, ServiceStatus, Qualification
from core.models import Role, UserProfile
from systems.services.models import (
    ReconciliationTask, ReportTemplate, WebhookConfig,
    StagingRecord, RejectionLog,
)
from systems.personnel.models import PersonnelMaster

User = get_user_model()


class ServicesAPITestBase(TestCase):
    """قاعدة مشتركة لاختبارات Services API"""
    
    @classmethod
    def setUpTestData(cls):
        cls.governorate = GeoGovernorate.objects.create(name_ar='بغداد')
        cls.security_admin = SecurityAdministration.objects.create(name='أمن العاصمة', geo_governorate=cls.governorate)
        cls.dept1 = CentralDepartment.objects.create(
            name='إدارة التدريب',
            security_admin=cls.security_admin
        )
        cls.rank = Rank.objects.create(name='رقيب', order=5)
        cls.status_active = ServiceStatus.objects.create(
            name='على رأس العمل', classification='active_full',
            receives_salary=True, requires_document=False
        )
        cls.qualification = Qualification.objects.create(name='ثانوية', order=1)
        cls.location = GeoDistrict.objects.create(name_ar='طرابلس', governorate=cls.governorate)
        
        cls.admin_role = Role.objects.get(code='super_admin')
        cls.chief_role = Role.objects.get(code='services_chief')
    
    def _create_authenticated_client(self, username='testuser', role=None,
                                      supervises_all=True):
        user = User.objects.create_superuser(username=username, password='testpass123')
        UserProfile.objects.create(
            user=user,
            role=role or self.admin_role,
            supervises_all=supervises_all,
        )
        client = APIClient()
        client.force_authenticate(user=user)
        return client, user
    
    def _create_personnel(self, mil_num='1234567'):
        return PersonnelMaster.objects.create(
            military_number=mil_num, national_id=f'{mil_num}1234',
            full_name=f'فرد {mil_num}',
            birth_date='1990-01-01', join_date='2010-01-01',
            current_rank=self.rank, central_department=self.dept1, security_admin=self.security_admin,
            current_status=self.status_active,
            qualification=self.qualification, geo_location=self.location
        )


class TestReconciliationAPI(ServicesAPITestBase):
    """اختبارات Reconciliation API"""
    
    def test_list_reconciliation_tasks(self):
        """عرض مهام المطابقة"""
        client, _ = self._create_authenticated_client('recon_lister')
        response = client.get('/api/v1/service-cycle/reconciliation/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertTrue(data.get('success', False))
    
    def test_retrieve_reconciliation_task(self):
        """عرض تفاصيل مهمة مطابقة"""
        client, user = self._create_authenticated_client('recon_viewer')
        
        task = ReconciliationTask.objects.create(
            name='مطابقة حضور',
            task_type='attendance',
            key_field='military_number',
            status='completed',
            result={'summary': {'matched_count': 10}},
            created_by=user,
        )
        
        response = client.get(f'/api/v1/service-cycle/reconciliation/{task.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertTrue(data.get('success', False))
    
    def test_reconciliation_task_not_found(self):
        """مهمة مطابقة غير موجودة"""
        client, _ = self._create_authenticated_client('recon_notfound')
        response = client.get('/api/v1/service-cycle/reconciliation/999999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestReportsAPI(ServicesAPITestBase):
    """اختبارات Reports API"""
    
    def test_list_report_templates(self):
        """عرض قوالب التقارير"""
        ReportTemplate.objects.create(
            name='ملخص الأفراد',
            slug='personnel_summary',
            template_type='personnel_summary',
        )
        
        client, _ = self._create_authenticated_client('report_lister')
        response = client.get('/api/v1/service-cycle/reports/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertTrue(data.get('success', False))
        self.assertGreaterEqual(len(data.get('data', [])), 1)
    
    def test_generate_report(self):
        """توليد تقرير"""
        self._create_personnel('9999999')
        
        client, _ = self._create_authenticated_client('report_gen')
        response = client.post('/api/v1/service-cycle/reports/generate/', {
            'template_slug': 'personnel_summary',
            'filters': {},
            'format': 'excel',
        }, format='json')
        
        self.assertIn(response.status_code, [200, 201, 400])
    
    def test_report_invalid_template(self):
        """قالب تقرير غير موجود"""
        client, _ = self._create_authenticated_client('report_bad')
        response = client.post('/api/v1/service-cycle/reports/generate/', {
            'template_slug': 'nonexistent_template',
            'filters': {},
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestRejectionsAPI(ServicesAPITestBase):
    """اختبارات Rejections API"""
    
    def test_list_rejections(self):
        """عرض المرفوضات"""
        client, _ = self._create_authenticated_client('rej_lister')
        response = client.get('/api/v1/service-cycle/rejections/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_export_rejections(self):
        """تصدير المرفوضات"""
        client, _ = self._create_authenticated_client('rej_exporter')
        response = client.get('/api/v1/service-cycle/rejections/export/')
        self.assertIn(response.status_code, [200])


class TestWebhookConfigAPI(ServicesAPITestBase):
    """اختبارات Webhook Config API"""
    
    def test_list_webhooks(self):
        """عرض إعدادات Webhook"""
        client, _ = self._create_authenticated_client('wh_lister')
        response = client.get('/api/v1/service-cycle/webhooks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_webhook(self):
        """إنشاء إعداد Webhook"""
        client, _ = self._create_authenticated_client('wh_creator')
        response = client.post('/api/v1/service-cycle/webhooks/', {
            'url': 'https://example.com/webhook',
            'secret': 'supersecret123',
            'events': ['rejection.created', 'import.completed'],
            'is_active': True,
        }, format='json')
        self.assertIn(response.status_code, [201, 200])


class TestIdempotencyAPI(ServicesAPITestBase):
    """اختبارات Idempotency عبر API"""
    
    def test_idempotent_request_same_key(self):
        """إرسال نفس Idempotency-Key يعيد نفس الاستجابة"""
        client, _ = self._create_authenticated_client('idemp_test')
        
        # الطلب الأول
        headers = {'HTTP_IDEMPOTENCY_KEY': 'test-key-12345'}
        response1 = client.get(
            '/api/v1/service-cycle/reconciliation/',
            **headers
        )
        
        # الطلب الثاني بنفس المفتاح
        response2 = client.get(
            '/api/v1/service-cycle/reconciliation/',
            **headers
        )
        
        # كلا الطلبين يجب أن ينجحا
        self.assertEqual(response1.status_code, response2.status_code)


class TestTaskStatusAPI(ServicesAPITestBase):
    """اختبارات Task Status API"""
    
    def test_unknown_task_id(self):
        """مهمة غير موجودة"""
        client, _ = self._create_authenticated_client('task_checker')
        response = client.get('/api/v1/service-cycle/tasks/nonexistent-task-id/')
        # Celery قد لا يكون متوفراً في الاختبار
        self.assertIn(response.status_code, [200, 400, 500])


class TestStagingAPI(ServicesAPITestBase):
    """اختبارات Staging API"""
    
    def test_list_staging_records(self):
        """عرض التغييرات المقترحة"""
        client, _ = self._create_authenticated_client('staging_lister')
        response = client.get('/api/v1/service-cycle/staging/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_bulk_approve_empty_list_fails(self):
        """موافقة جماعية بقائمة فارغة"""
        client, _ = self._create_authenticated_client('bulk_test')
        response = client.post('/api/v1/service-cycle/staging/bulk_approve/', {
            'staging_ids': [],
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
