from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from system.views import ShowServer
from accounts.views import  login_user, sign_up


router = routers.DefaultRouter()


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('system.urls')),
    path('', include('django.contrib.auth.urls')),
    path('dashboard/', include('accounts.urls')),
    path('login/', login_user.as_view()),
    path('signup/', sign_up.as_view()),
    path('api/', include('monitoring.urls'))
]
