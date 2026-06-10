from rest_framework import serializers
from monitoring.models import ServerStatus
from system.models import Server



class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServerStatus
        fields = [
            'cpu_usage',
            'ram_usage',
            'disk_usage',
            'lastupdate'
        ]


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


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServerStatus
        fields = [
            'cpu_usage',
            'ram_usage',
            'disk_usage',
            'uptime',
        ]


class DashboardSerializer(serializers.ModelSerializer):
    latest_status = serializers.SerializerMethodField()
    class Meta:
        model = Server
        fields = [
            'id',
            'ipaddress',
            'hostname',
            'os',
            'status',
            'latest_status',
        ]

    def get_latest_status(self, obj):
        status = obj.statuses.order_by(
            "-lastupdate"
        ).first()
        if not status:
            return None
        return StatusSerializer(status).data


class AddStatusSerializer(serializers.ModelSerializer):
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

    class Meta:
        model = ServerStatus
        fields = [
            'server',
            'id',
            'cpu_usage',
            'ram_usage',
            'disk_usage',
            'uptime',
            'lastupdate',
        ]
