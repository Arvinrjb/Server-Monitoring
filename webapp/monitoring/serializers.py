from rest_framework import serializers
from monitoring.models import SystemStatus
from system.models import Server


class ServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Server
        fields = [
            'id',
            'hostname',
            'ipaddress',
        ]


class MonitoringSerializer(serializers.ModelSerializer):
    server = ServerSerializer(
        read_only = True
    )
    
    class Meta:
        model = SystemStatus
        fields = [
            'server',
            'cpu_usage',
            'ram_usage',
            'disk_usage',
            'uptime',
        ]
