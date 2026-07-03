from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CorrespondenceViewSet, TaskViewSet, CircularViewSet

router = DefaultRouter()
router.register(r'correspondences', CorrespondenceViewSet, basename='correspondence')
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'circulars', CircularViewSet, basename='circular')

app_name = 'secretariat'

urlpatterns = [
    path('', include(router.urls)),
]
