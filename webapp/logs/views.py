from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework import status, authentication, permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from logs.serializers import LogSerializer, ViewLogSerializer, LogBatchSerializer
from logs.models import Logs
from system.models import Server
from core.pagination import PagePagination, ApiPagination


class AgentLog(APIView):
    permission_classes = []
    authentication_classes = []
    
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
        except Server.DoesNotExist:
            return Response(
                {"error":"invalid token"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        # serializer = LogSerializer(
        #     data = request.data
        # )
        # serializer.is_valid(
        #     raise_exception=True
        # )
        # serializer.save(
        #     server = server
        # )
        serializer = LogBatchSerializer(
            data = request.data
        )
        serializer.is_valid(
            raise_exception=True
        )
        for log in serializer.validated_data["logs"]:
            Logs.objects.create(
                server=server, 
                message=log["message"],
                level=log["level"],
            )
        return Response(
            {"status": "ok"},
            status=status.HTTP_201_CREATED
        )



class LogsViewSet(ReadOnlyModelViewSet):
    pagination_class = ApiPagination
    authentication_classes = [
        authentication.SessionAuthentication,
    ]
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = ViewLogSerializer

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_fields = [
        'server',
        'level',
    ]

    search_fields = [
        'server__hostname',
        'server__ipaddress',
        'message',
        'level',
    ]

    ordering_fields = [ 
        'created_at',
    ]

    def get_queryset(self):
        return Logs.objects.filter(
            server__user = self.request.user
        ).order_by("-id")
