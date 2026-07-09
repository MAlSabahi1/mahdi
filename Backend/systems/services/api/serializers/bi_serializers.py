from rest_framework import serializers
from ...models import BIDataSource, EnterpriseReportTemplate

class BIDataSourceSerializer(serializers.ModelSerializer):
    source_type_display = serializers.CharField(source='get_source_type_display', read_only=True)

    class Meta:
        model = BIDataSource
        fields = ['id', 'name', 'source_type', 'source_type_display', 'target', 'description', 'is_active']


class EnterpriseReportTemplateSerializer(serializers.ModelSerializer):
    data_source_details = BIDataSourceSerializer(source='data_source', read_only=True)

    class Meta:
        model = EnterpriseReportTemplate
        fields = [
            'id', 'title', 'slug', 'description', 'data_source', 
            'data_source_details', 'config_schema', 'is_active', 
            'created_by', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_at']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['created_by'] = request.user
        return super().create(validated_data)
