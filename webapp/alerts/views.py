from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework import authentication, permissions
from alerts.models import Alert
from alerts.serializers import ShowAlertsSerializer

class AlertViewSet(ReadOnlyModelViewSet):
    authentication_classes = [
        authentication.SessionAuthentication,
    ]
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = ShowAlertsSerializer
    def get_queryset(self):
        if self.request.user.is_staff:
            return Alert.objects.all()

        return Alert.objects.filter(
            server__user = self.request.user
        ).select_related(
            "server"
        )