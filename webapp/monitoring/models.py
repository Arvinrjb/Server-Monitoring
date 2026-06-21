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
    uptime = models.DateTimeField(
        blank=True, 
        null=True
    )
    lastupdate = models.DateTimeField(
        blank=True, 
        null=True
    )

    def __str__(self):
        return self.server.ipaddress + '\t' + self.server.hostname

    
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