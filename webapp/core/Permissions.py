from rest_framework.permissions import BasePermission


class IsServerOwnerOrAdmin(BasePermission):
    message = "You do not have permission to perform this action."

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_staff or request.user.is_superuser:
            return True
        return True
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or request.user.is_superuser:
            return True
        return obj.user == request.user
    
class IsSupport(BasePermission):
    message = "You do not have permission to perform this action."

    def has_permission(self, request, view):
        return request.user.has_perms(
            [
                "system.view_all_servers",
                "monitoring.view_all_statuses",
                "logs.view_all_logs",
                "alerts.view_all_alerts",
            ]
        )

class IsAdmin:
    message = "You do not have permission to perform this action."

    def has_permission(self, request, view):
        return request.user.has_perms(
            [
                "system.manage_servers",
                "monitoring.manage_statuses",
                "logs.manage_logs",
                "alerts.manage_alerts",
            ]
        )