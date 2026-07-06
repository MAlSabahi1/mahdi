from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from d_services.models.GrantSource import GrantSource
from config.imports.viewmodel_core import DynamicFieldsModelSerializer

class GrantSourceSerializer(DynamicFieldsModelSerializer):
    source_type__display = serializers.ReadOnlyField(source='get_source_type_display')

    class Meta:
        model = GrantSource
        fields = '__all__'
        read_only_fields = ['id']
    

