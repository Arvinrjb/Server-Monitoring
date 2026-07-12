# Licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).
# See the LICENSE file in the project root for the full license text.
# Copyright (C) 2026 arvin, arvinrjb13@gmail.com

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