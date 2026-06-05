from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from rest_framework.authtoken.models import Token



@receiver(post_save, sender=User)
def create_group(sender, instance, created, **kwargs):
    if created :
        group = Group.objects.get(name='client')
        instance.groups.add(group)


@receiver(post_save, sender=User)
def create_user_token(sender, instance, created, **kwargs):
    if created:
        Token.objects.get_or_create(user=instance)