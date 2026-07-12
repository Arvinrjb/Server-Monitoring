# Licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).
# See the LICENSE file in the project root for the full license text.
# Copyright (C) 2026 arvin, arvinrjb13@gmail.com

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from accounts.views import  login_user, sign_up
from system.views import Home



urlpatterns = [
    path('admin/', admin.site.urls, name="Admin"),
    path('login/', login_user.as_view(), name="Login"),
    path('', include('django.contrib.auth.urls')),
    path('', Home.as_view(), name="Home"),
    path('dashboard/', include('system.urls'), name="Dashboard"),
    path('admin-dashboard', include('core.urls')),
    path('signup/', sign_up.as_view(), name="SignUp"),
    path('api/', include('core.api_urls'), name="MainAPI"),
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh', TokenRefreshView.as_view()),
]
