from django_filters.rest_framework import DjangoFilterBackend
from django.core.cache import cache
from rest_framework import authentication, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.exceptions import ValidationError
from monitoring.models import ServerStatus
from monitoring.serializers import AddStatusSerializer, DashboardSerializer, ServerSerializer
from system.models import Server
from core.pagination import MyPagination, StatusPagination




class DashboardViewSet(ModelViewSet):
    serializer_class = DashboardSerializer
    pagination_class = MyPagination
    authentication_classes = [
        authentication.SessionAuthentication,
    ]
    permission_classes = [
        permissions.IsAuthenticated
    ]
    def get_queryset(self):
        return Server.objects.filter(
            user = self.request.user
        )


class AddStatus(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        token = request.headers.get(
            "X-Agent-Token"
        )
        server = Server.objects.get(
            agent_token = token
        )
        if not server:
            return Response(
                {"error": "Invalid token"},
                status=401
            )
        ServerStatus.objects.create(
            server=server,
            cpu_usage=request.data["cpu_usage"],
            ram_usage=request.data["ram_usage"],
            disk_usage=request.data["disk_usage"],
            lastupdate= request.data["lastupdate"],
        )
        return Response(
            {"status": "ok"},
            status=201
        )



class AddStatusViewSet(ModelViewSet):
    pagination_class = StatusPagination
    serializer_class = AddStatusSerializer
    authentication_classes = [
        authentication.TokenAuthentication,
        # authentication.SessionAuthentication
    ]
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter, 
        OrderingFilter,
    ]
    filterset_fields = {
        'server':['exact'],
        'cpu_usage':['gte', 'lte'],
        'ram_usage':['gte', 'lte'],
        'disk_usage':['gte', 'lte'],
        'uptime':['gte', 'lte'],
    }

    search_fields = [
        'server__hostname',
        'server__ipaddress',
    ]

    ordering_fields = [
        'cpu_usage',
        'ram_usage',
        'disk_usage',
        'uptime',
    ]

    def get_queryset(self):
        return ServerStatus.objects.filter(
            server__user = self.request.user
        )
    
    def perform_create(self, serializer):
        server = serializer.validated_data['server']
        if server.user != self.request.user:
            raise ValidationError(
                "You do not own this server."
            )
        serializer.save()


class AddServerViewSet(ModelViewSet):
    pagination_class = MyPagination
    authentication_classes = [
        authentication.SessionAuthentication
    ]
    permission_classes = [
        permissions.IsAuthenticated
    ]
    
    serializer_class = ServerSerializer

    def get_queryset(self): 
        return Server.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):
        return serializer.save(
            user=self.request.user
            )
    
