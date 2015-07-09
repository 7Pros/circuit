"""@package posts
Post views file.

@author 7Pros
@copyright
"""
from django.contrib import messages
from django.shortcuts import redirect, Http404
from django.views.generic import ListView, DetailView
from django.core.urlresolvers import reverse
from django.views import generic

from circles.models import PUBLIC_CIRCLE, Circle, ME_CIRCLE
from posts.models import Post, Hashtag
import users
from users.models import User
from users.views import email_notification_for_user


def post_create(request):
    has_image = 'image' in request.FILES
    if not request.user.is_authenticated:
        messages.error(request, 'Not logged in')
    elif 'content' not in request.POST \
            or not Post.content_is_valid(request.POST['content']):
        messages.error(request, 'Invalid post content')
    elif has_image and not Post.image_is_valid(request.FILES['image']):
        messages.error(request, 'Invalid image format')
    elif 'circle' not in request.POST:
        messages.error(request, 'No circle selected')
    else:
        circle_pk = int(request.POST['circle'])
        pseudo_circle = Circle(circle_pk)  # not saved to DB, only used to store PK, do not use for anything else!
        post = Post(content=request.POST['content'], author=request.user, circles=pseudo_circle)
        if has_image:
            post.image = request.FILES['image']
        post.save()
        parsed_content = Post.parse_content(request.POST['content'])
        post.save_hashtags(parsed_content['hashtags'])
        for mentionedUser in User.objects.filter(username__in=parsed_content['mentions']):
            mentionedUser_is_in_circle = False
            for member in post.circles.members.all():
                if mentionedUser == member:
                    mentionedUser_is_in_circle = True
            if mentionedUser_is_in_circle:
                context = {
                    'content': "%s mentioned you in his post" % request.user.username,
                    'link_to_subject': reverse("posts:post", kwargs={'pk': post.pk})
                }
                email_notification_for_user(mentionedUser, "You were mentioned",
                                            'users/notification_for_post_email.html', context)

    return redirect(request.META['HTTP_REFERER'] or 'landingpage')


class PostDetailView(DetailView):
    template_name = 'posts/post_detail.html'
    model = Post

    def render_to_response(self, context, **response_kwargs):
        context['post'].set_post_extra(self.request)

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
        has_img = 'image' in self.request.FILES
        if has_img and not Post.image_is_valid(self.request.FILES['image']):
            messages.error(self.request, 'Invalid image format')

        if not Post.content_is_valid(self.request.POST['content']):
            return self.form_invalid(form)
        old_post = self.object
        parsed_content_old = Post.parse_content(old_post.content)
        post = form.save()
        parsed_content_new = Post.parse_content(post.content)
        for mentionedUser in User.objects.filter(username__in=parsed_content_new['mentions']):
            mentionedUser_is_in_circle = False
            for member in post.circles.members.all():
                if mentionedUser == member:
                    mentionedUser_is_in_circle = True
                if mentionedUser.username in parsed_content_old['mentions']:
                    context = {
                        'content': "%s changed his post you were metioned in" % self.request.user.username,
                        'link_to_subject': reverse("posts:post", kwargs={'pk': post.pk})
                    }
                else:
                    context = {
                        'content': "%s mentioned you in his post" % self.request.user.username,
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
        if has_img:
            post.image = self.request.FILES['image']

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

    check = repost_original.check_repost(user)
    if check == 'not_auth':
        return redirect('posts:post', pk=repost_original.pk)
    if check != 'ok':
        return redirect(request.META['HTTP_REFERER'] or 'landingpage')

    repost = Post(content=repost_original.content,
                  author=user,
                  repost_original=repost_original)
    repost.save()
    context = {
        'content': "There is a new repost to a post of you made by %s" % user.username,
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

    check = reply_original.check_reply(user)
    if check != 'ok':
        return redirect('posts:post', pk=reply_original.pk)

    reply = Post(content=request.POST['content_reply'],
                 author=user,
                 reply_original=reply_original)

    reply.save()
    context = {
        'content': "There is a new reply to a post of you made by %s" % user.username,
        'link_to_subject': reverse("posts:post", kwargs={'pk': reply.pk})
    }
    users.views.email_notification_for_user(author, "There is a new reply to your post",
                                            'users/notification_for_post_email.html', context)
    reply_original.reply.add(reply)

    return redirect('posts:post', pk=reply_original.pk)


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
        'content': "%s favorited your post" % request.user.username,
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
