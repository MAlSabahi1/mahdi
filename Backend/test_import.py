import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from systems.services.application.services.import_service import ExcelImportService
from systems.services.models import ExportLog

# Try with a completely random file
svc = ExcelImportService(
    file_content=b"random content",
    export_id="00000000-0000-0000-0000-000000000000",
    imported_by=None,
    original_filename="random.xlsx",
    service_month="2026-07"
)
try:
    svc.process()
    print("ACCEPTED!")
except Exception as e:
    print(f"REJECTED: {e}")
