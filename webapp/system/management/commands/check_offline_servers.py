from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from system.models import Server
from alerts.models import Alert



class Command(BaseCommand):
    help = "Check offline servers and create alerts"

    def handle(self, *args, **kwargs):
        offline_limit = timezone.now() - timedelta(
            minutes=5
        )
        self.check_offline_servers(
            offline_limit
        )
        self.resolve_online_servers(
            offline_limit
        )
    def check_offline_servers(self, offline_limit):
        servers = Server.objects.filter(
            lastseen__lt=offline_limit
        )
        for server in servers:
            if server.status != "offline":
                server.status = "offline"
                server.save(
                    update_fields=["status"]
                )
            existing = Alert.objects.filter(
                server=server,
                title="Server Offline",
                is_active=True,
            ).exists()
            if not existing:
                Alert.objects.create(
                    server=server,
                    title="Server Offline",
                    message=(
                        f"{server.hostname} "
                        "is not responding"
                    ),
                    level="ERROR",
                )
                self.stdout.write(
                    self.style.ERROR(
                        f"{server.hostname} offline"
                    )
                )
    def resolve_online_servers(self, offline_limit):
        servers = Server.objects.filter(
            lastseen__gte=offline_limit
        )
        for server in servers:
            if server.status != "online":
                server.status = "online"
                server.save(
                    update_fields=["status"]
                )
            alert = Alert.objects.filter(
                server=server,
                title="Server Offline",
                is_active=True,
            ).first()
            if alert:
                alert.is_active = False
                alert.save(
                    update_fields=["is_active"]
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f"{server.hostname} online"
                    )
                )