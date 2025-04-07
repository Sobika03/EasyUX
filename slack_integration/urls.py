from django.urls import path
from openui.views import sample

urlpatterns = [
    path("slack/events/", sample, name="slack-events"),
]