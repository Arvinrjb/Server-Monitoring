from django.contrib import admin
from logs.models import Logs

@admin.register(Logs)
class LogsListAdmin(admin.ModelAdmin):
    list_display = [
        "server",
        "level",
        "created_at",
    ]

    list_filter = [
        "server",
        "level",
        "created_at"
    ]