from django.shortcuts import render, redirect
from .models import Server
from django.http import HttpResponse, Http404
import datetime
from .forms import CreateServer, GetServer
from django.views import View


class ShowServer(View):
    def get(self, request):
        form = GetServer()
        return render (request, 'systems.html', {'form':form})
    def post(self, request):
        form = CreateServer(request.POST)
        if form.is_valid:
            form.save()
            return redirect('/admin/system/server/')
        else:
            return HttpResponse('Try again')