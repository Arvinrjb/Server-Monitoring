from rest_framework import serializers
from system.models import Server


class ServerSerializer(serializers.ModelSerializer):
    user = serializers.CharField(
        source="user.username",
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
            'lastseen',
        ]
        read_only_fields = [
            'user',
            'id',
            
        ]