# Licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).
# See the LICENSE file in the project root for the full license text.
# Copyright (C) 2026 arvin, arvinrjb13@gmail.com

from django.contrib import admin
from logs.models import Logs

@admin.register(Logs)
class LogsListAdmin(admin.ModelAdmin):
    list_display = [
        "server",
        "level",
        "created_at",
    ]

    list_filter = [
        "server",
        "level",
        "created_at"
    ]