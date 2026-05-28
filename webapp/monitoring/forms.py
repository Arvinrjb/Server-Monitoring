from django.forms import ModelForm
from .models import SystemStatus


class MonitoringForm(ModelForm):
    class Meta:
        print('check data')
        molde = SystemStatus
        fields = ["cpu_usage", "ram_usage", "disk_usage", "uptime"]
