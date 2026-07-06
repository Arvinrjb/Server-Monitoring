from time import sleep
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views import View
from django.core.cache import cache
from rest_framework import status, viewsets, mixins
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework import status, permissions, authentication
from rest_framework.permissions import AllowAny
from core.Permissions import IsOwnerOrAdmin
from accounts.forms import RegisterForm
from accounts.serializers import RegisterSerializer, ProfileSerializer
from accounts.models import User


class ProfileViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    authentication_classes = [
        authentication.SessionAuthentication,
    ]
    permission_classes = [
        IsOwnerOrAdmin,
        permissions.IsAuthenticated
    ]
    serializer_class = ProfileSerializer

    def list(self, request, *args, **kwargs):
        cache_key = (
            f"profile_{self.request.user.id}_"
            f"{self.request.GET.urlencode()}"
            )
        cache_data = cache.get(
            cache_key
        )
        if cache_data:
            return Response(
                cache_data
            )
        queryset = self.get_queryset()
        serializer = self.get_serializer(
            queryset,
            many=True
        )
        cache.set(
            cache_key,
            serializer.data,
            timeout=6000
        )
        return Response(
            serializer.data
        )
    
    def invalidate_cache(self):
        cache.delete(
            f"profile_{self.request.user.id}"
        )
        
    def get_queryset(self):
        if self.request.user.has_perms(
            [
                "accounts.view_all_users",
                "accounts.manage_users"
            ]
        ):
            return User.objects.all()
        else:
            return User.objects.filter(
                id = self.request.user.id
            )

    def perform_update(self, serializer):
        serializer.save()
        self.invalidate_cache()



class RegisterApiView(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = RegisterSerializer
    permission_classes = [
        AllowAny
    ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data
        )
        serializer.is_valid(
            raise_exception=True
        )
        result = serializer.save()

        return Response(
            {
            "refresh": result["refresh"],
            "access": result["access"],
            "user_id": result["user"].id,
            },
            status=status.HTTP_201_CREATED
        )


class login_user(View):
    def get(self, request):
        print("Test")
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'registration/login.html')
    def post(self, request):
        email = request.POST.get('email','').strip()
        password = request.POST.get('password', '').strip()
        if not email or not password:
            messages.error(request, 'Please enter your email and password.')
            return render(request, 'registration/login.html')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'login Success')
            return redirect('/')
        else:
            messages.error(request, 'Error in login try again..')
            return render(request, 'registration/login.html')
      


class sign_up(View):
    def get(self, request):
        if self.request.user.is_authenticated:
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

