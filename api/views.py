from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.utils.timezone import now
import datetime
# Create your views here.


class AuthenticateView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request: Request) -> Response:

        if request.user.verified:
            request.user.date_verified = now
            request.user.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
class IsAuthenticatedView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request: Request) -> Response:

        if request.user.verified:
            td = now - request.user.date_verified
            if td < datetime.timedelta(hours=1) :
                return Response(data={"verified": True}, status=status.HTTP_200_OK)
            return Response(data={"verified": False}, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_401_UNAUTHORIZED)


