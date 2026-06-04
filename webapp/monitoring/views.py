from rest_framework import authentication, permissions
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from monitoring.models import ServerStatus
from monitoring.serializers import MonitoringSerializer, ServerSerializer
from system.models import Server


class MyPageNumberPagination(PageNumberPagination):
    page_size = 10


class MonitoringViewSet(ModelViewSet):
    serializer_class = MonitoringSerializer
    authentication_classes = [
        authentication.SessionAuthentication,
        authentication.TokenAuthentication
    ]
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    
    filter_backends = [
        DjangoFilterBackend,
        
    ]
    filterset_fields = [
        'server',
        'cpu_usage',
        'ram_usage',
        'disk_usage',
        'uptime',
    ]

    def get_queryset(self):
        return ServerStatus.objects.filter(
            server__user = self.request.user
        )

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
    
