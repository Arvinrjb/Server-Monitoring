from rest_framework.routers import DefaultRouter
from monitoring.views import MonitoringViewSet, AddServerViewSet, DashboardViewSet


router = DefaultRouter()

router.register(
    r"servers",
    DashboardViewSet,
    basename='MonitoringViewSet'
)

router.register(
    r"addserver",
    AddServerViewSet,
    basename="servers",
)

router.register(
    r"agent/report",
    MonitoringViewSet,
    basename="agent"
)

urlpatterns = router.urls
