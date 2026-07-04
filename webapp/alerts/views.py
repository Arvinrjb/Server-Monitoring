from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework import authentication, permissions
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
            return Alert.objects.all()

        return Alert.objects.filter(
            server__user = self.request.user
        ).select_related(
            "server"
        )