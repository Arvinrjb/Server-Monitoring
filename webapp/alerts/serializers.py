from rest_framework import serializers
from alerts.models import Alert



class ShowAlertsSerializer(serializers.ModelSerializer):
    server_name = serializers.CharField(
        source="server.hostname",
        read_only=True
    )
    class Meta:
        model = Alert
        fields = [
            'is_active',
            'title',
            'message',
            'level',
            'server_name',
            'created_at',
        ]