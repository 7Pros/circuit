"""
Router required for the communication to the channels between client and server

@author 7Pros
@copyright 
"""
from swampdragon import route_handler
from swampdragon.route_handler import ModelPubRouter, get_publisher

from .models import Notification
from .serializers import NotificationSerializer


class NotificationRouter(ModelPubRouter):
    """
    Generic router class.

    Creates a route called `notifications` and registers it for the communication between client and server.
    """
    valid_verbs = ['subscribe']
    route_name = 'notifications'
    model = Notification
    serializer_class = NotificationSerializer

route_handler.register(NotificationRouter)
