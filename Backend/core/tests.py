"""
Core App Tests - اختبارات التطبيق الأساسي
محدَّثة لتتوافق مع المعمارية الجديدة:
  GeoGovernorate → SecurityAdministration → CentralDepartment → Division → Unit
"""
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from core.models import (
    Rank, ServiceStatus, JobCategory, JobTitle, Qualification,
    GeoGovernorate, SecurityAdministration, CentralDepartment,
    Division, Unit,
)


# ──────────────────────────────────────────────────────────
# 1. Rank
# ──────────────────────────────────────────────────────────

class RankModelTest(TestCase):
    """اختبارات نموذج الرتبة"""

    def test_create_rank(self):
        rank = Rank.objects.create(name="عقيد", order=3, is_officer=True)
        self.assertEqual(rank.name, "عقيد")
        self.assertTrue(rank.is_officer)
        self.assertEqual(str(rank), "عقيد")

    def test_rank_ordering(self):
        """order أصغر = رتبة أعلى"""
        Rank.objects.create(name="لواء", order=1, is_officer=True)
        Rank.objects.create(name="عميد", order=2, is_officer=True)
        Rank.objects.create(name="عقيد", order=3, is_officer=True)
        ranks = list(Rank.objects.all())
        self.assertEqual(ranks[0].name, "لواء")
        self.assertEqual(ranks[1].name, "عميد")

    def test_rank_order_is_highest_when_smallest(self):
        highest = Rank.objects.create(name="لواء",  order=1,  is_officer=True)
        lowest  = Rank.objects.create(name="عريف", order=10, is_officer=False)
        self.assertLess(highest.order, lowest.order)

    def test_rank_unique_order(self):
        from django.db import transaction
        Rank.objects.create(name="لواء", order=1, is_officer=True)
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Rank.objects.create(name="عميد", order=1, is_officer=True)


# ──────────────────────────────────────────────────────────
# 2. ServiceStatus
# ──────────────────────────────────────────────────────────

class ServiceStatusModelTest(TestCase):
    def test_create_active_status(self):
        status = ServiceStatus.objects.create(
            name="عامل",
            classification="active_full",
            receives_salary=True,
            requires_document=False,
            is_permanent_deactivation=False,
        )
        self.assertEqual(status.name, "عامل")
        self.assertTrue(status.receives_salary)
        self.assertFalse(status.is_permanent_deactivation)

    def test_permanent_deactivation_status(self):
        status = ServiceStatus.objects.create(
            name="شهيد",
            classification="inactive_perm",
            receives_salary=False,
            requires_document=True,
            is_permanent_deactivation=True,
        )
        self.assertTrue(status.is_permanent_deactivation)
        self.assertTrue(status.requires_document)
        self.assertFalse(status.receives_salary)


# ──────────────────────────────────────────────────────────
# 3. Qualification
# ──────────────────────────────────────────────────────────

class QualificationModelTest(TestCase):
    def test_create_qualification(self):
        qual = Qualification.objects.create(name="جامعي", order=3)
        self.assertEqual(qual.name, "جامعي")

    def test_qualification_ordering(self):
        Qualification.objects.create(name="دكتوراه", order=1)
        Qualification.objects.create(name="ماجستير", order=2)
        Qualification.objects.create(name="جامعي",   order=3)
        quals = list(Qualification.objects.all())
        self.assertEqual(quals[0].name, "دكتوراه")
        self.assertEqual(quals[1].name, "ماجستير")


# ──────────────────────────────────────────────────────────
# 4. JobCategory & JobTitle
# ──────────────────────────────────────────────────────────

class JobCategoryModelTest(TestCase):
    def test_create_job_category(self):
        cat = JobCategory.objects.create(name="إداري")
        self.assertEqual(cat.name, "إداري")
        self.assertEqual(str(cat), "إداري")


class JobTitleModelTest(TestCase):
    def setUp(self):
        self.category = JobCategory.objects.create(name="إداري")

    def test_create_job_title(self):
        title = JobTitle.objects.create(name="محاسب", category=self.category)
        self.assertEqual(title.name, "محاسب")
        self.assertEqual(title.category, self.category)

    def test_job_title_category_relationship(self):
        JobTitle.objects.create(name="محاسب",  category=self.category)
        JobTitle.objects.create(name="سكرتير", category=self.category)
        self.assertEqual(self.category.job_titles.count(), 2)


# ──────────────────────────────────────────────────────────
# 5. Organizational Hierarchy (New Architecture)
#    GeoGovernorate(name_ar) → SecurityAdministration → CentralDepartment → Division → Unit
# ──────────────────────────────────────────────────────────

class OrganizationHierarchyTest(TestCase):
    """اختبار الهيكل التنظيمي الأمني الجديد"""

    def setUp(self):
        # GeoGovernorate uses name_ar / name_en (not name/code)
        self.gov = GeoGovernorate.objects.create(
            name_ar="محافظة المحافظة الأولى",
            name_en="Marib Governorate",
        )
        self.sec_admin = SecurityAdministration.objects.create(
            name="إدارة أمن المحافظة الأولى",
            code="MARIB_SEC",
            geo_governorate=self.gov,
        )
        self.dept = CentralDepartment.objects.create(
            name="الإدارة المركزية للتدريب",
            code="TRAIN_DEPT",
            security_admin=self.sec_admin,
        )
        self.division = Division.objects.create(
            name="قسم الرماية",
            central_department=self.dept,
        )
        self.unit = Unit.objects.create(
            name="وحدة الرماية المتقدمة",
            division=self.division,
        )

    def test_hierarchy_creation(self):
        self.assertEqual(self.gov.name_ar, "محافظة المحافظة الأولى")
        self.assertEqual(self.sec_admin.geo_governorate, self.gov)
        self.assertEqual(self.dept.security_admin, self.sec_admin)
        self.assertEqual(self.division.central_department, self.dept)
        self.assertEqual(self.unit.division, self.division)

    def test_division_single_parent_constraint(self):
        """قيد: القسم في جهة واحدة فقط (central_department OR branch OR district_police)"""
        self.assertIsNotNone(self.division.central_department)
        self.assertIsNone(self.division.branch)
        self.assertIsNone(self.division.district_police)

    def test_str_representations(self):
        self.assertIn("المحافظة الأولى", str(self.gov))
        self.assertIn("المحافظة الأولى", str(self.sec_admin))


# ──────────────────────────────────────────────────────────
# 6. TimestampedModel
# ──────────────────────────────────────────────────────────

class TimestampedModelTest(TestCase):
    """اختبار الحقول الزمنية التلقائية"""

    def test_auto_timestamps(self):
        gov = GeoGovernorate.objects.create(name_ar="عدن", name_en="Aden")
        self.assertIsNotNone(gov.created_at)
        self.assertIsNotNone(gov.updated_at)
        diff = abs((gov.updated_at - gov.created_at).total_seconds())
        self.assertLess(diff, 2)

    def test_updated_at_changes_on_save(self):
        gov = GeoGovernorate.objects.create(name_ar="حضرموت", name_en="Hadramout")
        original_updated = gov.updated_at
        gov.name_ar = "حضرموت - المكلا"
        gov.save()
        gov.refresh_from_db()
        self.assertGreaterEqual(gov.updated_at, original_updated)
