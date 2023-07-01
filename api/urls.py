from django.urls import path
from .views import AuthenticateView, VerifyView, IsAuthenticatedView

urlpatterns = [
    path('authenticate', AuthenticateView.as_view()),
    path('verify', VerifyView.as_view()),
    path('is_authenticated', IsAuthenticatedView.as_view())
    ]
