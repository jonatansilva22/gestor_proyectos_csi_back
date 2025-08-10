#from django.urls import path
#from .views import UserCreateView

#urlpatterns = [
#path('register/', UserCreateView.as_view(), name='user-register'),
#]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

#Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'create-user', UserViewSet, basename='create-user')

urlpatterns = [
    path('', include(router.urls)),
]