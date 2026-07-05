# calls/urls.py
from django.urls import path
from .views import call_room

app_name = "calls"

urlpatterns = [
    path("call/<str:room_id>/", call_room, name="call_room"),
]