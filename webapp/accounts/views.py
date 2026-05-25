from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View



# loguot(request)   /logout



class login_user(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/admin/')
        return render(request, 'login.html')
    def post(self, request):
        username = request.POST.get('username','').strip()
        password = request.POST.get('password', '').strip()
        if not username or not password:
            messages.error(request, 'Please enter your username and password.')
            return render(request, 'login.html')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'login Success')
            return redirect('/admin/')
        else:
            messages.success(request, 'Error in login try again..')
            return render(request, 'login.html')
      

