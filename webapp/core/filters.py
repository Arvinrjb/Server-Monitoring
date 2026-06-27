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