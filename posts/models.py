from django.db import models

from users.models import User


class Post(models.Model):
    content = models.CharField(max_length=256)
    author = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content

class Hashtag(models.Model):
    name = models.CharField(max_length=255)
    posts = models.ManyToManyField(Post)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def filter_posts_by_hashtag(self, post_content):
        return self.objects.filter(posts__name=post_content)