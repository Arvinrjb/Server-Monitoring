from django.urls import path
from accounts import views


urlpatterns = [
    path('', views.dashboard.as_view()),
    path('servers/', views.Servers.as_view())
]
