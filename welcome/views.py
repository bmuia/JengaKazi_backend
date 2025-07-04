from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView


class WelcomeView(APIView):
    def get(self, request):
        try:
            return Response({
                'message': 'Hello from backend'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': 'API communication between frontend and backend has failed'
            }, status=status.HTTP_400_BAD_REQUEST)
