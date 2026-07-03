from django.db import models
from secrets import token_hex
from accounts.models import User

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
    hostname = models.CharField(
        max_length=100, 
        blank=False, 
        null=False
    )
    ipaddress = models.GenericIPAddressField(
        blank=False, 
        null=False
    )
    os = models.CharField(
        max_length=20,
        blank=False, 
        null=False
    )
    status = models.CharField(
        max_length=7, 
        choices=stat, 
        default='offline'
    )
    lastseen = models.DateTimeField(
        auto_now=True
    )
    agent_token = models.CharField(
        max_length=64, 
        unique=True, 
        default=generate_token
    )


    def __str__(self):
        return  self.hostname + self.ipaddress
    
    
    class Meta:
        permissions = [
            (
                "view_all_servers",
                "Can view all servers"
            ),
            (
                "manage_servers",
                "Can manage servers"
            )
        ]


