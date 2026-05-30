from django.contrib import admin
from django.urls import path, include
from system.views import ShowServer
from accounts.views import  login_user, sign_up
from monitoring.views import ReceiveData
from rest_framework import routers
# from monitoring.views import ReceiveData

router = routers.DefaultRouter()
# router.register(r'systems', ReceiveData)
urlpatterns = router.urls

urlpatterns += [
    path('admin/', admin.site.urls),
    # path('', include('router.urls')),
    path('', include('system.urls')),
    path('', include('django.contrib.auth.urls')),
    path('dashboard/', include('accounts.urls')),
    path('login/', login_user.as_view()),
    path('signup/', sign_up.as_view()),
    path('monitoringdata/', ReceiveData.as_view()),
    # path("api-auth/", include("rest_framework.urls", namespace="rest_framework"))
    
]
