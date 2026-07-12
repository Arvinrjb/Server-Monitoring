# Licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).
# See the LICENSE file in the project root for the full license text.
# Copyright (C) 2026 arvin, arvinrjb13@gmail.com

import django_filters
from monitoring.models import ServerStatus


class MonitoringFilter(django_filters.FilterSet):
    min_cpu = django_filters.NumberFilter(
        field_name='cpu_usage',
        lookup_expr='gte'
    )
    max_cpu = django_filters.NumberFilter(
        field_name='cpu_usage',
        lookup_expr='lte'
    )
    min_ram = django_filters.NumberFilter(
        field_name='ram_usage',
        lookup_expr='gte'
    )
    max_ram = django_filters.NumberFilter(
        field_name='ram_usage',
        lookup_expr='lte'
    )
    class Meta:
        model = ServerStatus
        fields = [
            'server',
        ]