# Licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).
# See the LICENSE file in the project root for the full license text.
# Copyright (C) 2026 arvin, arvinrjb13@gmail.com

from celery import shared_task
from django.core.management import call_command


@shared_task
def delete_old_statuses():
    call_command("delete_old_statuses")
