# chat/routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/webcam/$', consumers.webCamConsumers.as_asgi()),
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.webCamConsumers.as_asgi()),
]