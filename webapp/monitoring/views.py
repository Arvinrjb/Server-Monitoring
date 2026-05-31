from rest_framework import views, status
from rest_framework.response import Response
from rest_framework import authentication, permissions
from monitoring.models import SystemStatus
from monitoring.serializers import MonitoringSerializer, ServerSerializer



class Monitoring(views.APIView):
    authentication_classes = [
        authentication.SessionAuthentication,
    ]
    permission_classes = [
        permissions.IsAuthenticated,    
    ]

    def get(self, request, format=None):
        status = SystemStatus.objects.filter(server__user = self.request.user)
        serializer = MonitoringSerializer(status, many=True)
        return Response(serializer.data)

