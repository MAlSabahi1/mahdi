from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from core.models.settings import SystemSetting
from core.api.settings_serializers import SystemSettingSerializer

class SystemSettingViewSet(viewsets.ModelViewSet):
    """
    API للتحكم في الإعدادات العامة للنظام.
    """
    queryset = SystemSetting.objects.all()
    serializer_class = SystemSettingSerializer
    # In production, require admin permissions
    permission_classes = [permissions.AllowAny]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_active']
    search_fields = ['title', 'key', 'description']
    ordering_fields = ['category', 'title']
    ordering = ['category', 'title']
