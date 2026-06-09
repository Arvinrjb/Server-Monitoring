from django.urls import path
from rest_framework.routers import DefaultRouter
from monitoring.views import DashboardViewSet, AddStatus


router = DefaultRouter()

router.register(
    r"servers",
    DashboardViewSet,
    basename='MonitoringViewSet'
)



urlpatterns = router.urls
urlpatterns += [
    path(
        'agent/report/',
        AddStatus.as_view(),
        name='Agent'
    )
]
