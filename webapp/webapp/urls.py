from django.contrib import admin
from django.urls import path, include
from accounts.views import  login_user, sign_up



urlpatterns = [
    path('admin/', admin.site.urls, name="Admin"),
    path('', include('system.urls'), name="Systems"),
    path('', include('django.contrib.auth.urls')),
    path('dashboard/', include('accounts.urls'), name="Dashboard"),
    path('login/', login_user.as_view(), name="Login"),
    path('signup/', sign_up.as_view(), name="SignUp"),
    path('api/', include('monitoring.urls'), name="API"),
]
