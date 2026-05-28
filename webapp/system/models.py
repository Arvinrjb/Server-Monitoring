from django.db import models
from django.contrib.auth.models import User
# from django.conf import settings
# Create your models here.

class Server(models.Model):
    stat =[
        ("online", "system online"),
        ("offline", "system offline")
    ]
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user',
        null=True,
        blank=True
    )
    # id = models.IntegerField(primary_key=True)
    hostname = models.CharField(max_length=100, blank=False, null=False)
    ipaddress = models.GenericIPAddressField(blank=False, null=False)
    os = models.CharField(max_length=20, blank=False, null=False)
    status = models.CharField(max_length=7, choices=stat)
    lastseen = models.DateTimeField(auto_now=True)
    # token
    def __str__(self):
        return self.ipaddress
    



