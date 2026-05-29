from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import MonitoringForm



class ReceiveData(LoginRequiredMixin, View):
    def post(self, request):
        form = MonitoringForm(request.POST)
        print(form.is_valid)
        if form.is_valid:
            form.save()
