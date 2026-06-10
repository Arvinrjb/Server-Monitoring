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
        related_name='Logs',
    )

    level = models.CharField(
        max_length=10,
        choices=LEVELS,
        blank=True,
        null=True,
    )
    message = models.TextField(
        null=True,
        blank=True,
        name="ServerLogs",
    )

    created_at = models.DateField(
        auto_now=True,
    )