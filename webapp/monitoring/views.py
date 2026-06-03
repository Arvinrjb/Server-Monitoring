from rest_framework import authentication, permissions
from rest_framework.viewsets import ModelViewSet
from monitoring.models import SystemStatus
from monitoring.serializers import MonitoringSerializer
from system.models import Server
from system.serializers import ServerSerializer


class MonitoringViewSet(ModelViewSet):
    serializer_class = MonitoringSerializer
    authentication_classes = [
        authentication.SessionAuthentication,
        authentication.TokenAuthentication
    ]
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    
    def get_queryset(self):
        return SystemStatus.objects.filter(
            server__user = self.request.user
            
        )

    def perform_create(self, serializer):
        return 
    
class AddServerViewSet(ModelViewSet):
    authentication_classes = [
        authentication.SessionAuthentication,
    ]
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = ServerSerializer

    def get_queryset(self):
        return Server.objects.filter(
            user = self.request.user
        )
    
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
    
