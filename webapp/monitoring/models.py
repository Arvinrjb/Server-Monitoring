# Licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).
# See the LICENSE file in the project root for the full license text.
# Copyright (C) 2026 arvin, arvinrjb13@gmail.com

from django.db import models
from system.models import Server


class ServerStatus(models.Model):
    server = models.ForeignKey(
        Server,
        on_delete=models.CASCADE,
        related_name="statuses",
    )
    cpu_usage = models.FloatField(
        verbose_name="Cpu Usage",
        default=0, 
        blank=True, 
        null=True,
    )
    ram_usage =models.FloatField(
        verbose_name="Ram Usage", 
        default=0, 
        blank=True, 
        null=True,
    )
    disk_usage = models.FloatField(
        verbose_name="Disk Usage", 
        default=0, 
        blank=True, 
        null=True
    )
    network_in = models.FloatField(
        verbose_name="network_in",
        default=0,
        blank=True, 
        null=True
    )
    network_out = models.FloatField(
        verbose_name="network_out",
        default=0,
        blank=True, 
        null=True
    )
    process_count = models.IntegerField(
        verbose_name="process_count",
        default=0,
        blank=True,
        null=True
    )
    uptime_seconds = models.BigIntegerField(
        default=0,
        blank=True,
        null=True
    )
    lastupdate = models.DateTimeField(
        auto_now=True,
        blank=True, 
        null=True
    )

    class Meta:
        permissions = [
            (
                "view_all_statuses",
                "Can view all statuses"
            ),
            (
                "manage_statuses",
                "Can manage statuses"
            )
        ] 
        ordering = [
            "lastupdate",
            "id"
        ]