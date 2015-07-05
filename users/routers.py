"""
--Brief Description--

@author 7Pros
@copyright 
"""
from swampdragon import route_handler
from swampdragon.route_handler import ModelPubRouter

from .models import Notification
from .serializers import NotificationSerializer


class NotificationRouter(ModelPubRouter):
    valid_verbs = ['subscribe', 'update']
    route_name = 'notifications'
    model = Notification
    serializer_class = NotificationSerializer


route_handler.register(NotificationRouter)