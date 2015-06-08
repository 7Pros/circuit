from django.db import models
from django.http import Http404
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

    def filter_posts_by_hashtag(self, hashtag_name):
        try:
            hashtagObject = self.objects.get(name=hashtag_name)
        except:
            raise Http404("Hashtag does not exist")
        return hashtagObject.posts.all()