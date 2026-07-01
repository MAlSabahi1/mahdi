"""
URL configuration for HRMS project.
المرحلة 4: Master Router مع Versioning و Swagger
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from drf_spectacular.views import (
    SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView,
)


def api_root(request):
    return JsonResponse({
        'success': True,
        'message': 'HRMS API - نظام إدارة الموارد',
        'version': 'v1',
        'endpoints': {
            'docs': '/api/v1/docs/',
            'redoc': '/api/v1/redoc/',
            'schema': '/api/v1/schema/',
            'auth': '/api/v1/auth/',
            'personnel': '/api/v1/personnel/',
            'service_cycle': '/api/v1/service-cycle/',
            'dictionaries': '/api/v1/dictionaries/',
            'admin_panel': '/admin/',
        }
    })


# API v1 patterns
api_v1_patterns = [
    # Identity Infrastructure
    path('', include('infra.accounts.urls')),

    # Authorization (RBAC + Permissions)
    path('', include('infra.authorization.urls')),

    # Audit
    path('', include('infra.audit.urls')),

    # Security: Dual Auth + Telemetry + Settings
    path('', include('infra.security.urls')),

    # Personnel
    path('personnel/', include('systems.personnel.urls')),

    # Service Cycle
    path('service-cycle/', include('systems.services.urls')),

    # Dictionaries
    path('dictionaries/', include('core.api.urls')),

    # Storage
    path('storage/', include('infra.storage.urls')),
]

urlpatterns = [
    # Root
    path('', api_root, name='api-root'),
    
    # Admin
    path('admin/', admin.site.urls),
    
    # Schema & Documentation (outside namespace so drf-spectacular can reverse them)
    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/v1/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/v1/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # API v1
    path('api/v1/', include((api_v1_patterns, 'api'), namespace='v1')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
