# Licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).
# See the LICENSE file in the project root for the full license text.
# Copyright (C) 2026 arvin, arvinrjb13@gmail.com

from django.db import models
from system.models import Server



class Alert(models.Model):
    server = models.ForeignKey(
        Server,
        on_delete=models.CASCADE,
        related_name="alerts",
    )

    title = models.CharField(
        max_length=200
    )

    message = models.TextField()

    level = models.CharField(
        max_length=10
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )
    
    class Meta:
        permissions = [
            (
                "view_all_alerts",
                "Can view all alerts"
            ),
            (
                "manage_alerts",
                "Can manage alerts"
            )
        ]