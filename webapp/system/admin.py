# Licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).
# See the LICENSE file in the project root for the full license text.
# Copyright (C) 2026 arvin, arvinrjb13@gmail.com

from django.contrib import admin
from .models import Server


@admin.register(Server)
class ServerListAdmin(admin.ModelAdmin):
    list_display = [
        "hostname", 
        "user", 
        "ipaddress", 
        "status"
    ]

    list_filter = [
        "user",
        "ipaddress",
        "status"
    ]
