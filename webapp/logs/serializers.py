from rest_framework import serializers
from logs.models import Logs



class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logs
        fields = [
            "message",
            "level"
        ]

class LogBatchSerializer(serializers.Serializer):
    logs = LogSerializer(many=True)
    

class ViewLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logs
        fields = [
            'server',
            'message',
            'level'
        ]