# Licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).
# See the LICENSE file in the project root for the full license text.
# Copyright (C) 2026 arvin, arvinrjb13@gmail.com

from django.views import View
from django.shortcuts import render
from django.http import HttpResponseForbidden


class AdminDashboardView(View):
    def get(self, request):
        if self.request.user.has_perms(
            [
                "system.view_all_servers",
                "system.manage_servers",
                "monitoring.view_all_statuses",
                "monitoring.manage_statuses",
                "logs.view_all_logs",
                "logs.manage_logs",
                "alerts.view_all_alerts",
                "alerts.manage_alerts",
                "accounts.view_all_users",
                "accounts.manage_users"
            ]
        ):
            return render(request, 'admin_dashboard.html')
        return HttpResponseForbidden('You do not have permission to perform this action.')
