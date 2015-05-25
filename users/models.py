from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, username, password):
        if not email:
            raise ValueError('Users must have an email address')

        if not username:
            raise ValueError('Users must have an username')

        if not password:
            raise ValueError('Users must have a password')

        user = self.model(
            email=self.normalize_email(email),
            username=username
        )

        user.set_password(password)
        user.save(using=self._db)

        return user


class User(AbstractBaseUser):
    username = models.CharField(unique=True, max_length=32)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=50)
    description = models.TextField(default='')
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.email
