from django.db import models


class User(models.Model):
    username = models.CharField(unique=True, max_length=32)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    description = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username
