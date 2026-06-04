from rest_framework.routers import DefaultRouter
from monitoring.views import MonitoringViewSet, AddServerViewSet


router = DefaultRouter()


router.register(
    r"servers",
    MonitoringViewSet,
    basename='MonitoringViewSet'
)

router.register(
    r"addserver",
    AddServerViewSet,
    basename="servers",
)

urlpatterns = router.urls

