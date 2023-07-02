from django.contrib.auth import authenticate, login, logout
from .models import User
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework import status
from .serializers import UserSerializer

class SignUpView(APIView):

    def post(self, request, format=None):
        username = request.data['username']
        password = request.data['password']
        user = User.objects.create_user(username=username, password=password)
        user.first_name = request.data['first_name']
        if 'email' in request.data:
            user.email = request.data['email']
        user.save()
        print(user.email)
        login(request, user)
        return Response({'Success' : "Logged in successfully"}, status=status.HTTP_200_OK)
    
class MeView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        user = request.user
        return Response(data=UserSerializer(instance=user).data, status=status.HTTP_200_OK)