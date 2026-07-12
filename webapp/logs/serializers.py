# Licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).
# See the LICENSE file in the project root for the full license text.
# Copyright (C) 2026 arvin, arvinrjb13@gmail.com

from rest_framework import serializers
from logs.models import Logs



class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logs
        fields = [
            "message",
            "level",
        ]

class LogBatchSerializer(serializers.Serializer):
    logs = LogSerializer(many=True)
    

class ViewLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logs
        fields = [
            'server',
            'message',
            'level',
            'created_at'
        ]