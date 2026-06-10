from rest_framework.routers import DefaultRouter
from django.urls import path
from logs.views import AgentLog


urlpatterns = [
    path('agent/logs/report/', AgentLog.as_view()),
]
