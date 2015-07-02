"""
--Brief Description--

@author 7Pros
@copyright 
"""
from users.models import User
from posts.models import Post
from rest_framework import serializers

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('content', )

    def create(self, validated_data):
        """
        Create and return a new `Post` instance, given the validated data.
        """
        return Post.objects.create(**validated_data)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username',)

class ErrorSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=200)
