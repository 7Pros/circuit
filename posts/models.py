"""@package posts
Post and Hashtag model file.

@author 7Pros
@copyright
"""
import datetime
import re

from PIL import Image
from django.core.exceptions import ValidationError
from django.db import models

from django.db.models import Count

from users.models import User
from circles.models import Circle, PUBLIC_CIRCLE


class Post(models.Model):
    """
    Post model that stores all information of a post
    """
    content = models.CharField(max_length=256)
    author = models.ForeignKey(User)
    # the post of which this is a repost
    repost_original = models.ForeignKey('self', null=True, blank=True, related_name='repost')
    reply_original = models.ForeignKey('self', null=True, blank=True, related_name='reply')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    favorites = models.ManyToManyField(User, related_name='favorites')
    circles = models.ForeignKey(Circle, null=True, blank=True, related_name='circles')
    image = models.ImageField(upload_to='tmp/', null=True, blank=True, height_field=None,
                              width_field=None)  # TODO:put right directory in here

    def original_or_self(self):
        """
        Helper method for getting the original post of a repost.

        Loops until the original is found to avoid database inconsistencies.

        @return `self.repost_original` if set, `self` otherwise
        """
        p = self
        while p.repost_original:
            p = p.repost_original
        return p

    def set_post_extra(self, request):
        """
        Add an `extra` attribute to a post for easy information access in a template.

        @param self: the post to add extra information to
        @param request: the request for which information is added
        """
        can_be_reposted = 'ok' == self.original_or_self().check_repost(request.user)
        can_be_edited = self.original_or_self().author.pk == request.user.pk
        is_favorited = self.original_or_self().favorites.filter(pk=request.user.pk).exists()
        can_be_deleted = self.author.pk == request.user.pk

        setattr(self, 'extra', {
            'can_be_reposted': can_be_reposted,
            'can_be_edited': can_be_edited,
            'is_favorited': is_favorited,
            'can_be_deleted': can_be_deleted,
            'replies': self.reply.all(),
        })

    def save_hashtags(self, hashtags):
        for hashtagWord in hashtags:
            hashtagList = Hashtag.objects.filter(name=hashtagWord)

            if len(hashtagList) == 0:
                hashtag = Hashtag(name=hashtagWord.lower())
                hashtag.save()
                hashtag.posts.add(self)
            else:
                hashtagList[0].posts.add(self)

    def check_repost(self, user):
        """
        Check if a post can be reposted by a user.

        @param self: the post to repost
        @param user: the user that wants to repost
        @return `ok` if the post can be reposted by the user, a different error string otherwise
        """
        if not user.is_authenticated():
            return 'not_auth'  # no user to repost as

        if user.pk == self.author.pk:
            return 'own_post'  # don't repost own post

        existing_repost = Post.objects.filter(author=user, repost_original=self).exists()
        if existing_repost:
            # don't repost more than once
            return 'already_reposted_as'

        return 'ok'

    def check_reply(self, user):
        """
        Checks if a post can be replied to

        @param user: the user that wants to reply to a post.

        @return: 'not_auth' in case the user isn't authenticated, 'ok' otherwise.
        """
        if not user.is_authenticated():
            return 'not_auth'

        return 'ok'

    def __str__(self):
        return self.content

    @staticmethod
    def parse_content(content):
        hashtags = re.findall(r"#(\w+)", content)
        mentions = re.findall(r"@(\w+)", content)
        return {'hashtags': hashtags, 'mentions': mentions}

    @staticmethod
    def content_is_valid(content):
        return 0 < len(content) <= 256

    @staticmethod
    def image_is_valid(image):
        try:
            this_image = Image.open(image)
            if this_image:
                if this_image.format in ('BMP', 'PNG', 'JPEG', 'PPM', 'JPG'):
                    return True
                raise ValidationError("unsupported image type")
        except OSError:
            return False

    @staticmethod
    def visible_posts_for(user):
        """
        Returns a pre-filtered query object containing all posts visible for the specified user.
        @param user: instance of the User model
        """
        own = Post.objects.filter(author=user)
        public = Post.objects.filter(circles=PUBLIC_CIRCLE)
        my_circle = Post.objects.filter(circles__owner=user.pk)
        in_circle = Post.objects.filter(circles__members=user.pk)
        return own | public | my_circle | in_circle


class Hashtag(models.Model):
    name = models.CharField(max_length=255)
    posts = models.ManyToManyField(Post)

    def __str__(self):
        return self.name

    @staticmethod
    def filter_posts_by_hashtag(hashtag_name):
        """
        Filters posts by hashtag.

        @param hashtag_name the hashtag name to filter with
        @return the posts that have used this hashtag
        """
        return Hashtag.objects.get(name=hashtag_name).posts.all()

    @staticmethod
    def top():
        """
        Shows most used hashtags in last 24 hours
        @return filters hashtags in descending order from last 24 h
        """
        return Hashtag.objects.filter(posts__created_at__gt=datetime.datetime.now() - datetime.timedelta(days=1)) \
            .annotate(itemcount=Count('name')).order_by('-itemcount')
