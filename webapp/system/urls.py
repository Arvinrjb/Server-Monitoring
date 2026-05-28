from django.urls import path
from . import views


urlpatterns = [
    path('systems/', views.ShowServer.as_view()),
    # path('system/<int:pk>', views.get_system),
]
