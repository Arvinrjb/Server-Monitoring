from django.contrib import admin
from .models import Server


@admin.register(Server)
class ServerListAdmin(admin.ModelAdmin):
    list_display = [
        "hostname", 
        "user", 
        "ipaddress", 
        "status"
    ]

    list_filter = [
        "user",
        "ipaddress",
        "status"
    ]
