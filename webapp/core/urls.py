from django.urls import path
from core.views import AdminDashboardView



urlpatterns = [
    path(
        '',
        AdminDashboardView.as_view(),
        name="Admin panel"
    )
]
