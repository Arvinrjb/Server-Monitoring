from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import UserPassesTestMixin
from system.models import Server
from monitoring.models import ServerStatus
from alerts.models import Alert
from logs.models import Logs


class AdminDashboardView(
    UserPassesTestMixin,
    TemplateView,
    ):
    template_name = 'admin_dashboard.html'

    def test_func(self):
        return self.request.user.is_staff



