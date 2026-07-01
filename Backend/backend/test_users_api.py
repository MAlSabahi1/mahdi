import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.base")
django.setup()

from infra.accounts.models.user import User
from infra.accounts.serializers.user_serializers import UserOutputSerializer

user = User.objects.first()
serializer = UserOutputSerializer(user)
print("SERIALIZED DATA:", serializer.data)
