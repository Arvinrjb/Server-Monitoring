from django.urls import path
from rest_framework.routers import DefaultRouter
from monitoring.views import DashboardViewSet, AddStatus, Status, ServerChartAPIView


router = DefaultRouter()

router.register(
    r"servers",
    DashboardViewSet,
    basename='MonitoringViewSet'
)



urlpatterns = router.urls
urlpatterns += [
    path(
        'agent/status/report/',
        AddStatus.as_view(),
        name='AgentStatus'
    ),
    path(
        "servers/<int:server_id>/chart/",
        ServerChartAPIView.as_view(),
        name="server-chart"
    ),
]
