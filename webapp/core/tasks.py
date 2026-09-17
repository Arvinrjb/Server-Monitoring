from datetime import timedelta
from django.utils import timezone
from monitoring.models import ServerStatus
from logs.models import Logs
from alerts.models import Alert
from orbittask.decorators import task_thread


@task_thread
def delete_statuses():
    cutoff = timezone.now() - timedelta(
        weeks=1
    )
    deleted_count, _ = ServerStatus.objects.filter(
        lastupdate__lte = cutoff
    ).delete()
    return f"{deleted_count} statuses deleted"


@task_thread
def delete_logs():
    cutoff = timezone.now() - timedelta(
        weeks=1
    )
    deleted_count, _ = Logs.objects.filter(
        created_at__lte=cutoff
    ).delete()
    return f"{deleted_count} logs deleted"


@task_thread
def delete_alerts():
    cutoff = timezone.now() - timedelta(
        weeks=1
    )
    deleted_count, _ = Alert.objects.filter(
        created_at__lte=cutoff
    ).delete()
    return f"{deleted_count} alerts deleted"
