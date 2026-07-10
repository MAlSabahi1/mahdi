import os, sys, django
sys.path.append('/home/mahdi/Desktop/n/mahdi/Backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from infra.storage.models import Document
docs = Document.objects.filter(personnel__military_number='6042041').exclude(context_type='NationalIdUpdate').filter(document_type__in=['national_id_front', 'national_id_back', 'id_card', 'other'])
print(f"Found {docs.count()} duplicates")
for d in docs:
    print(d.id, d.document_type, d.context_type)
    d.delete()
print("Done")
