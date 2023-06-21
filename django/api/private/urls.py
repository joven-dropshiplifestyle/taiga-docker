from django.urls import path

from .registration.views import RegistrationAPIView

urlpatterns = [
    path('registration', RegistrationAPIView.as_view()),
]
