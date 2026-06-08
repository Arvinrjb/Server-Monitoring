from django.urls import path
from rest_framework.routers import DefaultRouter
from monitoring.views import AddStatusViewSet, AddServerViewSet, DashboardViewSet, AddStatus


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

# router.register(
#     r"agent/report",
#     AddStatusViewSet,
#     basename="Agent"
# )

urlpatterns = router.urls
urlpatterns += [
    path(
        'agent/report/',
        AddStatus.as_view(),
        name='Agent'
    )
]
