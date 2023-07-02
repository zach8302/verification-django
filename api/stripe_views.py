
from .models import User
import stripe
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework import status
from .serializers import UserSerializer

class VerificationSessionView(APIView):

    def post(self, request, format=None):
        # Set your secret key. Remember to switch to your live secret key in production.
        # See your keys here: https://dashboard.stripe.com/apikeys
        stripe.api_key = 'sk_test_51NOtuQENXUDWXy01vZ0UjvktC1kwlhQypbLsim47lCgOsYzuQgXi2MrrQYNkGNj7xi7CeJmm7A1jMn7jeVeyUJv400MtAbnhLN'

        # In the route handler for /create-verification-session:
        # Authenticate your user.

        # Create the session.
        verification_session = stripe.identity.VerificationSession.create(
            type='document',
            metadata={
                'user_id': '{{USER_ID}}',
            },
        )

        # Return only the client secret to the frontend
        url = verification_session.url


        return Response({'url' : url}, status=status.HTTP_200_OK)