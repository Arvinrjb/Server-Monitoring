from django.urls import path, include

urlpatterns = [
    path('', include('system.api_urls')),
    path('', include('monitoring.api_urls')),
    path('', include('accounts.api_urls')),
    path('', include('alerts.api_urls')),
    path('', include('logs.api_urls')),

]