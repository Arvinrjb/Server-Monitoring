from django.dispatch import receiver
from django.db.models.signals import post_save
from system.models import Server
from monitoring.models import ServerStatus


@receiver(post_save, sender=Server)
def create_status(sender, instance, created, **kwargs):
    if created:
        ServerStatus.objects.create(
            server = instance
        )