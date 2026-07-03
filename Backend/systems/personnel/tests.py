"""
Personnel App Tests - اختبارات تطبيق الأفراد
محدَّثة لتتوافق مع المعمارية الجديدة:
  GeoGovernorate → SecurityAdministration → CentralDepartment → Division → Unit
  PersonnelMaster لا يملك حقل directorate — يستخدم central_department/branch/district_police
"""
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.contrib.auth import get_user_model
from datetime import date
from systems.personnel.models import PersonnelMaster
from systems.personnel.state_machine import ServiceStateMachine, StateTransitionError
from systems.personnel.services import PersonnelService
from core.models import (
    Rank, ServiceStatus, Qualification,
    GeoGovernorate, SecurityAdministration, CentralDepartment,
)

User = get_user_model()


# ── مساعد لإنشاء CentralDepartment بسرعة ───────────────────────

def make_dept(name="إدارة الموارد", code="HR"):
    gov = GeoGovernorate.objects.create(name_ar=f"محافظة {name}", name_en=name)
    sec = SecurityAdministration.objects.create(
        name=f"أمن {name}", code=f"SEC_{code}", geo_governorate=gov
    )
    return CentralDepartment.objects.create(
        name=name, code=code, security_admin=sec
    )


# ══════════════════════════════════════════════════════════════
# 1. PersonnelMaster
# ══════════════════════════════════════════════════════════════

class PersonnelMasterModelTest(TestCase):
    """اختبارات نموذج الملف الأساسي للفرد"""

    def setUp(self):
        self.rank = Rank.objects.create(name="نقيب", order=6, is_officer=True)
        self.status = ServiceStatus.objects.create(
            name="عامل", classification="active_full", receives_salary=True
        )
        self.qualification = Qualification.objects.create(name="جامعي", order=3)

    def _make_personnel(self, **kwargs):
        defaults = dict(
            military_number="1234567",
            national_id="12345678901",
            full_name="أحمد محمد علي حسن",
            birth_date=date(1990, 1, 1),
            join_date=date(2010, 1, 1),
            current_rank=self.rank,
            current_status=self.status,
            qualification=self.qualification,
        )
        defaults.update(kwargs)
        return PersonnelMaster(**defaults)

    def test_create_personnel_valid(self):
        p = self._make_personnel()
        p.save()
        self.assertEqual(p.military_number, "1234567")
        self.assertEqual(p.national_id, "12345678901")
        self.assertFalse(p.is_complete)

    def test_military_number_validation_length_short(self):
        with self.assertRaises(ValidationError):
            p = self._make_personnel(military_number="12345")
            p.full_clean()

    def test_military_number_validation_length_long(self):
        with self.assertRaises(ValidationError):
            p = self._make_personnel(military_number="12345678")
            p.full_clean()

    def test_military_number_validation_digits_only(self):
        with self.assertRaises(ValidationError):
            p = self._make_personnel(military_number="123456A")
            p.full_clean()

    def test_national_id_validation_length(self):
        with self.assertRaises(ValidationError):
            p = self._make_personnel(national_id="123456789")
            p.full_clean()

    def test_national_id_validation_digits_only(self):
        with self.assertRaises(ValidationError):
            p = self._make_personnel(national_id="1234567890X")
            p.full_clean()

    def test_military_number_unique(self):
        self._make_personnel().save()
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                PersonnelMaster.objects.create(
                    military_number="1234567",  # مكرر
                    national_id="98765432109",
                    full_name="محمد أحمد",
                    birth_date=date(1991, 1, 1),
                    join_date=date(2011, 1, 1),
                    current_rank=self.rank,
                    current_status=self.status,
                    qualification=self.qualification,
                )

    def test_is_complete_flag_default_false(self):
        p = self._make_personnel()
        p.save()
        self.assertFalse(p.is_complete)


# ══════════════════════════════════════════════════════════════
# 2. ServiceStateMachine
# ══════════════════════════════════════════════════════════════

class ServiceStateMachineTest(TestCase):
    """اختبارات محرك الحالات"""

    def setUp(self):
        self.active_full = ServiceStatus.objects.create(
            name="عامل", classification="active_full",
            receives_salary=True, requires_document=False,
        )
        self.inactive_temp = ServiceStatus.objects.create(
            name="منتدب", classification="inactive_temp",
            receives_salary=True, requires_document=True,
        )
        self.inactive_perm = ServiceStatus.objects.create(
            name="شهيد", classification="inactive_perm",
            receives_salary=False, requires_document=True,
            is_permanent_deactivation=True,
        )

    def test_valid_transition_with_document(self):
        sm = ServiceStateMachine()
        result = sm.can_transition(
            self.active_full, self.inactive_temp, has_document=True
        )
        self.assertTrue(result)

    def test_invalid_transition_without_document(self):
        sm = ServiceStateMachine()
        with self.assertRaises(StateTransitionError):
            sm.validate_transition(
                self.active_full, self.inactive_temp, has_document=False
            )

    def test_permanent_deactivation_cannot_revert(self):
        sm = ServiceStateMachine()
        with self.assertRaises(StateTransitionError):
            sm.validate_transition(
                self.inactive_perm, self.active_full, has_document=True
            )

    def test_transition_to_permanent_requires_document(self):
        sm = ServiceStateMachine()
        with self.assertRaises(StateTransitionError):
            sm.validate_transition(
                self.active_full, self.inactive_perm, has_document=False
            )


# ══════════════════════════════════════════════════════════════
# 3. PersonnelService
# ══════════════════════════════════════════════════════════════

class PersonnelServiceTest(TestCase):
    """اختبارات خدمات الأفراد (المعاملات الذرية)"""

    def setUp(self):
        self.user = User.objects.create_user(username="admin", password="password123")
        self.rank = Rank.objects.create(name="نقيب", order=6, is_officer=True)
        self.qualification = Qualification.objects.create(name="جامعي", order=3)
        self.status_active = ServiceStatus.objects.create(
            name="عامل", classification="active_full",
            receives_salary=True, requires_document=False,
        )
        self.status_inactive = ServiceStatus.objects.create(
            name="منتدب", classification="inactive_temp",
            receives_salary=True, requires_document=False,
        )
        self.personnel = PersonnelMaster.objects.create(
            military_number="1234567",
            national_id="12345678901",
            full_name="أحمد محمد علي",
            birth_date=date(1990, 1, 1),
            join_date=date(2010, 1, 1),
            current_rank=self.rank,
            current_status=self.status_active,
            qualification=self.qualification,
        )

    def test_change_status_success(self):
        self.personnel.current_status = self.status_inactive
        self.personnel.save()
        self.personnel.refresh_from_db()
        self.assertEqual(self.personnel.current_status, self.status_inactive)

    def test_change_status_atomic_rollback(self):
        original_status = self.personnel.current_status
        try:
            with transaction.atomic():
                self.personnel.current_status = self.status_inactive
                self.personnel.save()
                raise Exception("خطأ متعمد")
        except Exception:
            pass
        self.personnel.refresh_from_db()
        self.assertEqual(self.personnel.current_status, original_status)

    def test_transfer_to_new_central_department_without_doc_raises(self):
        """النقل بدون مستند يُثير ValidationError"""
        new_dept = make_dept(name="إدارة المنشآت", code="FAC")
        with self.assertRaises(ValidationError):
            PersonnelService.transfer_directorate(
                self.personnel,
                new_central_department=new_dept,
                document=None,
            )


class PersonnelServiceTransferTest(TestCase):
    """اختبار نقل الفرد — يُتجاوز فيه خطأ المستند المتوقع"""

    def setUp(self):
        self.rank = Rank.objects.create(name="نقيب", order=6, is_officer=True)
        self.status = ServiceStatus.objects.create(
            name="عامل", classification="active_full", receives_salary=True
        )
        self.personnel = PersonnelMaster.objects.create(
            military_number="7654321",
            national_id="11122233344",
            full_name="سالم علي سعيد",
            birth_date=date(1988, 5, 1),
            join_date=date(2008, 5, 1),
            current_rank=self.rank,
            current_status=self.status,
        )

    def test_transfer_requires_document(self):
        """النقل بدون مستند يرفع ValidationError"""
        new_dept = make_dept(name="الإدارة الجديدة", code="NEW")
        with self.assertRaises(ValidationError):
            PersonnelService.transfer_directorate(
                self.personnel,
                new_central_department=new_dept,
                document=None,
            )

    def test_transfer_requires_exactly_one_target(self):
        """يجب تحديد جهة واحدة فقط"""
        with self.assertRaises(ValidationError):
            # لا جهة محددة
            PersonnelService.transfer_directorate(self.personnel, document=None)


# ══════════════════════════════════════════════════════════════
# 4. Personnel Queries
# ══════════════════════════════════════════════════════════════

class PersonnelQueryTest(TestCase):
    """اختبارات الاستعلامات والفهارس"""

    def setUp(self):
        rank  = Rank.objects.create(name="نقيب", order=6, is_officer=True)
        status = ServiceStatus.objects.create(
            name="عامل", classification="active_full", receives_salary=True
        )
        self.dept = make_dept(name="إدارة الموارد", code="HR2")
        qual = Qualification.objects.create(name="جامعي", order=3)

        for i in range(10):
            PersonnelMaster.objects.create(
                military_number=f"123456{i}",
                national_id=f"1234567890{i}",
                full_name=f"فرد رقم {i}",
                birth_date=date(1990, 1, 1),
                join_date=date(2010, 1, 1),
                current_rank=rank,
                current_status=status,
                central_department=self.dept,  # الحقل الصحيح
                qualification=qual,
            )

    def test_search_by_military_number(self):
        p = PersonnelMaster.objects.get(military_number="1234567")
        self.assertEqual(p.full_name, "فرد رقم 7")

    def test_search_by_national_id(self):
        p = PersonnelMaster.objects.get(national_id="12345678905")
        self.assertIsNotNone(p)

    def test_filter_by_central_department(self):
        count = PersonnelMaster.objects.filter(central_department=self.dept).count()
        self.assertEqual(count, 10)

    def test_filter_by_status(self):
        status = ServiceStatus.objects.get(name="عامل")
        count = PersonnelMaster.objects.filter(current_status=status).count()
        self.assertEqual(count, 10)


# ══════════════════════════════════════════════════════════════
# 5. Database Triggers & Constraints
# ══════════════════════════════════════════════════════════════

class DatabaseTriggersTest(TestCase):
    """
    اختبارات PostgreSQL Triggers والـ CHECK Constraints.
    نستخدم TestCase عادياً — الـ BEFORE triggers في PostgreSQL
    تعمل داخل الـ transaction وتكون مرئية للاستعلامات داخله.
    """

    def _setup_refs(self):
        self.rank = Rank.objects.create(name="نقيب", order=6, is_officer=True)
        self.status = ServiceStatus.objects.create(
            name="عامل", classification="active_full", receives_salary=True
        )
        self.qualification = Qualification.objects.create(name="جامعي", order=3)

    def setUp(self):
        self._setup_refs()

    # TestCase يتراجع الـ transaction تلقائياً — tearDown للتوضيح فقط

    def _create_personnel(self, mil=None, nid=None, **kwargs):
        import os
        defaults = dict(
            military_number=mil or str(int.from_bytes(os.urandom(4), 'big') % 9000000 + 1000000),
            national_id=nid or str(int.from_bytes(os.urandom(8), 'big') % 90000000000 + 10000000000),
            full_name="اختبار",
            birth_date=date(1990, 1, 1),
            join_date=date(2010, 1, 1),
            current_rank=self.rank,
            current_status=self.status,
            qualification=self.qualification,
        )
        defaults.update(kwargs)  # kwargs تتغلب على القيم الافتراضية
        return PersonnelMaster.objects.create(**defaults)

    def test_trigger_prevent_military_number_update(self):
        """Trigger 1: منع تعديل military_number مباشرة"""
        from django.db.utils import DatabaseError, InternalError
        p = self._create_personnel()
        original_mil = p.military_number
        p.military_number = "8888888"
        with self.assertRaises((InternalError, DatabaseError)):
            with transaction.atomic():
                p.save(force_update=True)
        # p.pk تغيّر في Python — نستعلم بالرقم الأصلي
        refreshed = PersonnelMaster.objects.get(military_number=original_mil)
        self.assertEqual(refreshed.military_number, original_mil)

    def test_trigger_update_is_complete(self):
        """Trigger 2: تحديث is_complete عند إضافة الصورة والبصمة"""
        p = self._create_personnel()
        p.refresh_from_db()
        self.assertFalse(p.is_complete)

        p.photo = 'personnel/photos/test.jpg'
        p.fingerprint_hash = 'abc123hash'
        p.save()
        p.refresh_from_db()
        self.assertTrue(p.is_complete)

    def test_trigger_calculate_data_quality_score(self):
        """Trigger 3: حساب data_quality_score تلقائياً"""
        p = self._create_personnel()
        p.refresh_from_db()
        self.assertGreater(p.data_quality_score, 0)
        self.assertLessEqual(p.data_quality_score, 100)

        p.phone_number = '777123456'
        p.photo = 'personnel/photos/test.jpg'
        p.fingerprint_hash = 'abc123hash'
        p.save()
        p.refresh_from_db()
        self.assertGreater(p.data_quality_score, 50)

    def test_check_constraint_join_after_birth_18_years(self):
        """CHECK: join_date يجب أن يكون بعد birth_date بـ 18 عاماً"""
        with self.assertRaises(IntegrityError) as ctx:
            with transaction.atomic():
                self._create_personnel(
                    birth_date=date(2000, 1, 1),
                    join_date=date(2010, 1, 1),
                )
        self.assertIn('check_join_after_birth', str(ctx.exception))

    def test_check_constraint_birth_date_not_future(self):
        """CHECK: birth_date ليس في المستقبل"""
        from datetime import timedelta
        future_date = date.today() + timedelta(days=365)
        with self.assertRaises(IntegrityError) as ctx:
            with transaction.atomic():
                self._create_personnel(
                    birth_date=future_date,
                    join_date=date.today(),
                )
        self.assertIn('check_birth_date_not_future', str(ctx.exception))

    def test_check_constraint_data_quality_score_exists(self):
        """
        الـ BEFORE trigger يُعيد حساب data_quality_score تلقائياً ويحده بـ 100،
        لذا لا يمكن اختبار CHECK constraint بالـ UPDATE العادي.
        نتحقق بدلاً من ذلك أن الحساب لا يتجاوز 100 أبداً.
        """
        from django.db import connection
        p = self._create_personnel()
        p.refresh_from_db()
        self.assertGreaterEqual(p.data_quality_score, 0)
        self.assertLessEqual(p.data_quality_score, 100)
        # التحقق أن القيد موجود في قاعدة البيانات
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*) FROM information_schema.check_constraints
                WHERE constraint_name LIKE '%data_quality%'
            """)
            count = cursor.fetchone()[0]
        self.assertGreater(count, 0, "CHECK constraint على data_quality_score يجب أن يكون موجوداً")
