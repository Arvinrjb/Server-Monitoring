from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, Http404
from django.views import View
from system.models import Server
from system.forms import InfServer





class home(View):
    def get(self, request):
        return render(request, 'home.html')

class ShowServer(LoginRequiredMixin, View):
    def get(self, request):
        form = InfServer()
        return render (request, 'systems.html', {'form':form})
    def post(self, request):
        form = InfServer(request.POST)
        if form.is_valid:
            server = form.save(commit=False)
            server.author = request.user
            server.save()
            return redirect('/')
        else:
            return HttpResponse('Try again')
