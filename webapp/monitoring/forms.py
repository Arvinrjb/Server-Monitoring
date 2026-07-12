# Licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).
# See the LICENSE file in the project root for the full license text.
# Copyright (C) 2026 arvin, arvinrjb13@gmail.com

from django.forms import ModelForm
from .models import SystemStatus


class MonitoringForm(ModelForm):
    class Meta:
        print('check data')
        molde = SystemStatus
        fields = ["cpu_usage", "ram_usage", "disk_usage", "uptime"]
