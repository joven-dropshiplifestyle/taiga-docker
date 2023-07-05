from django.urls import path

from .epics.id.duplicate.views import EpicsIdDuplicateAPIView

urlpatterns = [
    path('epics/<int:epic_id>/duplicate', EpicsIdDuplicateAPIView.as_view()),
]
