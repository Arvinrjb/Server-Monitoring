from datetime import timedelta
from django.core.management import BaseCommand
from django.utils import timezone
from alerts.models import Alert



class Command(BaseCommand):
    def handle(self, *args, **options):
        cutoff = timezone.now() - timedelta(
            weeks=2
        )

    def delete_alerts(self, cutoff):
        delete_count = (
            Alert.objects.filter(
                created_at__lte=cutoff
            )
        ).delete()
        self.stdout.write(
            self.style.SUCCESS(
                f"Deleted {delete_count} Alerts"
            )
        )