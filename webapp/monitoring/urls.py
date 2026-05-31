from django.urls import path
from monitoring.views import Monitoring

urlpatterns = [
    path('servers/', Monitoring.as_view()),
    # path('servers/<str:pk>/', get_server.as_view()),
]