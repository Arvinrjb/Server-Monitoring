from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

GROUPS = {
    "Admin": "all",  
    "Support": [    
        ("accounts", "view_all_users"),
        ("accounts", "manage_users"),
        ("alerts", "view_all_alerts"),
        ("alerts", "manage_alerts"),
        ("logs", "view_all_logs"),
        ("logs", "manage_logs"),
        ("monitoring", "view_all_statuses"),
        ("monitoring", "manage_statuses"),
        ("system", "view_all_servers"),
        ("system", "manage_servers"),
    ],
    "Client": [    
        ("accounts", "view_user"),
        ("alerts", "view_alert"),
        ("logs", "view_logs"),
        ("monitoring", "view_serverstatus"),
        ("system", "view_server"),
    ],
}


class Command(BaseCommand):
    help = "Create default groups and assign permissions"

    def handle(self, *args, **options):

        admin_group, _ = Group.objects.get_or_create(name="Admin")
        admin_perms = Permission.objects.all()
        admin_group.permissions.set(admin_perms)
        self.stdout.write(self.style.SUCCESS("Admin group synced with ALL permissions."))

        for group_name in ["Support", "Client"]:
            group, _ = Group.objects.get_or_create(name=group_name)
            perm_defs = GROUPS[group_name]

            perms = []
            for app_label, codename in perm_defs:
                try:
                    perm = Permission.objects.get(
                        content_type__app_label=app_label,
                        codename=codename,
                    )
                    perms.append(perm)
                except Permission.DoesNotExist:
                    self.stdout.write(
                        self.style.ERROR(f"Missing permission: {app_label}.{codename}")
                    )

            group.permissions.set(perms)
            self.stdout.write(self.style.SUCCESS(f"{group_name} group synced."))
