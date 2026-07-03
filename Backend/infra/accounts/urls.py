"""
Accounts URLs — مسارات API إدارة المستخدمين
═══════════════════════════════════════════════
Auth:     /auth/login/, /auth/logout/, /auth/refresh/, /auth/me/, /auth/change-password/
Users:    /users/, /users/<id>/, /users/<id>/activate/, ...
Sessions: /sessions/, /sessions/terminate/, /sessions/terminate-all/
"""
from django.urls import path
from rest_framework.routers import DefaultRouter

from infra.accounts.api.auth_views import AuthViewSet
from infra.accounts.api.user_views import UserManagementViewSet
from infra.accounts.api.session_views import SessionViewSet

router = DefaultRouter()
router.register(r'users', UserManagementViewSet, basename='user')

urlpatterns = [
    # ── Auth ──
    path(
        'auth/login/',
        AuthViewSet.as_view({'post': 'login'}),
        name='accounts-auth-login',
    ),
    path(
        'auth/logout/',
        AuthViewSet.as_view({'post': 'logout'}),
        name='accounts-auth-logout',
    ),
    path(
        'auth/logout-all/',
        AuthViewSet.as_view({'post': 'logout_all'}),
        name='accounts-auth-logout-all',
    ),
    path(
        'auth/refresh/',
        AuthViewSet.as_view({'post': 'refresh'}),
        name='accounts-auth-refresh',
    ),
    path(
        'auth/me/',
        AuthViewSet.as_view({'get': 'me', 'put': 'update_me', 'patch': 'update_me'}),
        name='accounts-auth-me',
    ),
    path(
        'auth/change-password/',
        AuthViewSet.as_view({'post': 'change_password'}),
        name='accounts-auth-change-password',
    ),

    # ── Sessions (Device Management) ──
    path(
        'sessions/',
        SessionViewSet.as_view({'get': 'list'}),
        name='accounts-session-list',
    ),
    path(
        'sessions/terminate/',
        SessionViewSet.as_view({'post': 'terminate'}),
        name='accounts-session-terminate',
    ),
    path(
        'sessions/terminate-all/',
        SessionViewSet.as_view({'post': 'terminate_all'}),
        name='accounts-session-terminate-all',
    ),
]

urlpatterns += router.urls
