from django.urls import path

from .epics.ref.ref_id.duplicate.views import EpicsRefRefIdDuplicateAPIView

urlpatterns = [
    path('epics/ref/<int:ref_id>/duplicate', EpicsRefRefIdDuplicateAPIView.as_view()),
]
