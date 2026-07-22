# Licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).
# See the LICENSE file in the project root for the full license text.
# Copyright (C) 2026 arvin, arvinrjb13@gmail.com

from rest_framework import serializers
from monitoring.models import ServerStatus
from system.models import Server
from logs.serializers import LogSerializer

class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServerStatus
        fields = [
            'uptime_seconds',
            'process_count',
            'cpu_usage',
            'ram_usage',
            'disk_usage',
            'network_in',
            'network_out',
            'lastupdate',
        ]


class StatusSerializer(serializers.ModelSerializer):
    server = serializers.CharField(
        source='server.hostname',
        read_only=True
    )
    class Meta:
        model = ServerStatus
        fields = [
            'server',
            'uptime_seconds',
            'process_count',
            'cpu_usage',
            'ram_usage',
            'disk_usage',
            'network_in',
            'network_out',
            'lastupdate',
        ]


class DashboardSerializer(serializers.ModelSerializer):
    latest_status = serializers.SerializerMethodField()
    lastest_log = serializers.SerializerMethodField()
    user = serializers.CharField(
        source="user.first_name",
        read_only=True
    )
    class Meta:
        model = Server
        fields = [
            'user',
            'id',
            'ipaddress',
            'hostname',
            'os',
            'status',
            'latest_status',
            'lastest_log',
            'agent_token'
        ]
        read_only_fields=[
            "agent_token"
        ]

    def get_latest_status(self, obj):
        status = obj.prefetched_statuses
        if not status:
            return None
        return StatusSerializer(status[0]).data
    
    def get_lastest_log(self, obj):
        log = obj.prefetch_logs
        if not log:
            return None
        return LogSerializer(log[0]).data
    
