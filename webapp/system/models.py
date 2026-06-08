from django.db import models
from django.contrib.auth.models import User
from secrets import token_hex


def generate_token():
    return token_hex(32)

class Server(models.Model):
    stat =[
        ("online", "system online"),
        ("offline", "system offline")
    ]
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='servers',
        null=False,
        blank=False
    )
    hostname = models.CharField(max_length=100, blank=False, null=False)
    ipaddress = models.GenericIPAddressField(blank=False, null=False)
    os = models.CharField(max_length=20, blank=False, null=False)
    status = models.CharField(max_length=7, choices=stat, default='offline')
    lastseen = models.DateTimeField(auto_now=True)
    agent_token = models.CharField(max_length=64, unique=True, default=generate_token)

    # def save(self, *args, **kwargs):
    #     if not self.agent_token:
    #         self.agent_token = token_hex(32)
    #     return super().save(*args, **kwargs)
    

    def __str__(self):
        return self.ipaddress
    



