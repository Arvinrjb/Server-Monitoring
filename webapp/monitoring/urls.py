from rest_framework.routers import DefaultRouter
from monitoring.views import AddStatusViewSet, AddServerViewSet, DashboardViewSet


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
    AddStatusViewSet,
    basename="agent"
)

urlpatterns = router.urls
