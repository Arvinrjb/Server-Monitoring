# Licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).
# See the LICENSE file in the project root for the full license text.
# Copyright (C) 2026 arvin, arvinrjb13@gmail.com

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