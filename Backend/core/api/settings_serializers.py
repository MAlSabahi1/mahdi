from rest_framework import serializers
from core.models.settings import SystemSetting

class SystemSettingSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    
    class Meta:
        model = SystemSetting
        fields = [
            'id', 'category', 'category_display', 'key', 'title', 
            'description', 'value_type', 'value', 'is_active', 'updated_at'
        ]
        read_only_fields = ['id', 'key', 'value_type', 'category', 'title', 'description', 'updated_at']

    def validate_value(self, value):
        # Validate value castability based on instance type
        instance = getattr(self, 'instance', None)
        if instance:
            vt = instance.value_type
            try:
                if vt == 'int':
                    int(value)
                elif vt == 'float':
                    float(value)
                elif vt == 'bool':
                    if str(value).lower() not in ['true', 'false', '1', '0', 'yes', 'no', 't', 'f']:
                        raise ValueError
                elif vt == 'json':
                    import json
                    json.loads(value)
            except ValueError:
                raise serializers.ValidationError(f"يجب أن تكون القيمة من نوع {instance.get_value_type_display()}")
        return value
