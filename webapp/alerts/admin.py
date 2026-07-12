# Licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).
# See the LICENSE file in the project root for the full license text.
# Copyright (C) 2026 arvin, arvinrjb13@gmail.com

from django.contrib import admin
from alerts.models import Alert


@admin.register(Alert)
class AletListAdmin(admin.ModelAdmin):
    list_display = [
        "server",
        "title",
        "level",
        "is_active",
        "created_at",
    ]
    
    list_filter = [
        "server",
        "level",
        "is_active",
        "created_at",
        "title",
    ]