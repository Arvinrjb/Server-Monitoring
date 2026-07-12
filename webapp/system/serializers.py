# Licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).
# See the LICENSE file in the project root for the full license text.
# Copyright (C) 2026 arvin, arvinrjb13@gmail.com

from rest_framework import serializers
from system.models import Server


class ServerSerializer(serializers.ModelSerializer):
    user = serializers.CharField(
        source="user.first_name",
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
            'id'
        ]