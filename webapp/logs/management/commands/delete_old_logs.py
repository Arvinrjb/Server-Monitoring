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