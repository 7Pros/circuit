from django.db import models

from users.models import User


class Post(models.Model):
    content = models.CharField(max_length=256)
    author = models.ForeignKey(User)
    # the post of which this is a repost
    original_post = models.ForeignKey('self', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def original_or_self(self):
        p = self
        while p.original_post:
            p = p.original_post
        return p
