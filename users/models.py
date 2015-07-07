"""@package users.models
User model.

@author     7Pros
@copyright  Some license
"""
import hashlib
import os

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from swampdragon.models import SelfPublishModel
from .serializers import NotificationSerializer
from django.db import models

def create_hash():
    """Generate a random sha1 hash.

    @return string - the hash
    """
    hash = hashlib.sha1()
    hash.update(os.urandom(5))
    return hash.hexdigest()


class UserManager(BaseUserManager):
    """The UserManager class which manages users
    """
    def create_user(self, email, username, password):
        """Creates and saves a User with the given email, username and password.

        @param self: object - User's model object
        @param email: email - user's email
        @param username: string - user's username
        @param password: string - user's password

        @return object - created user
        """
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

    def create_superuser(self, email, username, password):
        """Creates and saves a superuser with the given email, username and password.

        @param self: object - User's model object
        @param email: email - user's email
        @param username: string - user's username
        @param password: string - user's password

        @return object - created superuser
        """
        if not email:
            raise ValueError('Superusers must have an email address')

        if not username:
            raise ValueError('Superusers must have an username')

        if not password:
            raise ValueError('Superusers must have a password')

        superuser = self.model(
            email=self.normalize_email(email),
            username=username,
            is_staff=True,
            is_superuser=True
        )

        superuser.set_password(password)
        superuser.save(using=self._db)

        return superuser


class User(AbstractBaseUser):
    """The circuit User model
    """
    username = models.CharField(unique=True, max_length=32)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=50, default='', blank=True)
    description = models.TextField(default='', blank=True)
    is_active = models.BooleanField(default=False)
    confirm_token = models.CharField(default=create_hash, max_length=40)
    password_reset_token = models.CharField(default=create_hash, max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # needed for using Django's admin panel
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def gravatar_hash(self):
        return hashlib.md5(self.email.strip().lower().encode()).hexdigest()

    def get_circles(self):
        """
        Returns the circles this user is at.

        @return: ForeingKeyObject - contains the circles he is at.
        """
        return self.members.all()

    def get_full_name(self):
        """ Alias for get_name
        @return: string - returns the name
        """
        return self.name

    def get_short_name(self):
        """ Alias for get_name
        @return: string - returns the name
        """
        return self.name

    def __str__(self):
        return self.email

    def has_perm(self, perm_str):
        """Needed for using Django's admin panel."""
        return self.is_superuser

    def has_module_perms(self, module_label):
        """Needed for using Django's admin panel."""
        return self.is_superuser

class Notification(SelfPublishModel, models.Model):
    """
    Generic SwampDragon SelfPublishModel class.
    """
    TYPE_OF_NOTIFICATIONS = (
        (0, 'circle-related'),
        (1, 'post-related')
    )

    message = models.CharField(max_length=255)
    status = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User)
    post = models.ForeignKey('posts.Post', blank=True, null=True)
    type = models.IntegerField(default=1, choices=TYPE_OF_NOTIFICATIONS)
    serializer_class = NotificationSerializer

    @staticmethod
    def set_all_as_read(user):
        """
        Set all the user's notifications as read.

        @param user: the user that will get all his notifications as read.
        """
        user_notifications = Notification.objects.filter(user=user).filter(status=False)
        if len(user_notifications) > 0:
            for notification in user_notifications:
                notification.status = True
                notification.save()

    @staticmethod
    def get_number_of_unseen_notifications(user):
        """
        Returns the number of unseen notifications.

        @param user: the user of the notifications.

        @return: int - number of unseen notifications.
        """
        return len(Notification.objects.filter(user=user).filter(status=False))

