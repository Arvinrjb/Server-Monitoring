from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseForbidden
from rest_framework.viewsets import ModelViewSet
from system.models import Server
from monitoring.models import ServerStatus
from alerts.models import Alert
from logs.models import Logs


class AdminDashboardView(
    View,
):    
    def get(self, request):
        if self.request.user.has_perms(
            [
                "system.view_all_servers",
                "monitoring.view_all_statuses",
                "logs.view_all_logs",
                "alerts.view_all_alerts",
            ]
        ):
            return render(request, 'admin_dashboard.html')
        return HttpResponseForbidden('You do not have permission to perform this action.')
    
