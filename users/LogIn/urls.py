from django.urls import path
from .views import LogInView

urlpatterns = [
    path('login/', LogInView.as_view(), name='login'),
]