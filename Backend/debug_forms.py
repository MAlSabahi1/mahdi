from systems.personnel.models import PersonnelMaster
from infra.storage.models import Document
from systems.services.models import StatusChangeForm

p = PersonnelMaster.objects.get(military_number='9900003')
docs = Document.objects.filter(personnel=p, status='committed')
print("--- Documents ---")
for d in docs:
    if d.context_type == 'StatusChangeForm':
        print(f"Doc ID: {d.id}, context_type: {d.context_type}, context_id: '{d.context_id}', repr: {repr(d.context_id)}")

form_ids = [str(d.context_id).replace('#', '') for d in docs if d.context_type == 'StatusChangeForm' and d.context_id]
print("\n--- Form IDs extracted ---")
print(form_ids)

forms = StatusChangeForm.objects.filter(id__in=form_ids)
print("\n--- Forms found in DB ---")
for f in forms:
    print(f"Form ID: {f.id}, type: {f.form_type}")

print("\n--- Are they matching? ---")
forms_dict = {str(f.id): f.form_type for f in forms}
for d in docs:
    if d.context_type == 'StatusChangeForm':
        cid = str(d.context_id).replace('#', '')
        print(f"Checking cid '{cid}' against forms_dict keys {list(forms_dict.keys())} -> {cid in forms_dict}")
