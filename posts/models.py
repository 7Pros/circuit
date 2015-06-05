from django.db import models

from users.models import User


class Post(models.Model):
    content = models.CharField(max_length=256)
    author = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
