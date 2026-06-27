from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import View
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from accounts.forms import RegisterForm
from accounts.serializers import RegisterSerializer




class RegisterApiView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [
        AllowAny
    ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data
        )
        result = serializer.is_valid(
            raise_exception=True
        )
        result = serializer.save()

        return Response(
            {
            "refresh": result["refresh"],
            "access": result["access"],
            "username": result["user"].username,
            },
            status=status.HTTP_201_CREATED
        )


class login_user(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'registration/login.html')
    def post(self, request):
        username = request.POST.get('username','').strip()
        password = request.POST.get('password', '').strip()
        if not username or not password:
            messages.error(request, 'Please enter your username and password.')
            return render(request, 'registration/login.html')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'login Success')
            return redirect('/')
        else:
            messages.error(request, 'Error in login try again..')
            return render(request, 'registration/login.html')
      

class sign_up(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        form = RegisterForm()
        return render(request, 'registration/sign_up.html', {'form':form})
    def post(self, request):
        form = RegisterForm(request.POST)
        # group = Group.objects.get(name='client')
        if form.is_valid():
            user = form.save()
            # user.groups.add(group)
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'registration/sign_up.html', {'form':form})

