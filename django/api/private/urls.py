from django.urls import path

from .registration.views import RegistrationAPIView
from .authenticate.views import AuthenticateAPIView
from .redirect.views import RedirectHTMLView
from .accounts.email.views import AccountEmailAPIView
from .management.epics.views import ManagementEpicsView

urlpatterns = [
    path('registration', RegistrationAPIView.as_view()),
    path('authenticate', AuthenticateAPIView.as_view()),
    path('redirect/', RedirectHTMLView, name='redirect'),
    path('management/epics', ManagementEpicsView, name='redirect'),
    path('accounts/email/<str:email_id>', AccountEmailAPIView.as_view()),
]
