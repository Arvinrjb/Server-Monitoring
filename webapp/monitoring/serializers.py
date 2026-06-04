from rest_framework import serializers
from monitoring.models import ServerStatus
from system.models import Server


class ServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Server
        fields = [
            'id',
            'ipaddress',
            'hostname',
            'os',
            'status',
            'lastseen',
        ]


class MonitoringSerializer(serializers.ModelSerializer):
    cpu_usage = serializers.FloatField(
        min_value = 0,
        max_value = 100
    )
    ram_usage = serializers.FloatField(
        min_value = 0,
        max_value = 100
    )
    disk_usage = serializers.FloatField(
        min_value = 0,
        max_value = 100
    )
    server = ServerSerializer(
        read_only = True
    )
    class Meta:
        model = ServerStatus
        fields = [
            'server',
            'id',
            'cpu_usage',
            'ram_usage',
            'disk_usage',
            'uptime',
        ]
