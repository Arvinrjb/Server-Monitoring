from django.db import models
from system.models import Server


class SystemStatus(models.Model):
    server = models.ForeignKey(
        Server,
        on_delete=models.CASCADE,
        related_name="SystemStatus",
    )
    s = models.FloatField(verbose_name="Cpu Usage", blank=True, null=True)
    ram_usage =models.FloatField(verbose_name="Ram Usage", blank=True, null=True)
    disk_usage = models.FloatField(verbose_name="Disk Usage", blank=True, null=True)
    network_in = models.CharField(max_length=20, blank=True, null=True)
    network_out = models.CharField(max_length=20, blank=True, null=True)
    uptime = models.DateTimeField(blank=True, null=True)
    lastupdate = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.server.ipaddress + '\t' + self.server.hostname
    
