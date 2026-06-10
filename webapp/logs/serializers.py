from rest_framework import serializers
from logs.models import Logs


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logs
        fields = [
            "message",
        ]
