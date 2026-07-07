import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.base")
django.setup()

from systems.personnel.models import PersonnelMaster
from systems.services.models import StatusChangeForm, ServiceCatalog
from infra.storage.models import Document
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

def run():
    print("Starting test submission...")
    personnel = PersonnelMaster.objects.filter(military_number="7000055").first()
    if not personnel:
        print("Personnel not found!")
        return

    admin = User.objects.filter(is_superuser=True).first()
    if not admin:
        print("Admin user not found!")
        return

    # Check / Create document IDs
    doc_ids = [42, 43, 44, 45]
    docs = list(Document.objects.filter(id__in=doc_ids))
    print(f"Found {len(docs)} documents out of required")

    # Create status change form for martyr
    form = StatusChangeForm.objects.create(
        personnel=personnel,
        security_admin=getattr(personnel, 'security_admin', None),
        form_type="martyr",
        form_data={
            "martyrdom_date": "2026-07-07",
            "martyrdom_cause": "أثناء تأدية الواجب الوطني دفاعاً عن الوطن",
            "martyrdom_location": "محافظة مأرب — مديرية صرواح",
            "occurrence_context": "أثناء الواجب"
        },
        from_status=personnel.current_status,
        to_status=None, # can be set by workflow or manually
        effective_date=timezone.now().date(),
        status="draft",
        submitted_by=admin,
        required_attachments=[
            "death_certificate",
            "heir_ruling",
            "power_of_attorney",
            "national_id_front",
            "attorney_id",
            "appointment_ruling",
            "operations_report",
            "assignment_order"
        ],
        notes="تم الرفع بواسطة النظام لغرض الاختبار والتحقق من الربط.",
    )
    
    # Associate documents
    form.attachments.set(docs)
    form.attachments_complete = len(docs) >= 2
    form.save()
    
    print(f"Form created as draft. ID: {form.id}")

    # Now submit the form (which moves it to in_progress)
    catalog = ServiceCatalog.objects.filter(form_type="martyr").first()
    if not catalog:
        print("Martyr service catalog not found!")
        return
        
    print(f"Service catalog found: {catalog.name_ar}, approval_type: {catalog.approval_type}")
    
    from systems.services.application.use_cases.status_change_use_cases import SubmitStatusFormUseCase, SubmitFormCommand
    from systems.services.infrastructure.repositories.django_status_change_repo import DjangoStatusChangeFormRepository

    repo = DjangoStatusChangeFormRepository()
    uc = SubmitStatusFormUseCase(repo)
    cmd = SubmitFormCommand(
        form_id=form.id,
        submitted_by=admin.id,
        submitted_at=timezone.now(),
        first_step_id=None
    )
    uc.execute(cmd)
    
    # Refresh from DB
    form.refresh_from_db()
    print(f"Form status after submission: {form.status}")
    print(f"Current step: {form.current_step}")
    print("Test submission completed successfully!")

if __name__ == "__main__":
    run()
