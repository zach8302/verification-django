from django.urls import path
from .views import AuthenticateView, VerifyView, IsAuthenticatedView
from .auth_views import MeView
from .stripe_views import VerificationSessionView, VerificationWebhookView

urlpatterns = [
    path('authenticate', AuthenticateView.as_view()),
    path('verify', VerifyView.as_view()),
    path('is-authenticated', IsAuthenticatedView.as_view()),
    path('me', MeView.as_view()),
    path('create-verification-session', VerificationSessionView.as_view()),
    path('webhook', VerificationWebhookView.as_view())
    ]
