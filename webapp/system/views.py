from rest_framework.viewsets import ModelViewSet
from rest_framework import authentication, permissions
from django.shortcuts import render
from django.views import View
from system.serializers import ServerSerializer
from system.models import Server
from core.pagination import PagePagination



class Home(View):
    def get(self, request):
        return render(request, 'home.html')


class AddServerViewSet(ModelViewSet):
    pagination_class = PagePagination
    authentication_classes = [
        authentication.SessionAuthentication
    ]
    permission_classes = [
        permissions.IsAuthenticated
    ]
    
    serializer_class = ServerSerializer

    def get_queryset(self): 
        if self.request.user.is_staff:
            return Server.objects.all()
        
        return Server.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):
        return serializer.save(
            user=self.request.user
            )
    

