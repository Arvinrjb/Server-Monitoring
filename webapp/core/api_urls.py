# Licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).
# See the LICENSE file in the project root for the full license text.
# Copyright (C) 2026 arvin, arvinrjb13@gmail.com

from django.urls import path, include

urlpatterns = [
    path('', include('system.api_urls')),
    path('', include('monitoring.api_urls')),
    path('', include('accounts.api_urls')),
    path('', include('alerts.api_urls')),
    path('', include('logs.api_urls')),

]