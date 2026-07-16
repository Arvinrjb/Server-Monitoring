# Licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).
# See the LICENSE file in the project root for the full license text.
# Copyright (C) 2026 arvin, arvinrjb13@gmail.com

from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from monitoring.models import ServerStatus


class Command(BaseCommand):
    help = "Delete old ServerStatuses"

    def handle(self, *args, **options):
        cutoff = timezone.now() - timedelta(
            weeks=1
        )
        self.delete_statuses(
            cutoff
        )

    def delete_statuses(self, cutoff):
        deleted_count = (
            ServerStatus.objects.filter(
                lastupdate__lte=cutoff
            )
        ).delete()
        self.stdout.write(
            self.style.SUCCESS(
                f"Deleted {deleted_count} statuses"
            )
        )
