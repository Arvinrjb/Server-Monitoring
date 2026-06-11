from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework import status
from logs.serializers import LogSerializer
from system.models import Server


class AgentLog(APIView):
    permission_classes = []
    authentication_classes = []
    
    def post(self, request):
        try:
            token = request.headers.get(
                "X-Agent-Token"
            )
        except:
            return Response(
                {"error":"Token not send"},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            server = Server.objects.get(
                agent_token = token
            )
        except Server.DoesNotExist:
            return Response(
                {"error":"invalid token"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        serializer = LogSerializer(
            data = request.data
        )
        serializer.is_valid(
            raise_exception=True
        )
        serializer.save(
            server = server
        )
        return Response(
            {"status": "ok"},
            status=status.HTTP_201_CREATED
        )



class LogsViewSet(ReadOnlyModelViewSet):
    pass
