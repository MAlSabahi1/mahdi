import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from infra.storage.models import Document
docs = Document.objects.order_by('-created_at')[:5]
for doc in docs:
    print(doc.id, doc.document_type, doc.original_filename)
