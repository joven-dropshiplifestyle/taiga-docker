from django.urls import path

from .registration.views import RegistrationAPIView
from .authenticate.views import AuthenticateAPIView
from .redirect.views import RedirectHTMLView

urlpatterns = [
    path('registration', RegistrationAPIView.as_view()),
    path('authenticate', AuthenticateAPIView.as_view()),
    path('redirect/', RedirectHTMLView, name='redirect'),
]
