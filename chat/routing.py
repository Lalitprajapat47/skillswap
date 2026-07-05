from django.urls import re_path
from .consumers import SessionChatConsumer

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<session_id>\d+)/$", SessionChatConsumer.as_asgi()),
]
