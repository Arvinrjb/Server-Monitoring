from django.urls import path
from system import views


urlpatterns = [
    path('', views.home.as_view()),
    # path('system/<int:pk>', views.get_system),
]
