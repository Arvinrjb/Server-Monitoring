# Licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).
# See the LICENSE file in the project root for the full license text.
# Copyright (C) 2026 arvin, arvinrjb13@gmail.com

import os
from celery import Celery
from celery.schedules import crontab
from django.utils import timezone


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webapp.settings")

app = Celery("webapp")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.timezone = timezone.get_current_timezone_name()

app.conf.beat_schedule = {
    "check-servers-every-night": {
        "task": "system.tasks.check_offline_servers",
        "schedule": 1800,
    },
    "cleanup-statuses-every-night": {
        "task": "monitoring.tasks.delete_old_statuses",
        "schedule": crontab(hour=1, minute=0),
    },
    "cleanup-logs-every-night": {
        "task": "logs.tasks.delete_old_logs",
        "schedule": crontab(hour=1, minute=10),
    },
    "cleanup-alerts-every-night": {
        "task": "alerts.tasks.delete_old_alerts",
        "schedule": crontab(hour=1, minute=20),
    }
}
