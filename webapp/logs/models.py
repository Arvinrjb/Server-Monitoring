# Licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).
# See the LICENSE file in the project root for the full license text.
# Copyright (C) 2026 arvin, arvinrjb13@gmail.com

from django.db import models
from system.models import Server


class Logs(models.Model):
    LEVELS = [
        ("INFO", "INFO"),
        ("WARNING", "WARNING"),
        ("ERROR", "ERROR"),
    ]

    server = models.ForeignKey(
        Server,
        on_delete=models.CASCADE,
        related_name='logs',
    )

    level = models.CharField(
        max_length=10,
        choices=LEVELS,
        blank=True,
        null=True,
        default="INFO"
    )
    message = models.TextField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=True
    )

    
    class Meta:
        permissions = [
            (
                "view_all_logs",
                "Can view all logs"
            ),
            (
                "manage_logs",
                "Can manage logs"
            )
        ]