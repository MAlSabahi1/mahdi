import os
import re

TEST_FILES = [
    "test_monthly_snapshot.py",
    "test_staging_review.py",
    "test_export_service.py",
    "test_full_cycle.py",
    "test_import_service.py",
    "test_api_phase4.py"
]

for filename in TEST_FILES:
    filepath = os.path.join("/home/mahdi/Desktop/POL/backend/services/tests", filename)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Imports
    content = re.sub(
        r"from core\.models import Governorate,\s*Directorate,\s*Rank,\s*ServiceStatus,\s*Qualification,\s*Location",
        "from core.models import GeoGovernorate, SecurityAdministration, CentralDepartment, GeoLocation, Rank, ServiceStatus, Qualification",
        content
    )
    # Class usage
    content = content.replace("Governorate.objects.create", "GeoGovernorate.objects.create")
    content = content.replace("Directorate.objects.create", "CentralDepartment.objects.create")
    content = content.replace("Location.objects.create", "GeoLocation.objects.create")
    
    # Models references (if any)
    content = content.replace("Governorate", "GeoGovernorate")
    content = content.replace("Directorate", "CentralDepartment")
    content = content.replace("Location", "GeoLocation")
    
    # Fields
    content = content.replace("directorate=self.directorate", "central_department=self.directorate")
    content = content.replace("directorate=self.dept1", "central_department=self.dept1")
    content = content.replace("directorate=self.dept2", "central_department=self.dept2")
    content = content.replace("directorate=department", "central_department=department")
    content = content.replace("directorate=empty_dept", "central_department=empty_dept")
    
    # kwargs and dicts
    content = content.replace("'directorate_id': self.directorate.id", "'central_department_id': self.directorate.id")
    content = content.replace("'directorate_id': self.dept1.id", "'central_department_id': self.dept1.id")
    content = content.replace("'directorate_id': department.id", "'central_department_id': department.id")
    
    # location field
    content = content.replace("location=self.location", "geo_location=self.location")
    content = content.replace("location=location", "geo_location=location")
    
    # fix CentralDepartment creation kwargs
    content = re.sub(r"governorate=self\.governorate(,\s*level=\d+)?", r"security_admin=self.security_admin", content)
    content = re.sub(r"governorate=governorate(,\s*level=\d+)?", r"security_admin=security_admin", content)
    
    # ensure security_admin is created
    # find where GeoGovernorate is created and insert SecurityAdmin creation
    if "self.security_admin = SecurityAdministration" not in content and "self.governorate = " in content:
        content = content.replace(
            "self.governorate = GeoGovernorate.objects.create(",
            "self.security_admin = SecurityAdministration.objects.create(name='أمن العاصمة')\n        self.governorate = GeoGovernorate.objects.create("
        )
    elif "security_admin = SecurityAdministration" not in content and "governorate = GeoGovernorate" in content:
        content = content.replace(
            "governorate = GeoGovernorate.objects.create(",
            "security_admin = SecurityAdministration.objects.create(name='أمن العاصمة')\n    governorate = GeoGovernorate.objects.create("
        )
    elif "cls.security_admin = SecurityAdministration" not in content and "cls.governorate = GeoGovernorate" in content:
        content = content.replace(
            "cls.governorate = GeoGovernorate.objects.create(",
            "cls.security_admin = SecurityAdministration.objects.create(name='أمن العاصمة')\n        cls.governorate = GeoGovernorate.objects.create("
        )
    
    # remove `level=1` if it survived
    content = content.replace(", level=1,", ",")
    content = content.replace(" level=1,", "")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
        
print("Replacement script executed.")
