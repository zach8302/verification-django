
from .models import User
import stripe
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework import status
from .serializers import UserSerializer

stripe.api_key = 'sk_test_51NOtuQENXUDWXy01vZ0UjvktC1kwlhQypbLsim47lCgOsYzuQgXi2MrrQYNkGNj7xi7CeJmm7A1jMn7jeVeyUJv400MtAbnhLN'

class VerificationSessionView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        # Set your secret key. Remember to switch to your live secret key in production.
        # See your keys here: https://dashboard.stripe.com/apikeys
        # In the route handler for /create-verification-session:
        # Authenticate your user.

        # Create the session.
        email = request.user.email

        verification_session = stripe.identity.VerificationSession.create(
            type='document',
            metadata={
                'user_id': email,
            },
        )

        # Return only the client secret to the frontend
        url = verification_session.url
        print(verification_session.metadata.user_id)


        return Response({'url' : url}, status=status.HTTP_200_OK)
    
class VerificationWebhookView(APIView):

    def post(self, request, format=None):
        signature = request.headers.get('stripe-signature')
        payload = request.data
        endpoint_secret = "whsec_zIdspvETnidcC0cgMzKUj3oaW12jyxvq"
        

        # Verify webhook signature and extract the event.
        # See https://stripe.com/docs/webhooks/signatures for more information.
        try:
            event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=signature,
            secret=endpoint_secret,
            )
        except ValueError as e:
            # Invalid payload.
            print("payload")
            return Response({'Bad Request': 'Invalid Payload'}, status=400)
        except stripe.error.SignatureVerificationError as e:
            # Invalid Signature.
            print("signature")
            return Response({'Bad Request': 'Invalid Signature'}, status=400)

        print(event)
        if event['type'] == 'identity.verification_session.verified':
            print("All the verification checks passed")
            verification_session = event.data.object
            email = verification_session.metadata.user_id
            user = User.objects.get(email=email)
            user.verified = True
            user.save()

        elif event['type'] == 'identity.verification_session.requires_input':
            print("At least one verification check failed")
            verification_session = event.data.object
            if verification_session.last_error.code == 'document_unverified_other':
                print("The document was invalid")
            elif verification_session.last_error.code == 'document_expired':
                print("The document was expired")
            elif verification_session.last_error.code == 'document_type_not_supported':
                print("The document type was not supported")
            else:
                print("other error code")