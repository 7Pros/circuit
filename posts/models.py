"""@package posts.models
Post and Hashtag model file.

@author 7Pros
@copyright
"""
from django.db import models

from users.models import User

class Post(models.Model):
    """Post model that stores all information of a post
    """
    content = models.CharField(max_length=256)
    author = models.ForeignKey(User)
    # the post of which this is a repost
    original_post = models.ForeignKey('self', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    favorites = models.ManyToManyField(User, related_name='favorites')

    def original_or_self(self):
        p = self
        while p.original_post:
            p = p.original_post
        return p

    def __str__(self):
        return self.content


class Hashtag(models.Model):
    name = models.CharField(max_length=255)
    posts = models.ManyToManyField(Post)

    def __str__(self):
        return self.name

    def filter_posts_by_hashtag(hashtag_name):
        """
        Filters posts by hashtag.

        @param hashtag_name: string - the hashtag name with which be used for filtering by its name.
        @return list - the posts that have used the hashtag_name
        """
        hashtagObject = Hashtag.objects.get(name=hashtag_name)
        return hashtagObject.posts.all()
