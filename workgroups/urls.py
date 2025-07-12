from rest_framework.routers import DefaultRouter
from .views import WorkGroupViewSet

router = DefaultRouter()
router.register(r'groups', WorkGroupViewSet, basename='group')

urlpatterns = router.urls
