"""@package circles.models
Circles models file.

@author 7Pros
@copyright
"""
import json
from django.db import models
from users.models import User


class Circle(models.Model):
    name = models.CharField(max_length=50, default='', blank=True)
    owner = models.ForeignKey(User)
    members  = models.ManyToManyField(User, related_name='members')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_members(self):
        return self.members.all()

    def members_json(self):
        members = [{
            'pk': m.pk,
            'username': m.username,
            'gravatar': m.gravatar_hash(),
        } for m in self.members.all()]
        return json.dumps(members)

    def __str__(self):
        return self.name
