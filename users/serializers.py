"""
Serializer of the users notification class.

@author 7Pros
@copyright 
"""
from swampdragon.serializers.model_serializer import ModelSerializer


class NotificationSerializer(ModelSerializer):
    """
    Generic class of the serializers.

    Creates a serialize model to send to the client, sending the fields message, post, notification's pk, creation date and the user's pk.
    """
    class Meta:
        model = 'users.Notification'
        publish_fields = ['message', 'post', 'pk', 'created_at', 'user']
