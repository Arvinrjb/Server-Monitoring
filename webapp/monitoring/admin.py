from django.contrib import admin
from .models import ServerStatus

@admin.register(ServerStatus)
class ServerStatusAdmin(admin.ModelAdmin):
    list_display = [
        "server",
        "cpu_usage",
        "ram_usage",
        "disk_usage"
    ]

    list_filter = [
        "server",
        "lastupdate"
    ]
    search_fields = [
        "lastupdate"
    ]