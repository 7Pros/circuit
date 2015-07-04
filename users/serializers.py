"""
--Brief Description--

@author 7Pros
@copyright 
"""
from swampdragon.serializers.model_serializer import ModelSerializer


class NotificationSerializer(ModelSerializer):
    class Meta:
        model = 'users.Notification'
        publish_fields = ['message']
        update_fields = ['status', 'updated_at']