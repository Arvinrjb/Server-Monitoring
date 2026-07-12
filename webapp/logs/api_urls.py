# Licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).
# See the LICENSE file in the project root for the full license text.
# Copyright (C) 2026 arvin, arvinrjb13@gmail.com

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
