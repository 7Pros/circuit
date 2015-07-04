"""
--Brief Description--

@author 7Pros
@copyright 
"""
from swampdragon import route_handler
from swampdragon.route_handler import ModelPubRouter
from .models import Notification
from .serializers import NotificationSerializer
from django.contrib.auth.decorators import login_required


class NotificationRouter(ModelPubRouter):
    valid_verbs = ['subscribe', 'update']
    route_name = 'notifications'
    model = Notification
    serializer_class = NotificationSerializer
    #
    # @login_required
    # def subscribe(self, **kwargs):
    #     super().subscribe(**kwargs)
    #
    # def get_subscription_contexts(self, **kwargs):
    #     return {'user_id': self.connection.user.pk}


route_handler.register(NotificationRouter)