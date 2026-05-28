from django.db import models
from system.models import Server



class Alerts(models.Model):
    resolved_choice = [
        ("Yes", "Yes"),
        ("No", "No")
    ]
    security_choice = [
        ('None', "None"),
        ('warning', 'warning'),
        ('critical', 'critical')
    ]

    server = models.ForeignKey(
        Server,
        related_name='alerts',
        on_delete=models.CASCADE
    )
    type = models.CharField(verbose_name="Error type", max_length=20, blank=True, null=True)
    admin_message = models.TextField(verbose_name="admin message for the problem", blank=True, null=True)
    security = models.CharField(max_length=8, choices=security_choice, verbose_name='Security status')
    resolved = models.CharField(max_length=3, choices=resolved_choice)
    # created_at = models.DateTimeField(auto_now_add=True)



class Logs(models.Model):
    server = models.ForeignKey(
        Server,
        on_delete=models.CASCADE,
        related_name='ServerLog'
    )
    log = models.TextField()