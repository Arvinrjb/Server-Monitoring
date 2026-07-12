# Licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).
# See the LICENSE file in the project root for the full license text.
# Copyright (C) 2026 arvin, arvinrjb13@gmail.com

from rest_framework.permissions import BasePermission


class IsOwnerOrAdmin(BasePermission):
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
        return obj.user.email == request.user.email
    
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