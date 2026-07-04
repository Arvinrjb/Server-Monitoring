from datetime import timedelta
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.core.cache import cache
from rest_framework import authentication, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.authentication import JWTAuthentication
from monitoring.models import ServerStatus
from monitoring.serializers import AddStatusSerializer, DashboardSerializer, AgentSerializer, ServerSerializer, StatusSerializer
from system.models import Server
from core.pagination import PagePagination, ApiPagination
from core.AlertManager import AlertsManager_CPU, AlertsManager_RAM, AlertsManager_DISK
from core.Permissions import IsOwnerOrAdmin, IsSupport, IsAdmin


class DashboardViewSet(ModelViewSet):
    serializer_class = DashboardSerializer
    pagination_class = PagePagination
    authentication_classes = [
        authentication.SessionAuthentication,
    ]
    permission_classes = [
        IsOwnerOrAdmin
    ]

    def list(self, request, *args, **kwargs):
        cache_key = (
            f"dashboard_{self.request.user.id}_"
            f"{self.request.GET.urlencode()}"
            )
        cache_data = cache.get(
            cache_key
        )
        if cache_data:
            return Response(
                cache_data
            )

        queryset = self.filter_queryset(
            self.get_queryset()
        )
        page = self.paginate_queryset(
            queryset
        )
        serializer = self.get_serializer(
            page,
            many=True
        )
        data = self.get_paginated_response(
            serializer.data
        ).data
        cache.set(
            cache_key,
            data,
            timeout=10
        )
        return Response(
            data
        )

    def get_queryset(self):
        if self.request.user.has_perms(
            [
                "monitoring.view_all_statuses",
            ]
        ):
            return Server.objects.all()

        return Server.objects.filter(
            user = self.request.user
        )


class AddStatus(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        try:
            token = request.headers.get(
                "X-Agent-Token"
            )
        except:
            return Response(
                {"error":"Token not send"},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:        
            server = Server.objects.get(
                agent_token = token
            )
            server.lastseen = timezone.now()
            server.save(
                update_fields=["lastseen"]
            )
        except Server.DoesNotExist:
            return Response(
                {"error": "Invalid token"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        serializer = AgentSerializer(
            data = request.data
        )

        serializer.is_valid(
            raise_exception=True
        )
        Server_status = serializer.save(
            server = server
        )
        AlertsManager_CPU(server, Server_status)
        AlertsManager_RAM(server, Server_status)
        AlertsManager_DISK(server, Server_status)

        return Response(
            {"status": "ok"},
            status=status.HTTP_201_CREATED
        )


class ServerChartAPIView(APIView):
    authentication_classes=[
        authentication.SessionAuthentication,
    ]
    permission_classes = [
        IsOwnerOrAdmin,
    ]

    def get(self, request, server_id):
        if self.request.user.has_perms(
            [
                "monitoring.view_all_statuses",
            ]
        ):            
            server = get_object_or_404(
                Server,
                id=server_id,
            )
        else:
            server = get_object_or_404(
                Server,
                id=server_id,
                user=request.user,
            )
        cache_key = (
            f"chart_{self.request.user.id}_"
            f"{server.id}"
        )
        cache_data = cache.get(
            cache_key
        )

        if cache_data:
            return Response(
                cache_data
            )
        
        last_24_hours = timezone.now() - timedelta(
            hours=24
        )

        statuses = ServerStatus.objects.filter(
            server=server,
            lastupdate__gte=last_24_hours,
        ).order_by(
            "lastupdate"
        )

        result = []
        groups = {}

        for status in statuses:
            bucket = status.lastupdate.replace(
            minute=(status.lastupdate.minute // 10) * 10,
            second=0,
            microsecond=0
            )
            if bucket not in groups:
                groups[bucket] = {
                "cpu": [],
                "ram": [],
                "disk": [],
                }
            groups[bucket]["cpu"].append(
            status.cpu_usage
            )
            groups[bucket]["ram"].append(
                status.ram_usage
            )
            groups[bucket]["disk"].append(
                status.disk_usage
            )

        for bucket, values in groups.items():
            avg_cpu = sum(
                values["cpu"]
            ) / len(values["cpu"])
            avg_ram = sum(
                values["ram"]
            ) / len(values["ram"])
            avg_disk = sum(
                values["disk"]
            ) / len(values["disk"])

            result.append({
                "time": bucket.strftime(
                    "%H:%M"
                ),
                "cpu": round(avg_cpu, 2),
                "ram": round(avg_ram, 2),
                "disk": round(avg_disk, 2),
            })

        cache.set(
            cache_key,
            result,
            timeout=600
        )

        return Response(
            result
        )


class Status(APIView):
    authentication_classes = [
        authentication.SessionAuthentication,
    ]
    permission_classes = [
        IsOwnerOrAdmin
    ]
    def get(self, request):
        if self.request.user.is_staff and self.request.user.is_superuser:
            data = ServerStatus.objects.all()
        else:
            data = ServerStatus.objects.filter(
            server__user = self.request.user 
            )
        serializer = StatusSerializer(
            data,
            many=True
        )
        return Response(serializer.data)

class AddStatusViewSet(ModelViewSet):
    pagination_class = ApiPagination
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
    pagination_class = PagePagination
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
    
