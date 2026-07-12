# Licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).
# See the LICENSE file in the project root for the full license text.
# Copyright (C) 2026 arvin, arvinrjb13@gmail.com

from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework import authentication
from alerts.models import Alert
from alerts.serializers import ShowAlertsSerializer
from core.Permissions import IsOwnerOrAdmin


class AlertViewSet(ReadOnlyModelViewSet):
    authentication_classes = [
        authentication.SessionAuthentication,
    ]
    permission_classes = [
        IsOwnerOrAdmin
    ]
    serializer_class = ShowAlertsSerializer
    def get_queryset(self):
        if self.request.user.has_perms(
            [
                "alerts.view_all_alerts"
            ]
        ):
            alerts = Alert.objects.all()
        else:
            alerts = Alert.objects.filter(
                server__user = self.request.user
            )
        return alerts.select_related(
            "server"
        )