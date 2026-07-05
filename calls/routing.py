from django.urls import re_path
from .consumers import CallConsumer, NotifyConsumer

websocket_urlpatterns = [
    re_path(r"ws/call/(?P<room_id>\w+)/$", CallConsumer.as_asgi()),
    re_path(r"ws/notify/$", NotifyConsumer.as_asgi()),
]