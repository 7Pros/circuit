"""@package posts
Post views file.

@author 7Pros
@copyright
"""
import datetime
import re

from django.contrib import messages
from django.db.models import Count

from django.shortcuts import redirect, Http404

from django.views.generic import ListView, DetailView

from django.core.urlresolvers import reverse

from django.views import generic

from PIL import Image

from django.core.exceptions import ValidationError

from circles.models import PUBLIC_CIRCLE, Circle, ME_CIRCLE
from posts.models import Post, Hashtag
import users
from users.models import User


def post_content_is_valid(content):
    return 0 < len(content) <= 256


def post_image_is_valid(image):
    try:
        this_image = Image.open(image)
        if this_image:
            if this_image.format in ('BMP', 'PNG', 'JPEG', 'PPM', 'JPG'):
                return True
            raise ValidationError("unsupported image type")
    except OSError as error:
        return False


def check_repost(post, user):
    """
    Check if a post can be reposted by a user.

    @param post: the post to repost
    @param user: the user that wants to repost
    @return `ok` if the post can be reposted by the user, a different error string otherwise
    """
    if not user.is_authenticated():
        return 'not_auth'  # no user to repost as

    if user.pk == post.author.pk:
        return 'own_post'  # don't repost own post

    existing_repost = Post.objects.filter(author=user, repost_original=post).exists()
    if existing_repost:
        # don't repost more than once
        return 'already_reposted_as'

    return 'ok'


def set_post_extra(post, request):
    """
    Add an `extra` attribute to a post for easy information access in a template.

    @param post: the post to add extra information to
    @param request: the request for which information is added
    """
    can_be_reposted = 'ok' == check_repost(post.original_or_self(), request.user)
    can_be_edited = post.original_or_self().author.pk == request.user.pk
    is_favorited = post.original_or_self().favorites.filter(pk=request.user.pk).exists()
    can_be_deleted = post.author.pk == request.user.pk

    setattr(post, 'extra', {
        'can_be_reposted': can_be_reposted,
        'can_be_edited': can_be_edited,
        'is_favorited': is_favorited,
        'can_be_deleted': can_be_deleted,
        'replies': post.reply.all(),
    })


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


def check_reply(user):
    """
    Checks if a post can be replied to

    @param user: the user that wants to reply to a post.

    @return: 'not_auth' in case the user isn't authenticated, 'ok' otherwise.
    """
    if not user.is_authenticated():
        return 'not_auth'

    return 'ok'


def post_create(request):
    has_img = 'image' in request.FILES
    if not request.user.is_authenticated:
        messages.error(request, 'Not logged in')
    elif 'content' not in request.POST \
            or not post_content_is_valid(request.POST['content']):
        messages.error(request, 'Invalid post content')
    elif has_img and not post_image_is_valid(request.FILES['image']):
        messages.error(request, 'Invalid image format')
    elif 'circle' not in request.POST:
        messages.error(request, 'No circle selected')
    else:
        circle_pk = int(request.POST['circle'])
        pseudo_circle = Circle(circle_pk)  # not saved to DB, only used to store PK, do not use for anything else!
        post = Post(content=request.POST['content'], author=request.user, circles=pseudo_circle)
        if has_img:
            post.image = request.FILES['image']
        post.save()
        parsed_content = parse_content(request.POST['content'])
        save_hashtags(parsed_content['hashtags'], post)
        for mentionedUser in User.objects.filter(username__in=parsed_content['mentions']):
            mentionedUser_is_in_circle = False
            for member in post.circles.members.all():
                if mentionedUser == member:
                    mentionedUser_is_in_circle = True
            if mentionedUser_is_in_circle:
                context = {
                    'content': "%s mentioned you in his post" % (request.user.username),
                    'link_to_subject': reverse("posts:post", kwargs={'pk': post.pk})
                }
                users.views.email_notification_for_user(mentionedUser, "You were mentioned",
                                                        'users/notification_for_post_email.html', context)

    return redirect(request.META['HTTP_REFERER'] or 'landingpage')


class PostDetailView(DetailView):
    template_name = 'posts/post_detail.html'
    model = Post

    def render_to_response(self, context, **response_kwargs):
        set_post_extra(context['post'], self.request)

        return super(PostDetailView, self).render_to_response(context, **response_kwargs)


class PostEditView(generic.UpdateView):
    """Edit a post's content and/or circle."""
    model = Post
    fields = [
        'content',
        'circles',
    ]

    def form_valid(self, form):
        """
        Check if the user is allowed to edit the post this way.

        The user must be logged in and the post content must be
        at most 256 python characters long.

        @param form: the form containing the new post
        @return `form_valid` if accepted, `form_invalid` if not
        """
        if not self.request.user.is_authenticated:
            return self.form_invalid(form)

        if not post_content_is_valid(self.request.POST['content']):
            return self.form_invalid(form)
        old_post = self.object
        parsed_content_old = parse_content(old_post.content)
        post = form.save()
        parsed_content_new = parse_content(post.content)
        for mentionedUser in User.objects.filter(username__in=parsed_content_new['mentions']):
            mentionedUser_is_in_circle = False
            for member in post.circles.members.all():
                if mentionedUser == member:
                    mentionedUser_is_in_circle = True
                if mentionedUser.username in parsed_content_old['mentions']:
                    context = {
                        'content': "%s changed his post you were metioned in" % (self.request.user.username),
                        'link_to_subject': reverse("posts:post", kwargs={'pk': post.pk})
                    }
                else:
                    context = {
                        'content': "%s mentioned you in his post" % (self.request.user.username),
                        'link_to_subject': reverse("posts:post", kwargs={'pk': post.pk})
                    }
                users.views.email_notification_for_user(mentionedUser, "You were mentioned",
                                                        'users/notification_for_post_email.html', context)

        circle_pk = int(self.request.POST['circle'])
        if circle_pk not in (ME_CIRCLE, PUBLIC_CIRCLE):
            circle_owner_id = Circle.objects.get(pk=circle_pk).owner_id
            # Is the selected circle not one of the user's circles?
            if circle_owner_id != self.request.user.pk:
                return self.form_invalid(form)

        post = form.save()

        circle_pk = int(self.request.POST['circle'])
        post.circles = Circle(circle_pk)

        return super(PostEditView, self).form_valid(form)

    def get_success_url(self):
        return reverse('posts:post', kwargs={'pk': self.object.pk})


def post_repost(request, pk=None):
    """
    Repost a post.

    This always reposts the original post.

    Redirects to the post's page if the repost was successful or if the user
    is not authenticated.
    Otherwise, redirects to the referer if present, or the landingpage if not.

    @param pk: the primary key which identifies the post
    @return redirect depending on the success
    """
    user = request.user
    repost_original = Post.objects.get(pk=pk).original_or_self()

    check = check_repost(repost_original, user)
    if check == 'not_auth':
        return redirect('posts:post', pk=repost_original.pk)
    if check != 'ok':
        return redirect(request.META['HTTP_REFERER'] or 'landingpage')

    repost = Post(content=repost_original.content,
                  author=user,
                  repost_original=repost_original)
    repost.save()
    context = {
        'content': "There is a new repost to a post of you made by %s" % (user.username),
        'link_to_subject': reverse("posts:post", kwargs={'pk': repost.pk})
    }
    users.views.email_notification_for_user(repost_original.author, "There is a new repost to your post",
                                            'users/notification_for_post_email.html', context)

    return redirect('posts:post', pk=repost.pk)


def post_reply(request, pk=None):
    """
    Reply to a post.

    Redirects to the post page.

    @param request:
    @param pk:

    @return:
    """
    user = request.user
    reply_original = Post.objects.get(pk=pk)
    author = reply_original.author

    check = check_reply(user)
    if check == 'not_auth':
        return redirect('posts:post', pk=reply_original.pk)

    reply = Post(content=request.POST['content_reply'],
                 author=user,
                 reply_original=reply_original)

    reply.save()
    context = {
        'content': "There is a new reply to a post of you made by %s" % (user.username),
        'link_to_subject': reverse("posts:post", kwargs={'pk': reply.pk})
    }
    users.views.email_notification_for_user(author, "There is a new reply to your post",
                                            'users/notification_for_post_email.html', context)
    reply_original.reply.add(reply)

    return redirect('posts:post', pk=reply_original.pk)


def parse_content(content):
    hashtags = re.findall(r"#(\w+)", content)
    mentions = re.findall(r"@(\w+)", content)
    return {'hashtags': hashtags, 'mentions': mentions}


def save_hashtags(hashtags, post):
    for hashtagWord in hashtags:
        hashtagList = Hashtag.objects.filter(name=hashtagWord)

        if len(hashtagList) == 0:
            hashtag = Hashtag(name=hashtagWord.lower())
            hashtag.save()
            hashtag.posts.add(post)
        else:
            hashtagList[0].posts.add(post)


class PostsListView(ListView):
    template_name = 'posts/posts_list.html'
    model = Post

    def get_queryset(self):
        """
        Returns the posts containing a wished hashtag

        @return posts objects that contain the searched hashtag
        """
        try:
            posts = Hashtag.filter_posts_by_hashtag(self.kwargs['hashtag_name'])
        except Hashtag.DoesNotExist:
            raise Http404('Hashtag "%s" does not exist' % self.kwargs['hashtag_name'])
        return posts


def post_favorite(request, pk=None):
    """
    Favorite or un-favorite a post.

    @param pk: the primary key which identifies the post
    @return redirect to the referer if present, to the post's page otherwise
    """
    post = Post.objects.get(pk=pk).original_or_self()
    if post.favorites.filter(pk=request.user.pk).exists():
        post.favorites.remove(request.user)
    else:
        post.favorites.add(request.user)
    post.save()
    context = {
        'content': "%s favorited your post" % (request.user.username),
        'link_to_subject': reverse("posts:post", kwargs={'pk': post.pk})
    }
    users.views.email_notification_for_user(post.author, "There is a new repost to your post",
                                            'users/notification_for_post_email.html', context)

    referer = request.META['HTTP_REFERER']
    if referer:
        return redirect(referer)
    else:
        return redirect('posts:post', pk=post.pk)


class PostDeleteView(generic.DeleteView):
    model = Post

    def get_success_url(self):
        return reverse('users:profile', kwargs={'pk': self.request.user.pk})


def top_hashtags():
    return Hashtag.objects.filter(posts__created_at__gt=datetime.datetime.now() - datetime.timedelta(days=1)) \
        .annotate(itemcount=Count('name')).order_by('-itemcount')
