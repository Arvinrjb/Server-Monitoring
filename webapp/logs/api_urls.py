from rest_framework.routers import DefaultRouter
from django.urls import path
from logs.views import AgentLog, LogsViewSet

router = DefaultRouter()

router.register(
    'logs',
    LogsViewSet,
    basename='logs'
)
urlpatterns = router.urls

urlpatterns += [
    path('agent/logs/report/', AgentLog.as_view()),
]
