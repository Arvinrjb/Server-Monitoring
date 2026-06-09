from django.urls import path
from rest_framework.routers import DefaultRouter
from system.views import AddServerViewSet


router = DefaultRouter()

router.register(
    'addserver',
    AddServerViewSet,
    basename='Servers'
)


urlpatterns = router.urls