from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from django.core.cache import cache
from rest_framework import authentication, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.exceptions import ValidationError
from monitoring.models import ServerStatus
from monitoring.serializers import AddStatusSerializer, DashboardSerializer, AgentSerializer, ServerSerializer
from system.models import Server
from core.pagination import PagePagination, ApiPagination
from core.AlertManager import AlertsManager_CPU, AlertsManager_RAM, AlertsManager_DISK
from core.Permissions import IsServerOwnerOrAdmin


class DashboardViewSet(ModelViewSet):
    serializer_class = DashboardSerializer
    pagination_class = PagePagination
    authentication_classes = [
        authentication.SessionAuthentication,
    ]
    permission_classes = [
        IsServerOwnerOrAdmin
    ]
    def get_queryset(self):
        if self.request.user.is_staff:
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



# class AddStatusViewSet(ModelViewSet):
#     pagination_class = ApiPagination
#     serializer_class = AddStatusSerializer
#     authentication_classes = [
#         authentication.TokenAuthentication,
#         # authentication.SessionAuthentication
#     ]
#     permission_classes = [
#         permissions.IsAuthenticated,
#     ]

#     filter_backends = [
#         DjangoFilterBackend,
#         SearchFilter, 
#         OrderingFilter,
#     ]
#     filterset_fields = {
#         'server':['exact'],
#         'cpu_usage':['gte', 'lte'],
#         'ram_usage':['gte', 'lte'],
#         'disk_usage':['gte', 'lte'],
#         'uptime':['gte', 'lte'],
#     }

#     search_fields = [
#         'server__hostname',
#         'server__ipaddress',
#     ]

#     ordering_fields = [
#         'cpu_usage',
#         'ram_usage',
#         'disk_usage',
#         'uptime',
#     ]

#     def get_queryset(self):
#         return ServerStatus.objects.filter(
#             server__user = self.request.user
#         )
    
#     def perform_create(self, serializer):
#         server = serializer.validated_data['server']
#         if server.user != self.request.user:
#             raise ValidationError(
#                 "You do not own this server."
#             )
#         serializer.save()


# class AddServerViewSet(ModelViewSet):
#     pagination_class = PagePagination
#     authentication_classes = [
#         authentication.SessionAuthentication
#     ]
#     permission_classes = [
#         permissions.IsAuthenticated
#     ]
    
#     serializer_class = ServerSerializer

#     def get_queryset(self): 
#         return Server.objects.filter(
#             user=self.request.user
#         )

#     def perform_create(self, serializer):
#         return serializer.save(
#             user=self.request.user
#             )
    
