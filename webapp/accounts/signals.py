from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_group(sender, instance, created, **kwargs):
    if created :
        group = Group.objects.get(name='client')
        instance.groups.add(group)
