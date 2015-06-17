from django.db import models
from users.models import User


class Circle(models.Model):
    name = models.CharField(max_length=50, default='', blank=True)
    owner = models.ForeignKey(User)
    members  = models.ManyToManyField(User, related_name='members')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
