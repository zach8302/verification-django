from django.urls import path
from .views import AuthenticateView, VerifyView, IsAuthenticatedView
from .auth_views import MeView

urlpatterns = [
    path('authenticate', AuthenticateView.as_view()),
    path('verify', VerifyView.as_view()),
    path('is_authenticated', IsAuthenticatedView.as_view()),
    path('me', MeView.as_view())
    ]
