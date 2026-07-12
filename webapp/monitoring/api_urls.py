# Licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).
# See the LICENSE file in the project root for the full license text.
# Copyright (C) 2026 arvin, arvinrjb13@gmail.com

from django.urls import path
from rest_framework.routers import DefaultRouter
from monitoring.views import DashboardViewSet, AddStatus, ServerChartAPIView


router = DefaultRouter()

router.register(
    r"servers",
    DashboardViewSet,
    basename='View Dashboard'
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
