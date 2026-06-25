from django.contrib import admin
from alerts.models import Alert


@admin.register(Alert)
class AletListAdmin(admin.ModelAdmin):
    list_display = [
        "server",
        "title",
        "level",
        "is_active",
        "created_at",
    ]
    
    list_filter = [
        "server",
        "level",
        "is_active",
        "created_at",
        "title",
    ]