from rest_framework import serializers
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