"""
URL configuration for webapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from system.views import ShowServer
from accounts.views import  login_user, sign_up
from monitoring.views import ReceiveData

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('system.urls')),
    path('', include('django.contrib.auth.urls')),
    path('dashboard/', include('accounts.urls')),
    path('login/', login_user.as_view()),
    path('signup/', sign_up.as_view()),
    path('monitoringdata/', ReceiveData.as_view())
    
]
