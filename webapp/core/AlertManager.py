from alerts.models import Alert


def AlertsManager_CPU(server, status):
    if status.cpu_usage >= 90:
        existing  = Alert.objects.filter(
            server =server,
            title="High CPU Usage",
            is_active=True,
        ).first()

        if not existing:
            Alert.objects.create(
                server=server,
                title="High CPU Usage",
                message=f"CPU usage is {status.cpu_usage}%",
                level="WARNING"
            )
    else:
        alert = Alert.objects.filter(
            server=server,
            title="High CPU Usage",
            is_active=True,
        ).first()
        if alert:
            alert.is_active = False
            alert.save()
    
def AlertsManager_RAM(server, status):
    if status.ram_usage >= 90:
        existing  = Alert.objects.filter(
            server =server,
            title="High RAM Usage",
            is_active=True,
        ).first()

        if not existing:
            Alert.objects.create(
                server=server,
                title="High RAM Usage",
                message=f"RAM usage is {status.ram_usage}%",
                level="WARNING"
            )
    else:
        alert = Alert.objects.filter(
            server=server,
            title="High RAN Usage",
            is_active=True,
        ).first()
        if alert:
            alert.is_active = False
            alert.save()
    


def AlertsManager_DISK(server, status):
    if status.disk_usage >= 90:
        existing  = Alert.objects.filter(
            server =server,
            title="High DISK Usage",
            is_active=True,
        ).first()

        if not existing:
            Alert.objects.create(
                server=server,
                title="High DISK Usage",
                message=f"DISK usage is {status.disk_usage}%",
                level="WARNING"
            )
    else:
        alert = Alert.objects.filter(
            server=server,
            title="High DISK Usage",
            is_active=True,
        ).first()
        if alert:
            alert.is_active = False
            alert.save()
    