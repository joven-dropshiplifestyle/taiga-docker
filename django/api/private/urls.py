from django.urls import path

from .registration.views import RegistrationAPIView
from .authenticate.views import AuthenticateAPIView
from .redirect.views import RedirectHTMLView
from .accounts.email.views import AccountEmailAPIView

urlpatterns = [
    path('registration', RegistrationAPIView.as_view()),
    path('authenticate', AuthenticateAPIView.as_view()),
    path('redirect/', RedirectHTMLView, name='redirect'),
    path('accounts/email/<str:email_id>', AccountEmailAPIView.as_view()),
]
