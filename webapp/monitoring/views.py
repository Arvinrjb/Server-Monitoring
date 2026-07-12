# Licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).
# See the LICENSE file in the project root for the full license text.
# Copyright (C) 2026 arvin, arvinrjb13@gmail.com

from datetime import timedelta
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.core.cache import cache
from django.db.models import Prefetch
from rest_framework import authentication, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from monitoring.models import ServerStatus
from monitoring.serializers import DashboardSerializer, AgentSerializer, StatusSerializer
from logs.models import Logs
from system.models import Server
from core.pagination import PagePagination
from core.AlertManager import AlertsManager_CPU, AlertsManager_RAM, AlertsManager_DISK
from core.Permissions import IsOwnerOrAdmin


class DashboardViewSet(ReadOnlyModelViewSet):
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
        statuses_prefetch = Prefetch(
            "statuses",
            queryset=ServerStatus.objects.order_by(
                "-lastupdate"
            ),
            to_attr="prefetched_statuses"
        )
        logs_prefetch = Prefetch(
            "logs",
            queryset=Logs.objects.order_by(
                "-id"
            ),
            to_attr="prefetch_logs"
        )
        if self.request.user.has_perms(
            [
                "monitoring.view_all_statuses",
            ]
        ):
            qs = Server.objects.select_related(
                "user"
            )
        else:
            qs =  Server.objects.filter(
                user = self.request.user
            ).select_related(
                "user"
            )
        return qs.prefetch_related(
            statuses_prefetch,
            logs_prefetch
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
            server.lastseen = timezone.localtime(timezone.now())
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
            local_dt = timezone.localtime(status.lastupdate)
            bucket = local_dt.replace(
            minute=(local_dt.minute // 10) * 10,
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

