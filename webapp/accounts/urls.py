from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.dashboard.as_view()),
    path('servers/', views.Servers.as_view())
    # path('', include('django.contrib.auth.urls')),
    # path('', views.login_user.as_view()),
]
