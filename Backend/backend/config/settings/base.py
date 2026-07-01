"""
Django settings for HRMS project.
المرحلة 4: إعداد كامل لـ DRF + JWT + Throttling + Spectacular + Celery
"""

from pathlib import Path
import environ
import os
from datetime import timedelta

# Build paths inside the project
# config/settings/base.py يقع في backend/config/settings/
# نصعد 3 مستويات للوصول لجذر backend/
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Initialize environment variables
env = environ.Env(
    DEBUG=(bool, False)
)

# Read .env file
environ.Env.read_env(os.path.join(BASE_DIR.parent, '.env'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])


# Application definition

INSTALLED_APPS = [
    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',

    # Third party
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'django_fsm',
    'guardian',
    'django_filters',
    'drf_spectacular',
    'django_celery_results',
    'simple_history',

    # Infrastructure — البنية التحتية المشتركة
    'infra.accounts.apps.AccountsConfig',
    'infra.authorization.apps.AuthorizationConfig',
    'infra.audit.apps.AuditConfig',
    'infra.security.apps.SecurityConfig',
    'infra.storage.apps.StorageConfig',
    'infra.workflows.apps.WorkflowsConfig',

    # Core — البيانات المرجعية المشتركة
    'core.apps.CoreConfig',

    # Systems — الأنظمة التشغيلية
    'systems.personnel.apps.PersonnelConfig',
    'systems.services.apps.ServicesConfig',

    # Extensions
    'extensions.webhooks.apps.WebhooksConfig',
]

# Custom User Model
AUTH_USER_MODEL = 'accounts.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'infra.accounts.middleware.audit_context.AuditContextMiddleware',
    'infra.security.middleware.CurrentUserMiddleware',
    'config.middleware.GovernorateMiddleware',
    'infra.accounts.middleware.activity.ActivityTrackingMiddleware',
    'infra.authorization.middleware.permission_loader.PermissionLoaderMiddleware',
    'infra.security.request_signing.RequestSigningMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
        'DISABLE_SERVER_SIDE_CURSORS': True,
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
     'OPTIONS': {'min_length': 8}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
    {'NAME': 'infra.accounts.validators.password_validators.ArabicPasswordValidator'},
    {'NAME': 'infra.accounts.validators.password_validators.NoUsernameInPasswordValidator'},
]

# Password Hashers — Argon2 في المقدمة (الأكثر أماناً)
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]


# Internationalization
LANGUAGE_CODE = 'ar'
TIME_ZONE = 'Asia/Riyadh'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# =============================================================================
# CORS Settings
# =============================================================================
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3001",
    "http://localhost:5173",  # Frontend-new Vite dev server
    "http://127.0.0.1:5173",
    "http://localhost:5174",  # Fallback Vite dev server
    "http://127.0.0.1:5174",
]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    'accept', 'accept-encoding', 'authorization', 'content-type',
    'dnt', 'origin', 'user-agent', 'x-csrftoken', 'x-requested-with',
    'x-idempotency-key',  # المرحلة 4: Idempotency (with x- prefix)
    'idempotency-key',     # المرحلة 4: Idempotency (without x- prefix)
    'x-signature',         # Request signing
    'x-timestamp',         # Request timestamp for signing
]

# =============================================================================
# REST Framework Configuration (المرحلة 4)
# =============================================================================
REST_FRAMEWORK = {
    # Authentication
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    
    # Permissions
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    
    # Pagination
    'DEFAULT_PAGINATION_CLASS': 'core.pagination.DynamicPageSizePagination',
    'PAGE_SIZE': 50,
    'MAX_PAGE_SIZE': 1000,  # Allow clients to request up to 1000 items
    
    # Filtering
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    
    # Throttling (Rate Limiting)
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '30/minute',
        'user': '120/minute',
        'upload': '10/minute',
        'auth': '20/minute',
    },
    
    # Versioning
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
    'DEFAULT_VERSION': 'v1',
    'ALLOWED_VERSIONS': ['v1'],
    
    # Schema
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    
    # Renderers
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    
    # Exception Handling
    'EXCEPTION_HANDLER': 'core.exception_handler.global_exception_handler',
    
    # Date/Time
    'DATETIME_FORMAT': '%Y-%m-%dT%H:%M:%S%z',
    'DATE_FORMAT': '%Y-%m-%d',
}

# =============================================================================
# JWT Settings (المرحلة 4)
# =============================================================================
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),  # 15 دقيقة حسب المواصفات
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,  # نحدّث يدوياً في AuthService
    
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}

# =============================================================================
# DRF Spectacular (Swagger/OpenAPI)
# =============================================================================
SPECTACULAR_SETTINGS = {
    'TITLE': 'HRMS API - نظام إدارة الموارد',
    'DESCRIPTION': (
        'واجهة برمجة تطبيقات نظام إدارة الموارد.\n'
        'يدعم: JWT Authentication, RBAC/ABAC, Idempotency Keys, '
        'Rate Limiting, Async Tasks (Celery).'
    ),
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'SCHEMA_PATH_PREFIX': r'/api/v[0-9]',
    'TAGS': [
        {'name': 'auth', 'description': 'المصادقة وإدارة الجلسات'},
        {'name': 'users', 'description': 'إدارة المستخدمين (للمدير)'},
        {'name': 'roles', 'description': 'إدارة الأدوار (للمدير)'},
        {'name': 'personnel', 'description': 'إدارة بيانات الأفراد'},
        {'name': 'service-cycle', 'description': 'دورة الكشوفات الشهرية'},
        {'name': 'reconciliation', 'description': 'المطابقة'},
        {'name': 'reports', 'description': 'التقارير'},
        {'name': 'dictionaries', 'description': 'إدارة القواميس'},
        {'name': 'audit', 'description': 'سجل التدقيق'},
        {'name': 'dual-auth', 'description': 'التفويض المزدوج'},
        {'name': 'telemetry', 'description': 'المراقبة الأمنية'},
    ],
}

# =============================================================================
# Redis Cache
# =============================================================================
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# Session
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
SESSION_COOKIE_AGE = 1800  # 30 minutes

# Accounts — Session Inactivity Timeout
SESSION_INACTIVITY_TIMEOUT = 1800  # 30 دقيقة بدون نشاط → session revoke
MAX_SESSIONS_PER_USER = 5  # الحد الأقصى للجلسات النشطة لكل مستخدم

# =============================================================================
# Celery Configuration
# =============================================================================
CELERY_BROKER_URL = env('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = 'django-db'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 600  # 10 minutes max
CELERY_TASK_SOFT_TIME_LIMIT = 540

# =============================================================================
# Guardian (Object-Level Permissions)
# =============================================================================
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
)

# =============================================================================
# HMAC Audit Signing Key (المرحلة 3)
# =============================================================================
AUDIT_SIGNING_KEY = env('AUDIT_SIGNING_KEY', default=SECRET_KEY)
