# Licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).
# See the LICENSE file in the project root for the full license text.
# Copyright (C) 2026 arvin, arvinrjb13@gmail.com

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import Token
from accounts.models import User


@receiver(post_save, sender=User)
def create_group(sender, instance, created, **kwargs):
    if created :
        group = Group.objects.get(name='client')
        instance.groups.add(group)


@receiver(post_save, sender=User)
def create_user_token(sender, instance, created, **kwargs):
    if created:
        Token.objects.get_or_create(user=instance)