# Licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).
# See the LICENSE file in the project root for the full license text.
# Copyright (C) 2026 arvin, arvinrjb13@gmail.com

from datetime import timedelta
from django.core.management import BaseCommand
from django.utils import timezone
from logs.models import Logs

class Command(BaseCommand):
    def handle(self, *args, **options):
        cutoff = timezone.now() - timedelta(
            weeks=1
        )
        self.delete_logs(
            cutoff
        )


    def delete_logs(self, cutoff):
        delete_count = (
            Logs.objects.filter(
            created_at__lte=cutoff
            )
        ).delete()
        self.stdout.write(
            self.style.SUCCESS(
                f"Deleted {delete_count} Logs"
            )
        )