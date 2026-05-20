from django.urls import path
from . import views


urlpatterns = [
    path('cpu/', views.cpu_usage),
]
