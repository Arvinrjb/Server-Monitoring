from django.urls import path
from system import views


urlpatterns = [
    path('', views.Home.as_view(), name='HomePage'),
    # path('system/<int:pk>', views.get_system),
]
