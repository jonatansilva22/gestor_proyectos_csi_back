from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, StatusTypeViewSet

# Create a router and register our viewsets with it.

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'status-types', StatusTypeViewSet, basename='status-type')

# The API URLs are now determined automatically by the router.

urlpatterns = [
    path('', include(router.urls)),
]