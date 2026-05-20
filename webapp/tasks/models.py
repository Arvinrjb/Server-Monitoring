from django.db import models

# Create your models here.

class ServerTables(models.Model):
    stat =[
        ("online", "system online"),
        ("offline", "system offline")
    ]
    id = models.IntegerField(primary_key=True, blank=False, null=False)
    hostname = models.CharField(max_length=100, blank=False, null=False)
    ipaddress = models.GenericIPAddressField(blank=False, null=False)
    os = models.CharField(max_length=20, blank=False, null=False)
    status = models.CharField(max_length=7, choices=stat)
    lastseen = models.DateTimeField(auto_now=True)
    # token
    def __str__(self):
        return self.ipaddress


