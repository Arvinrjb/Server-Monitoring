from django.contrib import admin
from accounts.models import User

@admin.register(User)
class UserListAdmin(admin.ModelAdmin):
    list_display = [
        "email",
        "first_name",
        "last_name",
        "phone_number"
    ]

    list_filter = [
        "email"
    ]
