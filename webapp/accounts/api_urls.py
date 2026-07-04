from rest_framework.routers import DefaultRouter
from accounts.views import ProfileViewSet

router = DefaultRouter()

router.register(
    "profile",
    ProfileViewSet,
    basename="Profile"
)

urlpatterns = router.urls