# Licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).
# See the LICENSE file in the project root for the full license text.
# Copyright (C) 2026 arvin, arvinrjb13@gmail.com

from django_filters.rest_framework import DjangoFilterBackend
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework import status, authentication
from rest_framework.filters import SearchFilter, OrderingFilter
from logs.serializers import ViewLogSerializer, LogBatchSerializer
from logs.models import Logs
from system.models import Server
from core.pagination import ApiPagination
from core.Permissions import IsOwnerOrAdmin

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
        IsOwnerOrAdmin
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

    def list(self, request, *args, **kwargs):
        cache_key = (
            f"logs_{self.request.user.id}_"
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
            data,
            serializer.data,
            timeout=60
        )
        return Response(
            serializer.data
        )
    
    def get_queryset(self):
        if self.request.user.has_perms(
            [
                "logs.view_all_logs"
            ]
        ):
            logs =  Logs.objects.all()
        else:
            logs = Logs.objects.filter(
            server__user = self.request.user
        ).order_by("-id")
        return logs
