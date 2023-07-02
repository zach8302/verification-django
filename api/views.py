from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.utils.timezone import now
import datetime
from .models import AuthBlob, User
from .services import generate_code, hash_sha256
# Create your views here.


class VerifyView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request: Request) -> Response:
            request.user.verified = True
            request.user.save()
            return Response(status=status.HTTP_200_OK)

class AuthenticateView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request: Request) -> Response:
        if request.user.verified:
            code = generate_code(6)
            hashed = hash_sha256(code)
            blob = AuthBlob(value=hashed)
            blob.save()
            return Response(status=status.HTTP_200_OK, data = {"code" : code})
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
class IsAuthenticatedView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request: Request) -> Response:
        code = request.data.get('code')
        hashed = hash_sha256(code)

        queryset = AuthBlob.objects.filter(value = hashed)
        if queryset.exists() :
            blob = queryset[0]
            print(blob.value)
            td = now() - blob.created
            if td < datetime.timedelta(hours=1) :
                return Response(data={"verified": True}, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_401_UNAUTHORIZED)




