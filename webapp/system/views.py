from django.shortcuts import render
from django.views import View
from django.core.cache import cache
from django.http import HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import authentication
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from system.serializers import ServerSerializer
from system.models import Server
from core.pagination import PagePagination
from core.Permissions import IsOwnerOrAdmin


class Home(View):
    def get(self, request):
        return render(request, 'home.html')


class dashboard(
    LoginRequiredMixin,
    View
):  
    def get(self, request):
        if self.request.user.has_perms(
            [
                "system.view_server"
            ]
        ):
            return render(request, 'dashboard.html', )
        return HttpResponseForbidden('You do not have permission to perform this action.')


class Servers(
    LoginRequiredMixin, 
    View
):
    def get(self, request):
        if self.request.user.has_perms(
            [
                "system.view_server"
            ]
        ):
            return render(request, 'servers.html')
        return HttpResponseForbidden('You do not have permission to perform this action.')


class AddServerViewSet(ModelViewSet):
    serializer_class = ServerSerializer
    pagination_class = PagePagination
    authentication_classes = [
        authentication.SessionAuthentication
    ]
    permission_classes = [
        IsOwnerOrAdmin
    ]
    
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
    ]

    filterset_fields = [
        "user",
        "os",
        "status",
    ]

    search_fields = [
        "user",
        "hostname",
        "ipaddress",
        "os",
    ]

    def list(self, request, *args, **kwargs):
        cache_key = (
            f"servers_{self.request.user.id}"
        )

        cache_data = cache.get(
            cache_key
        )

        if cache_data:
            return Response(
                cache_data
            )

        queryset = self.filter_queryset(
            self.get_queryset()
        )

        page = self.paginate_queryset(
            queryset
        )

        serializer = self.get_serializer(
            page,
            many=True
        )

        data = self.get_paginated_response(
            serializer.data
        ).data

        cache.set(
            cache_key,
            data,
            timeout=6000
        )

        return Response(
            data
        )
        
    def invalidate_cache(self):
        cache.delete(
            f"servers_{self.request.user.id}"
        )

    def get_queryset(self): 
        if self.request.user.has_perms(
            [
                "system.view_all_servers"
            ]
        ):
            servers = Server.objects.all()
        else:
            servers = Server.objects.filter(
                user=self.request.user
            )
        return servers.select_related(
            "user"
        )

    def perform_create(self, serializer):
        self.invalidate_cache()
        return serializer.save(
            user=self.request.user
            )
    
    def perform_update(self, serializer):
        serializer.save()
        self.invalidate_cache()

    def perform_destroy(self, instance):
        instance.delete()
        self.invalidate_cache()
    
